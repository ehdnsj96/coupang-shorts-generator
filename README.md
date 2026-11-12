# 🧪 돈값연구소 (@dongap_lab) - 쿠팡 파트너스 유튜브 쇼츠 완전 무인 자동화 파이프라인

"이건 진짜 돈값 한다!" 싶은 알짜배기 쿠팡 꿀템을 **하루 3회(08시·12시·18시) 자동으로 영상화하고, 모바일 최저가 검색 페이지와 텔레그램 채널까지 100% 무인 연동**하는 올인원 시스템입니다.

---

## 🌟 핵심 기능

1. **화사한 화이트 인테리어 룸 클린 디자인 & 어린이 똑부러진 보이스**
   - 햇살 비치는 화이트 룸 배경 + 실물 쿠팡 1위 제품 중앙 포커스
   - 낭랑하고 똑부러진 어린이 보이스(선희 +25Hz)로 0.1초 만에 시선 집중
   - 쿠팡 시그니처 3단 특가 뱃지 (`로켓배송 🚀` + `실시간 가격` + `★ 4.8 평점`)
   - 💡 체크포인트 3종 스펙 카드 + 방송용 두꺼운 볼드 외곽선 자막

2. **하루 3회 골든 타임 슬롯 자동 데몬 (`auto_daily.py --daemon`)**
   - 08:00 (출근길 피크), 12:00 (점심시간 피크), 18:00 (퇴근·저녁 피크) 자동 순환
   - 테마 자동 전환: 자취·리빙 ➔ 주방·살림 ➔ 식비·간편식 ➔ 데스크테리어
   - 영상 렌더링 즉시 **모바일 누적 검색 도감 갱신(GitHub Pages)** 및 **텔레그램 채널(@ym_hotdeal) 자동 전송**

3. **쿠팡 상품 원클릭 자동 수집기 (`product_collector.py`)**
   - 상품 대표 이미지를 웹/CDN에서 자동으로 다운로드하고 640x640 정방형 캔버스로 자동 최적화
   - 대사(voice_script), 체크포인트, 뱃지, 태그 자동 생성
   - `custom_products.json`에 저장되어 데일리 러너에 즉시 자동 투입

4. **모바일 최저가 실시간 검색 & 카테고리 필터 웹페이지**
   - 영상이 발행될 때마다 해당 상품들이 검색 목록에 자동으로 차곡차곡 누적
   - 0.01초 인스턴트 검색창 + 카테고리 칩 필터 + 쿠팡 다이렉트 검색 폴백
   - 라이브 주소: `https://ehdnsj96.github.io/gooditem-archive/`

---

## 🚀 빠른 시작 가이드

### 1. 터미널에서 즉시 1개 생성 테스트
```bash
python3 auto_daily.py --now
```

### 2. 오늘 치 3개 영상 한 번에 연달아 일괄 생성
```bash
python3 auto_daily.py --batch 3
```

### 3. 매일 3회(8시·12시·18시) 완전 무인 자동 데몬 (가장 추천!)
```bash
nohup python3 auto_daily.py --daemon > daily.log 2>&1 &
```

---

## 📦 신규 쿠팡 상품 자동 수집 & 등록 (`product_collector.py`)

원하는 새로운 꿀템을 파이프라인에 추가하고 싶을 때 언제든 사용하세요:

### 방법 1. 대화형 터미널 마법사 (가장 간편!)
```bash
python3 product_collector.py -i
```
터미널에서 안내에 따라 상품명, 가격, 쿠팡링크, 이미지 URL을 입력하면 자동으로 이미지를 받고 등록됩니다.

### 방법 2. 단일 명령어로 즉시 등록
```bash
python3 product_collector.py \
  --theme living \
  --title "샤오미 무선 청소기 G10" \
  --price "198,000원" \
  --url "https://link.coupang.com/a/..." \
  --image "https://thumbnail.coupangcdn.com/..."
```

### 등록된 상품 목록 확인
```bash
python3 product_collector.py --list
```

---

## 📁 주요 디렉터리 및 파일 구조

- `auto_daily.py`: 하루 3회 무인 자동화 러너 (슬롯 관리, 웹페이지 갱신, 텔레그램 배달)
- `product_collector.py`: 신규 쿠팡 상품 자동 수집 및 이미지 다운로더
- `product_pool.py`: 테마별 상품 풀 및 custom_products 자동 병합 엔진
- `slide_renderer.py`: 화사한 룸 클린 디자인 & 슬라이드 렌더러
- `video_builder.py`: FFmpeg 기반 60fps 쇼츠 비디오 빌더
- `voice_generator.py`: Edge-TTS 어린이 보이스 생성기
- `web_updater.py`: GitHub Pages 모바일 누적 검색 도감 갱신 & Git 자동 푸시
- `assets/`: 폰트 및 캐시된 상품 이미지
- `output/daily/`: 날짜별 완성된 고화질 쇼츠 MP4 영상
