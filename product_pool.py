from dataclasses import dataclass
from typing import Dict, List, Optional
import config

assets = config.ASSETS_DIR


@dataclass
class ProductItem:
    item_id: str
    title: str
    header_badge: str
    discount: str
    price: str
    tag: str
    card_badge_left: str
    card_badge_right: str
    caption1: str
    caption2: str
    voice_script: str
    image_path: str
    coupang_url: str = ""


# 테마별 제품 데이터 풀 (제품마다 개별 최저가 구매 링크 포함)
THEMES: Dict[str, dict] = {
    "living": {
        "theme_name": "자취생 삶의 질 떡상",
        "hook_title": "자취생 삶의 질 떡상\n쿠팡 꿀템 TOP 3!",
        "hook_voice": "아직도 이거 모르고 사셨나요? 자취 3년 차가 꼽은, 쿠팡에서 안 사면 진짜 손해인 삶의 질 떡상템 탑 3입니다!",
        "hook_caption1": "아직도 이거 모르고 사셨나요?",
        "hook_caption2": "자취 3년 차가 꼽은 찐 꿀템 3가지!",
        "hook_image": str(assets / "hook.png"),
        "hashtags": ["#쿠팡꿀템", "#자취꿀템", "#삶의질상승", "#쿠팡추천", "#가성비템"],
        "products": [
            ProductItem(
                item_id="living_vacuum",
                title="홈플래닛 무선 핸디 청소기",
                header_badge="자취생 필수템",
                discount="특가할인",
                price="27,990원",
                tag="로켓배송",
                card_badge_left="★ 4.8 (후기 4만+)",
                card_badge_right="[프로필 01번 링크]",
                caption1="머리카락·먼지 흡입 끝판왕!",
                caption2="원룸·차량 청소 3초 컷",
                voice_script="첫 번째는 홈플래닛 무선 핸디 청소기입니다. 책상 위 먼지나 머리카락 치울 때 무거운 청소기 꺼낼 필요 없이 삼초 만에 싹 정리돼요.",
                image_path=str(assets / "real_vacuum.png"),
                coupang_url="https://link.coupang.com/a/iACeuVKLq8"
            ),
            ProductItem(
                item_id="living_mat",
                title="코멧 홈 빨아쓰는 규조토 발매트",
                header_badge="순간흡수 발매트",
                discount="특가할인",
                price="8,090원",
                tag="로켓배송",
                card_badge_left="★ 4.8 (후기 8만+)",
                card_badge_right="[프로필 02번 링크]",
                caption1="물기 3초 만에 싹 마름!",
                caption2="세탁기로 빨아쓰는 소프트 매트",
                voice_script="두 번째는 코멧 홈 빨아쓰는 규조토 발매트입니다. 젖은 발 올리자마자 물기를 싹 흡수하고 세탁기에도 바로 돌릴 수 있어서 천 매트 빨래 걱정이 영원히 사라집니다.",
                image_path=str(assets / "real_mat.png"),
                coupang_url="https://link.coupang.com/a/iACiFQU8Oq"
            ),
            ProductItem(
                item_id="living_trashcan",
                title="코멧 모션인식 센서 휴지통 10L",
                header_badge="스마트 센서 휴지통",
                discount="특가할인",
                price="12,990원",
                tag="로켓배송",
                card_badge_left="★ 4.8 (후기 2만+)",
                card_badge_right="[프로필 03번 링크]",
                caption1="손 안 대고 버리는 자동 오픈!",
                caption2="원룸 냄새·벌레 완벽 차단",
                voice_script="세 번째는 코멧 모션인식 센서 휴지통입니다. 손만 갖다 대면 알아서 열리고 닫혀서 냄새랑 벌레까지 완벽하게 차단해 줘요.",
                image_path=str(assets / "real_trashcan.png"),
                coupang_url="https://link.coupang.com/a/iACmJ9LnZQ"
            ),
            ProductItem(
                item_id="living_drying_rack",
                title="접이식 원룸 빨래건조대",
                header_badge="원룸 공간절약템",
                discount="32% 특가",
                price="19,800원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 5,200개)",
                card_badge_right="[댓글 01번 링크]",
                caption1="접으면 두께 5cm로 틈새 쏙!",
                caption2="원룸 방 좁아질 걱정 제로",
                voice_script="원룸 공간 확 넓혀주는 접이식 빨래건조대입니다. 빨래 다 널고 접으면 두께가 5센치밖에 안 돼서 문 뒤나 틈새에 쏙 들어가요.",
                image_path=str(assets / "drying_rack.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%A0%91%EC%9D%B4%EC%8B%9D%20%EC%9B%90%EB%A3%B8%20%EB%B9%A8%EB%9E%98%EA%B1%B4%EC%A1%B0%EB%8C%80&lptag=AF7086198"
            ),
            ProductItem(
                item_id="living_storage_cart",
                title="슬림 틈새 슬라이딩 수납장",
                header_badge="틈새 수납 종결자",
                discount="36% 특가",
                price="14,900원",
                tag="무료배송",
                card_badge_left="★ 4.8 (후기 4,100개)",
                card_badge_right="[댓글 02번 링크]",
                caption1="냉장고 옆 틈새 15cm의 기적!",
                caption2="바퀴 달린 부드러운 수납 카트",
                voice_script="다음은 슬림 틈새 슬라이딩 수납장입니다. 냉장고 옆이나 세탁기 옆 죽은 틈새 십오 센티미터 공간을 알짜 수납창고로 만들어 줍니다.",
                image_path=str(assets / "storage_cart.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%8A%AC%EB%A6%BC%20%ED%8B%88%EC%83%88%20%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%94%A9%20%EC%88%98%EB%82%A9%EC%9E%A5&lptag=AF7086198"
            ),
            ProductItem(
                item_id="living_lint_remover",
                title="충전식 무선 보풀제거기",
                header_badge="새옷 복구 필수템",
                discount="42% 특가",
                price="13,800원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 7,300개)",
                card_badge_right="[댓글 03번 링크]",
                caption1="낡은 니트·코트 3분 만에 새 옷!",
                caption2="원단 손상 없는 안전 칼날",
                voice_script="마지막은 충전식 무선 보풀제거기입니다. 겨울철 니트나 코트에 핀 보풀을 슥슥 문지르기만 하면 방금 산 새 옷처럼 말끔하게 복구돼요.",
                image_path=str(assets / "lint_remover.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%B6%A9%EC%A0%84%EC%8B%9D%20%EB%AC%B4%EC%84%A0%20%EB%B3%B4%ED%92%80%EC%A0%9C%EA%B1%B0%EA%B8%B0&lptag=AF7086198"
            )
        ]
    },

    "kitchen": {
        "theme_name": "주방 살림 혁명",
        "hook_title": "요리시간 반으로 줄여주는\n주방 꿀템 TOP 3!",
        "hook_voice": "주방 일 아직도 손으로 힘들게 하시나요? 살림 고수들이 입을 모아 극찬한, 요리 시간 반으로 줄여주는 주방 꿀템 탑 3입니다!",
        "hook_caption1": "주방 일 힘드셨죠?",
        "hook_caption2": "살림 고수들이 숨겨둔 찐 꿀템 3가지!",
        "hook_image": str(assets / "kitchen_hook.png"),
        "hashtags": ["#주방용품 #살림꿀템 #쿠팡추천 #요리필수템 #가성비주방템"],
        "products": [
            ProductItem(
                item_id="kitchen_opener",
                title="전동 원터치 자동 오프너",
                header_badge="원터치 자동 오프너",
                discount="30% 특가",
                price="15,900원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 2,300개)",
                card_badge_right="[댓글 01번 링크]",
                caption1="버튼 하나로 뚜껑 자동 오픈!",
                caption2="단단한 캔·병뚜껑 2초 컷",
                voice_script="첫 번째는 전동 원터치 자동 오프너입니다. 꽉 닫힌 잼 병이나 와인도 버튼 한 번만 누르면 힘들이지 않고 2초 만에 쏙 열립니다.",
                image_path=str(assets / "kitchen_opener.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%A0%84%EB%8F%99%20%EC%9B%90%ED%84%B0%EC%B9%98%20%EC%9E%90%EB%8F%99%20%EC%98%A4%ED%94%84%EB%84%88&lptag=AF7086198"
            ),
            ProductItem(
                item_id="kitchen_drain",
                title="항균 실리콘 배수구 커버",
                header_badge="실리콘 배수구 거름망",
                discount="25% 특가",
                price="8,900원",
                tag="1+1 세트",
                card_badge_left="★ 4.8 (후기 5,100개)",
                card_badge_right="[댓글 02번 링크]",
                caption1="음식물 찌꺼기 쏙 버리기!",
                caption2="싱크대 냄새·물때 걱정 제로",
                voice_script="두 번째는 항균 실리콘 배수구 커버입니다. 뒤집어서 툭 털어내면 음식물 쓰레기가 싹 떨어져서 손에 더러운 물 묻힐 필요가 없어요.",
                image_path=str(assets / "kitchen_drain.png"),
                coupang_url="https://www.coupang.com/np/search?q=%ED%95%AD%EA%B7%A0%20%EC%8B%A4%EB%A6%AC%EC%BD%98%20%EB%B0%B0%EC%88%98%EA%B5%AC%20%EC%BB%A4%EB%B2%84&lptag=AF7086198"
            ),
            ProductItem(
                item_id="kitchen_screen",
                title="기름 튐 방지 미세망 커버",
                header_badge="스테인리스 기름방패",
                discount="32% 특가",
                price="12,500원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 3,800개)",
                card_badge_right="[댓글 03번 링크]",
                caption1="삼겹살 구워도 기름 안 튐!",
                caption2="가스레인지 청소 탈출",
                voice_script="세 번째는 기름 튐 방지 미세망입니다. 고기나 튀김 요리할 때 덮어두기만 하면 수증기는 빠지고 기름만 완벽하게 막아줘서 청소가 끝납니다.",
                image_path=str(assets / "kitchen_screen.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B8%B0%EB%A6%84%20%ED%8A%90%20%EB%B0%A9%EC%A7%80%20%EB%AF%B8%EC%84%B8%EB%A7%9D%20%EC%BB%A4%EB%B2%84&lptag=AF7086198"
            )
        ]
    },

        "food": {
        "theme_name": "식비 절약 가성비 간편식",
        "hook_title": "식비 반으로 줄여주는\n쿠팡 가성비 간편식 TOP 3!",
        "hook_voice": "요즘 배달비랑 외식비 너무 비싸죠? 냉동실에 쟁여두면 식비 삼십만 원 아껴주는 쿠팡 꿀맛 간편식 탑 3입니다!",
        "hook_caption1": "요즘 외식비·배달비 너무 비싸죠?",
        "hook_caption2": "식비 30만 원 아껴주는 갓성비 간편식 TOP 3!",
        "hook_image": str(assets / "food_chicken.png"),
        "hashtags": ["#식비절약", "#쿠팡간편식", "#쿠팡식품", "#로켓프레시", "#가성비식품", "#자취식비"],
        "products": [
            ProductItem(
                item_id="food_chicken",
                title="곰곰 촉촉한 오븐구이 닭가슴살 10팩",
                header_badge="겉촉속촉 닭가슴살",
                discount="로켓프레시 특가",
                price="19,900원",
                tag="로켓프레시",
                card_badge_left="★ 4.9 (후기 12만+)",
                card_badge_right="[프로필 01번 링크]",
                caption1="퍽퍽함 제로! 육즙 가득 닭가슴살",
                caption2="식단 관리·단백질 보충 1위",
                voice_script="첫 번째는 곰곰 촉촉한 오븐구이 닭가슴살입니다. 퍽퍽함이 전혀 없고 닭다리살처럼 부드러워서 식단 관리할 때 물리지 않고 매일 먹을 수 있어요.",
                image_path=str(assets / "food_chicken.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B3%B0%EA%B3%B0%20%EC%B4%89%EC%B4%89%ED%95%9C%20%EC%98%A4%EB%B8%90%EA%B5%AC%EC%9D%B4%20%EB%8B%AD%EA%B0%80%EC%8A%B4%EC%82%B4%2010%ED%8C%A9&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_friedrice",
                title="곰곰 한끼뚝딱 가성비 냉동 볶음밥 6종",
                header_badge="한끼 2천원대 볶음밥",
                discount="로켓프레시 특가",
                price="13,800원",
                tag="로켓프레시",
                card_badge_left="★ 4.8 (후기 9만+)",
                card_badge_right="[프로필 02번 링크]",
                caption1="전자레인지 3분 뚝딱 완성!",
                caption2="배달 음식 생각 싹 사라지는 맛",
                voice_script="두 번째는 곰곰 가성비 냉동 볶음밥 세트입니다. 배고플 때 전자레인지에 3분만 돌리면 전문점 볶음밥 맛이 나서 배달 음식 끊게 만들어 줍니다.",
                image_path=str(assets / "food_friedrice.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B3%B0%EA%B3%B0%20%ED%95%9C%EB%81%BC%EB%9A%9D%EB%94%B1%20%EA%B0%80%EC%84%B1%EB%B9%84%20%EB%83%89%EB%8F%99%20%EB%B3%B6%EC%9D%8C%EB%B0%A5%206%EC%A2%85&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_yogurt",
                title="그릭데이 시그니처 대용량 그릭요거트",
                header_badge="꾸덕함 끝판왕 그릭요거트",
                discount="특가할인",
                price="14,800원",
                tag="로켓프레시",
                card_badge_left="★ 4.9 (후기 5만+)",
                card_badge_right="[프로필 03번 링크]",
                caption1="치즈처럼 꾸덕한 리얼 그릭!",
                caption2="바쁜 아침 건강한 1분 식사",
                voice_script="세 번째는 그릭데이 시그니처 대용량 그릭요거트입니다. 크림치즈처럼 진하고 꾸덕해서 꿀이나 그래놀라 얹어 먹으면 아침 식사 대용으로 최고예요.",
                image_path=str(assets / "food_yogurt.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B7%B8%EB%A6%AD%EB%8D%B0%EC%9D%B4%20%EC%8B%9C%EA%B7%B8%EB%8B%88%EC%B2%98%20%EB%8C%80%EC%9A%A9%EB%9F%89%20%EA%B7%B8%EB%A6%AD%EC%9A%94%EA%B1%B0%ED%8A%B8&lptag=AF7086198"
            )
        ]
    },
    "desk": {
        "theme_name": "직장인 데스크테리어",
        "hook_title": "칼퇴 부르는 책상 위\n데스크테리어 꿀템 TOP 3!",
        "hook_voice": "책상 위 아직도 어수선하신가요? 일잘러들이 책상 위에 꼭 올려두는 업무 효율 두 배 높여주는 데스크테리어 꿀템 탑 3입니다!",
        "hook_caption1": "책상 위 아직도 지저분한가요?",
        "hook_caption2": "일잘러들이 쓰는 데스크테리어 꿀템 3가지!",
        "hook_image": str(assets / "desk_hook.png"),
        "hashtags": ["#데스크테리어 #직장인꿀템 #재택근무 #책상꾸미기 #쿠팡추천"],
        "products": [
            ProductItem(
                item_id="desk_charger",
                title="접이식 3in1 무선충전기",
                header_badge="3in1 맥세이프 충전기",
                discount="38% 특가",
                price="28,900원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 4,800개)",
                card_badge_right="[댓글 01번 링크]",
                caption1="폰·워치·이어폰 동시 고속충전!",
                caption2="지저분한 충전선 한 번에 정리",
                voice_script="첫 번째는 접이식 3in1 맥세이프 무선충전기입니다. 스마트폰, 워치, 무선이어폰까지 선 하나로 동시 충전돼서 책상이 정말 깔끔해집니다.",
                image_path=str(assets / "desk_charger.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%A0%91%EC%9D%B4%EC%8B%9D%203in1%20%EB%AC%B4%EC%84%A0%EC%B6%A9%EC%A0%84%EA%B8%B0&lptag=AF7086198"
            ),
            ProductItem(
                item_id="desk_lightbar",
                title="시력보호 모니터 조명바",
                header_badge="모니터 스크린바 조명",
                discount="32% 특가",
                price="24,900원",
                tag="눈피로 제로",
                card_badge_left="★ 4.8 (후기 6,200개)",
                card_badge_right="[댓글 02번 링크]",
                caption1="화면 반사 없이 책상만 밝게!",
                caption2="장시간 모니터 봐도 눈 안 아픔",
                voice_script="두 번째는 시력보호 모니터 조명바입니다. 모니터 위에 얹기만 하면 화면 반사 없이 책상 위만 부드럽게 비춰줘서 눈의 피로가 싹 사라집니다.",
                image_path=str(assets / "desk_lightbar.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%8B%9C%EB%A0%A5%EB%B3%B4%ED%98%B8%20%EB%AA%A8%EB%8B%88%ED%84%B0%20%EC%A1%B0%EB%AA%85%EB%B0%94&lptag=AF7086198"
            ),
            ProductItem(
                item_id="desk_mouse",
                title="무소음 인체공학 버티컬마우스",
                header_badge="인체공학 버티컬 마우스",
                discount="40% 특가",
                price="19,800원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 5,900개)",
                card_badge_right="[댓글 03번 링크]",
                caption1="손목 꺾임 없는 편안한 각도!",
                caption2="딸깍 소리 없는 도서관급 무소음",
                voice_script="세 번째는 무소음 인체공학 버티컬 마우스입니다. 악수하듯 편안하게 쥐는 각도로 손목 통증을 없애주고 도서관에서도 쓸 수 있는 무소음 클릭이에요.",
                image_path=str(assets / "desk_mouse.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EB%AC%B4%EC%86%8C%EC%9D%8C%20%EC%9D%B8%EC%B2%B4%EA%B3%B5%ED%95%99%20%EB%B2%84%ED%8B%B0%EC%BB%AC%EB%A7%88%EC%9A%B0%EC%8A%A4&lptag=AF7086198"
            )
        ]
    }
}


def load_custom_products():
    """custom_products.json에 저장된 사용자의 신규 수집 상품들을 테마 풀에 자동 병합"""
    import json
    custom_file = config.BASE_DIR / "custom_products.json"
    if not custom_file.exists():
        return
    try:
        with open(custom_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for theme_key, items in data.items():
            if theme_key in THEMES:
                for d in items:
                    p = ProductItem(
                        item_id=d["item_id"],
                        title=d["title"],
                        header_badge=d.get("header_badge", "가성비 추천템"),
                        discount=d.get("discount", "특가할인"),
                        price=d["price"],
                        tag=d.get("tag", "로켓배송"),
                        card_badge_left=d.get("card_badge_left", "★ 4.8"),
                        card_badge_right=d.get("card_badge_right", "[프로필 링크]"),
                        caption1=d.get("caption1", ""),
                        caption2=d.get("caption2", ""),
                        voice_script=d.get("voice_script", ""),
                        image_path=d["image_path"],
                        coupang_url=d.get("coupang_url", "")
                    )
                    if not any(x.item_id == p.item_id for x in THEMES[theme_key]["products"]):
                        THEMES[theme_key]["products"].append(p)
    except Exception as e:
        print(f"⚠️ custom_products 로드 중 오류: {e}")


load_custom_products()

