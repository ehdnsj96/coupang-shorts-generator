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
                header_badge="원터치 전동 오프너",
                discount="30% 특가",
                price="15,900원",
                tag="로켓배송",
                card_badge_left="★ 4.9 (후기 2,300개)",
                card_badge_right="[댓글 01번 링크]",
                caption1="버튼 하나로 코르크 자동 오픈!",
                caption2="단단한 와인 코르크 2초 컷",
                voice_script="첫 번째는 전동 원터치 자동 오프너입니다. 꽉 닫힌 코르크도 버튼 한 번만 누르면 힘들이지 않고 2초 만에 쏙 열립니다.",
                image_path=str(assets / "kitchen_opener.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%A0%84%EB%8F%99%20%EC%99%80%EC%9D%B8%EC%98%A4%ED%94%84%EB%84%88&lptag=AF7086198"
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
                title="굽네 닭가슴살 스테이크 매콤갈비맛",
                header_badge="오븐구이 닭가슴살",
                discount="로켓프레시 특가",
                price="19,900원",
                tag="로켓프레시",
                card_badge_left="★ 4.9 (후기 12만+)",
                card_badge_right="[프로필 01번 링크]",
                caption1="퍽퍽함 제로! 육즙 가득 스테이크",
                caption2="식단 관리·단백질 보충 1위",
                voice_script="첫 번째는 굽네 닭가슴살 스테이크입니다. 퍽퍽함이 전혀 없고 육즙 가득 부드러워서 식단 관리할 때 물리지 않고 매일 먹을 수 있어요.",
                image_path=str(assets / "food_chicken.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B5%BD%EB%84%A4%20%EB%8B%AD%EA%B0%80%EC%8A%B4%EC%82%B4%20%EC%8A%A4%ED%85%8C%EC%9D%B4%ED%81%AC%20%EB%A7%A4%EC%BD%A4%EA%B0%88%EB%B9%84%EB%A7%9B&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_friedrice",
                title="프레시지 대파 삼겹 볶음밥",
                header_badge="고소한 대파삼겹 볶음밥",
                discount="로켓프레시 특가",
                price="13,800원",
                tag="로켓프레시",
                card_badge_left="★ 4.8 (후기 9만+)",
                card_badge_right="[프로필 02번 링크]",
                caption1="전자레인지 3분 뚝딱 완성!",
                caption2="고소한 대파 기름 풍미 가득",
                voice_script="두 번째는 프레시지 대파 삼겹 볶음밥입니다. 고소한 삼겹살과 대파 기름 풍미가 가득해서 전자레인지에 삼분만 돌리면 전문점 볶음밥 맛이 납니다.",
                image_path=str(assets / "food_friedrice.png"),
                coupang_url="https://www.coupang.com/np/search?q=%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8C%80%ED%8C%8C%20%EC%82%BC%EA%B2%B9%20%EB%B3%B6%EC%9D%8C%EB%B0%A5&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_yogurt",
                title="꾸덕한 수제 그릭요거트 대용량",
                header_badge="꾸덕함 끝판왕 그릭요거트",
                discount="특가할인",
                price="14,800원",
                tag="로켓프레시",
                card_badge_left="★ 4.9 (후기 5만+)",
                card_badge_right="[프로필 03번 링크]",
                caption1="치즈처럼 꾸덕한 리얼 그릭!",
                caption2="바쁜 아침 건강한 1분 식사",
                voice_script="세 번째는 꾸덕한 수제 그릭요거트입니다. 크림치즈처럼 진하고 꾸덕해서 꿀이나 그래놀라 얹어 먹으면 아침 식사 대용으로 최고예요.",
                image_path=str(assets / "food_yogurt.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%BE%B8%EB%8D%95%ED%95%9C%20%EA%B7%B8%EB%A6%AD%EC%9A%94%EA%B1%B0%ED%8A%B8&lptag=AF7086198"
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
    },

    "bath": {
        "theme_name": "욕실·샤워 리셋",
        "hook_title": "샤워만 해도 리셋되는\n욕실 꿀템 TOP 3!",
        "hook_voice": "샤워기 물이랑 욕실 바닥, 아직도 그냥 쓰고 계셨나요? 사천 원대부터 시작하는, 욕실이 확 달라지는 쿠팡 꿀템 탑 쓰리입니다!",
        "hook_caption1": "샤워기 필터, 언제 갈았죠?",
        "hook_caption2": "욕실이 확 달라지는 찐 꿀템 3가지!",
        "hook_image": str(assets / "bath_shower_filter.png"),
        "hashtags": ["#욕실꿀템", "#샤워기필터", "#욕실화추천", "#쿠팡추천", "#자취꿀템"],
        "products": [
            ProductItem(
                item_id="bath_shower_filter",
                title="코멧 홈 파워수압 필터 샤워기 본품 + 필터 2개입",
                header_badge="코멧 파워수압 샤워기",
                discount="37% 할인",
                price="6,290원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 2만+)",
                card_badge_right="[프로필 01번 링크]",
                caption1="수압은 세게, 물은 깨끗하게!",
                caption2="필터 2개입 포함 6,290원",
                voice_script="첫 번째는 코멧 홈 파워수압 필터 샤워기입니다. 수압은 세게 올려주면서 미세 필터가 물속 이물질까지 걸러줘서, 샤워하고 나면 피부가 확 달라집니다.",
                image_path=str(assets / "bath_shower_filter.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%BD%94%EB%A9%A7%20%ED%99%88%20%ED%8C%8C%EC%9B%8C%EC%88%98%EC%95%95%20%ED%95%84%ED%84%B0%20%EC%83%A4%EC%9B%8C%EA%B8%B0&lptag=AF7086198"
            ),
            ProductItem(
                item_id="bath_microfilter",
                title="코멧 홈 샤워기 헤드 퓨어 마이크로 필터 3개",
                header_badge="마이크로 필터 교체팩",
                discount="63% 할인",
                price="7,210원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 1.3만+)",
                card_badge_right="[프로필 02번 링크]",
                caption1="갈아주는 순간 물이 달라져요",
                caption2="3개입이라 1년 내내 넉넉하게",
                voice_script="두 번째는 코멧 홈 마이크로 필터 3개입입니다. 샤워기 필터는 두세 달마다 갈아줘야 하는데, 세 개들이라 일 년 내내 넉넉하게 쓸 수 있어요.",
                image_path=str(assets / "bath_microfilter.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%BD%94%EB%A9%A7%20%ED%99%88%20%EC%83%A4%EC%9B%8C%EA%B8%B0%20%ED%97%A4%EB%93%9C%20%ED%93%A8%EC%96%B4%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%20%ED%95%84%ED%84%B0&lptag=AF7086198"
            ),
            ProductItem(
                item_id="bath_slippers",
                title="글랑앤 미끄럼방지 욕실화 실내화 남성용, 그레이",
                header_badge="미끄럼방지 욕실화",
                discount="40% 할인",
                price="5,900원",
                tag="BEST AWARDS",
                card_badge_left="★ 4.5 (후기 5만+)",
                card_badge_right="[프로필 03번 링크]",
                caption1="물기 많은 욕실 바닥 미끄럼 방지",
                caption2="후기 5만 개 넘은 검증된 기본템",
                voice_script="세 번째는 글랑앤 미끄럼방지 욕실화입니다. 물기 많은 욕실 바닥에서도 미끄러지지 않고, 물빠짐 구멍 덕분에 늘 뽀송하게 신을 수 있어요.",
                image_path=str(assets / "bath_slippers.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EA%B8%80%EB%9E%91%EC%95%A4%20%EB%AF%B8%EB%81%84%EB%9F%BC%EB%B0%A9%EC%A7%80%20%EC%9A%95%EC%8B%A4%ED%99%94%20%EB%82%A8%EC%84%B1%EC%9A%A9&lptag=AF7086198"
            )
        ]
    },

    "car": {
        "theme_name": "차 안 리셋 꿀템",
        "hook_title": "세차장 안 가도 되는\n차 안 꿀템 TOP 3!",
        "hook_voice": "세차장 갈 시간도 없고 차 냄새는 신경 쓰이시죠? 물 없이도 차가 반짝이는, 쿠팡 차량 꿀템 탑 쓰리입니다!",
        "hook_caption1": "세차할 시간이 없으시다면?",
        "hook_caption2": "물 없이 차가 반짝이는 꿀템 3가지!",
        "hook_image": str(assets / "car_waterless.png"),
        "hashtags": ["#차량용품", "#물없이세차", "#차량방향제", "#셀프세차", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="car_diffuser",
                title="코코도르 우드볼 차량용 디퓨저 50ml 2개입 우디호텔",
                header_badge="우드볼 차량 디퓨저",
                discount="53% 할인",
                price="7,900원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 1.5만+)",
                card_badge_right="[프로필 01번 링크]",
                caption1="시동 걸면 은은하게 퍼지는 호텔 향",
                caption2="2개입이라 대시보드까지 커버",
                voice_script="첫 번째는 코코도르 우드볼 차량용 디퓨저입니다. 시동 걸자마자 호텔 라운지 향이 은은하게 퍼져서, 차에 타는 순간 기분이 확 좋아집니다.",
                image_path=str(assets / "car_diffuser.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%BD%94%EC%BD%94%EB%8F%84%EB%A5%B4%20%EC%9A%B0%EB%93%9C%EB%B3%BC%20%EC%B0%A8%EB%9F%89%EC%9A%A9%20%EB%94%94%ED%93%A8%EC%A0%80%20%EC%9A%B0%EB%94%94%ED%98%B8%ED%85%94&lptag=AF7086198"
            ),
            ProductItem(
                item_id="car_waterless",
                title="카렉스 스마트 워터리스 카워시 750ml",
                header_badge="물없이 세차 카워시",
                discount="39% 할인",
                price="4,200원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 4,300+)",
                card_badge_right="[프로필 02번 링크]",
                caption1="물 없이 뿌리고 닦으면 끝!",
                caption2="세차장 줄 설 일 없어져요",
                voice_script="두 번째는 카렉스 스마트 워터리스 카워시입니다. 물 없이 뿌리고 닦기만 하면 오염 제거부터 광택까지 한 번에 끝나서, 아파트 주차장에서도 세차가 됩니다.",
                image_path=str(assets / "car_waterless.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EC%B9%B4%EB%A0%89%EC%8A%A4%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%9B%8C%ED%84%B0%EB%A6%AC%EC%8A%A4%20%EC%B9%B4%EC%9B%8C%EC%8B%9C&lptag=AF7086198"
            ),
            ProductItem(
                item_id="car_wax",
                title="불스원 하이브리드 물왁스 600ml",
                header_badge="불스원 하이브리드 왁스",
                discount="베스트상품",
                price="5,540원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 9,500+)",
                card_badge_right="[프로필 03번 링크]",
                caption1="물 묻은 차에 뿌리고 닦으면 광택",
                caption2="왁스칠 한 번에 비 오염까지",
                voice_script="세 번째는 불스원 하이브리드 물왁스입니다. 물 묻은 차에 그대로 뿌리고 닦기만 해도 광택이 올라와서, 왁스칠 한 번으로 한 달은 반짝입니다.",
                image_path=str(assets / "car_wax.png"),
                coupang_url="https://www.coupang.com/np/search?q=%EB%B6%88%EC%8A%A4%EC%9B%90%20%ED%95%98%EC%9D%B4%EB%B8%8C%EB%A6%AC%EB%93%9C%20%EB%AC%BC%EC%99%81%EC%8A%A4&lptag=AF7086198"
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

