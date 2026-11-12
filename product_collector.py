#!/usr/bin/env python3
"""
돈값연구소 (dongap_lab) - 쿠팡 상품 자동 수집 & 등록 모듈 (product_collector.py)

기능:
1. 쿠팡 상품 URL(단축링크/상세페이지) 또는 이미지 URL에서 상품 자동 등록
2. 상품 대표 이미지 자동 다운로드 (640x640 정방형 자동 최적화)
3. 대사(voice_script), 체크포인트, 뱃지, 태그 자동 생성
4. custom_products.json에 저장하여 auto_daily.py 쇼츠 생성 파이프라인에 즉시 반영
"""

import os
import re
import sys
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image, ImageOps

import config

CUSTOM_FILE = config.BASE_DIR / "custom_products.json"


def download_and_optimize_image(image_url: str, save_path: Path) -> bool:
    """웹 이미지 URL을 다운로드하여 640x640 정방형 캔버스에 깔끔하게 최적화 저장"""
    try:
        req = urllib.request.Request(
            image_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Referer": "https://www.coupang.com/",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()

        temp_path = save_path.with_suffix(".tmp")
        with open(temp_path, "wb") as f:
            f.write(data)

        # 이미지 종횡비 보존 640x640 화이트 캔버스 패딩
        with Image.open(temp_path) as img:
            img = img.convert("RGBA")
            target_size = (640, 640)
            img.thumbnail(target_size, Image.Resampling.LANCZOS)

            bg = Image.new("RGBA", target_size, (255, 255, 255, 255))
            offset_x = (target_size[0] - img.width) // 2
            offset_y = (target_size[1] - img.height) // 2
            bg.paste(img, (offset_x, offset_y), img)
            bg.convert("RGB").save(save_path, "PNG", quality=95)

        if temp_path.exists():
            temp_path.unlink()

        print(f"✅ 이미지 다운로드 및 정방형 최적화 완료: {save_path.name}")
        return True
    except Exception as e:
        print(f"❌ 이미지 다운로드 실패 ({image_url}): {e}")
        return False


def load_custom_products() -> Dict[str, list]:
    if CUSTOM_FILE.exists():
        try:
            with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_custom_products(data: Dict[str, list]):
    with open(CUSTOM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_product(
    theme: str,
    title: str,
    price: str,
    coupang_url: str,
    image_url: str,
    header_badge: str = "가성비 추천템",
    caption1: str = "",
    caption2: str = "",
    tag: str = "로켓배송",
    rating: str = "★ 4.8",
    voice_script: str = ""
) -> bool:
    """새 쿠팡 상품을 수집하여 파이프라인에 등록"""
    # item_id 생성
    clean_title = re.sub(r"[^a-zA-Z0-9가-힣]", "", title)[:12]
    item_id = f"custom_{theme}_{clean_title}"
    img_filename = f"{item_id}.png"
    img_save_path = config.ASSETS_DIR / img_filename

    # 이미지 다운로드
    if not download_and_optimize_image(image_url, img_save_path):
        return False

    if not caption1:
        caption1 = f"가성비 끝판왕 {title}!"
    if not caption2:
        caption2 = "자취·살림 필수 꿀템"
    if not voice_script:
        voice_script = f"다음은 {title}입니다. 실사용 만족도 최고에 가격도 {price}으로 진짜 돈값 하는 추천템이에요."

    product_entry = {
        "item_id": item_id,
        "title": title,
        "header_badge": header_badge,
        "discount": "특가할인",
        "price": price if "원" in price else f"{price}원",
        "tag": tag,
        "card_badge_left": rating,
        "card_badge_right": "[프로필 링크]",
        "caption1": caption1,
        "caption2": caption2,
        "voice_script": voice_script,
        "image_path": str(img_save_path),
        "image_url": image_url,
        "coupang_url": coupang_url
    }

    data = load_custom_products()
    if theme not in data:
        data[theme] = []

    # 중복 체크 (동일 coupang_url 또는 title)
    data[theme] = [p for p in data[theme] if p.get("coupang_url") != coupang_url and p.get("title") != title]
    data[theme].append(product_entry)
    save_custom_products(data)

    print(f"\n🎉 [{theme}] 카테고리에 새 상품이 성공적으로 등록되었습니다!")
    print(f"  • 상품명: {title}")
    print(f"  • 가격: {product_entry['price']}")
    print(f"  • 이미지: {img_save_path.name}")
    print(f"  • 구매링크: {coupang_url}")
    print(f"  • 이제 'python3 auto_daily.py --now' 실행 시 새 상품이 영상과 웹페이지에 자동 반영됩니다.")
    return True


def interactive_mode():
    """터미널 대화형 상품 등록 마법사"""
    print("\n" + "=" * 50)
    print("🧪 돈값연구소 - 쿠팡 상품 간편 등록 마법사")
    print("=" * 50)

    print("카테고리를 선택하세요:")
    print("  1. 자취·리빙 (living)")
    print("  2. 주방·살림 (kitchen)")
    print("  3. 식비·간편식 (food)")
    print("  4. 데스크테리어 (desk)")
    cat_choice = input("선택 (1~4) [기본 1]: ").strip()
    theme_map = {"1": "living", "2": "kitchen", "3": "food", "4": "desk"}
    theme = theme_map.get(cat_choice, "living")

    title = input("👉 상품명 (예: 홈플래닛 무선 핸디 청소기): ").strip()
    if not title:
        print("❌ 상품명은 필수입니다.")
        return

    price = input("👉 가격 (예: 27,990원): ").strip()
    coupang_url = input("👉 쿠팡 파트너스 링크 (예: https://link.coupang.com/a/...): ").strip()
    image_url = input("👉 상품 대표 이미지 URL (쿠팡 이미지 우클릭 -> 이미지 주소 복사): ").strip()

    if not image_url:
        print("❌ 이미지 URL은 필수입니다.")
        return

    add_product(
        theme=theme,
        title=title,
        price=price,
        coupang_url=coupang_url,
        image_url=image_url
    )


def main():
    parser = argparse.ArgumentParser(description="쿠팡 상품 자동 수집 & 등록 도구")
    parser.add_argument("--interactive", "-i", action="store_true", help="터미널 대화형 마법사 실행")
    parser.add_argument("--theme", type=str, default="living", choices=["living", "kitchen", "food", "desk"], help="카테고리 테마")
    parser.add_argument("--title", type=str, help="상품명")
    parser.add_argument("--price", type=str, help="가격")
    parser.add_argument("--url", type=str, help="쿠팡 파트너스 구매 링크")
    parser.add_argument("--image", type=str, help="대표 이미지 URL (Coupang CDN 또는 웹 이미지)")
    parser.add_argument("--list", "-l", action="store_true", help="등록된 커스텀 상품 목록 조회")

    args = parser.parse_args()

    if args.list:
        data = load_custom_products()
        print("\n📦 현재 등록된 커스텀 상품 목록:")
        total = 0
        for th, items in data.items():
            print(f"[{th}] ({len(items)}개)")
            for it in items:
                print(f"  • {it['title']} - {it['price']} ({it['coupang_url']})")
                total += 1
        print(f"총 {total}개 상품 등록됨.\n")
        return

    if args.interactive or (not args.title and not args.url):
        interactive_mode()
        return

    if not args.title or not args.image:
        print("❌ --title과 --image는 필수 인자입니다. 대화형으로 등록하시려면 'python3 product_collector.py -i'를 실행하세요.")
        return

    add_product(
        theme=args.theme,
        title=args.title,
        price=args.price or "특가할인",
        coupang_url=args.url or "",
        image_url=args.image
    )


if __name__ == "__main__":
    main()
