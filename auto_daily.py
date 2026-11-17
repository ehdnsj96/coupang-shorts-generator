import argparse
import copy
import json
import os
import sys
import io
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# 윈도우 환경 한글(CP949) 인코딩 충돌 방지 및 UTF-8 강제
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

from models import ShortsScript
from episode_builder import get_next_dynamic_episode, normalize_title
from slide_renderer import SlideRenderer
from video_builder import VideoBuilder
from voice_generator import VoiceGenerator
from youtube_uploader import YouTubeUploader
from web_updater import update_link_page
from publish_guard import (
    collect_guard,
    describe_guard,
    load_archive_items,
    reconcile_state_with_archive,
)
from preflight import check_episode, format_problems
import config

STATE_FILE = config.BASE_DIR / "daily_state.json"
DAILY_OUTPUT_DIR = config.OUTPUT_DIR / "daily"
DAILY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 유튜브 쇼츠 알고리즘 최적 3대 골든 타임 슬롯 (기본: 아침 8시, 점심 12시, 저녁 18시)
DEFAULT_SLOTS = [8, 12, 18]


# =====================================================================
# 실행 전 자동 Git 동기화 (PC 는 실행 직전 최신 코드를 자동으로 받아온다)
# =====================================================================
GIT_REMOTE = "origin"
GIT_BRANCH = "main"
GIT_TIMEOUT = 120          # 네트워크가 죽어 있어도 데몬이 멈추지 않도록 초 단위 상한
SYNC_CHILD_ENV = "COUPANG_SHORTS_SYNC_CHILD"

# git reset --hard 는 '추적 중인' 파일만 되돌린다.
# 아래 로컬 전용 파일/디렉터리는 .gitignore 대상이라 동기화로 절대 지워지지 않아야 하며,
# 동기화 후 실제로 남아 있는지 매번 확인한다.
LOCAL_ONLY_PATHS = (
    "daily_state.json",
    "token.pickle",
    "client_secrets.json",
    "output",
)


def _git(args: List[str], cwd: Path, timeout: int = GIT_TIMEOUT):
    """git 명령을 비대화식으로 실행한다(무인 실행 중 인증 입력 대기 방지)."""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.setdefault("GIT_ASKPASS", "echo")
    return subprocess.run(
        ["git"] + list(args),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )


def _local_only_snapshot(repo_dir: Path) -> dict:
    return {name: (repo_dir / name).exists() for name in LOCAL_ONLY_PATHS}


def _backup_tracked_changes(repo_dir: Path, timeout: int = GIT_TIMEOUT) -> Optional[str]:
    """reset --hard 로 사라질 로컬 추적 파일 변경분을 patch 로 남겨 둔다(복구용)."""
    try:
        diff = _git(["diff", "HEAD"], repo_dir, timeout)
        if diff.returncode != 0 or not diff.stdout.strip():
            return None
        backup_dir = config.OUTPUT_DIR / "git_sync_backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        path = backup_dir / f"local_changes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.patch"
        path.write_text(diff.stdout, encoding="utf-8")
        return str(path)
    except Exception:
        return None


