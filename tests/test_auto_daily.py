# -*- coding: utf-8 -*-
"""auto_daily 파이프라인 배선 테스트 (업로드·전송 없이).

ffmpeg/TTS 없이도 '가드 → 사전검증 → 상태 기록' 배선이 정상인지 확인한다.
렌더러·보이스·비디오 빌더는 테스트용 스텁으로 대체한다.
"""

import json
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import auto_daily
import publish_guard
from PIL import Image

failures = []


def check(cond, message):
    print(("  ✅ " if cond else "  ❌ ") + message)
    if not cond:
        failures.append(message)


class FakeRenderer:
    def __init__(self, *a, **kw):
        pass

    def render_slide(self, slide, output_path, with_character=False):
        Image.new("RGB", (108, 192), (255, 255, 255)).save(output_path)


class FakeVoice:
    def __init__(self, *a, **kw):
        pass

    def generate_slide_audio(self, text, output_path):
        Path(output_path).write_bytes(b"fake-mp3")
        return 2.0


class FakeVideo:
    def __init__(self, *a, **kw):
        pass

    def build_shorts_video(self, slide_items, output_path):
        Path(output_path).write_bytes(b"fake-mp4")
        return True


calls = {"web": 0, "upload": 0}

auto_daily.SlideRenderer = FakeRenderer
auto_daily.VoiceGenerator = FakeVoice
auto_daily.VideoBuilder = FakeVideo
auto_daily.update_link_page = lambda **kw: calls.__setitem__("web", calls["web"] + 1) or True


class SpyUploader:
    def __init__(self, *a, **kw):
        pass

    def is_configured(self):
        return True

    def upload(self, **kw):
        calls["upload"] += 1
        return "https://youtu.be/SHOULD_NOT_HAPPEN"


auto_daily.YouTubeUploader = SpyUploader

tmp_state = Path(tempfile.mkdtemp()) / "state.json"
auto_daily.STATE_FILE = tmp_state

print("\n=== A. 신규 회차 1회 드라이런 (업로드·전송·도감푸시 금지) ===")
archive_items, _ = publish_guard.load_archive_items()
seed = {"completed_slots": [], "history": []}
seed = publish_guard.reconcile_state_with_archive(seed, archive_items)
seed_used = {k: set(v) for k, v in seed.get("used_items_by_theme", {}).items()}
tmp_state.write_text(json.dumps(seed, ensure_ascii=False), encoding="utf-8")

result = auto_daily.run_daily_job(slot_id="test_dryrun_01", force=True, dry_run=True)
state = json.loads(tmp_state.read_text(encoding="utf-8"))

# 어느 테마가 선택될지는 도감 게시분에 따라 달라지므로, 이번 실행으로 새로 소모된 테마를 찾아 검증한다.
new_theme = None
for theme_key, ids in state.get("used_items_by_theme", {}).items():
    if set(ids) - seed_used.get(theme_key, set()):
        new_theme = theme_key
newly_used = set(state["used_items_by_theme"][new_theme]) - seed_used.get(new_theme, set()) if new_theme else set()

check(result is not None and result.exists(), "영상 파일 생성 단계까지 도달")
check(calls["upload"] == 0, "유튜브 업로드 호출 0회 (드라이런)")
check(calls["web"] == 0, "도감(history.json) 갱신 호출 0회 (드라이런)")
check(new_theme is not None and len(newly_used) == 3, f"새 회차 테마({new_theme}) 상품 3종이 사용 처리됨 ({sorted(newly_used)})")
check("test_dryrun_01" in state["completed_slots"], "완료 슬롯 기록됨")
check(
    new_theme is not None
    and state.get("episode_counts_by_theme", {}).get(new_theme, 0)
    == seed.get("episode_counts_by_theme", {}).get(new_theme, 0) + 1,
    "회차 카운트가 1 증가",
)
check(
    len(state.get("published_titles", [])) >= len(seed.get("published_titles", [])),
    f"게시 제목 잠금 유지 ({len(state.get('published_titles', []))}건)",
)

