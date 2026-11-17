"""업로드 전 무결성 사전 검증(Preflight Check).

영상 제작·업로드 전에 아래 세 가지를 자동 검증하고, 하나라도 어긋나면
생성/업로드를 차단한다.

① 모든 슬라이드 이미지 파일이 실제로 존재하는가
② 각 상품의 쿠팡 링크에 파트너스 태그(lptag=AF7086198)가 들어 있는가
③ 영상 속 제품 3종이 설명란·슬라이드와 1:1 로 정확히 매칭되는가
"""

from pathlib import Path
from typing import List, Tuple

import config
from models import ShortsScript

EXPECTED_ITEM_COUNT = 3
REQUIRED_LPTAG = f"lptag={config.COUPANG_TRACKING_ID}"


def check_episode(script: ShortsScript) -> Tuple[bool, List[str]]:
    """에피소드 무결성 검사. (통과 여부, 문제 목록) 을 돌려준다."""
    problems: List[str] = []
    items = list(script.items or [])

    # ③ 1:1 매칭(3종 구성) 확인
    if len(items) != EXPECTED_ITEM_COUNT:
        problems.append(f"상품이 {len(items)}종입니다. 정확히 {EXPECTED_ITEM_COUNT}종이어야 합니다.")
    item_ids = [getattr(p, "item_id", "") for p in items]
    if len(set(item_ids)) != len(item_ids):
        problems.append(f"상품이 중복되었습니다: {item_ids}")

    for idx, item in enumerate(items, start=1):
        label = f"{idx}번 상품({getattr(item, 'title', '제목없음')})"

        if not (item.title or "").strip():
            problems.append(f"{label}: 상품명이 비어 있습니다.")
        if not (item.price or "").strip():
            problems.append(f"{label}: 가격이 비어 있습니다.")

        # ① 실물 이미지 파일 존재 확인
        img = Path(item.image_path) if item.image_path else None
        if img is None or not img.exists():
            problems.append(f"{label}: 이미지 파일이 없습니다 → {item.image_path}")
        elif img.stat().st_size <= 0:
            problems.append(f"{label}: 이미지 파일이 0바이트입니다 → {item.image_path}")

        # ② 쿠팡 파트너스 링크 확인
        url = item.coupang_url or ""
        if REQUIRED_LPTAG not in url:
            problems.append(f"{label}: 쿠팡 링크에 {REQUIRED_LPTAG} 가 없습니다 → {url or '(빈 링크)'}")

    # 슬라이드 구성 및 이미지 매칭
    slides = list(script.slides or [])
    if len(slides) != EXPECTED_ITEM_COUNT + 2:
        problems.append(f"슬라이드가 {len(slides)}장입니다. 훅·제품3·아우트로 = 5장이어야 합니다.")

    for slide in slides:
        if not slide.image_path:
            problems.append(f"[{slide.step_name}] 슬라이드에 이미지 경로가 없습니다.")
            continue
        sp = Path(slide.image_path)
        if not sp.exists():
            problems.append(f"[{slide.step_name}] 슬라이드 이미지가 없습니다 → {slide.image_path}")
        elif sp.stat().st_size <= 0:
            problems.append(f"[{slide.step_name}] 슬라이드 이미지가 0바이트입니다 → {slide.image_path}")

    for idx, item in enumerate(items, start=1):
        step = f"ITEM_{idx}"
        match = next((s for s in slides if s.step_name == step), None)
        if match is None:
            problems.append(f"[{step}] 슬라이드가 없습니다.")
            continue
        if Path(match.image_path or "") != Path(item.image_path or ""):
            problems.append(
                f"[{step}] 슬라이드 이미지와 상품 이미지가 다릅니다 "
                f"(슬라이드={match.image_path}, 상품={item.image_path})"
            )
        if (match.main_title or "").strip() != (item.title or "").strip():
            problems.append(f"[{step}] 슬라이드 제목이 상품명과 다릅니다.")
        if (match.price_badge or "").strip() != (item.price or "").strip():
            problems.append(f"[{step}] 슬라이드 가격이 상품 가격과 다릅니다.")

    # 설명란에 3종 상품명이 모두 들어 있는지 (도감·검색 유입 1:1 일치)
    desc = script.youtube_description or ""
    for idx, item in enumerate(items, start=1):
        if item.title not in desc:
            problems.append(f"설명란에 {idx}번 상품명('{item.title}')이 없습니다.")

    if not (script.youtube_title or "").strip():
        problems.append("유튜브 제목이 비어 있습니다.")

    return (len(problems) == 0), problems


def format_problems(problems: List[str]) -> str:
    lines = ["❌ 사전 검증(Preflight) 실패 — 업로드를 차단합니다."]
    lines += [f"   · {p}" for p in problems]
    return "\n".join(lines)
