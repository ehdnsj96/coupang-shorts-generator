from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class Slide:
    step_name: str                     # 'HOOK', 'ITEM_1', 'ITEM_2', 'ITEM_3', 'OUTRO'
    header_badge: str                  # 상단 카테고리 태그 (예: 'BEST 01 · 자취생 필수 꿀템')
    main_title: str                    # 상품명 또는 강조 문구
    discount_badge: Optional[str] = None  # 할인율 뱃지 (예: '35% 특가')
    price_badge: Optional[str] = None     # 가격 텍스트 (예: '29,800원')
    tag_badge: Optional[str] = None       # 태그 뱃지 (예: '로켓배송')
    card_badge_left: str = "★ 4.9 (추천)" # 카드 좌측 상단 평점 뱃지
    card_badge_right: str = "쿠팡 베스트" # 카드 우측 상단 뱃지
    caption_line1: str = ""            # 화면 하단 강조 자막 1줄 (형광 옐로우)
    caption_line2: str = ""            # 화면 하단 강조 자막 2줄 (화이트)
    voice_script: str = ""             # AI 성우 멘트
    image_path: Optional[str] = None   # 실제 제품 사진 로컬 파일 경로
    step_index: int = 1                # 현재 슬라이드 인덱스 (1~5)
    total_steps: int = 5               # 전체 슬라이드 수
    preview_items: Optional[List[Any]] = None # 첫장/마지막장용 3종 제품 프리뷰 리스트


@dataclass
class ShortsScript:
    topic: str
    youtube_title: str
    youtube_description: str
    hashtags: List[str]
    slides: List[Slide] = field(default_factory=list)
    items: List[Any] = field(default_factory=list)