print("\n=== B. 남은 상품이 없을 때 건너뛰기 ===")
exhausted = json.loads(tmp_state.read_text(encoding="utf-8"))
# 18종을 모두 사용 처리해 '새 상품 없음' 상태를 만든다
from product_pool import THEMES

for theme_key, theme in THEMES.items():
    exhausted.setdefault("used_items_by_theme", {})[theme_key] = [p.item_id for p in theme["products"]]
tmp_state.write_text(json.dumps(exhausted, ensure_ascii=False), encoding="utf-8")

# 네트워크 근거(RSS·원격 도감)를 못 쓰는 폴백 상황에서는 로컬 상태(전부 사용)를 그대로 신뢰한다
_saved_guard = auto_daily.collect_guard
_saved_describe = auto_daily.describe_guard
auto_daily.collect_guard = lambda state, *a, **k: {
    "blocked_item_ids": {i for ids in state.get("used_items_by_theme", {}).values() for i in ids},
    "published_titles": set(state.get("published_titles", [])),
    "rss_titles": set(),
    "archive_items": [],
    "sources": {"rss_ok": False, "archive_source": "local", "archive_items": 0,
                "local_items": 0, "rss_titles": 0, "local_titles": 0},
    "warnings": [],
}
auto_daily.describe_guard = lambda guard: "[stub guard]"
try:
    result2 = auto_daily.run_daily_job(slot_id="test_dryrun_02", force=True, dry_run=True)
finally:
    auto_daily.collect_guard = _saved_guard
    auto_daily.describe_guard = _saved_describe
check(result2 is None, "새 상품이 없으면 None 반환 (생성·업로드 skip)")
check(calls["upload"] == 0, "skip 시에도 업로드 없음")

print("\n=== C. 사전 검증 실패 시 상품 소모 없음 ===")
seed2 = {"completed_slots": [], "history": []}
seed2 = publish_guard.reconcile_state_with_archive(seed2, archive_items)
tmp_state.write_text(json.dumps(seed2, ensure_ascii=False), encoding="utf-8")

original_check = auto_daily.check_episode
auto_daily.check_episode = lambda script: (False, ["forced preflight failure"])
result3 = auto_daily.run_daily_job(slot_id="test_dryrun_03", force=True, dry_run=True)
auto_daily.check_episode = original_check
state3 = json.loads(tmp_state.read_text(encoding="utf-8"))

check(result3 is None, "사전 검증 실패 시 None 반환 (차단)")

def _norm_used(mapping):
    return {k: sorted(v) for k, v in (mapping or {}).items()}

check(
    _norm_used(state3.get("used_items_by_theme")) == _norm_used(seed2.get("used_items_by_theme")),
    "실패 시 새 상품이 소모되지 않음(상태 롤백)",
)
check("test_dryrun_03" not in state3.get("completed_slots", []), "슬롯이 완료 처리되지 않음")


# =====================================================================
# D. sync_repo — 실행 전 자동 Git 동기화
# =====================================================================
print("\n=== D. sync_repo: 원격 최신 코드 자동 동기화 ===")

import os
import subprocess as sp

GIT_ENV = dict(
    os.environ,
    GIT_AUTHOR_NAME="test", GIT_AUTHOR_EMAIL="test@example.com",
    GIT_COMMITTER_NAME="test", GIT_COMMITTER_EMAIL="test@example.com",
    GIT_CONFIG_NOSYSTEM="1",
)


def run_git(*args, cwd):
    res = sp.run(["git"] + list(args), cwd=str(cwd), capture_output=True, text=True, env=GIT_ENV)
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} 실패: {res.stderr.strip()}")
    return res


def commit_all(repo, message):
    run_git("add", "-A", cwd=repo)
    run_git("commit", "-m", message, cwd=repo)


sync_root = Path(tempfile.mkdtemp())
origin_dir = sync_root / "origin.git"
upstream = sync_root / "upstream"     # 코코 쪽(새 테마·코드 갱신을 푸시하는 곳)
work = sync_root / "work"             # 윤민 님 PC

