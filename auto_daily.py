import argparse
import copy
import json
import sys
import io
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
    print("💡 중단하려면 Ctrl+C를 누르세요.\n")

    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        current_hour = now.hour

        if current_hour in slots:
            slot_id = f"{today_str}_{current_hour:02d}"
            state = load_state()
            completed_slots = state.get("completed_slots", [])

            if slot_id not in completed_slots:
                # 오늘 완료된 슬롯 수 계산
                today_done = [s for s in completed_slots if s.startswith(today_str)]
                print(f"\n[알림] ⏰ {current_hour:02d}:00 슬롯 도달! (오늘 {len(today_done) + 1}/{len(slots)}번째 영상 생성 시작)")
                run_daily_job(slot_id=slot_id, force=False, theme=theme, upload_youtube=upload_youtube, dry_run=dry_run)

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

    args = parser.parse_args()
    dry_run = args.dry_run

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
        run_daily_job(force=args.force or args.now, theme=args.theme, upload_youtube=args.youtube, dry_run=dry_run)


if __name__ == "__main__":
    main()
