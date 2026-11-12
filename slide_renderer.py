import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from models import Slide
import config


class SlideRenderer:
    def __init__(self, width: int = config.VIDEO_WIDTH, height: int = config.VIDEO_HEIGHT, theme: str = "bright_room_minimal"):
        self.width = width
        self.height = height
        self.theme = theme
        self.font_bold_path = config.FONT_BOLD_PATH
        self.font_extrabold_path = config.FONT_EXTRABOLD_PATH
        self.bg_path = config.ASSETS_DIR / "bright_room_bg.png"

    def _get_font(self, size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
        target_path = self.font_extrabold_path if bold else self.font_bold_path
        if target_path and Path(target_path).exists():
            try:
                return ImageFont.truetype(str(target_path), size)
            except Exception:
                pass
        return ImageFont.load_default()

    def _draw_background(self) -> Image.Image:
        """화사한 화이트 인테리어 룸 배경 + 텍스트 가독성 소프트 오버레이"""
        if self.bg_path.exists():
            try:
                bg = Image.open(self.bg_path).convert("RGBA")
                bg = ImageOps.fit(bg, (self.width, self.height), method=Image.Resampling.LANCZOS)
            except Exception:
                bg = Image.new("RGBA", (self.width, self.height), (248, 249, 252, 255))
        else:
            bg = Image.new("RGBA", (self.width, self.height), (248, 249, 252, 255))

        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        # 상단 헤더 영역 소프트 화이트
        for y in range(300):
            alpha = int(140 * (1 - y / 300))
            odraw.line([(0, y), (self.width, y)], fill=(255, 255, 255, alpha))
        # 하단 자막 영역 클린 다크 소프트 비네팅
        for y in range(self.height - 430, self.height):
            alpha = int(185 * ((y - (self.height - 430)) / 430))
            odraw.line([(0, y), (self.width, y)], fill=(15, 20, 32, alpha))

        return Image.alpha_composite(bg, overlay).convert("RGB")

    def _draw_top_header(self, draw: ImageDraw.ImageDraw, tag_text: str, title_text: str):
        """돈값연구소 상단 브랜딩 & 메인 타이틀"""
        f_badge = self._get_font(26, bold=True)
        draw.rounded_rectangle([60, 60, 260, 110], radius=14, fill=(255, 255, 255, 235), outline=(220, 226, 238), width=1)
        draw.text((160, 72), "돈값연구소 🧪", font=f_badge, fill=(20, 25, 38), anchor="mt")

        f_rank = self._get_font(28, bold=True)
        draw.text((self.width - 60, 72), tag_text, font=f_rank, fill=(0, 102, 255), anchor="ra")

        f_title = self._get_font(54, bold=True)
        draw.text((60, 135), title_text, font=f_title, fill=(18, 24, 38))

    def _draw_viral_subtitle(self, draw: ImageDraw.ImageDraw, line1: str, line2: Optional[str] = None, y: int = 1500):
        """중앙 정렬 방송용 볼드 외곽선 자막"""
        f_sub1 = self._get_font(58, bold=True)
        f_sub2 = self._get_font(48, bold=True)
        if line1:
            draw.text((self.width // 2, y), line1, font=f_sub1, fill=(255, 235, 0), stroke_width=8, stroke_fill=(15, 18, 25), anchor="mt")
        if line2:
            draw.text((self.width // 2, y + 82), line2, font=f_sub2, fill=(255, 255, 255), stroke_width=8, stroke_fill=(15, 18, 25), anchor="mt")

    def render_slide(self, slide: Slide, output_path: Path, with_character: bool = False):
        output_path.parent.mkdir(exist_ok=True, parents=True)
        if slide.step_name == "HOOK":
            img = self._render_hook_slide(slide)
        elif slide.step_name == "OUTRO":
            img = self._render_outro_slide(slide)
        else:
            img = self._render_item_slide(slide)

        img.save(str(output_path), format="PNG")

    def _render_hook_slide(self, slide: Slide) -> Image.Image:
        """미니멀 클린 훅: 호기심 공백(Curiosity Gap) 극대화 미스터리 시크릿 카드"""
        img = self._draw_background()
        draw = ImageDraw.Draw(img)

        # 테마에 맞는 동적 상단 헤더
        header_tag = slide.header_badge or "TOP 3 랭킹 공개 🚨"
        header_title = slide.main_title.replace("\n", " ") if slide.main_title else "쿠팡 가성비 꿀템 TOP 3"
        self._draw_top_header(draw, header_tag, header_title)

        # 중앙 대형 미스터리 카드
        target_sz = (960, 820)
        cx, cy = (self.width - target_sz[0]) // 2, 230

        base_rgba = img.convert("RGBA")
        shadow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle([cx + 10, cy + 20, cx + target_sz[0] - 10, cy + target_sz[1] + 30], radius=40, fill=(0, 0, 0, 45))
        shadow = shadow.filter(ImageFilter.GaussianBlur(35))
        base_rgba = Image.alpha_composite(base_rgba, shadow)

        card = Image.new("RGBA", (target_sz[0], target_sz[1]), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(card)
        cdraw.rounded_rectangle([0, 0, target_sz[0], target_sz[1]], radius=38, fill=(255, 255, 255, 250), outline=(225, 232, 245), width=2)

        # 캡슐 뱃지
        f_sec_badge = self._get_font(34, bold=True)
        cdraw.rounded_rectangle([target_sz[0] // 2 - 240, 60, target_sz[0] // 2 + 240, 130], radius=18, fill=(240, 244, 255))
        cdraw.text((target_sz[0] // 2, 77), "🔒 90%가 몰라서 손해 보는 템", font=f_sec_badge, fill=(0, 102, 255), anchor="mt")

        f_huge_q = self._get_font(210, bold=True)
        cdraw.text((target_sz[0] // 2, 190), "?", font=f_huge_q, fill=(0, 102, 255), stroke_width=6, stroke_fill=(210, 230, 255), anchor="mt")

        f_secret = self._get_font(52, bold=True)
        cdraw.text((target_sz[0] // 2, 540), "1번은 진짜 무조건 사세요", font=f_secret, fill=(20, 25, 38), anchor="mt")
        f_secret_sub = self._get_font(36, bold=True)
        cdraw.text((target_sz[0] // 2, 630), "돈값 제대로 하는 필수템 공개 🔥", font=f_secret_sub, fill=(95, 110, 135), anchor="mt")

        base_rgba.paste(card, (cx, cy), mask=card)
        img = base_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)

        # 제품 밑: 화이트 글래스 인포 카드
        self._draw_info_card(
            img, draw,
            "미공개",
            "로켓배송",
            "★ 4.9",
            "(실구매 만족도 99%)",
            ["• 광고 0% 솔직 검증", "• 만족도 3배 상승", "• 가성비 1위 검증"]
        )

        # 하단 자막
        cap1 = slide.caption_line1 or "아직도 이거 모르고 산다고?"
        cap2 = slide.caption_line2 or "놓치면 후회하는 찐 꿀템 TOP 3!"
        self._draw_viral_subtitle(draw, cap1, cap2)

        return img

    def _render_item_slide(self, slide: Slide) -> Image.Image:
        """미니멀 클린 본문: 실물 제품 컷(비율 100% 보존 · 잘림 방지) + 화이트 글래스 인포 카드 + 볼드 자막"""
        img = self._draw_background()
        draw = ImageDraw.Draw(img)

        tag_text = slide.header_badge or "BEST 01 / 03"
        self._draw_top_header(draw, tag_text, slide.main_title)

        # 중앙 대형 실물 제품 컷 (원본 비율 100% 보존하여 잘림 절대 방지)
        target_sz = (960, 820)
        cx = (self.width - target_sz[0]) // 2
        cy = 230

        base_rgba = img.convert("RGBA")
        shadow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle([cx + 10, cy + 20, cx + target_sz[0] - 10, cy + target_sz[1] + 30], radius=40, fill=(0, 0, 0, 45))
        shadow = shadow.filter(ImageFilter.GaussianBlur(35))
        base_rgba = Image.alpha_composite(base_rgba, shadow)

        # 흰색 배경 카드 생성
        card_img = Image.new("RGBA", target_sz, (255, 255, 255, 255))
        card_mask = Image.new("L", target_sz, 0)
        ImageDraw.Draw(card_mask).rounded_rectangle([0, 0, target_sz[0], target_sz[1]], radius=38, fill=255)

        if slide.image_path and Path(slide.image_path).exists():
            try:
                p_img = Image.open(slide.image_path).convert("RGBA")
                # 가로 세로 최대 760px 안에서 원본 종횡비 유지 축소 (잘림 0%)
                max_w, max_h = target_sz[0] - 80, target_sz[1] - 60
                p_img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

                # 카드 정중앙에 배치
                offset_x = (target_sz[0] - p_img.width) // 2
                offset_y = (target_sz[1] - p_img.height) // 2
                card_img.paste(p_img, (offset_x, offset_y), mask=p_img)
            except Exception as e:
                print(f"[SlideRenderer] 이미지 로드 에러: {e}")

        # 카드 테두리
        card_frame = Image.new("RGBA", (target_sz[0] + 10, target_sz[1] + 10), (0, 0, 0, 0))
        ImageDraw.Draw(card_frame).rounded_rectangle([0, 0, target_sz[0] + 10, target_sz[1] + 10], radius=40, fill=(255, 255, 255, 250), outline=(230, 235, 245), width=2)
        base_rgba.paste(card_frame, (cx - 5, cy - 5), mask=card_frame)
        base_rgba.paste(card_img, (cx, cy), mask=card_mask)
        img = base_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)

        # 제품 밑: 화이트 글래스 인포 카드
        price_clean = (slide.price_badge or "27,990원").replace("원", "").strip()
        points = self._get_item_points(slide.main_title)
        self._draw_info_card(
            img, draw,
            price_clean,
            slide.tag_badge or "로켓배송",
            "★ 4.8",
            slide.card_badge_left or "(후기 4만+)",
            points
        )

        # 하단 자막
        cap1 = slide.caption_line1
        cap2 = slide.caption_line2
        self._draw_viral_subtitle(draw, cap1, cap2)

        return img

    def _render_outro_slide(self, slide: Slide) -> Image.Image:
        """미니멀 클린 아웃트로: 채널 프로필 링크 안내 및 3종 최저가 요약"""
        img = self._draw_background()
        draw = ImageDraw.Draw(img)

        self._draw_top_header(draw, "구매 안내 📌", "영상 속 꿀템 3가지 최저가는?")

        # 중앙 대형 모바일 링크 쇼케이스 카드
        target_sz = (960, 820)
        cx, cy = (self.width - target_sz[0]) // 2, 230

        base_rgba = img.convert("RGBA")
        shadow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle([cx + 10, cy + 20, cx + target_sz[0] - 10, cy + target_sz[1] + 30], radius=40, fill=(0, 0, 0, 45))
        shadow = shadow.filter(ImageFilter.GaussianBlur(35))
        base_rgba = Image.alpha_composite(base_rgba, shadow)

        card = Image.new("RGBA", (target_sz[0], target_sz[1]), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(card)
        cdraw.rounded_rectangle([0, 0, target_sz[0], target_sz[1]], radius=38, fill=(255, 255, 255, 250), outline=(225, 232, 245), width=2)

        items = slide.preview_items[:3] if slide.preview_items else [
            {"badge": "01", "title": "홈플래닛 무선 핸디 청소기", "price": "27,990원"},
            {"badge": "02", "title": "코멧 홈 규조토 발매트", "price": "8,090원"},
            {"badge": "03", "title": "코멧 모션인식 센서 휴지통", "price": "12,990원"},
        ]

        f_num = self._get_font(34, bold=True)
        f_name = self._get_font(36, bold=True)
        f_p = self._get_font(34, bold=True)

        row_y = 50
        for idx, item in enumerate(items):
            num = f"0{idx+1}"
            title = item.get("title", "")
            price = item.get("price", "")

            cdraw.rounded_rectangle([40, row_y, target_sz[0] - 40, row_y + 130], radius=20, fill=(245, 248, 255), outline=(225, 232, 245), width=1)
            cdraw.rounded_rectangle([65, row_y + 26, 135, row_y + 96], radius=14, fill=(0, 102, 255))
            cdraw.text((100, row_y + 39), num, font=f_num, fill=(255, 255, 255), anchor="mt")

            cdraw.text((165, row_y + 42), title[:18], font=f_name, fill=(20, 25, 38))
            cdraw.text((target_sz[0] - 70, row_y + 44), f"{price} ➔", font=f_p, fill=(0, 102, 255), anchor="ra")
            row_y += 155

        # 하단 메가 CTA 버튼 (황금색)
        btn_y = target_sz[1] - 250
        cdraw.rounded_rectangle([40, btn_y, target_sz[0] - 40, btn_y + 190], radius=28, fill=(255, 215, 0))
        f_btn = self._get_font(48, bold=True)
        cdraw.text((target_sz[0] // 2, btn_y + 36), "👇 채널 프로필 링크 터치!", font=f_btn, fill=(15, 18, 26), anchor="mt")
        f_btn_sub = self._get_font(32, bold=True)
        cdraw.text((target_sz[0] // 2, btn_y + 112), "쿠팡 공식 최저가로 1초 만에 바로 이동", font=f_btn_sub, fill=(60, 70, 90), anchor="mt")

        base_rgba.paste(card, (cx, cy), mask=card)
        img = base_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)

        # 제품 밑: 화이트 글래스 인포 카드
        self._draw_info_card(
            img, draw,
            "최저가",
            "로켓배송",
            "100%",
            "(공식 정품 인증)",
            ["• 프로필 상단 링크", "• 01~03번 실시간 연동", "• 로켓배송 최저가 직행"]
        )

        # 하단 자막
        cap1 = slide.caption_line1 or "채널 프로필 링크에서 바로 확인!"
        cap2 = slide.caption_line2 or "구독 누르고 매일 알짜 꿀템 받기"
        self._draw_viral_subtitle(draw, cap1, cap2)

        return img

    def _draw_info_card(self, img: Image.Image, draw: ImageDraw.ImageDraw, price_clean: str, tag: str, star: str, review_text: str, points: List[str]):
        """제품 바로 밑 화이트 글래스 인포 카드 (가로 960 x 세로 270)"""
        card_w, card_h = 960, 270
        card_x = (self.width - card_w) // 2
        card_y = 1090

        base_rgba = img.convert("RGBA")
        card = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(card)
        cdraw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=28, fill=(255, 255, 255, 245), outline=(225, 232, 245), width=2)
        base_rgba = Image.alpha_composite(base_rgba, card)
        img.paste(base_rgba.convert("RGB"))
        draw = ImageDraw.Draw(img)

        # 좌측: 가격 & 로켓배송
        f_p_num = self._get_font(54, bold=True)
        f_p_unit = self._get_font(34, bold=True)
        bbox = draw.textbbox((0, 0), price_clean, font=f_p_num)
        w_num = bbox[2] - bbox[0]

        draw.text((card_x + 45, card_y + 35), price_clean, font=f_p_num, fill=(20, 25, 38))
        if price_clean != "미공개" and price_clean != "최저가":
            draw.text((card_x + 45 + w_num + 12, card_y + 51), "원", font=f_p_unit, fill=(0, 102, 255))

        # 로켓배송 뱃지
        f_rk = self._get_font(26, bold=True)
        draw.rounded_rectangle([card_x + 45, card_y + 115, card_x + 205, card_y + 160], radius=10, fill=(0, 114, 255))
        draw.text((card_x + 125, card_y + 124), f"{tag} 🚀", font=f_rk, fill=(255, 255, 255), anchor="mt")

        # 평점 & 리뷰 (중복 별점 완벽 제거 및 정돈)
        f_star = self._get_font(28, bold=True)
        clean_rev = re.sub(r"[★☆]\s*\d+\.\d+", "", review_text).strip()
        formatted_rating = f"{star}  {clean_rev}" if clean_rev else star
        draw.text((card_x + 45, card_y + 190), formatted_rating, font=f_star, fill=(90, 105, 130))

        # 버티컬 구분선
        draw.line([(card_x + 360, card_y + 35), (card_x + 360, card_y + card_h - 35)], fill=(225, 230, 242), width=2)

        # 우측: 💡 체크포인트
        f_pt_label = self._get_font(26, bold=True)
        draw.rounded_rectangle([card_x + 400, card_y + 35, card_x + 550, card_y + 75], radius=8, fill=(240, 244, 255))
        draw.text((card_x + 475, card_y + 43), "💡 체크포인트", font=f_pt_label, fill=(0, 102, 255), anchor="mt")

        f_pt_item = self._get_font(30, bold=True)
        f_pt_sub = self._get_font(28, bold=False)

        p1 = points[0] if len(points) > 0 else "• 강력 추천 알짜템"
        p2 = points[1] if len(points) > 1 else "• 가성비 1위 검증"
        p3 = points[2] if len(points) > 2 else "• 내돈내산 평점 만점"

        draw.text((card_x + 400, card_y + 98), p1, font=f_pt_item, fill=(25, 32, 48))
        draw.text((card_x + 400, card_y + 148), p2, font=f_pt_item, fill=(0, 102, 255))
        draw.text((card_x + 400, card_y + 196), p3, font=f_pt_sub, fill=(95, 110, 135))

    def _get_item_points(self, title: str) -> List[str]:
        if "청소기" in title:
            return ["• 무선 미니 에어건 겸용", "• 12,000Pa 초강력 흡입", "• C타입 고속 충전 · 차량/책상용"]
        elif "발매트" in title or "규조토" in title:
            return ["• 물기 3초 급속 건조", "• 세탁기 통세탁 가능", "• 미끄럼 방지 논슬립 패드"]
        elif "휴지통" in title or "쓰레기통" in title:
            return ["• 0.3초 스마트 모션 센서", "• 냄새 완벽 차단 밀폐 뚜껑", "• 10L 넉넉한 자취 용량"]
        elif "닭가슴살" in title:
            return ["• 겉촉속촉 퍽퍽함 제로", "• 단백질 22g 고단백 식단", "• 전자레인지 1분 완성"]
        elif "볶음밥" in title:
            return ["• 한 끼 2천 원대 갓성비", "• 6종 골라먹는 재미", "• 프라이팬 3분 뚝딱"]
        elif "그릭요거트" in title:
            return ["• 크림치즈급 꾸덕한 질감", "• 단백질 풍부 무가당", "• 아침 식사대용 꿀조합"]
        else:
            return ["• 광고 0% 솔직 검증", "• 실사용 만족도 최상", "• 로켓배송 최저가"]