run_git("init", "--bare", "-b", "main", str(origin_dir), cwd=sync_root)
run_git("clone", str(origin_dir), str(upstream), cwd=sync_root)
(upstream / "product_pool.py").write_text("POOL = 'v1'\n", encoding="utf-8")
(upstream / ".gitignore").write_text(
    "daily_state.json\noutput/\ntoken.pickle\nclient_secrets.json\n", encoding="utf-8"
)
commit_all(upstream, "init")
run_git("push", "-u", "origin", "main", cwd=upstream)
run_git("clone", str(origin_dir), str(work), cwd=sync_root)

# PC 에만 있는 상태·인증 파일 (gitignore 대상 → 동기화로 지워지면 안 됨)
STATE_JSON = '{"completed_slots": ["2026-11-17_08"]}'
(work / "daily_state.json").write_text(STATE_JSON, encoding="utf-8")
(work / "token.pickle").write_bytes(b"\x80\x04pc-token")
(work / "output").mkdir(exist_ok=True)
(work / "output" / "keep.txt").write_text("video", encoding="utf-8")


# D-1. 이미 최신
res = auto_daily.sync_repo(repo_dir=work)
check(res["status"] == "up_to_date", f"D-1 이미 최신이면 up_to_date (실제 {res['status']}: {res['message']})")

# D-2. 원격이 앞서 있으면 fast-forward
(upstream / "product_pool.py").write_text("POOL = 'v2'\n", encoding="utf-8")
commit_all(upstream, "pool v2")
run_git("push", "origin", "main", cwd=upstream)
res = auto_daily.sync_repo(repo_dir=work)
check(res["status"] == "updated", f"D-2 원격이 앞서면 updated (실제 {res['status']}: {res['message']})")
check((work / "product_pool.py").read_text(encoding="utf-8") == "POOL = 'v2'\n", "D-2 최신 product_pool.py 내용 반영")
check("product_pool.py" in res["changed_files"], f"D-2 갱신 파일 목록에 product_pool.py 포함 (실제 {res['changed_files']})")
check(res["before"] != res["after"], "D-2 커밋 해시 변경 기록")
check((work / "daily_state.json").read_text(encoding="utf-8") == STATE_JSON, "D-2 ff 동기화 후 daily_state.json 보존")
check((work / "token.pickle").exists() and (work / "output" / "keep.txt").exists(), "D-2 token.pickle·output/ 보존")
check(res["missing_local_files"] == [], "D-2 로컬 전용 파일 유실 없음")

# D-3. 로컬 추적 파일을 고쳐 ff 병합이 막히면 reset --hard 폴백 (상태 파일은 보존)
(work / "product_pool.py").write_text("POOL = 'LOCAL_EDIT'\n", encoding="utf-8")
(upstream / "product_pool.py").write_text("POOL = 'v3'\n", encoding="utf-8")
commit_all(upstream, "pool v3")
run_git("push", "origin", "main", cwd=upstream)

_orig_output_dir = auto_daily.config.OUTPUT_DIR
auto_daily.config.OUTPUT_DIR = sync_root / "out"
try:
    res = auto_daily.sync_repo(repo_dir=work)
finally:
    auto_daily.config.OUTPUT_DIR = _orig_output_dir

check(res["status"] == "updated", f"D-3 ff 병합 실패 시 reset --hard 폴백 (실제 {res['status']}: {res['message']})")
check((work / "product_pool.py").read_text(encoding="utf-8") == "POOL = 'v3'\n", "D-3 원격 코드로 맞춰짐")
check("product_pool.py" in res["changed_files"], "D-3 되돌린 로컬 변경 파일 기록")
check(bool(res["backup_patch"]) and Path(res["backup_patch"]).exists(), "D-3 로컬 변경 patch 백업본 생성")
if res["backup_patch"]:
    check("LOCAL_EDIT" in Path(res["backup_patch"]).read_text(encoding="utf-8"), "D-3 백업 patch 에 로컬 수정 내용 보존")
