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
                coupang_url="https://www.coupang.com/vp/products/5234137115?itemId=7375667237&lptag=AF7086198"
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
                coupang_url="https://www.coupang.com/vp/products/6989053316?itemId=17099465335&lptag=AF7086198"
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
                coupang_url="https://www.coupang.com/vp/products/9725911694?itemId=29104988493&lptag=AF7086198"
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
                title="벨라쿠진 전동 와인 오프너",
                header_badge="원터치 전동 오프너",
                discount="쿠폰할인",
                price="15,580원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 798)",
                card_badge_right="[댓글 01번 링크]",
                caption1="버튼 하나로 코르크 자동 오픈!",
                caption2="단단한 와인 코르크 2초 컷",
                voice_script="첫 번째는 전동 원터치 자동 오프너입니다. 꽉 닫힌 코르크도 버튼 한 번만 누르면 힘들이지 않고 2초 만에 쏙 열립니다.",
                image_path=str(assets / "kitchen_opener.png"),
                coupang_url="https://www.coupang.com/vp/products/1796526368?itemId=3056347060&vendorItemId=71044341298&lptag=AF7086198"
            ),
            ProductItem(
                item_id="kitchen_drain",
                title="코멧 홈 냄새차단 실리콘 배수구 커버",
                header_badge="실리콘 배수구 거름망",
                discount="2개입 특가",
                price="3,800원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 6,894)",
                card_badge_right="[댓글 02번 링크]",
                caption1="음식물 찌꺼기 쏙 버리기!",
                caption2="싱크대 냄새·물때 걱정 제로",
                voice_script="두 번째는 항균 실리콘 배수구 커버입니다. 뒤집어서 툭 털어내면 음식물 쓰레기가 싹 떨어져서 손에 더러운 물 묻힐 필요가 없어요.",
                image_path=str(assets / "kitchen_drain.png"),
                coupang_url="https://www.coupang.com/vp/products/7702601317?itemId=20627342844&vendorItemId=87701366382&lptag=AF7086198"
            ),
            ProductItem(
                item_id="kitchen_screen",
                title="4BNK 스테인레스 심플 후라이팬 덮개 32cm",
                header_badge="스테인리스 기름방패",
                discount="BEST AWARDS",
                price="8,010원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 11,138)",
                card_badge_right="[댓글 03번 링크]",
                caption1="삼겹살 구워도 기름 안 튐!",
                caption2="가스레인지 청소 탈출",
                voice_script="세 번째는 기름 튐 방지 미세망입니다. 고기나 튀김 요리할 때 덮어두기만 하면 수증기는 빠지고 기름만 완벽하게 막아줘서 청소가 끝납니다.",
                image_path=str(assets / "kitchen_screen.png"),
                coupang_url="https://www.coupang.com/vp/products/6317163928?itemId=784715207&vendorItemId=4987822596&lptag=AF7086198"
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
                title="굽네 오븐구이 통닭가슴살 3종 7팩 세트",
                header_badge="오븐구이 닭가슴살",
                discount="로켓배송 특가",
                price="19,400원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 1,508)",
                card_badge_right="[프로필 01번 링크]",
                caption1="퍽퍽함 제로! 육즙 가득 스테이크",
                caption2="식단 관리·단백질 보충 1위",
                voice_script="첫 번째는 굽네 오븐구이 통닭가슴살 세트입니다. 오리지널에 매콤바베큐, 양념갈비맛까지 일곱 팩이 들어 있어서 퍽퍽함 없이 매일 다른 맛으로 단백질 챙길 수 있어요.",
                image_path=str(assets / "food_chicken.png"),
                coupang_url="https://www.coupang.com/vp/products/6585894149?itemId=14840190872&vendorItemId=82079461649&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_friedrice",
                title="곰곰 대패삼겹 볶음밥 300g 6개",
                header_badge="고소한 대파삼겹 볶음밥",
                discount="로켓배송 특가",
                price="14,290원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 10,813)",
                card_badge_right="[프로필 02번 링크]",
                caption1="전자레인지 3분 뚝딱 완성!",
                caption2="고소한 대파 기름 풍미 가득",
                voice_script="두 번째는 곰곰 대패삼겹 볶음밥입니다. 고소한 대패삼겹과 대파 기름 풍미가 가득해서 전자레인지에 삼분만 돌리면 전문점 볶음밥 맛이 납니다.",
                image_path=str(assets / "food_friedrice.png"),
                coupang_url="https://www.coupang.com/vp/products/1310396683?itemId=2327020825&vendorItemId=70323614196&lptag=AF7086198"
            ),
            ProductItem(
                item_id="food_yogurt",
                title="요빌 거품 싹 뺀 수제 그릭요거트 무가당 1kg",
                header_badge="꾸덕함 끝판왕 그릭요거트",
                discount="특가할인",
                price="20,690원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 6,973)",
                card_badge_right="[프로필 03번 링크]",
                caption1="치즈처럼 꾸덕한 리얼 그릭!",
                caption2="바쁜 아침 건강한 1분 식사",
                voice_script="세 번째는 꾸덕한 수제 그릭요거트입니다. 크림치즈처럼 진하고 꾸덕해서 꿀이나 그래놀라 얹어 먹으면 아침 식사 대용으로 최고예요.",
                image_path=str(assets / "food_yogurt.png"),
                coupang_url="https://www.coupang.com/vp/products/7663543620?itemId=20423381605&vendorItemId=85001639216&lptag=AF7086198"
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
                title="맨큐 접이식 3in1 무선충전기",
                header_badge="3in1 맥세이프 충전기",
                discount="특가할인",
                price="19,800원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 1,397)",
                card_badge_right="[댓글 01번 링크]",
                caption1="폰·워치·이어폰 동시 고속충전!",
                caption2="지저분한 충전선 한 번에 정리",
                voice_script="첫 번째는 접이식 3in1 맥세이프 무선충전기입니다. 스마트폰, 워치, 무선이어폰까지 선 하나로 동시 충전돼서 책상이 정말 깔끔해집니다.",
                image_path=str(assets / "desk_charger.png"),
                coupang_url="https://www.coupang.com/vp/products/9606479201?itemId=28678659938&vendorItemId=95683864660&lptag=AF7086198"
            ),
            ProductItem(
                item_id="desk_lightbar",
                title="파파 LED 모니터 조명 PA-450M",
                header_badge="모니터 스크린바 조명",
                discount="특가할인",
                price="23,660원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 1,705)",
                card_badge_right="[댓글 02번 링크]",
                caption1="화면 반사 없이 책상만 밝게!",
                caption2="장시간 모니터 봐도 눈 안 아픔",
                voice_script="두 번째는 시력보호 모니터 조명바입니다. 모니터 위에 얹기만 하면 화면 반사 없이 책상 위만 부드럽게 비춰줘서 눈의 피로가 싹 사라집니다.",
                image_path=str(assets / "desk_lightbar.png"),
                coupang_url="https://www.coupang.com/vp/products/2322111552?itemId=4010546523&vendorItemId=71994763312&lptag=AF7086198"
            ),
            ProductItem(
                item_id="desk_mouse",
                title="코시 무소음 버티컬 무선마우스 M4003WL",
                header_badge="인체공학 버티컬 마우스",
                discount="특가할인",
                price="19,500원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 1,549)",
                card_badge_right="[댓글 03번 링크]",
                caption1="손목 꺾임 없는 편안한 각도!",
                caption2="딸깍 소리 없는 도서관급 무소음",
                voice_script="세 번째는 무소음 인체공학 버티컬 마우스입니다. 악수하듯 편안하게 쥐는 각도로 손목 통증을 없애주고 도서관에서도 쓸 수 있는 무소음 클릭이에요.",
                image_path=str(assets / "desk_mouse.png"),
                coupang_url="https://www.coupang.com/vp/products/5001481074?itemId=6686136608&vendorItemId=73979826014&lptag=AF7086198"
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
                card_badge_left="★ 5.0 (후기 19,968)",
                card_badge_right="[프로필 01번 링크]",
                caption1="수압은 세게, 물은 깨끗하게!",
                caption2="필터 2개입 포함 6,290원",
                voice_script="첫 번째는 코멧 홈 파워수압 필터 샤워기입니다. 수압은 세게 올려주면서 미세 필터가 물속 이물질까지 걸러줘서, 샤워하고 나면 피부가 확 달라집니다.",
                image_path=str(assets / "bath_shower_filter.png"),
                coupang_url="https://www.coupang.com/vp/products/7178787283?itemId=18101284961&vendorItemId=85253394509&lptag=AF7086198"
            ),
            ProductItem(
                item_id="bath_microfilter",
                title="코멧 홈 샤워기 헤드 퓨어 마이크로 필터 3개",
                header_badge="마이크로 필터 교체팩",
                discount="63% 할인",
                price="7,210원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 13,790)",
                card_badge_right="[프로필 02번 링크]",
                caption1="갈아주는 순간 물이 달라져요",
                caption2="3개입이라 1년 내내 넉넉하게",
                voice_script="두 번째는 코멧 홈 마이크로 필터 3개입입니다. 샤워기 필터는 두세 달마다 갈아줘야 하는데, 세 개들이라 일 년 내내 넉넉하게 쓸 수 있어요.",
                image_path=str(assets / "bath_microfilter.png"),
                coupang_url="https://www.coupang.com/vp/products/189592912?itemId=541466221&vendorItemId=4416600777&lptag=AF7086198"
            ),
            ProductItem(
                item_id="bath_slippers",
                title="글랑앤 미끄럼방지 욕실화 실내화 남성용, 그레이",
                header_badge="미끄럼방지 욕실화",
                discount="40% 할인",
                price="5,900원",
                tag="BEST AWARDS",
                card_badge_left="★ 4.5 (후기 53,846)",
                card_badge_right="[프로필 03번 링크]",
                caption1="물기 많은 욕실 바닥 미끄럼 방지",
                caption2="후기 5만 개 넘은 검증된 기본템",
                voice_script="세 번째는 글랑앤 미끄럼방지 욕실화입니다. 물기 많은 욕실 바닥에서도 미끄러지지 않고, 물빠짐 구멍 덕분에 늘 뽀송하게 신을 수 있어요.",
                image_path=str(assets / "bath_slippers.png"),
                coupang_url="https://www.coupang.com/vp/products/6267699231?itemId=12799889489&vendorItemId=80065914547&lptag=AF7086198"
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
                title="코코도르 우드볼 차량용 디퓨저 50ml 2개입",
                header_badge="우드볼 차량 디퓨저",
                discount="53% 할인",
                price="7,900원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 15,841)",
                card_badge_right="[프로필 01번 링크]",
                caption1="시동 걸면 은은하게 퍼지는 호텔 향",
                caption2="2개입이라 대시보드까지 커버",
                voice_script="첫 번째는 코코도르 우드볼 차량용 디퓨저입니다. 시동 걸자마자 호텔 라운지 향이 은은하게 퍼져서, 차에 타는 순간 기분이 확 좋아집니다.",
                image_path=str(assets / "car_diffuser.png"),
                coupang_url="https://www.coupang.com/vp/products/8680115623?itemId=25183113443&vendorItemId=91885198654&lptag=AF7086198"
            ),
            ProductItem(
                item_id="car_waterless",
                title="카렉스 스마트 워터리스 카워시 750ml",
                header_badge="물없이 세차 카워시",
                discount="39% 할인",
                price="4,200원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 4,353)",
                card_badge_right="[프로필 02번 링크]",
                caption1="물 없이 뿌리고 닦으면 끝!",
                caption2="세차장 줄 설 일 없어져요",
                voice_script="두 번째는 카렉스 스마트 워터리스 카워시입니다. 물 없이 뿌리고 닦기만 하면 오염 제거부터 광택까지 한 번에 끝나서, 아파트 주차장에서도 세차가 됩니다.",
                image_path=str(assets / "car_waterless.png"),
                coupang_url="https://www.coupang.com/vp/products/96100031?itemId=21817928152&vendorItemId=3728392925&lptag=AF7086198"
            ),
            ProductItem(
                item_id="car_wax",
                title="불스원 하이브리드 물왁스 600ml",
                header_badge="불스원 하이브리드 왁스",
                discount="베스트상품",
                price="5,540원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 9,534)",
                card_badge_right="[프로필 03번 링크]",
                caption1="물 묻은 차에 뿌리고 닦으면 광택",
                caption2="왁스칠 한 번에 비 오염까지",
                voice_script="세 번째는 불스원 하이브리드 물왁스입니다. 물 묻은 차에 그대로 뿌리고 닦기만 해도 광택이 올라와서, 왁스칠 한 번으로 한 달은 반짝입니다.",
                image_path=str(assets / "car_wax.png"),
                coupang_url="https://www.coupang.com/vp/products/209472308?itemId=21352632856&vendorItemId=89833893802&lptag=AF7086198"
            )
        ]
    },

    "cleaning": {
        "theme_name": "청소 끝판왕",
        "hook_title": "청소 30분을 10분으로\n청소 꿀템 TOP 3!",
        "hook_voice": "청소할 때 아직도 허리 숙여서 걸레질하시나요? 밀대 하나로 바닥부터 먼지까지 끝내는, 쿠팡 청소 꿀템 탑 쓰리입니다!",
        "hook_caption1": "청소하다 허리 아프셨죠?",
        "hook_caption2": "집안일 절반 줄여주는 청소 꿀템 3가지!",
        "hook_image": str(assets / "cleaning_mop.png"),
        "hashtags": ["#청소꿀템", "#청소용품", "#자취청소", "#쿠팡추천", "#살림꿀템"],
        "products": [
            ProductItem(
                item_id="cleaning_mop",
                title="코멧 스프레이 밀대걸레 + 극세사 패드 5개 + 다용도 클리너 1개",
                header_badge="코멧 스프레이 밀대걸레",
                discount="67% 할인",
                price="10,310원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 41,964)",
                card_badge_right="[프로필 01번 링크]",
                caption1="물통 없이 분사하며 한 번에!",
                caption2="극세사 패드 5장 + 클리너 포함",
                voice_script="첫 번째는 코멧 스프레이 밀대걸레입니다. 손잡이를 당기면 물이 슥 나와서 물통 들고 다닐 필요 없이 바닥을 한 번에 닦을 수 있어요.",
                image_path=str(assets / "cleaning_mop.png"),
                coupang_url="https://www.coupang.com/vp/products/6113657232?itemId=11538728285&vendorItemId=78813769516&lptag=AF7086198"
            ),
            ProductItem(
                item_id="cleaning_magicblock",
                title="코멧 매직블럭 중형 100개 + 집게핀 1개, 1세트",
                header_badge="코멧 매직블럭 100개입",
                discount="56% 할인",
                price="5,980원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 6,817)",
                card_badge_right="[프로필 02번 링크]",
                caption1="찌든 때는 물만 묻혀 쓱쓱!",
                caption2="100개 들이라 1년 내내 넉넉",
                voice_script="두 번째는 코멧 매직블럭 백 개 들이입니다. 물만 묻혀서 문틈이나 싱크대 찌든 때를 문지르면 새것처럼 지워져요.",
                image_path=str(assets / "cleaning_magicblock.png"),
                coupang_url="https://www.coupang.com/vp/products/7790158804?itemId=3987560154&vendorItemId=71971864635&lptag=AF7086198"
            ),
            ProductItem(
                item_id="cleaning_duster",
                title="코멧 홈 길이조절 롱 먼지털이개, 혼합색상, 1개",
                header_badge="길이조절 롱 먼지털이개",
                discount="43% 할인",
                price="5,110원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 4,732)",
                card_badge_right="[프로필 03번 링크]",
                caption1="천장·몰딩 먼지까지 손 닿게!",
                caption2="길이조절 + 구부러지는 헤드",
                voice_script="세 번째는 길이조절 롱 먼지털이개입니다. 길게 늘려서 천장 몰딩이나 에어컨 위 먼지를 안전하게 털어낼 수 있어요.",
                image_path=str(assets / "cleaning_duster.png"),
                coupang_url="https://www.coupang.com/vp/products/6994008705?itemId=17126820181&vendorItemId=84300028449&lptag=AF7086198"
            )
        ]
    },

    "winter": {
        "theme_name": "한파 방한 필수템",
        "hook_title": "출근길 한파 막아주는\n겨울 방한 꿀템 TOP 3!",
        "hook_voice": "아침 출근길 칼바람에 손 시리고 목 시리셨죠? 손과 목, 손끝까지 따뜻하게 막아주는 쿠팡 방한 꿀템 탑 쓰리입니다!",
        "hook_caption1": "출근길 칼바람, 그냥 나가셨죠?",
        "hook_caption2": "손·목·손끝 완벽 방한 꿀템 3가지!",
        "hook_image": str(assets / "winter_handwarmer.png"),
        "hashtags": ["#겨울필수템", "#방한용품", "#손난로", "#넥워머", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="winter_handwarmer",
                title="티엘팩토리 충전식 손난로 보조배터리 5000mAh, 플랫블랙",
                header_badge="충전식 손난로 보조배터리",
                discount="54% 할인",
                price="11,200원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 5,347)",
                card_badge_right="[프로필 01번 링크]",
                caption1="전원만 켜면 금방 따뜻!",
                caption2="핸드폰 충전까지 되는 1석 2조",
                voice_script="첫 번째는 티엘팩토리 충전식 손난로입니다. 전원만 켜면 금방 따뜻해지고 핸드폰 충전까지 되는 보조배터리라 겨울 내내 들고 다니게 돼요.",
                image_path=str(assets / "winter_handwarmer.png"),
                coupang_url="https://www.coupang.com/vp/products/6130716221?itemId=11689247307&vendorItemId=87188180201&lptag=AF7086198"
            ),
            ProductItem(
                item_id="winter_neckwarmer",
                title="캐럿 이지 넥워머, 블랙, Free",
                header_badge="캐럿 이지 넥워머",
                discount="54% 할인",
                price="5,000원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 5,197)",
                card_badge_right="[프로필 02번 링크]",
                caption1="목만 감싸도 체감 온도 쑥!",
                caption2="목도리보다 편한 보들 기모",
                voice_script="두 번째는 캐럿 이지 넥워머입니다. 목만 감싸도 온몸이 따뜻해지고, 목도리처럼 풀리거나 흘러내릴 일이 없어서 출근길에 딱이에요.",
                image_path=str(assets / "winter_neckwarmer.png"),
                coupang_url="https://www.coupang.com/vp/products/2145302183?itemId=3642726396&vendorItemId=71628248629&lptag=AF7086198"
            ),
            ProductItem(
                item_id="winter_gloves",
                title="이츠굿텐 보온 플러스 기모 방한 장갑, Black, M",
                header_badge="기모 스마트터치 장갑",
                discount="65% 할인",
                price="4,490원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 7,102)",
                card_badge_right="[프로필 03번 링크]",
                caption1="장갑 끼고도 폰 터치 쏙!",
                caption2="안감 기모라 손끝까지 따뜻",
                voice_script="세 번째는 이츠굿텐 기모 방한 장갑입니다. 안쪽이 기모라 손끝까지 따뜻하고, 장갑을 낀 채로 스마트폰 터치가 돼서 겨울에도 편해요.",
                image_path=str(assets / "winter_gloves.png"),
                coupang_url="https://www.coupang.com/vp/products/9247026267?itemId=20571923542&vendorItemId=87647349184&lptag=AF7086198"
            )
        ]
    },

    "laundry": {
        "theme_name": "세탁·의류관리 끝판왕",
        "hook_title": "니트 보풀부터 셔츠 구김까지\n세탁·의류관리 꿀템 TOP 3!",
        "hook_voice": "겨울 니트 보풀에 셔츠 구김, 실내 빨래까지 아직도 그냥 참고 계셨나요? 옷장 관리가 확 쉬워지는 쿠팡 세탁·의류관리 꿀템 탑 쓰리입니다!",
        "hook_caption1": "니트 보풀, 그냥 입고 다니셨죠?",
        "hook_caption2": "옷장 관리 확 쉬워지는 꿀템 3가지!",
        "hook_image": str(assets / "laundry_lint.png"),
        "hashtags": ["#의류관리", "#보풀제거기", "#스팀다리미", "#빨래건조대", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="laundry_lint",
                title="필립스 보풀제거기, GC-026, 블루",
                header_badge="필립스 보풀제거기",
                discount="57% 할인",
                price="10,610원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 42,139)",
                card_badge_right="[프로필 01번 링크]",
                caption1="니트·코트 보풀 3초 만에 싹!",
                caption2="후기 4만 개 넘은 필립스 정품",
                voice_script="첫 번째는 필립스 보풀제거기입니다. 니트나 코트에 올라온 보풀도 문지르면 삼 초 만에 싹 사라져서, 비싼 옷도 새것처럼 되살아납니다.",
                image_path=str(assets / "laundry_lint.png"),
                coupang_url="https://www.coupang.com/vp/products/4947594003?itemId=6529631478&vendorItemId=91289787989&lptag=AF7086198"
            ),
            ProductItem(
                item_id="laundry_steamer",
                title="홈플래닛 핸디형 스탠드 스팀다리미, MW-801",
                header_badge="핸디형 스팀다리미",
                discount="54% 할인",
                price="26,990원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 52,935)",
                card_badge_right="[프로필 02번 링크]",
                caption1="옷걸이에 건 채로 구김 1분 컷!",
                caption2="다림판 없이도 셔츠가 쫙 펴져요",
                voice_script="두 번째는 홈플래닛 핸디형 스탠드 스팀다리미입니다. 옷걸이에 걸어둔 채로 쓱쓱 켜기만 하면 셔츠 구김이 일 분 만에 펴져서, 아침 출근 준비가 훨씬 빨라져요.",
                image_path=str(assets / "laundry_steamer.png"),
                coupang_url="https://www.coupang.com/vp/products/310080038?itemId=977484067&vendorItemId=5392665218&lptag=AF7086198"
            ),
            ProductItem(
                item_id="laundry_rack",
                title="코멧 홈 접이식 대형 빨래건조대, 그레이, 1개",
                header_badge="접이식 대형 건조대",
                discount="33% 할인",
                price="15,930원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 22,477)",
                card_badge_right="[프로필 03번 링크]",
                caption1="실내건조 빨래도 하루면 뽀송!",
                caption2="안 쓸 땐 접어서 틈새 수납",
                voice_script="세 번째는 코멧 홈 접이식 대형 빨래건조대입니다. 빨래를 넓게 펼 수 있어서 실내에서도 하루면 뽀송하게 마르고, 안 쓸 때는 접어서 틈새에 세워둘 수 있어요.",
                image_path=str(assets / "laundry_rack.png"),
                coupang_url="https://www.coupang.com/vp/products/7180955044?itemId=18110930549&vendorItemId=85262569120&lptag=AF7086198"
            )
        ]
    },

    "sleep": {
        "theme_name": "숙면 부르는 침실 꿀템",
        "hook_title": "뒤척이다 새벽 3시\n숙면 부르는 침실 꿀템 TOP 3!",
        "hook_voice": "누웠는데 자꾸 뒤척이고 새벽에 자꾸 깨시죠? 목부터 빛까지 잠을 방해하는 것들을 한 번에 잡아주는 쿠팡 숙면 꿀템 탑 쓰리입니다!",
        "hook_caption1": "누우면 뒤척이고 새벽에 깨시죠?",
        "hook_caption2": "잠을 부르는 침실 꿀템 3가지!",
        "hook_image": str(assets / "sleep_pillow.png"),
        "hashtags": ["#숙면꿀템", "#경추베개", "#암막커튼", "#수면안대", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="sleep_pillow",
                title="코멧 홈 메모리폼 경추베개, 그레이, 1개",
                header_badge="메모리폼 경추베개",
                discount="54% 할인",
                price="8,990원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 25,580)",
                card_badge_right="[프로필 01번 링크]",
                caption1="목이 안 꺾이는 높이 그대로!",
                caption2="메모리폼이 목·어깨를 받쳐줘요",
                voice_script="첫 번째는 코멧 홈 메모리폼 경추베개입니다. 목이 꺾이지 않는 높이로 어깨까지 받쳐줘서, 아침마다 목이 뻐근했던 분들이 특히 좋아하는 베개예요.",
                image_path=str(assets / "sleep_pillow.png"),
                coupang_url="https://www.coupang.com/vp/products/5314973223?itemId=20129056696&vendorItemId=87223184831&lptag=AF7086198"
            ),
            ProductItem(
                item_id="sleep_curtain",
                title="코멧 홈 단열 아일렛 암막 커튼, 차콜 그레이, 135x170cm, 1장",
                header_badge="단열 암막커튼",
                discount="59% 할인",
                price="7,990원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 81,312)",
                card_badge_right="[프로필 02번 링크]",
                caption1="가로등 빛 완벽 차단, 낮잠도 꿀잠!",
                caption2="후기 8만 개 넘은 스테디셀러",
                voice_script="두 번째는 코멧 홈 단열 암막커튼입니다. 가로등이나 아침 햇살을 확 막아줘서 방이 완전히 어두워지고, 단열까지 돼서 겨울에도 덜 추워요.",
                image_path=str(assets / "sleep_curtain.png"),
                coupang_url="https://www.coupang.com/vp/products/180352941?itemId=536034204&vendorItemId=84147368736&lptag=AF7086198"
            ),
            ProductItem(
                item_id="sleep_mask",
                title="닥터김강 입체 4D 수면안대, 블랙, FREE",
                header_badge="입체 4D 수면안대",
                discount="19% 할인",
                price="7,900원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 12,645)",
                card_badge_right="[프로필 03번 링크]",
                caption1="눈 안 눌리는 입체형, 빛 차단 끝!",
                caption2="낮잠·여행·비행기 필수템",
                voice_script="세 번째는 닥터김강 입체 4D 수면안대입니다. 눈을 누르지 않는 입체형이라 속눈썹 하나 안 눌리고 빛은 완벽하게 막아줘서, 낮잠이나 여행 갈 때 특히 좋아요.",
                image_path=str(assets / "sleep_mask.png"),
                coupang_url="https://www.coupang.com/vp/products/7709524347?itemId=20662396489&vendorItemId=87735082174&lptag=AF7086198"
            )
        ]
    },

    "homecafe": {
        "theme_name": "홈카페·커피",
        "hook_title": "카페 커피값 아끼는\n홈카페 꿀템 TOP 3!",
        "hook_voice": "커피 한 잔에 오천 원씩, 한 달이면 십오만 원이 그냥 나가고 있죠? 원두 갈고 내리고 라떼까지 집에서 되는, 쿠팡 홈카페 꿀템 탑 쓰리입니다!",
        "hook_caption1": "하루 커피 두 잔, 한 달 15만 원이었다면?",
        "hook_caption2": "집이 카페 되는 홈카페 꿀템 3가지!",
        "hook_image": str(assets / "homecafe_grinder.png"),
        "hashtags": ["#홈카페", "#커피꿀템", "#전동커피그라인더", "#핸드드립", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="homecafe_grinder",
                title="위즈웰 아로마 커피그라인더, WSG-9900",
                header_badge="위즈웰 아로마 그라인더",
                discount="46% 할인",
                price="26,510원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 2,579)",
                card_badge_right="[프로필 01번 링크]",
                caption1="다이얼 하나로 분쇄도 세밀 조절!",
                caption2="한 달 2,000명 넘게 찾은 그라인더",
                voice_script="첫 번째는 위즈웰 아로마 커피그라인더입니다. 다이얼 하나로 분쇄도를 세밀하게 맞출 수 있어서, 드립부터 모카포트까지 원두를 그때그때 갈아 쓸 수 있어요.",
                image_path=str(assets / "homecafe_grinder.png"),
                coupang_url="https://www.coupang.com/vp/products/8472321870?itemId=24514067572&vendorItemId=91646025652&lptag=AF7086198"
            ),
            ProductItem(
                item_id="homecafe_dripper",
                title="빈플러스 에센셜 웨이브 글라스 핸드드립 커피 4종 세트",
                header_badge="핸드드립 4종 세트",
                discount="54% 할인",
                price="20,230원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 538)",
                card_badge_right="[프로필 02번 링크]",
                caption1="드리퍼·서버·여과지 한 번에!",
                caption2="따로 살 것 없이 5분이면 카페 한 잔",
                voice_script="두 번째는 빈플러스 핸드드립 4종 세트입니다. 드리퍼에 서버, 여과지에 계량스푼까지 다 들어 있어서, 처음 시작해도 따로 살 게 없어요.",
                image_path=str(assets / "homecafe_dripper.png"),
                coupang_url="https://www.coupang.com/vp/products/7829994107?itemId=21293548886&vendorItemId=88353399812&lptag=AF7086198"
            ),
            ProductItem(
                item_id="homecafe_frother",
                title="홈플래닛 핸디형 전동 우유거품기",
                header_badge="핸디형 전동 우유거품기",
                discount="50% 할인",
                price="6,420원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 4,654)",
                card_badge_right="[프로필 03번 링크]",
                caption1="우유 10초면 카페 라떼 완성!",
                caption2="한 달 3,000명이 담아간 템",
                voice_script="세 번째는 홈플래닛 전동 우유거품기입니다. 우유에 대고 십 초만 돌리면 거품이 폭신하게 올라와서, 집에서도 카페 라떼가 그대로 나옵니다.",
                image_path=str(assets / "homecafe_frother.png"),
                coupang_url="https://www.coupang.com/vp/products/7216511597?itemId=18276628727&vendorItemId=85422689306&lptag=AF7086198"
            )
        ]
    },

    "workout": {
        "theme_name": "홈트·실내운동",
        "hook_title": "헬스장 등록비 아끼는\n홈트 꿀템 TOP 3!",
        "hook_voice": "추워져서 헬스장 갈 엄두도 안 나시죠? 거실 한 평이면 충분한, 쿠팡 홈트 꿀템 탑 쓰리입니다!",
        "hook_caption1": "헬스장 등록비, 이젠 안 내도 돼요",
        "hook_caption2": "거실이 헬스장 되는 홈트 꿀템 3가지!",
        "hook_image": str(assets / "workout_mat.png"),
        "hashtags": ["#홈트", "#홈트레이닝", "#요가매트", "#폼롤러", "#쿠팡추천"],
        "products": [
            ProductItem(
                item_id="workout_mat",
                title="코멧 스포츠 NBR 요가매트 20mm, 네이비",
                header_badge="20mm 두꺼운 요가매트",
                discount="50% 할인",
                price="15,090원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 18,205)",
                card_badge_right="[프로필 01번 링크]",
                caption1="무릎·팔꿈치 하나도 안 아프게!",
                caption2="층간소음까지 잡는 20mm 두께",
                voice_script="첫 번째는 코멧 스포츠 20밀리 요가매트입니다. 두께가 이십 밀리라 무릎 꿇고 해도 하나도 안 아프고, 층간소음도 확 줄어들어요.",
                image_path=str(assets / "workout_mat.png"),
                coupang_url="https://www.coupang.com/vp/products/4888844473?itemId=6370601435&vendorItemId=73665788078&lptag=AF7086198"
            ),
            ProductItem(
                item_id="workout_roller",
                title="트라택 EPP 폼롤러 + 운동법 매뉴얼, 블랙",
                header_badge="트라택 EPP 폼롤러",
                discount="60% 할인",
                price="14,210원",
                tag="로켓배송",
                card_badge_left="★ 5.0 (후기 6,514)",
                card_badge_right="[프로필 02번 링크]",
                caption1="운동 후 뭉친 근육 5분 정리",
                caption2="운동법 매뉴얼까지 같이 와요",
                voice_script="두 번째는 트라택 EPP 폼롤러입니다. 단단해서 종아리나 등 뭉친 곳을 눌러주면 오 분 만에 확 풀리고, 운동법 매뉴얼이 같이 와서 처음 써도 헤매지 않아요.",
                image_path=str(assets / "workout_roller.png"),
                coupang_url="https://www.coupang.com/vp/products/45079633?itemId=17426798113&vendorItemId=3380243063&lptag=AF7086198"
            ),
            ProductItem(
                item_id="workout_band",
                title="코멧 스포츠 라텍스 루프밴드 5종 세트",
                header_badge="5단계 라텍스 루프밴드",
                discount="41% 할인",
                price="6,690원",
                tag="로켓배송",
                card_badge_left="★ 4.5 (후기 19,297)",
                card_badge_right="[프로필 03번 링크]",
                caption1="강도 5단계라 하체 자극 확실!",
                caption2="만 원도 안 해서 홈트 세트 완성",
                voice_script="세 번째는 코멧 스포츠 라텍스 루프밴드 오 종 세트입니다. 강도가 다섯 단계라 스쿼트부터 힙업까지 골라 쓰면 되고, 만 원도 안 해서 홈트 세트가 이걸로 완성됩니다.",
                image_path=str(assets / "workout_band.png"),
                coupang_url="https://www.coupang.com/vp/products/306146810?itemId=965291522&vendorItemId=5369727509&lptag=AF7086198"
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

