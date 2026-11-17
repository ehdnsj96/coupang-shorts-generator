# -*- coding: utf-8 -*-
"""중복 방지 가드·사전 검증·도감 정합성 로컬 테스트.

실행: python3 tests/test_guard.py
(유튜브 업로드는 절대 호출하지 않는다)
"""

import copy
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import config
import episode_builder
import preflight
import publish_guard
import web_updater
from product_pool import THEMES
from models import ShortsScript, Slide


def case(name):
    print(f"\n=== {name} ===")


failures = []


def check(cond, message):
    print(("  ✅ " if cond else "  ❌ ") + message)
    if not cond:
        failures.append(message)


# ---------------------------------------------------------------- 1. 상태 복원
case("1. 도감(history.json)으로 상태 자동 복원")
fresh = {"completed_slots": [], "history": []}
archive_items, source = publish_guard.load_archive_items()
check(len(archive_items) == 12, f"로컬 도감 사본 12종 읽기 (출처={source})")
state = publish_guard.reconcile_state_with_archive(fresh, archive_items)
restored = sum(len(v) for v in state["used_items_by_theme"].values())
check(restored == 12, f"도감에 올라간 12종이 used 로 자동 처리됨 (실제 {restored})")
check(
    all(state["episode_counts_by_theme"].get(k, 0) >= 1 for k in ["living", "kitchen", "food", "desk"]),
    "기존 4대 테마 회차가 1탄으로 복원됨",
)

# ------------------------------------------------------- 2. 새 회차 자동 선택
case("2. 새 테마 자동 선택 (기존 4테마 소진 상태)")
guard = {
    "blocked_item_ids": set(),
    "published_titles": set(state.get("published_titles", [])),
}
for ids in state["used_items_by_theme"].values():
    guard["blocked_item_ids"].update(ids)

script, state = episode_builder.get_next_dynamic_episode(
    state,
    blocked_item_ids=guard["blocked_item_ids"],
    published_titles=guard["published_titles"],
)
check(script is not None, "미사용 상품이 있으므로 새 에피소드가 생성됨")
check(script is not None and script.topic.startswith("욕실·샤워 리셋"), f"첫 새 회차는 욕실 테마 (topic={script.topic if script else None})")
check(script is not None and len(script.items) == 3, "상품 3종으로 구성됨")
check(
    script is not None and all(p.item_id.startswith("bath_") for p in script.items),
    f"선택 상품: {[p.item_id for p in script.items] if script else None}",
)

# ------------------------------------------------------------- 3. 사전 검증 통과
case("3. 사전 검증(Preflight) 통과")
ok, problems = preflight.check_episode(script)
check(ok, f"이미지·lptag·1:1 매칭 검사 통과 {problems if problems else ''}")

# --------------------------------------------------------------- 4. 슬라이드 렌더
case("4. 슬라이드 5장 실제 렌더링")
from slide_renderer import SlideRenderer

renderer = SlideRenderer()
out_dir = config.OUTPUT_DIR / "guard_test"
out_dir.mkdir(parents=True, exist_ok=True)
rendered = []
for i, slide in enumerate(script.slides):
    path = out_dir / f"bath_ep1_slide_{i:02d}.png"
    renderer.render_slide(slide, path)
    rendered.append(path)
check(all(p.exists() and p.stat().st_size > 10000 for p in rendered), f"슬라이드 5장 생성 ({[p.name for p in rendered]})")

# --------------------------------------- 5. 이미 게시된 제목 회차는 건너뛰기
case("5. 유튜브 RSS 제목 잠금 동작 (이미 게시된 회차 skip)")
published = set(state.get("published_titles", []))
published.add(episode_builder.normalize_title(script.youtube_title))
state_after = copy.deepcopy(state)
script2, state_after = episode_builder.get_next_dynamic_episode(
    state_after,
    blocked_item_ids=guard["blocked_item_ids"],
    published_titles=published,
)
check(script2 is not None and script2.topic.startswith("차 안 리셋"), f"욕실 회차는 건너뛰고 차량 테마로 (topic={script2.topic if script2 else None})")
ok2, problems2 = preflight.check_episode(script2)
check(ok2, f"차량 회차 사전 검증 통과 {problems2 if problems2 else ''}")