check((work / "daily_state.json").read_text(encoding="utf-8") == STATE_JSON, "D-3 reset --hard 후에도 daily_state.json 보존")
check((work / "token.pickle").exists(), "D-3 reset --hard 후에도 token.pickle 보존")
check((work / "output" / "keep.txt").read_text(encoding="utf-8") == "video", "D-3 reset --hard 후에도 output/ 보존")
check(res["missing_local_files"] == [], "D-3 로컬 전용 파일 유실 없음")

# D-4. 네트워크·원격 오류는 예외 없이 error 로 반환 (로컬 코드로 계속)
run_git("remote", "set-url", "origin", str(sync_root / "no-such-repo.git"), cwd=work)
res = auto_daily.sync_repo(repo_dir=work)
check(res["status"] == "error", f"D-4 원격 접속 실패는 error 반환 (실제 {res['status']})")
check(bool(res["message"]), "D-4 실패 사유 메시지 포함")
run_git("remote", "set-url", "origin", str(origin_dir), cwd=work)

# D-5. Git 저장소가 아니면( zip 배포본) skipped
plain_dir = sync_root / "plain"
plain_dir.mkdir(exist_ok=True)
res = auto_daily.sync_repo(repo_dir=plain_dir)
check(res["status"] == "skipped", f"D-5 Git 저장소 아님 → skipped (실제 {res['status']})")

# D-6. PC 에만 있는 로컬 커밋은 지우지 않는다 (앞서 있으면 병합할 것도 없음)
(work / "local_note.txt").write_text("pc only", encoding="utf-8")
commit_all(work, "pc only commit")
res = auto_daily.sync_repo(repo_dir=work)
check(res["status"] == "up_to_date", f"D-6 로컬 커밋이 앞서면 up_to_date (실제 {res['status']}: {res['message']})")
check((work / "local_note.txt").exists(), "D-6 로컬 커밋 유지")

# D-7. 로그 문구
check("코드 동기화" in auto_daily.describe_sync(res), "D-7 동기화 결과 로그 문구 생성")


# =====================================================================
# E. CLI 배선 (--no-sync / 실행 전 동기화 / 데몬 하위 프로세스)
# =====================================================================
print("\n=== E. CLI 배선: --no-sync·실행 전 동기화·데몬 하위 프로세스 ===")

