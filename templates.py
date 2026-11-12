from models import ShortsScript, Slide
import config


def get_preset_scripts() -> list[ShortsScript]:
    assets = config.ASSETS_DIR

    p1_preview = [
        {"badge": "BEST 01", "title": "핸디 청소기", "price": "27,990원", "image_path": str(assets / "real_vacuum.png")},
        {"badge": "BEST 02", "title": "규조토 발매트", "price": "8,090원", "image_path": str(assets / "real_mat.png")},
        {"badge": "BEST 03", "title": "센서 휴지통", "price": "12,990원", "image_path": str(assets / "real_trashcan.png")}
    ]

    return [
        # 프리셋 1: 자취생 삶의 질 수직상승 꿀템 TOP 3
        ShortsScript(
            topic="자취생 삶의 질 떡상 쿠팡 꿀템 TOP 3",
            youtube_title="아직도 이거 모르고 산다고? 자취생 삶의 질 수직상승 쿠팡 꿀템 TOP 3 #shorts",
            youtube_description=(
                "자취할 때 진짜 돈 안 아까운 쿠팡 필수템 TOP 3!\n"
                "📌 영상에 나온 제품 최저가 정보는 채널 프로필 링크에 남겨뒀습니다!\n\n"
                "#쿠팡꿀템 #자취꿀템 #삶의질상승 #쿠팡추천 #내돈내산 #가성비템"
            ),
            hashtags=["#쿠팡꿀템", "#자취꿀템", "#삶의질상승", "#쿠팡추천", "#가성비템"],
            slides=[
                Slide(
                    step_name="HOOK",
                    step_index=1,
                    total_steps=5,
                    header_badge="🚨 광고 0% · 솔직 가성비 검증",
                    main_title="아직도 이거 모르고 산다고?\n자취 삶의 질 떡상 TOP 3!",
                    discount_badge="실구매 1위",
                    price_badge="놓치면 후회하는 꿀템",
                    tag_badge="가성비 끝판왕",
                    card_badge_left="★ 만족도 1위",
                    card_badge_right="자취생 강력추천",
                    caption_line1="아직도 이거 모르고 사셨나요?",
                    caption_line2="자취 3년 차가 꼽은 찐 꿀템 3가지!",
                    voice_script="아직도 이거 모르고 사셨나요? 자취 3년 차가 꼽은, 쿠팡에서 안 사면 진짜 손해인 삶의 질 떡상템 탑 3입니다!",
                    image_path=str(assets / "hook.png"),
                    preview_items=p1_preview
                ),
                Slide(
                    step_name="ITEM_1",
                    step_index=2,
                    total_steps=5,
                    header_badge="BEST 01 · 자취생 필수템",
                    main_title="홈플래닛 무선 핸디 청소기",
                    discount_badge="특가할인",
                    price_badge="27,990원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.8 (후기 4만+)",
                    card_badge_right="[프로필 01번 링크]",
                    caption_line1="머리카락·먼지 흡입 끝판왕!",
                    caption_line2="원룸·차량 청소 3초 컷",
                    voice_script="첫 번째는 홈플래닛 무선 핸디 청소기입니다. 책상 위 먼지나 머리카락 치울 때 무거운 청소기 꺼낼 필요 없이 삼초 만에 싹 정리돼요.",
                    image_path=str(assets / "real_vacuum.png")
                ),
                Slide(
                    step_name="ITEM_2",
                    step_index=3,
                    total_steps=5,
                    header_badge="BEST 02 · 빠른건조 발매트",
                    main_title="코멧 홈 빨아쓰는 규조토 발매트",
                    discount_badge="특가할인",
                    price_badge="8,090원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.8 (후기 8만+)",
                    card_badge_right="[프로필 02번 링크]",
                    caption_line1="물기 3초 만에 싹 마름!",
                    caption_line2="세탁기로 빨아쓰는 소프트 매트",
                    voice_script="두 번째는 코멧 홈 빨아쓰는 규조토 발매트입니다. 젖은 발 올리자마자 물기를 싹 흡수하고 세탁기에도 바로 돌릴 수 있어서 천 매트 빨래 걱정이 영원히 사라집니다.",
                    image_path=str(assets / "real_mat.png")
                ),
                Slide(
                    step_name="ITEM_3",
                    step_index=4,
                    total_steps=5,
                    header_badge="BEST 03 · 자동 센서 휴지통",
                    main_title="코멧 모션인식 센서 휴지통 10L",
                    discount_badge="특가할인",
                    price_badge="12,990원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.8 (후기 2만+)",
                    card_badge_right="[프로필 03번 링크]",
                    caption_line1="손 안 대고 버리는 자동 오픈!",
                    caption_line2="원룸 냄새·벌레 완벽 차단",
                    voice_script="세 번째는 코멧 모션인식 센서 휴지통입니다. 손만 갖다 대면 알아서 열리고 닫혀서 냄새랑 벌레까지 완벽하게 차단해 줘요.",
                    image_path=str(assets / "real_trashcan.png")
                ),
                Slide(
                    step_name="OUTRO",
                    step_index=5,
                    total_steps=5,
                    header_badge="📌 영상 속 최저가 구매 안내",
                    main_title="영상 속 꿀템 3가지 링크는?\n채널 프로필 링크에 있어요!",
                    discount_badge="한정수량",
                    price_badge="로켓배송 특가 진행 중",
                    tag_badge="바로가기",
                    card_badge_left="★ 최저가 보장",
                    card_badge_right="쿠팡 로켓배송",
                    caption_line1="오늘 소개한 제품 최저가 링크는",
                    caption_line2="채널 프로필 링크에 남겨뒀어요!",
                    voice_script="오늘 소개해 드린 세 가지 제품 최저가 정보는 채널 프로필 링크에 남겨둘게요. 구독과 좋아요 누르고 알뜰 꿀템 놓치지 마세요!",
                    image_path=str(assets / "outro.png"),
                    preview_items=p1_preview
                )
            ]
        ),

        # 프리셋 2: 주방 살림 혁명 쿠팡 꿀템 TOP 3
        ShortsScript(
            topic="주방 살림 혁명 쿠팡 꿀템 TOP 3",
            youtube_title="주방 일 절반으로 줄여주는 주방 살림 혁명 쿠팡 꿀템 TOP 3 #shorts",
            youtube_description=(
                "요리와 주방 청소가 10배 편해지는 쿠팡 꿀템 TOP 3!\n"
                "📌 최저가 구매 링크는 채널 프로필을 확인해주세요!\n\n"
                "#주방용품 #살림꿀템 #쿠팡추천 #요리필수템 #가성비주방템"
            ),
            hashtags=["#주방용품", "#살림꿀템", "#쿠팡추천", "#요리필수템", "#가성비주방템"],
            slides=[
                Slide(
                    step_name="HOOK",
                    step_index=1,
                    total_steps=5,
                    header_badge="주방 살림 혁명",
                    main_title="요리시간 반으로 줄여주는\n주방 꿀템 TOP 3!",
                    discount_badge="주부 1위",
                    price_badge="신세계 열리는 주방템",
                    tag_badge="강력추천",
                    card_badge_left="★ 만족도 99%",
                    card_badge_right="주방 베스트",
                    caption_line1="주방 일 힘드셨죠?",
                    caption_line2="살림 고수들이 숨겨둔 찐 꿀템 3가지!",
                    voice_script="주방 일 아직도 손으로 힘들게 하시나요? 살림 고수들이 입을 모아 극찬한, 요리 시간 반으로 줄여주는 주방 꿀템 탑 3입니다!",
                    image_path=str(assets / "kitchen_hook.png")
                ),
                Slide(
                    step_name="ITEM_1",
                    step_index=2,
                    total_steps=5,
                    header_badge="BEST 01 · 원터치 자동 오프너",
                    main_title="전동 원터치 자동 오프너",
                    discount_badge="30% 특가",
                    price_badge="15,900원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.9 (후기 2,300개)",
                    card_badge_right="손목지킴이",
                    caption_line1="버튼 하나로 뚜껑 자동 오픈!",
                    caption_line2="단단한 캔·병뚜껑 2초 컷",
                    voice_script="첫 번째는 전동 원터치 자동 오프너입니다. 꽉 닫힌 잼 병이나 와인도 버튼 한 번만 누르면 힘들이지 않고 2초 만에 쏙 열립니다.",
                    image_path=str(assets / "kitchen_opener.png")
                ),
                Slide(
                    step_name="ITEM_2",
                    step_index=3,
                    total_steps=5,
                    header_badge="BEST 02 · 실리콘 배수구 거름망",
                    main_title="항균 실리콘 배수구 커버",
                    discount_badge="25% 특가",
                    price_badge="8,900원",
                    tag_badge="1+1 세트",
                    card_badge_left="★ 4.8 (후기 5,100개)",
                    card_badge_right="냄새·날파리 차단",
                    caption_line1="음식물 찌꺼기 쏙 버리기!",
                    caption_line2="싱크대 냄새·물때 걱정 제로",
                    voice_script="두 번째는 항균 실리콘 배수구 커버입니다. 뒤집어서 툭 털어내면 음식물 쓰레기가 싹 떨어져서 손에 더러운 물 묻힐 필요가 없어요.",
                    image_path=str(assets / "kitchen_drain.png")
                ),
                Slide(
                    step_name="ITEM_3",
                    step_index=4,
                    total_steps=5,
                    header_badge="BEST 03 · 스테인리스 기름방패",
                    main_title="기름 튐 방지 미세망 커버",
                    discount_badge="32% 특가",
                    price_badge="12,500원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.9 (후기 3,800개)",
                    card_badge_right="청소시간 단축",
                    caption_line1="삼겹살 구워도 기름 안 튐!",
                    caption_line2="가스레인지 청소 탈출",
                    voice_script="세 번째는 기름 튐 방지 미세망입니다. 고기나 튀김 요리할 때 덮어두기만 하면 수증기는 빠지고 기름만 완벽하게 막아줘서 청소가 끝납니다.",
                    image_path=str(assets / "kitchen_screen.png")
                ),
                Slide(
                    step_name="OUTRO",
                    step_index=5,
                    total_steps=5,
                    header_badge="제품 최저가 구매 안내",
                    main_title="채널 프로필 링크 확인!",
                    discount_badge="한정수량",
                    price_badge="로켓배송 특가 진행 중",
                    tag_badge="바로가기",
                    card_badge_left="★ 최저가 보장",
                    card_badge_right="쿠팡 로켓배송",
                    caption_line1="오늘 소개한 제품 최저가 링크는",
                    caption_line2="채널 프로필 링크에 남겨뒀어요!",
                    voice_script="오늘 소개해 드린 주방 꿀템 최저가 정보는 채널 프로필 링크에 남겨둘게요. 구독 누르고 삶의 질 올라가는 꿀템 챙겨가세요!",
                    image_path=str(assets / "outro.png")
                )
            ]
        ),

        # 프리셋 3: 직장인 책상 데스크테리어 꿀템 TOP 3
        ShortsScript(
            topic="직장인 데스크테리어 생산성 꿀템 TOP 3",
            youtube_title="책상 위에 이거 하나 뒀더니 업무 효율 2배? 직장인 데스크테리어 꿀템 TOP 3 #shorts",
            youtube_description=(
                "칼퇴를 부르는 책상 위 필수 생산성 꿀템 TOP 3!\n"
                "📌 최저가 구매 링크는 채널 프로필 링크에 있습니다!\n\n"
                "#데스크테리어 #직장인꿀템 #재택근무 #책상꾸미기 #생산성템 #쿠팡추천"
            ),
            hashtags=["#데스크테리어", "#직장인꿀템", "#재택근무", "#책상꾸미기", "#쿠팡추천"],
            slides=[
                Slide(
                    step_name="HOOK",
                    step_index=1,
                    total_steps=5,
                    header_badge="생산성 떡상템",
                    main_title="칼퇴 부르는 책상 위\n데스크테리어 꿀템 TOP 3!",
                    discount_badge="직장인 1위",
                    price_badge="내돈내산 인생템",
                    tag_badge="업무효율 2배",
                    card_badge_left="★ 만족도 98%",
                    card_badge_right="칼퇴보장",
                    caption_line1="책상 위 아직도 지저분한가요?",
                    caption_line2="일잘러들이 쓰는 데스크테리어 꿀템 3가지!",
                    voice_script="책상 위 아직도 어수선하신가요? 일잘러들이 책상 위에 꼭 올려두는 업무 효율 두 배 높여주는 데스크테리어 꿀템 탑 3입니다!",
                    image_path=str(assets / "desk_hook.png")
                ),
                Slide(
                    step_name="ITEM_1",
                    step_index=2,
                    total_steps=5,
                    header_badge="BEST 01 · 3in1 맥세이프 충전기",
                    main_title="접이식 3in1 무선충전기",
                    discount_badge="38% 특가",
                    price_badge="28,900원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.9 (후기 4,800개)",
                    card_badge_right="선 정리 종결",
                    caption_line1="폰·워치·이어폰 동시 고속충전!",
                    caption_line2="지저분한 충전선 한 번에 정리",
                    voice_script="첫 번째는 접이식 3in1 맥세이프 무선충전기입니다. 스마트폰, 워치, 무선이어폰까지 선 하나로 동시 충전돼서 책상이 정말 깔끔해집니다.",
                    image_path=str(assets / "desk_charger.png")
                ),
                Slide(
                    step_name="ITEM_2",
                    step_index=3,
                    total_steps=5,
                    header_badge="BEST 02 · 모니터 스크린바 조명",
                    main_title="시력보호 모니터 조명바",
                    discount_badge="32% 특가",
                    price_badge="24,900원",
                    tag_badge="눈피로 제로",
                    card_badge_left="★ 4.8 (후기 6,200개)",
                    card_badge_right="야근 필수템",
                    caption_line1="화면 반사 없이 책상만 밝게!",
                    caption_line2="장시간 모니터 봐도 눈 안 아픔",
                    voice_script="두 번째는 시력보호 모니터 조명바입니다. 모니터 위에 얹기만 하면 화면 반사 없이 책상 위만 부드럽게 비춰줘서 눈의 피로가 싹 사라집니다.",
                    image_path=str(assets / "desk_lightbar.png")
                ),
                Slide(
                    step_name="ITEM_3",
                    step_index=4,
                    total_steps=5,
                    header_badge="BEST 03 · 인체공학 버티컬 마우스",
                    main_title="무소음 인체공학 버티컬마우스",
                    discount_badge="40% 특가",
                    price_badge="19,800원",
                    tag_badge="로켓배송",
                    card_badge_left="★ 4.9 (후기 5,900개)",
                    card_badge_right="손목통증 탈출",
                    caption_line1="손목 꺾임 없는 편안한 각도!",
                    caption_line2="딸깍 소리 없는 도서관급 무소음",
                    voice_script="세 번째는 무소음 인체공학 버티컬 마우스입니다. 악수하듯 편안하게 쥐는 각도로 손목 통증을 없애주고 도서관에서도 쓸 수 있는 무소음 클릭이에요.",
                    image_path=str(assets / "desk_mouse.png")
                ),
                Slide(
                    step_name="OUTRO",
                    step_index=5,
                    total_steps=5,
                    header_badge="제품 최저가 구매 안내",
                    main_title="채널 프로필 링크 확인!",
                    discount_badge="한정수량",
                    price_badge="로켓배송 특가 진행 중",
                    tag_badge="바로가기",
                    card_badge_left="★ 최저가 보장",
                    card_badge_right="쿠팡 로켓배송",
                    caption_line1="오늘 소개한 제품 최저가 링크는",
                    caption_line2="채널 프로필 링크에 남겨뒀어요!",
                    voice_script="오늘 소개해 드린 데스크테리어 꿀템 최저가 정보는 채널 프로필 링크에 남겨둘게요. 구독 누르고 알짜 꿀템 매일 받아보세요!",
                    image_path=str(assets / "outro.png")
                )
            ]
        )
    ]