# ------------------------------------------- 6. 모든 상품 소진 시 None 반환
case("6. 모든 테마 소진 시 None (기존 무한 중복 버그 회귀 테스트)")
state_exhausted = copy.deepcopy(state_after)
script3, state_exhausted = episode_builder.get_next_dynamic_episode(
    state_exhausted,
    blocked_item_ids=set(),
    published_titles=set(),
)
check(script3 is None, "미사용 상품이 없으면 None 을 반환 (used 리셋 후 재업로드하지 않음)")
total_used = set()
for ids in state_exhausted["used_items_by_theme"].values():
    total_used.update(ids)
check(len(total_used) == 18, f"18종 전부 사용 처리됨 (실제 {len(total_used)})")

# ------------------------------------------------- 7. 사전 검증 실패 시 차단
case("7. 사전 검증 실패 케이스 차단")
broken = copy.deepcopy(script)


class _Bad:
    pass


bad_items = [copy.deepcopy(p) for p in broken.items]
bad_items[1].image_path = str(config.ASSETS_DIR / "없는이미지.png")
bad_items[2].coupang_url = "https://www.coupang.com/vp/products/6317163928?itemId=784715207&vendorItemId=4987822596"  # lptag 없음
broken.items = bad_items
ok3, problems3 = preflight.check_episode(broken)
check(not ok3, "깨진 에피소드는 검증 실패로 차단됨")
check(any("이미지 파일이 없습니다" in p for p in problems3), "누락 이미지가 지적됨")
check(any("lptag=AF7086198" in p for p in problems3), "쿠팡 링크 lptag 누락이 지적됨")

# ------------------------------------- 7-1. 검색 URL(np/search) 무조건 차단
case("7-1. 검색 페이지 링크(np/search) 차단 — lptag 가 있어도 실패")
search_url = "https://www.coupang.com/np/search?q=%EC%A0%84%EB%8F%99%20%EC%99%80%EC%9D%B8%EC%98%A4%ED%94%84%EB%84%88&lptag=AF7086198"
search_problems = preflight.check_coupang_url(search_url)
check(bool(search_problems), "검색 URL 은 문제로 판정")
check(any("검색 결과 페이지" in p for p in search_problems), f"차단 사유가 '검색 결과 페이지' ({search_problems})")

broken_search = copy.deepcopy(script)
bs_items = [copy.deepcopy(p) for p in broken_search.items]
bs_items[0].coupang_url = search_url
broken_search.items = bs_items
ok_search, problems_search = preflight.check_episode(broken_search)
check(not ok_search, "검색 URL 이 섞인 에피소드는 사전 검증 실패")
check(any("검색 결과 페이지" in p for p in problems_search), "사전 검증이 검색 URL 을 지적함")

valid_vp = "https://www.coupang.com/vp/products/6317163928?itemId=784715207&vendorItemId=4987822596&lptag=AF7086198"
valid_short = "https://link.coupang.com/a/iACeuVKLq8"
check(preflight.check_coupang_url(valid_vp) == [], "실제 상품 상세 URL(/vp/products + itemId)은 통과")
check(preflight.check_coupang_url(valid_short) == [], "파트너스 단축 링크(link.coupang.com)는 통과")
check(preflight.check_coupang_url("https://www.coupang.com/vp/products/6317163928?lptag=AF7086198") != [], "itemId 없는 /vp/products URL 은 실패")
check(preflight.check_coupang_url("https://www.coupang.com/vp/products/6317163928?itemId=784715207") != [], "lptag 없는 상품 URL 은 실패")

case("7-2. 상품 풀 18종 전수 검사 — 검색 URL 0건 · 실제 상품 URL 18건")
offenders = []
for theme_key, theme in THEMES.items():
    for prod in theme["products"]:
        probs = preflight.check_coupang_url(prod.coupang_url)
        if probs:
            offenders.append((theme_key, prod.item_id, probs))
check(not offenders, f"18종 모두 실제 상품 상세 URL (위반 {offenders if offenders else '없음'})")
check(
    not any("/np/search" in p.coupang_url for t in THEMES.values() for p in t["products"]),
    "검색 URL(np/search) 잔존 0건",
)