probe = sync_root / "probe.py"
probe.write_text(
    '''# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, {base!r})
import auto_daily

mode = sys.argv[1]


def boom(*a, **k):
    print("SYNC_CALLED")
    raise AssertionError("이 모드에서는 동기화가 호출되면 안 된다")


def fake_sync(status):
    def _f(*a, **k):
        print("SYNC_CALLED")
        return {{"status": status, "before": "a" * 40, "after": "a" * 40,
                 "changed_files": [], "backup_patch": None,
                 "missing_local_files": [], "message": "stub"}}
    return _f


auto_daily.run_daily_job = lambda **kw: print("JOB_CALLED slot=%s force=%s dry=%s" % (
    kw.get("slot_id"), kw.get("force"), kw.get("dry_run")))

if mode == "no_sync":
    auto_daily.sync_repo = boom
    sys.argv = ["auto_daily.py", "--now", "--slot", "2026-11-17_08", "--no-sync", "--dry-run"]
elif mode == "sync_uptodate":
    auto_daily.sync_repo = fake_sync("up_to_date")
    sys.argv = ["auto_daily.py", "--now", "--slot", "2026-11-17_09", "--dry-run"]
elif mode == "sync_updated":
    auto_daily.sync_repo = fake_sync("updated")
    auto_daily.respawn_with_latest_code = lambda extra: (print("RESPAWN %s" % extra), 0)[1]
    sys.argv = ["auto_daily.py", "--now", "--dry-run"]
elif mode == "daemon":
    auto_daily.daemon_loop = lambda **kw: print("DAEMON_START")
    auto_daily.sync_repo = boom
    sys.argv = ["auto_daily.py", "--daemon"]
elif mode == "daemon_slot":
    import datetime as _dt

    class FakeDateTime:
        @classmethod
        def now(cls):
            return _dt.datetime(2026, 11, 17, 8, 0, 0)

    class Stop(Exception):
        pass

    auto_daily.datetime = FakeDateTime
    auto_daily.load_state = lambda: {{"completed_slots": []}}
    events = []

    def fake_sync(*a, **k):
        events.append("sync")
        return {{"status": "up_to_date", "before": "a" * 40, "after": "a" * 40,
                 "changed_files": [], "backup_patch": None,
                 "missing_local_files": [], "message": ""}}

    def fake_spawn(slot_id, **kw):
        events.append(("spawn", slot_id, kw))
        return 0

    def fake_sleep(_seconds):
        print("EVENTS %s" % " > ".join(e[0] if isinstance(e, tuple) else e for e in events))
        for e in events:
            if isinstance(e, tuple):
                print("SPAWN slot=%s kw=%s" % (e[1], sorted(e[2].items())))
        raise Stop()

    auto_daily.sync_repo = fake_sync
    auto_daily.run_slot_in_new_process = fake_spawn
    auto_daily.time.sleep = fake_sleep
    try:
        auto_daily.daemon_loop(slots=[8, 12, 18], theme="bright_room_minimal",
                               upload_youtube=True, dry_run=True)
    except Stop:
        pass
    raise SystemExit(0)

try:
    auto_daily.main()
except SystemExit as e:
    print("EXIT_CODE %s" % e.code)
print("MAIN_DONE")
'''.format(base=str(BASE)),
    encoding="utf-8",
)


def run_probe(mode):
    return sp.run(
        [sys.executable, str(probe), mode],
        cwd=str(BASE), capture_output=True, text=True, timeout=180,
        env=dict(os.environ, PYTHONIOENCODING="utf-8"),
    )

# E-1. --now --no-sync → 동기화 없이 바로 실행, --slot 이 그대로 전달
proc = run_probe("no_sync")
check(proc.returncode == 0, f"E-1 프로세스 정상 종료 (실제 {proc.returncode}: {proc.stderr.strip()[:200]})")
check("SYNC_CALLED" not in proc.stdout, "E-1 --no-sync 는 sync_repo 를 호출하지 않음")
check("JOB_CALLED slot=2026-11-17_08" in proc.stdout, f"E-1 --slot 이 run_daily_job 으로 전달 (출력: {proc.stdout.strip()[-200:]})")

# E-2. 플래그 없이 --now → 실행 전 동기화 1회 후 현재 코드로 실행
proc = run_probe("sync_uptodate")
check(proc.returncode == 0, f"E-2 정상 종료 (실제 {proc.returncode}: {proc.stderr.strip()[:200]})")
check(proc.stdout.count("SYNC_CALLED") == 1, f"E-2 동기화 1회 수행 (실제 {proc.stdout.count('SYNC_CALLED')}회)")
check("JOB_CALLED slot=2026-11-17_09" in proc.stdout, "E-2 최신 상태면 그대로 실행")

# E-3. 동기화로 코드가 갱신되면 새 프로세스로 재실행하고 부모는 실행하지 않음
proc = run_probe("sync_updated")
check(proc.returncode == 0 and "EXIT_CODE 0" in proc.stdout, f"E-3 부모는 재실행 결과로 종료 (출력: {proc.stdout.strip()[-250:]})")
check("RESPAWN ['--now', '--dry-run']" in proc.stdout, f"E-3 코드가 갱신되면 같은 인자로 재실행 요청 (출력: {proc.stdout.strip()[-250:]})")
check("JOB_CALLED" not in proc.stdout, "E-3 코드가 갱신되면 부모 프로세스는 생성 작업을 하지 않음")

