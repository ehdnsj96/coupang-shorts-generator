import re
from typing import List, Optional, Set, Tuple
from models import ShortsScript, Slide
from product_pool import THEMES, ProductItem
import config

TITLE_PREFIX = "아직도 이거 모르고 산다고?"
TITLE_SUFFIX = "쿠팡 꿀템 TOP 3 #shorts"


def build_episode_title(theme_key: str, episode_num: int) -> str:
    """테마·회차별 유튜브 제목. 1탄은 기존 4편과 동일한 포맷을 유지한다."""
    theme_info = THEMES.get(theme_key, THEMES["living"])
    theme_name = theme_info["theme_name"]
    if episode_num > 1:
        return f"{TITLE_PREFIX} {theme_name} {episode_num}탄 {TITLE_SUFFIX}"
    return f"{TITLE_PREFIX} {theme_name} {TITLE_SUFFIX}"


def normalize_title(text: str) -> str:
    """제목 비교용 정규화 (공백·대소문자·특수기호 차이 무시)."""
    if not text:
        return ""
    cleaned = re.sub(r"[\s#]+", "", str(text)).lower()
    cleaned = cleaned.replace("#shorts", "").replace("shorts", "")
    return cleaned


def build_episode(theme_key: str, episode_num: int, items: List[ProductItem]) -> ShortsScript:
    theme_info = THEMES.get(theme_key, THEMES["living"])
    assets = config.ASSETS_DIR

    theme_name = theme_info["theme_name"]

    youtube_title = build_episode_title(theme_key, episode_num)

    # 제품명 리스트 (깔끔한 텍스트 포맷)
    product_names_text = "\n".join([
        f"0{i+1}. {item.title}"
        for i, item in enumerate(items[:3])
    ])

    # 쇼츠 설명란: 긴 주소로 깨지지 않고 채널 프로필 링크로 유도하는 깔끔한 공식 바이럴 포맷
    youtube_description = (
        f"{theme_name} 삶의 질을 확 올려주는 쿠팡 필수템 TOP 3!\n\n"
        f"📌 영상 속 제품 목록\n"
        f"{product_names_text}\n\n"
        f"👉 제품 최저가 구매 링크는 '채널 홈 프로필 링크'를 확인해 주세요!\n\n"
        f"* 쿠팡 파트너스 활동의 일환으로 일정액의 수수료를 제공받습니다.\n\n"
        f"{' '.join(theme_info['hashtags'])}"
    )

    preview_items = [
        {
            "badge": f"BEST 0{i+1}",
            "title": item.title,
            "price": item.price,
            "image_path": item.image_path
        }
        for i, item in enumerate(items[:3])
    ]

    slides = [
        # HOOK
        Slide(
            step_name="HOOK",
            step_index=1,
            total_steps=5,
            header_badge=f"🔥 {theme_name} {episode_num}탄" if episode_num > 1 else f"🔥 {theme_name}",
            main_title=theme_info["hook_title"],
            discount_badge="실구매 1위",
            price_badge="놓치면 후회하는 꿀템",
            tag_badge="가성비 끝판왕",
            card_badge_left="★ 만족도 1위",
            card_badge_right="강력추천",
            caption_line1=theme_info["hook_caption1"],
            caption_line2=theme_info["hook_caption2"],
            voice_script=theme_info["hook_voice"],
            image_path=theme_info["hook_image"],
            preview_items=preview_items
        )
    ]

    # ITEMS 1, 2, 3
    for i, item in enumerate(items[:3]):
        slides.append(
            Slide(
                step_name=f"ITEM_{i+1}",
                step_index=i + 2,
                total_steps=5,
                header_badge=f"BEST 0{i+1} · {item.header_badge}",
                main_title=item.title,
                discount_badge=item.discount,
                price_badge=item.price,
                tag_badge=item.tag,
                card_badge_left=item.card_badge_left,
                card_badge_right="프로필 링크 확인",
                caption_line1=item.caption1,
                caption_line2=item.caption2,
                voice_script=item.voice_script,
                image_path=item.image_path
            )
        )

    # OUTRO: 프로필 링크 유도
    slides.append(
        Slide(
            step_name="OUTRO",
            step_index=5,
            total_steps=5,
            header_badge="📌 제품 최저가 구매 안내",
            main_title="영상 속 꿀템 3가지 링크는?\n채널 프로필 링크에 있어요!",
            discount_badge="로켓배송",
            price_badge="프로필 링크 진행 중",
            tag_badge="바로가기",
            card_badge_left="★ 최저가 보장",
            card_badge_right="쿠팡 로켓배송",
            caption_line1="오늘 소개한 제품 구매 링크는",
            caption_line2="채널 홈 프로필에서 바로 확인!",
            voice_script="오늘 소개해 드린 세 가지 제품 최저가 정보는 채널 홈 프로필 링크에 남겨뒀어요! 프로필 누르고 로켓배송 특가 놓치지 마세요!",
            image_path=str(assets / "outro.png"),
            preview_items=preview_items
        )
    )

    return ShortsScript(
        topic=f"{theme_name} {episode_num}탄",
        youtube_title=youtube_title,
        youtube_description=youtube_description,
        hashtags=theme_info["hashtags"],
        slides=slides,
        items=items[:3]
    )


def get_next_dynamic_episode(
    state: dict,
    blocked_item_ids: Optional[Set[str]] = None,
    published_titles: Optional[Set[str]] = None,
) -> Tuple[Optional[ShortsScript], dict]:
    """아직 쓰지 않은 상품 3종으로 다음 에피소드를 만든다.

    - 사용 이력(로컬 상태 + 도감)에 있는 상품은 절대 재사용하지 않는다.
      (과거 버그: 상품이 3개뿐이라 다 쓰면 used 를 비우고 같은 영상을 무한 재업로드)
    - 이미 게시된 제목의 회차도 건너뛴다.
    - 어떤 테마에도 새 상품 3종이 남아 있지 않으면 None 을 반환하고,
      호출 측(auto_daily)이 생성·업로드를 건너뛴다.
    """
    theme_keys = list(THEMES.keys())
    start_idx = state.get("current_theme_index", 0) % len(theme_keys)

    blocked = set(blocked_item_ids or set())
    published = set(published_titles or set())

    used_map = state.setdefault("used_items_by_theme", {})
    episode_map = state.setdefault("episode_counts_by_theme", {})

    for offset in range(len(theme_keys)):
        theme_idx = (start_idx + offset) % len(theme_keys)
        theme_key = theme_keys[theme_idx]
        theme_info = THEMES[theme_key]

        used_items = set(used_map.get(theme_key, []))
        available_items = [
            p for p in theme_info["products"]
            if p.item_id not in used_items and p.item_id not in blocked
        ]
        if len(available_items) < 3:
            continue

        episodes_count = episode_map.get(theme_key, 0) + 1
        candidate_title = build_episode_title(theme_key, episodes_count)
        if normalize_title(candidate_title) in published:
            # 같은 제목의 회차가 이미 유튜브/도감에 올라가 있으면 이 테마는 건너뛴다.
            print(f"⏭️  '{candidate_title}' 은 이미 게시된 회차라 건너뜁니다.")
            continue

        selected_items = available_items[:3]
        script = build_episode(theme_key, episodes_count, selected_items)

        used_map[theme_key] = used_map.get(theme_key, []) + [p.item_id for p in selected_items]
        episode_map[theme_key] = episodes_count
        state["current_theme_index"] = (theme_idx + 1) % len(theme_keys)

        return script, state

    return None, state