def sync_repo(
    repo_dir: Optional[Path] = None,
    remote: str = GIT_REMOTE,
    branch: str = GIT_BRANCH,
    timeout: int = GIT_TIMEOUT,
) -> dict:
    """원격 origin/main 의 최신 코드를 로컬 코드로 당긴다.

    절차:
      1) git fetch → 원격 최신 커밋 확인 (이미 같으면 종료)
      2) git merge --ff-only origin/main (빠른 감기)
      3) 로컬 추적 파일 변경·분기로 ff 병합이 막히면 git reset --hard origin/main 으로 폴백
         — reset --hard 는 추적 파일만 되돌리므로 daily_state.json·output/·token.pickle 같은
           인증/상태 파일은 지워지지 않는다(사라졌는지 확인해 결과에 담는다)

    네트워크·git 오류는 예외를 올리지 않고 status="error" 로 돌려준다.
    호출 측은 경고만 찍고 기존 로컬 코드로 계속 실행한다.

    Returns: dict(status, before, after, changed_files, backup_patch, missing_local_files, message)
      status: "updated" | "up_to_date" | "skipped" | "error"
    """
    repo_dir = Path(repo_dir) if repo_dir else config.BASE_DIR
    result = {
        "status": "error",
        "before": None,
        "after": None,
        "changed_files": [],
        "backup_patch": None,
        "missing_local_files": [],
        "message": "",
    }
    protected_before = _local_only_snapshot(repo_dir)
    remote_ref = f"{remote}/{branch}"

    if not (repo_dir / ".git").exists():
        result["status"] = "skipped"
        result["message"] = "Git 저장소가 아니라서 코드 동기화를 건너뜁니다(zip 배포본)."
        return result

    try:
        head = _git(["rev-parse", "--verify", "HEAD"], repo_dir, timeout)
    except FileNotFoundError:
        result["status"] = "skipped"
        result["message"] = "git 실행 파일을 찾을 수 없어 코드 동기화를 건너뜁니다."
        return result
    except (subprocess.TimeoutExpired, OSError) as e:
        result["message"] = f"git 실행 오류: {e}"
        return result

    if head.returncode != 0 or not head.stdout.strip():
        result["message"] = f"현재 커밋을 읽지 못했습니다: {(head.stderr or '').strip()[:200]}"
        return result
    before = head.stdout.strip()
    result["before"] = before

    # 1) 원격 최신 커밋 가져오기
    try:
        fetch = _git(["fetch", "--prune", remote], repo_dir, timeout)
        if fetch.returncode != 0:
            result["message"] = f"git fetch 실패: {(fetch.stderr or fetch.stdout or '').strip()[:300]}"
            return result
        target_proc = _git(["rev-parse", "--verify", remote_ref], repo_dir, timeout)
        if target_proc.returncode != 0 or not target_proc.stdout.strip():
            result["message"] = f"원격 브랜치({remote_ref})를 찾지 못했습니다."
            return result
        target = target_proc.stdout.strip()
    except (subprocess.TimeoutExpired, OSError) as e:
        result["message"] = f"git 네트워크 오류: {type(e).__name__}: {e}"
        return result

    if target == before:
        result["status"] = "up_to_date"
        result["after"] = before
        result["message"] = f"이미 최신 코드입니다 ({before[:7]})."
        return _verify_local_only(result, repo_dir, protected_before)

    # 2) 빠른 감기 시도
    try:
        merge = _git(["merge", "--ff-only", remote_ref], repo_dir, timeout)
        after_proc = _git(["rev-parse", "HEAD"], repo_dir, timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        result["message"] = f"git 병합 오류: {type(e).__name__}: {e}"
        return result
    after = after_proc.stdout.strip() if after_proc.returncode == 0 else before

    if merge.returncode == 0:
        result["after"] = after
        if after == before:
            result["status"] = "up_to_date"
            result["message"] = f"원격 변경 없음(로컬 커밋이 앞서 있음) ({before[:7]})."
            return _verify_local_only(result, repo_dir, protected_before)

        files = _git(["diff", "--name-only", before, after], repo_dir, timeout)
        result["changed_files"] = [l.strip() for l in files.stdout.splitlines() if l.strip()]
        result["status"] = "updated"
        result["message"] = f"{before[:7]} → {after[:7]} ({len(result['changed_files'])}개 파일 갱신)"
        return _verify_local_only(result, repo_dir, protected_before)

    # 3) ff 병합 실패 → 로컬 추적 파일 변경·분기 상태이므로 하드 리셋 폴백
    dirty = _git(["status", "--porcelain", "--untracked-files=no"], repo_dir, timeout)
    dirty_files = [l[3:].strip() for l in dirty.stdout.splitlines() if l.strip()]
    ahead = _git(["rev-list", "--count", f"{target}..HEAD"], repo_dir, timeout)
    try:
        ahead_count = int((ahead.stdout or "0").strip() or 0)
    except ValueError:
        ahead_count = 0

    result["backup_patch"] = _backup_tracked_changes(repo_dir, timeout)
    try:
        reset = _git(["reset", "--hard", target], repo_dir, timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        result["message"] = f"git reset 오류: {type(e).__name__}: {e}"
        return result

    if reset.returncode != 0:
        result["message"] = f"git reset 실패: {(reset.stderr or reset.stdout or '').strip()[:300]}"
        return result

    after_proc = _git(["rev-parse", "HEAD"], repo_dir, timeout)
    after = after_proc.stdout.strip() if after_proc.returncode == 0 else target
    result["after"] = after
    result["changed_files"] = dirty_files
    result["status"] = "updated" if after != before else "up_to_date"
    note = f"ff 병합 불가 → 로컬 추적 파일 {len(dirty_files)}건을 원격({target[:7]}) 상태로 되돌림"
    if ahead_count > 0:
        note += f" · 로컬에만 있던 커밋 {ahead_count}건 폐기"
    if result["backup_patch"]:
        note += f" · 변경 백업 {Path(result['backup_patch']).name}"
    result["message"] = note
    return _verify_local_only(result, repo_dir, protected_before)


def _verify_local_only(result: dict, repo_dir: Path, protected_before: dict) -> dict:
    """동기화 후에도 상태·인증 파일이 그대로 남아 있는지 확인한다."""
    missing = [
        name for name, existed in protected_before.items()
        if existed and not (repo_dir / name).exists()
    ]
    result["missing_local_files"] = missing
    if missing:
        result["message"] = (
            result.get("message", "")
            + f" ⚠️ 로컬 전용 파일이 사라졌습니다: {', '.join(missing)}"
        )
    return result


def describe_sync(result: dict) -> str:
    """sync_repo 결과를 사람이 읽는 로그 한 덩어리로 만든다."""
    status = result.get("status")
    short = lambda value: (value or "")[:7]

    if status == "updated":
        files = result.get("changed_files") or []
        lines = [f"🔄 실행 전 코드 동기화: {short(result.get('before'))} → {short(result.get('after'))}"]
        if files:
            lines[-1] += f" (파일 {len(files)}건)"
            for name in files[:8]:
                lines.append(f"   · {name}")
            if len(files) > 8:
                lines.append(f"   · … 외 {len(files) - 8}건")
        if result.get("message"):
            lines.append(f"   · {result['message']}")
    elif status == "up_to_date":
        lines = [f"✅ 실행 전 코드 동기화: 이미 최신 코드입니다 ({short(result.get('after') or result.get('before'))})"]
    elif status == "skipped":
        lines = [f"ℹ️ 코드 동기화 건너뜀: {result.get('message', '')}"]
    else:
        lines = [f"⚠️ 코드 동기화 실패 → 현재 로컬 코드로 계속 실행합니다: {result.get('message', '')}"]

    if result.get("missing_local_files"):
        lines.append(f"⚠️ 동기화 후 사라진 로컬 전용 파일: {', '.join(result['missing_local_files'])}")
    return "\n".join(lines)


def _is_sync_child() -> bool:
    """동기화 때문에 재실행된 하위 프로세스인지(무한 재실행 방지)."""
    return os.environ.get(SYNC_CHILD_ENV) == "1"


def respawn_with_latest_code(extra_args: List[str]) -> int:
    """방금 받은 최신 코드가 새로 import 되도록 같은 명령을 새 파이썬 프로세스로 재실행한다."""
    cmd = [sys.executable, str(Path(__file__).resolve())] + list(extra_args) + ["--no-sync"]
    env = dict(os.environ)
    env[SYNC_CHILD_ENV] = "1"
    print("🔄 최신 코드가 반영되어 새 프로세스로 다시 시작합니다: " + " ".join(cmd[1:]))
    try:
        return subprocess.run(cmd, cwd=str(config.BASE_DIR), env=env).returncode
    except OSError as e:
        print(f"⚠️ 재실행 실패({e}) → 현재 코드로 계속 진행합니다.")
        return 0


def sync_before_run(argv: List[str]) -> Optional[int]:
    """1회 실행 모드의 실행 전 동기화.

    Returns: 최신 코드로 재실행한 경우 그 종료 코드, 재실행이 필요 없으면 None.
    """
    result = sync_repo()
    print(describe_sync(result))
    if result["status"] != "updated":
        return None
    # 이미 import 된 모듈은 이전 코드이므로 새 프로세스로 재실행해야 최신 코드가 적용된다.
    return respawn_with_latest_code(argv)


def run_slot_in_new_process(
    slot_id: str,
    theme: str = "bright_room_minimal",
    upload_youtube: bool = False,
    dry_run: bool = False,
) -> int:
    """방금 동기화한 최신 코드로 1회 실행할 하위 프로세스를 띄운다.

    같은 프로세스에서 run_daily_job() 을 부르면 방금 갱신된 product_pool.py 등이
    메모리에 다시 로드되지 않으므로, 반드시 새 파이썬 프로세스에서 실행한다.
    하위 프로세스에는 --no-sync 를 넘겨 재귀 동기화(무한 루프)를 막는다.
    """
    cmd = [
        sys.executable, str(Path(__file__).resolve()),
        "--now", "--slot", slot_id, "--no-sync",
        "--theme", theme,
    ]
    if upload_youtube:
        cmd.append("--youtube")
    if dry_run:
        cmd.append("--dry-run")

    env = dict(os.environ)
    env[SYNC_CHILD_ENV] = "1"
    print("🚀 최신 코드로 새 프로세스 실행: " + " ".join(cmd[1:]))
    try:
        return subprocess.run(cmd, cwd=str(config.BASE_DIR), env=env).returncode
    except OSError as e:
        print(f"⚠️ 하위 프로세스 실행 실패: {e}")
        return 1


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"completed_slots": [], "history": []}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run_daily_job(
    slot_id: Optional[str] = None,
    force: bool = False,
    theme: str = "bright_room_minimal",
    upload_youtube: bool = False,
    dry_run: bool = False
) -> Optional[Path]:
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_hour_slot = slot_id or f"{today_str}_{now.hour:02d}"

    state = load_state()
    completed_slots = state.get("completed_slots", [])

    if not force and current_hour_slot in completed_slots:
        print(f"ℹ️ 현재 슬롯({current_hour_slot})의 쇼츠는 이미 생성되었습니다.")
        print("💡 강제 재실행하려면 --force 플래그를 붙여 실행하세요.")
        if state.get("history"):
            return Path(state["history"][-1]["video_path"])
        return None

    # 도감(gooditem-archive)에 이미 올라간 상품은 상태에 자동 반영
    # → daily_state.json 이 유실되거나 git pull 로 되돌아가도 중복이 생기지 않는다.
    archive_items, _archive_source = load_archive_items()
    state = reconcile_state_with_archive(state, archive_items)

    # 삼중 중복 가드: 로컬 상태 + 원격 도감 + 유튜브 채널 RSS
    guard = collect_guard(state)
    print(describe_guard(guard))
    for warning in guard["warnings"]:
        print(f"   · {warning}")

    # 다음 순번 에피소드 자동 선택 (테마 및 상품 자동 회전, 사용 상품 재사용 금지)
    state_before_select = copy.deepcopy(state)
    selected_script, state = get_next_dynamic_episode(
        state,
        blocked_item_ids=guard["blocked_item_ids"],
        published_titles=guard["published_titles"],
    )

    if selected_script is None:
        print("\n🚫 새로운 미사용 상품이 없어 쇼츠 생성·업로드를 건너뜁니다.")
        print("   모든 테마의 미사용 실물 상품이 3종 미만입니다.")
        print("   product_pool.py 에 새 실물 상품(실제 제품 이미지 포함)을 추가하면 다음 슬롯부터 다시 생성됩니다.")
        save_state(state)
        return None

    # 업로드 전 무결성 사전 검증 (이미지·lptag·1:1 매칭)
    preflight_ok, problems = check_episode(selected_script)
    if not preflight_ok:
        print(format_problems(problems))
        print("   → 상태를 선택 전으로 되돌리고 종료합니다(상품 소모 없음).")
        save_state(state_before_select)
        return None
    print("✅ 사전 검증 통과: 상품 이미지 3종 존재 · 쿠팡 링크 lptag · 1:1 매칭 정상")

    timestamp = now.strftime("%Y%m%d_%H%M%S")
    work_dir = config.OUTPUT_DIR / f"temp_{timestamp}"
    work_dir.mkdir(parents=True, exist_ok=True)

    renderer = SlideRenderer(theme=theme)
    voice_gen = VoiceGenerator()
    video_builder = VideoBuilder()

    slide_items = []
    total_duration = 0.0

    print(f"\n=======================================================")
    print(f"🚀 쇼츠 자동 생성 슬롯 [{current_hour_slot}]: [{selected_script.topic}]")
    print(f"🎨 디자인 모드: 화사한 룸 미니멀 클린 (아이 목소리 적용)")
    print(f"=======================================================\n")

    for i, slide in enumerate(selected_script.slides):
        print(f"[{i+1}/{len(selected_script.slides)}] {slide.step_name} 슬라이드 처리 중...")

        # 1. 슬라이드 이미지 렌더링
        img_path = work_dir / f"slide_{i:02d}.png"
        renderer.render_slide(slide, img_path)

        # 2. AI 성우 음성 생성
        audio_path = work_dir / f"voice_{i:02d}.mp3"
        duration = voice_gen.generate_slide_audio(slide.voice_script, audio_path)
        total_duration += duration

        print(f"   -> 음성 길이: {duration:.2f}초 | 멘트: \"{slide.voice_script[:25]}...\"")
        slide_items.append((img_path, audio_path, duration))

    # 3. 비디오 인코딩 및 최종 병합
    safe_topic = "".join([c for c in selected_script.topic if c.isalnum() or c in (" ", "_")]).rstrip().replace(" ", "_")
    output_filename = f"Shorts_{safe_topic}_{timestamp}.mp4"
    output_video_path = DAILY_OUTPUT_DIR / output_filename

    print(f"\n🎥 영상 인코딩 및 최종 병합 중 (예상 길이: 약 {int(total_duration)}초)...")
    success = video_builder.build_shorts_video(slide_items, output_video_path)

    # 1번 훅 인트로 슬라이드를 비디오와 동일한 이름의 썸네일 파일로 자동 보존
    thumb_path = output_video_path.with_suffix(".thumb.png")
    hook_img = work_dir / "slide_00.png"
    if hook_img.exists():
        import shutil
        shutil.copy(hook_img, thumb_path)
        print(f"🖼️ 1번 훅 썸네일 이미지 자동 보존 완료: {thumb_path.name}")

    # 임시 디렉터리 정리
    import shutil
    shutil.rmtree(work_dir, ignore_errors=True)

    if not success:
        print("❌ 비디오 생성에 실패했습니다.")
        return None

    print(f"\n=======================================================")
    print(f"✨ 슬롯 [{current_hour_slot}] 쇼츠 영상 자동 제작 완료!")
    print(f"📁 파일 위치: {output_video_path.resolve()}")
    if thumb_path.exists():
        print(f"🖼️ 썸네일 위치: {thumb_path.resolve()}")
    print(f"⏱️ 영상 길이: 약 {int(total_duration)}초 (세로 1080x1920)")
    print(f"=======================================================\n")

    youtube_url = None
    uploader = YouTubeUploader()

    # 유튜브 자동 업로드 시도 (dry_run 이면 절대 업로드하지 않음)
    if not dry_run and (upload_youtube or uploader.is_configured()):
        print("\n📺 YouTube 자동 업로드 모듈 가동...")
        youtube_url = uploader.upload(
            video_path=output_video_path,
            title=selected_script.youtube_title,
            description=selected_script.youtube_description,
            tags=selected_script.hashtags,
            privacy_status="public",
            thumbnail_path=thumb_path if thumb_path.exists() else None
        )

    caption_text = (
        f"🎬 [{current_hour_slot}] 오늘의 쇼츠 완성!\n\n"
        f"📌 제목:\n{selected_script.youtube_title}\n\n"
        f"📝 설명란:\n{selected_script.youtube_description}\n\n"
        f"🏷️ 해시태그:\n{' '.join(selected_script.hashtags)}"
    )

    if youtube_url:
        caption_text = f"✨ 유튜브 쇼츠 자동 업로드 완료!\n🔗 {youtube_url}\n\n" + caption_text

    print(caption_text)
    print("\n-------------------------------------------------------")

    # 모바일 웹 링크 페이지(GitHub Pages) 자동 갱신 — 실제 게시된 영상만 도감에 올린다
    # (유튜브 업로드가 끝나지 않은 회차를 도감에 먼저 올리면 링크가 살아있는 영상이 없어진다)
    if selected_script.items and not dry_run:
        if uploader.is_configured() and not youtube_url:
            print("\n🌐 유튜브 업로드가 완료되지 않아 도감 갱신을 건너뜁니다(게시분만 반영).")
        else:
            print("\n🌐 모바일 링크 페이지(GitHub Pages) 자동 갱신 중...")
            try:
                update_link_page(theme_name=selected_script.topic, items=selected_script.items, auto_push=not dry_run)
                print("✅ 모바일 웹페이지 최신 꿀템 링크 자동 반영 완료!")
            except Exception as e:
                print(f"⚠️ 모바일 웹페이지 갱신 중 오류: {e}")

    # 상태 업데이트
    if "completed_slots" not in state:
        state["completed_slots"] = []
    if current_hour_slot not in state["completed_slots"]:
        state["completed_slots"].append(current_hour_slot)

    # 오래된 슬롯 기록 정리 (최근 30일 유지)
    if len(state["completed_slots"]) > 90:
        state["completed_slots"] = state["completed_slots"][-90:]

    state["last_run_date"] = today_str
    history_entry = {
        "slot": current_hour_slot,
        "date": today_str,
        "topic": selected_script.topic,
        "video_path": str(output_video_path)
    }
    if youtube_url:
        history_entry["youtube_url"] = youtube_url
    if "history" not in state:
        state["history"] = []
    state["history"].append(history_entry)

    # 게시된 회차 제목을 상태에 남겨 다음 실행에서 같은 제목 회차를 건너뛰게 한다.
    published_titles = state.setdefault("published_titles", [])
    normalized = normalize_title(selected_script.youtube_title)
    if normalized and normalized not in published_titles:
        published_titles.append(normalized)

    save_state(state)

    return output_video_path


def daemon_loop(slots: List[int] = DEFAULT_SLOTS, theme: str = "bright_room_minimal", upload_youtube: bool = False, dry_run: bool = False):
    slot_desc = ", ".join([f"{h:02d}:00" for h in sorted(slots)])
    print(f"🕒 데일리 쇼츠 하루 3회 무인 자동화 백그라운드 데몬 가동 중...")
    print(f"⏰ 지정된 슬롯 시각: 매일 [{slot_desc}] 총 {len(slots)}회 자동 생성 및 업로드")
    print(f"🔄 각 슬롯 직전에 원격 {GIT_REMOTE}/{GIT_BRANCH} 최신 코드를 자동으로 내려받은 뒤 새 프로세스로 실행합니다")
    print("💡 중단하려면 Ctrl+C를 누르세요.\n")

    retry_after = {}  # slot_id -> 이 시각(time.time()) 전에는 같은 슬롯을 재시도하지 않는다
    attempts = {}     # slot_id -> 이번 시간대에 하위 프로세스를 실행한 횟수
    max_attempts = 6  # 최대 6회(5분 간격)까지 재시도하고, 그래도 안 되면 다음 슬롯으로 넘긴다

    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        current_hour = now.hour

        if current_hour in slots:
            slot_id = f"{today_str}_{current_hour:02d}"
            state = load_state()
            completed_slots = state.get("completed_slots", [])

            if slot_id not in completed_slots and time.time() >= retry_after.get(slot_id, 0.0):
                # 오늘 완료된 슬롯 수 계산
                today_done = [s for s in completed_slots if s.startswith(today_str)]
                print(f"\n[알림] ⏰ {current_hour:02d}:00 슬롯 도달! (오늘 {len(today_done) + 1}/{len(slots)}번째 영상 생성 시작)")

                # 1) 실행 직전 최신 코드 동기화 (실패해도 경고만 찍고 로컬 코드로 계속)
                sync_result = sync_repo()
                print(describe_sync(sync_result))

                # 2) 방금 받은 최신 코드가 새로 import 되도록 새 프로세스에서 1회 실행
                attempts[slot_id] = attempts.get(slot_id, 0) + 1
                exit_code = run_slot_in_new_process(
                    slot_id, theme=theme, upload_youtube=upload_youtube, dry_run=dry_run
                )

                if exit_code == 0 and slot_id in load_state().get("completed_slots", []):
                    print(f"✅ 슬롯 [{slot_id}] 생성·게시 완료")
                elif attempts[slot_id] >= max_attempts:
                    print(f"⏭️ 슬롯 [{slot_id}] {attempts[slot_id]}회 시도 후 생성되지 않았습니다. 이번 시간대는 건너뜁니다.")
                    retry_after[slot_id] = float("inf")
                else:
                    reason = "비정상 종료" if exit_code != 0 else "생성 없이 종료"
                    print(
                        f"⚠️ 슬롯 [{slot_id}] {reason}(code={exit_code}) → 5분 후 재시도합니다 "
                        f"({attempts[slot_id]}/{max_attempts})"
                    )
                    retry_after[slot_id] = time.time() + 300

                if len(retry_after) > 60:
                    retry_after = {k: v for k, v in retry_after.items() if k >= today_str}
                    attempts = {k: v for k, v in attempts.items() if k >= today_str}


        time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description="쿠팡 파트너스 하루 3회 쇼츠 무인 자동화 러너")
    parser.add_argument("--now", action="store_true", help="지금 즉시 1회 생성")
    parser.add_argument("--batch", type=int, default=0, help="한 번에 연속 N개 영상 일괄 생성 (예: --batch 3)")
    parser.add_argument("--force", action="store_true", help="현재 슬롯이 이미 완료되었어도 강제 재실행")
    parser.add_argument("--theme", default="bright_room_minimal", help="디자인 테마")
    parser.add_argument("--youtube", action="store_true", help="생성 완료 후 YouTube Data API로 자동 업로드")
    parser.add_argument("--daemon", action="store_true", help="하루 3회 지정 슬롯에 자동 실행하는 데몬 모드")
    parser.add_argument("--dry-run", action="store_true", help="생성만 하고 유튜브 업로드·도감 푸시는 하지 않음(테스트용)")
    parser.add_argument("--slots", type=int, nargs="+", default=DEFAULT_SLOTS, help="실행 시각 슬롯 목록 (기본: 8 12 18)")
    parser.add_argument("--slot", default=None, help="완료 슬롯 ID 지정 (데몬이 하위 프로세스로 넘길 때 사용, 예: 2026-11-17_08)")
    parser.add_argument("--no-sync", action="store_true", help="실행 전 자동 Git 동기화를 건너뛰고 현재 코드로 바로 실행")

    args = parser.parse_args()
    dry_run = args.dry_run

    # 실행 전 자동 Git 동기화: 최신 코드를 받아오고, 코드가 갱신됐으면 새 프로세스로 재실행한다.
    # (데몬은 슬롯마다 따로 동기화하므로 기동 시점에는 건너뛴다. --no-sync·하위 프로세스도 건너뛴다.)
    if not args.no_sync and not args.daemon and not _is_sync_child():
        exit_code = sync_before_run(sys.argv[1:])
        if exit_code is not None:
            sys.exit(exit_code)

    if args.batch > 0:
        print(f"🎬 연속 {args.batch}개 영상 일괄 배치 생성을 시작합니다...\n")
        for i in range(args.batch):
            now = datetime.now()
            batch_slot_id = f"batch_{now.strftime('%Y%m%d_%H%M%S')}_{i+1}"
            print(f"\n>>> [배치 {i+1}/{args.batch}] 생성 시작 <<<")
            run_daily_job(slot_id=batch_slot_id, force=True, theme=args.theme, upload_youtube=args.youtube, dry_run=dry_run)
            if i < args.batch - 1:
                time.sleep(2)
        print(f"\n🎉 총 {args.batch}개 영상 일괄 배치 제작 완료!")
    elif args.daemon:
        daemon_loop(slots=args.slots, theme=args.theme, upload_youtube=args.youtube, dry_run=dry_run)
    else:
        run_daily_job(
            slot_id=args.slot,
            force=args.force or args.now,
            theme=args.theme,
            upload_youtube=args.youtube,
            dry_run=dry_run,
        )


if __name__ == "__main__":
    main()