# E-4. --daemon 기동 시에는 동기화하지 않음 (슬롯마다 따로 동기화)
proc = run_probe("daemon")
check("DAEMON_START" in proc.stdout and "SYNC_CALLED" not in proc.stdout, "E-4 데몬 기동 시점에는 동기화하지 않음")

# E-5. 데몬이 띄우는 하위 프로세스 명령 구성
recorded = {}
_orig_run = auto_daily.subprocess.run


class _FakeCompleted:
    returncode = 0


def _fake_run(cmd, **kw):
    recorded["cmd"] = list(cmd)
    recorded["cwd"] = kw.get("cwd")
    recorded["env"] = kw.get("env") or {}
    return _FakeCompleted()


try:
    auto_daily.subprocess.run = _fake_run
    worker_code = auto_daily.run_slot_in_new_process(
        "2026-11-17_08", theme="bright_room_minimal", upload_youtube=True, dry_run=True
    )
finally:
    auto_daily.subprocess.run = _orig_run

cmd = recorded.get("cmd", [])
check(worker_code == 0, "E-5 하위 프로세스 종료 코드 전달")
check(cmd[:2] == [sys.executable, str(BASE / "auto_daily.py")], f"E-5 같은 파이썬·같은 파일로 실행 (실제 {cmd[:2]})")
check("--now" in cmd and "--slot" in cmd and cmd[cmd.index("--slot") + 1] == "2026-11-17_08", "E-5 --now --slot <slot_id> 전달")
check("--no-sync" in cmd, "E-5 하위 프로세스는 --no-sync 로 재귀 동기화 차단")
check("--youtube" in cmd and "--dry-run" in cmd, "E-5 업로드·드라이런 플래그 전달")
check(str(recorded.get("cwd")) == str(BASE), "E-5 프로젝트 폴더에서 실행")
check(recorded.get("env", {}).get(auto_daily.SYNC_CHILD_ENV) == "1", "E-5 하위 프로세스 환경변수 표시")

# E-6. 동기화 후 재실행 명령에도 --no-sync 가 붙는다 (무한 재실행 방지)
recorded.clear()
_orig_run = auto_daily.subprocess.run
try:
    auto_daily.subprocess.run = _fake_run
    os.environ.pop(auto_daily.SYNC_CHILD_ENV, None)
    respawn_code = auto_daily.respawn_with_latest_code(["--now", "--dry-run"])
finally:
    auto_daily.subprocess.run = _orig_run

cmd = recorded.get("cmd", [])
check(respawn_code == 0, "E-6 재실행 종료 코드 전달")
check(cmd[:2] == [sys.executable, str(BASE / "auto_daily.py")], f"E-6 같은 파이썬·같은 파일로 재실행 (실제 {cmd[:2]})")
check("--now" in cmd and "--dry-run" in cmd, "E-6 원래 인자 유지")
check(cmd[-1] == "--no-sync", f"E-6 재실행 명령 끝에 --no-sync 부착 (실제 {cmd[-1:]})")
check(recorded.get("env", {}).get(auto_daily.SYNC_CHILD_ENV) == "1", "E-6 재실행 프로세스에 하위 프로세스 표시")
check(not auto_daily._is_sync_child(), "E-6 부모 프로세스 환경은 오염되지 않음")

# E-7. 데몬은 슬롯 도달 시 '동기화 → 새 프로세스 실행' 순서로 움직인다
proc = run_probe("daemon_slot")
check("EVENTS sync > spawn" in proc.stdout, f"E-7 동기화 후 하위 프로세스 실행 순서 (출력: {proc.stdout.strip()[-300:]})")
check("SPAWN slot=2026-11-17_08" in proc.stdout, "E-7 슬롯 ID 전달")
check("'upload_youtube', True" in proc.stdout and "'dry_run', True" in proc.stdout, "E-7 데몬 옵션 그대로 전달")


# =====================================================================
# F. 미게시 회차는 도감에 올리지 않는다 (token.json 보호 + 도감 갱신 조건)
# =====================================================================
print("\n=== F. 유튜브 업로드 실패·미설정 시 도감 갱신 차단 ===")