# --------------------------------------------- 8. 도감은 게시분만 유지
case("8. 도감(history.json) 정합성 — 미게시 상품 미리 올리지 않음")
local_history = json.loads(publish_guard.LOCAL_ARCHIVE_FILE.read_text(encoding="utf-8"))
clean = web_updater.sanitize_history(local_history)
check(len(clean) == 12, f"기존 게시분 12종 유지 (실제 {len(clean)})")
check(
    not any(x["item_id"].startswith(("bath_", "car_")) for x in clean),
    "아직 게시하지 않은 욕실·차량 상품은 도감에 포함되지 않음",
)
check(web_updater.theme_key_for_item("bath_slippers") == "bath", "새 테마 카테고리 매핑 정상")
html = web_updater.generate_html("테스트", [], clean)
check("욕실·샤워" in html and "차량·운전" in html, "도감 HTML 에 새 카테고리 필터가 생성됨")
check("t.me" not in html and "텔레그램" not in html, "도감 HTML 에 텔레그램 배너·링크가 없음")

case("9. 훅 슬라이드 문구가 테마와 일치 (렌더러 하드코딩 회귀 방지)")
from slide_renderer import SlideRenderer
from models import Slide

renderer2 = SlideRenderer()
bath_slides = episode_builder.build_episode("bath", 1, THEMES["bath"]["products"]).slides
style_bath = renderer2._hook_style(bath_slides[0])
check("욕실" in style_bath["line1"], f"욕실 테마 훅 문구: {style_bath['line1']} / {style_bath['tag']}")
check("데스크" not in style_bath["line1"], "데스크 문구가 욕실 훅에 섞이지 않음")

unknown = Slide(
    step_name="HOOK",
    header_badge="🔥 반려동물 꿀템",
    main_title="냥집사 필수템\n쿠팡 꿀템 TOP 3!",
    caption_line1="고양이가 좋아해요",
)
style_unknown = renderer2._hook_style(unknown)
check(style_unknown["line1"] == "냥집사 필수템", f"미등록 테마는 슬라이드 문구를 그대로 사용 ({style_unknown['line1']})")
check("데스크" not in style_unknown["tag"], f"미등록 테마도 데스크 문구로 대체되지 않음 ({style_unknown['tag']})")

case("10. 평점·후기 표기 (임의 4.8 고정 회귀 방지)")
star, rev = renderer2._split_rating("★ 5.0 (후기 2만+)")
check(star == "★ 5.0" and rev == "(후기 2만+)", f"상품 평점이 그대로 쓰임 ({star} {rev})")
star2, rev2 = renderer2._split_rating("(후기 5만+)")
check(star2 == "" and rev2 == "(후기 5만+)", "별점이 없으면 빈 별점 (가짜 4.8 생성 없음)")

case("11. 네트워크 실패 시 로컬 폴백 (무인 자동화가 막히지 않아야 함)")
import publish_guard as pg

_orig_rss, _orig_archive = pg.RSS_URL, pg.REMOTE_ARCHIVE_URL
pg.RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=INVALID_CHANNEL_FOR_TEST"
pg.REMOTE_ARCHIVE_URL = "https://raw.githubusercontent.com/ehdnsj96/gooditem-archive/main/__no_such_file__.json"
titles_offline, rss_ok_offline = pg.fetch_published_titles(timeout=6)
archive_offline, archive_src_offline = pg.load_archive_items(timeout=6)
guard_offline = pg.collect_guard({"used_items_by_theme": {"bath": ["bath_shower_filter"]}, "published_titles": ["x"]})
pg.RSS_URL, pg.REMOTE_ARCHIVE_URL = _orig_rss, _orig_archive

check(rss_ok_offline is False, "RSS 실패를 오류 없이 감지")
check(archive_src_offline == "local" and len(archive_offline) == 12, f"도감은 로컬 사본으로 폴백 ({archive_src_offline}, {len(archive_offline)}종)")
check(guard_offline["sources"]["archive_items"] == 12, "폴백 후에도 도감 잠금 12종 유지")
check("bath_shower_filter" in guard_offline["blocked_item_ids"], "로컬 상태의 사용 상품도 그대로 잠금")

print("\n" + "=" * 60)
if failures:
    print(f"실패 {len(failures)}건:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("모든 테스트 통과 ✅")
