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


calls = {"web": 0, "telegram": 0, "upload": 0}

auto_daily.SlideRenderer = FakeRenderer
auto_daily.VoiceGenerator = FakeVoice
auto_daily.VideoBuilder = FakeVideo
auto_daily.update_link_page = lambda **kw: calls.__setitem__("web", calls["web"] + 1) or True
auto_daily.send_video_to_telegram = lambda *a, **kw: calls.__setitem__("telegram", calls["telegram"] + 1) or True


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
tmp_state.write_text(json.dumps(seed, ensure_ascii=False), encoding="utf-8")

result = auto_daily.run_daily_job(slot_id="test_dryrun_01", force=True, send_telegram=True, dry_run=True)
state = json.loads(tmp_state.read_text(encoding="utf-8"))

check(result is not None and result.exists(), "영상 파일 생성 단계까지 도달")
check(calls["upload"] == 0, "유튜브 업로드 호출 0회 (드라이런)")
check(calls["telegram"] == 0, "텔레그램 전송 호출 0회 (드라이런)")
check(calls["web"] == 0, "도감(history.json) 갱신 호출 0회 (드라이런)")
check("bath" in state["used_items_by_theme"] and len(state["used_items_by_theme"]["bath"]) == 3, "욕실 상품 3종이 사용 처리됨")
check("test_dryrun_01" in state["completed_slots"], "완료 슬롯 기록됨")
check(any("욕실" in t or "욕실·샤워" in t for t in state.get("published_titles", [])) or len(state.get("published_titles", [])) == 5, f"게시 제목 잠금 5건 (실제 {len(state.get('published_titles', []))})")

print("\n=== B. 남은 상품이 없을 때 건너뛰기 ===")
exhausted = json.loads(tmp_state.read_text(encoding="utf-8"))
# 18종을 모두 사용 처리해 '새 상품 없음' 상태를 만든다
from product_pool import THEMES

for theme_key, theme in THEMES.items():
    exhausted.setdefault("used_items_by_theme", {})[theme_key] = [p.item_id for p in theme["products"]]
tmp_state.write_text(json.dumps(exhausted, ensure_ascii=False), encoding="utf-8")

result2 = auto_daily.run_daily_job(slot_id="test_dryrun_02", force=True, send_telegram=False, dry_run=True)
check(result2 is None, "새 상품이 없으면 None 반환 (생성·업로드 skip)")
check(calls["upload"] == 0 and calls["telegram"] == 0, "skip 시에도 업로드·전송 없음")

print("\n" + "=" * 60)
if failures:
    print(f"실패 {len(failures)}건:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("auto_daily 배선 테스트 통과 ✅")