import contextlib
import io as _io
from youtube_uploader import TOKEN_FILE as UPLOADER_TOKEN_FILE

gitignore_text = (BASE / ".gitignore").read_text(encoding="utf-8")
gitignore_lines = [line.strip() for line in gitignore_text.splitlines()]
check("token.json" in auto_daily.LOCAL_ONLY_PATHS, "F-1 LOCAL_ONLY_PATHS 에 token.json 포함 (동기화로 삭제 방지)")
check("token.pickle" in auto_daily.LOCAL_ONLY_PATHS, "F-1 LOCAL_ONLY_PATHS 에 token.pickle 유지")
check("token.json" in gitignore_lines, "F-2 .gitignore 에 token.json 등록")
check(UPLOADER_TOKEN_FILE.name == "token.json", f"F-2 업로더가 실제 쓰는 토큰 파일명 ({UPLOADER_TOKEN_FILE.name})")


class NotConfiguredUploader:
    """인증 파일이 없는 PC (is_configured == False) 를 재현한다."""

    def __init__(self, *a, **kw):
        pass

    def is_configured(self):
        return False

    def upload(self, **kw):
        raise AssertionError("미설정 상태에서는 upload() 가 호출되면 안 된다")


class FailingUploader:
    """업로드를 시도했지만 실패해 URL 이 없는 상태를 재현한다."""

    def __init__(self, *a, **kw):
        pass

    def is_configured(self):
        return True

    def upload(self, **kw):
        calls["upload"] += 1
        return None


_saved = {
    "uploader": auto_daily.YouTubeUploader,
    "archive": auto_daily.load_archive_items,
    "guard": auto_daily.collect_guard,
    "describe": auto_daily.describe_guard,
    "web": auto_daily.update_link_page,
}
auto_daily.load_archive_items = lambda *a, **k: ([], "stub")
auto_daily.collect_guard = lambda state, *a, **k: {
    "blocked_item_ids": set(), "published_titles": set(), "warnings": [], "sources": {}
}
auto_daily.describe_guard = lambda guard: "[stub guard]"


def _fresh_state():
    tmp_state.write_text(json.dumps({"completed_slots": [], "history": []}, ensure_ascii=False), encoding="utf-8")


SKIP_MESSAGE = "유튜브 업로드가 완료되지 않아 도감 갱신을 건너뜁니다"

try:
    # F-3. is_configured() == False → 도감 갱신 금지 (기존 버그: 도감만 먼저 올라감)
    _fresh_state()
    web_before = calls["web"]
    auto_daily.YouTubeUploader = NotConfiguredUploader
    auto_daily.update_link_page = lambda **kw: calls.__setitem__("web", calls["web"] + 1) or True
    out = _io.StringIO()
    with contextlib.redirect_stdout(out):
        res = auto_daily.run_daily_job(slot_id="test_noauth_01", force=True, dry_run=False)
    log = out.getvalue()
    check(res is not None, "F-3 인증 없음: 영상 생성까지는 진행")
    check(calls["web"] == web_before, "F-3 인증 없음: 도감(history.json) 갱신 호출 0회")
    check(SKIP_MESSAGE in log, "F-3 인증 없음: 도감 갱신 건너뜀 안내 출력")

    # F-4. 업로드 시도했지만 실패(None) → 도감 갱신 금지
    _fresh_state()
    web_before = calls["web"]
    auto_daily.YouTubeUploader = FailingUploader
    out = _io.StringIO()
    with contextlib.redirect_stdout(out):
        res = auto_daily.run_daily_job(slot_id="test_uploadfail_01", force=True, dry_run=False)
    log = out.getvalue()
    check(res is not None, "F-4 업로드 실패: 영상 생성까지는 진행")
    check(calls["web"] == web_before, "F-4 업로드 실패: 도감 갱신 호출 0회")
    check(SKIP_MESSAGE in log, "F-4 업로드 실패: 도감 갱신 건너뜀 안내 출력")

    # F-5. 업로드 성공 시에는 그대로 도감 갱신 (정상 경로 회귀 방지)
    _fresh_state()
    web_before = calls["web"]
    auto_daily.YouTubeUploader = SpyUploader
    out = _io.StringIO()
    with contextlib.redirect_stdout(out):
        res = auto_daily.run_daily_job(slot_id="test_uploadok_01", force=True, dry_run=False)
    log = out.getvalue()
    check(res is not None, "F-5 업로드 성공: 영상 생성 완료")
    check(calls["web"] == web_before + 1, f"F-5 업로드 성공: 도감 갱신 1회 호출 (실제 {calls['web'] - web_before}회)")
    check(SKIP_MESSAGE not in log, "F-5 업로드 성공: 건너뜀 안내 없음")

    # F-6. 업로드 실패로 daily_state 에만 남은 회차(청소 편)는 다음 실행에서 자동으로 다시 선택된다
    import episode_builder as _eb
    from product_pool import THEMES as _THEMES

    published_keys = ("living", "kitchen", "food", "desk")
    archive12 = [
        {"item_id": p.item_id, "category_key": k}
        for k in published_keys for p in _THEMES[k]["products"]
    ]
    rss_titles = {_eb.normalize_title(_eb.build_episode_title(k, 1)) for k in published_keys}
    cleaning_title = _eb.normalize_title(_eb.build_episode_title("cleaning", 1))
    stuck_state = {
        "completed_slots": [],
        "history": [],
        "used_items_by_theme": {"cleaning": ["cleaning_mop", "cleaning_magicblock", "cleaning_duster"]},
        "episode_counts_by_theme": {"cleaning": 1},
        "published_titles": [cleaning_title],
        "current_theme_index": list(_THEMES.keys()).index("cleaning"),
    }
    tmp_state.write_text(json.dumps(stuck_state, ensure_ascii=False), encoding="utf-8")
    auto_daily.collect_guard = lambda state, *a, **k: {
        "blocked_item_ids": {i["item_id"] for i in archive12}
        | set(state.get("used_items_by_theme", {}).get("cleaning", [])),
        "published_titles": rss_titles | set(state.get("published_titles", [])),
        "rss_titles": rss_titles,
        "archive_items": archive12,
        "sources": {"rss_ok": True, "archive_source": "remote", "archive_items": len(archive12),
                    "local_items": 0, "rss_titles": len(rss_titles), "local_titles": 0},
        "warnings": [],
    }
    auto_daily.YouTubeUploader = SpyUploader
    out = _io.StringIO()
    with contextlib.redirect_stdout(out):
        res = auto_daily.run_daily_job(slot_id="test_unlock_01", force=True, dry_run=True)
    log = out.getvalue()
    unlocked_state = json.loads(tmp_state.read_text(encoding="utf-8"))
    check("미게시 회차 잠금 해제: cleaning" in log, f"F-6 미게시 회차 잠금 해제 안내 출력")
    check(res is not None and "청소" in log, "F-6 청소 회차가 다시 생성됨 (영구 건너뛰기 방지)")
    check(unlocked_state.get("used_items_by_theme", {}).get("cleaning") ==
          ["cleaning_mop", "cleaning_magicblock", "cleaning_duster"], "F-6 새로 생성된 청소 3종이 사용 처리됨")
    check(cleaning_title in unlocked_state.get("published_titles", []), "F-6 청소 제목이 다시 잠금 처리됨")
finally:
    auto_daily.YouTubeUploader = _saved["uploader"]
    auto_daily.load_archive_items = _saved["archive"]
    auto_daily.collect_guard = _saved["guard"]
    auto_daily.describe_guard = _saved["describe"]
    auto_daily.update_link_page = _saved["web"]


print("\n" + "=" * 60)
if failures:
    print(f"실패 {len(failures)}건:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("auto_daily 배선 테스트 통과 ✅")
