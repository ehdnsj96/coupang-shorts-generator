# 🧪 돈값연구소 (@dongap_lab) - 쿠팡 파트너스 유튜브 쇼츠 완전 무인 자동화 파이프라인

"이건 진짜 돈값 한다!" 싶은 알짜배기 쿠팡 꿀템을 **하루 3회(08시·12시·18시) 자동으로 영상화하고, 모바일 누적 도감(GitHub Pages)과 유튜브 채널까지 100% 무인 연동**하는 올인원 시스템입니다.

---

## 🌟 핵심 기능

1. **화사한 화이트 인테리어 룸 클린 디자인 & 어린이 똑부러진 보이스**
   - 햇살 비치는 화이트 룸 배경 + 실물 쿠팡 1위 제품 중앙 포커스
   - 낭랑하고 똑부러진 어린이 보이스(선희 +25Hz)로 0.1초 만에 시선 집중
   - 쿠팡 시그니처 3단 특가 뱃지 (`로켓배송 🚀` + `실시간 가격` + `★ 4.8 평점`)
   - 💡 체크포인트 3종 스펙 카드 + 방송용 두꺼운 볼드 외곽선 자막

2. **하루 3회 골든 타임 슬롯 자동 데몬 (`auto_daily.py --daemon`)**
   - 08:00 (출근길 피크), 12:00 (점심시간 피크), 18:00 (퇴근·저녁 피크) 자동 순환
   - 테마 자동 전환: 자취·리빙 ➔ 주방·살림 ➔ 식비·간편식 ➔ 데스크테리어 ➔ 욕실·샤워 ➔ 차 안 리셋 ➔ 청소 끝판왕 ➔ 한파 방한 필수템 ➔ 세탁·의류관리 끝판왕 ➔ 숙면 부르는 침실 꿀템 ➔ 홈카페·커피 ➔ 홈트·실내운동 (테마당 실물 상품 3종, 총 12테마 36종)
   - 유튜브 업로드가 끝난 회차만 **모바일 누적 도감(GitHub Pages)** 에 1:1 상품 링크로 갱신

3. **삼중 중복 업로드 가드 (`publish_guard.py`)** — 같은 영상을 두 번 올리지 않는다
   - 1단계 로컬: `daily_state.json` 의 `used_items_by_theme` / `published_titles`
   - 2단계 원격 도감: `gooditem-archive/history.json` 에 이미 등록된 상품은 사용 처리 (실패 시 `web/history.json` 로컬 사본으로 폴백)
   - 3단계 유튜브: 채널 RSS(`channel_id=UCuzNtUgtrJyPumZ5HGd-m0g`)에 이미 올라간 영상 제목은 그 회차를 건너뜀 (실패 시 로컬 상태로 폴백)
   - 사용한 상품은 **절대 재사용하지 않으며**, 모든 테마의 미사용 실물 상품이 3종 미만이면 `None` 을 반환해 생성·업로드를 건너뛰고 안내만 남긴다 (과거 '같은 영상 무한 재업로드' 버그 수정)
   - `daily_state.json` 은 `.gitignore` 로 제외되어 `git pull` 충돌·덮어쓰기가 발생하지 않는다 (에피소드 회차·사용 상품은 도감에서 자동 복원)
   - 유튜브에도 도감에도 없는(게시되지 않은) 회차는 로컬 잠금을 자동 해제해 다음 실행에서 다시 생성·업로드한다
     (업로드 실패·인증 없음으로 `daily_state.json` 에만 "사용/게시"로 남은 회차가 영원히 건너뛰어지는 문제 방지. RSS·원격 도감이 둘 다 정상 확인된 경우에만 동작하므로 같은 영상 재업로드는 생기지 않는다)

4. **업로드 전 무결성 사전 검증 (`preflight.py`)**
   - ① 모든 슬라이드·상품 이미지 파일 실제 존재 여부
   - ② 각 상품 쿠팡 링크의 파트너스 태그 `lptag=AF7086198` 포함 여부
   - ③ 영상 속 제품 3종과 슬라이드·설명란의 1:1 매칭(제품명·가격·이미지) 여부
   - 하나라도 어긋나면 **생성·업로드를 차단**하고 문제 항목을 그대로 출력한다 (가짜 상품·깨진 링크가 나가는 일 방지)

5. **쿠팡 상품 원클릭 자동 수집기 (`product_collector.py`)**
   - 상품 대표 이미지를 웹/CDN에서 자동으로 다운로드하고 640x640 정방형 캔버스로 자동 최적화
   - 대사(voice_script), 체크포인트, 뱃지, 태그 자동 생성
   - `custom_products.json`에 저장되어 데일리 러너에 즉시 자동 투입

6. **실행 전 자동 Git 동기화 (`sync_repo`)** — PC 가 실행 직전에 최신 코드를 스스로 받아온다
   - 데몬은 슬롯 시각이 되면 ① `git fetch` → `git merge --ff-only origin/main` 으로 최신 코드를 당긴 뒤,
     ② **새 파이썬 프로세스**(`auto_daily.py --now --slot <slot_id> --no-sync`)에서 1회 실행한다
     → 방금 받은 `product_pool.py`(새 테마·상품)와 모듈이 메모리에 새로 로드된다
   - 로컬 추적 파일을 직접 고쳐 ff 병합이 막히면 `git reset --hard origin/main` 으로 폴백하되,
     `.gitignore` 대상인 `daily_state.json` · `output/` · `token.pickle` · `token.json` · `client_secrets.json` 은 지우지 않는다
     (동기화 후 실제 존재 여부까지 확인). 폴백 직전 로컬 변경분은 `output/git_sync_backup/*.patch` 로 백업
   - 네트워크·git 오류는 경고 로그만 찍고 **기존 로컬 코드로 계속 실행**한다 (무인 자동화가 멈추지 않음)
   - `python3 auto_daily.py --now` 도 시작할 때 1회 동기화하고, 코드가 갱신되면 자동으로 새 프로세스로 다시 시작한다
     (`--no-sync` 로 끌 수 있고, 테스트·오프라인 실행은 `--no-sync` 사용)
   - 자동 동기화는 **PC 폴더가 Git 저장소(Clone)** 일 때 작동한다. zip 압축 해제본에서는 안전하게 건너뛰고 현재 코드로 실행하므로,
     PC 는 `git clone https://github.com/ehdnsj96/coupang-shorts-generator.git` 으로 받아 두는 것이 좋다(이후 `git pull` 을 직접 할 필요 없음)

4. **모바일 최저가 실시간 검색 & 카테고리 필터 웹페이지**
   - 영상이 발행될 때마다 해당 상품들이 검색 목록에 자동으로 차곡차곡 누적
   - 카테고리 칩: 주방·살림 / 자취·리빙 / 식비·간편식 / 데스크 / 욕실·샤워 / 차량·운전 / 청소·수납 / 겨울·방한 / 세탁·의류 / 숙면·침실 / 홈카페·커피 / 홈트·운동 (새 테마 자동 반영)
   - 0.01초 인스턴트 검색창 + 카테고리 칩 필터 + 쿠팡 다이렉트 검색 폴백
   - 라이브 주소: `https://ehdnsj96.github.io/gooditem-archive/`

---

## 🚀 빠른 시작 가이드

### 1. 터미널에서 즉시 1개 생성 테스트
```bash
python3 auto_daily.py --now               # 시작할 때 최신 코드 동기화 후 실행
python3 auto_daily.py --now --no-sync     # 동기화 없이 현재 코드로 바로 실행(오프라인·테스트)
```

### 2. 오늘 치 3개 영상 한 번에 연달아 일괄 생성
```bash
python3 auto_daily.py --batch 3
```

### 3. 매일 3회(8시·12시·18시) 완전 무인 자동 데몬 (가장 추천!)
```bash
nohup python3 auto_daily.py --daemon > daily.log 2>&1 &
```
> 데몬은 슬롯마다 원격 `origin/main` 최신 코드를 먼저 받아온 뒤 새 프로세스로 실행합니다.
> PC 에서는 아무것도 건드리지 않아도 새 테마·새 상품이 다음 슬롯부터 자동 반영됩니다.

### 4. 업로드·전송 없이 파이프라인만 점검 (테스트)
```bash
python3 auto_daily.py --dry-run --force   # 생성만, 유튜브 업로드·도감 푸시 없음
python3 auto_daily.py --now --slot 2026-11-17_08 --no-sync   # 데몬이 하위 프로세스로 부르는 형태
python3 tests/test_guard.py               # 중복 가드·사전 검증·도감 정합성 테스트
python3 tests/test_auto_daily.py          # 파이프라인 배선 + 실행 전 Git 동기화(sync_repo)·--no-sync 테스트
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

- `auto_daily.py`: 하루 3회 무인 자동화 러너 (슬롯 관리, 실행 전 Git 동기화, 유튜브 업로드, 웹페이지 갱신)
- `publish_guard.py`: 삼중 중복 업로드 가드 (로컬 상태 · 원격 도감 · 유튜브 RSS)
- `preflight.py`: 업로드 전 무결성 사전 검증 (이미지 존재 · 검색 URL 차단 · /vp/products 상품 URL · lptag · 1:1 매칭)
- `tests/`: 중복 가드·사전 검증 로컬 테스트
- `product_collector.py`: 신규 쿠팡 상품 자동 수집 및 이미지 다운로더
- `product_pool.py`: 테마별 상품 풀 및 custom_products 자동 병합 엔진
- `slide_renderer.py`: 화사한 룸 클린 디자인 & 슬라이드 렌더러
- `video_builder.py`: FFmpeg 기반 60fps 쇼츠 비디오 빌더
- `voice_generator.py`: Edge-TTS 어린이 보이스 생성기
- `web_updater.py`: GitHub Pages 모바일 누적 검색 도감 갱신 & Git 자동 푸시
- `assets/`: 폰트 및 캐시된 상품 이미지
- `output/daily/`: 날짜별 완성된 고화질 쇼츠 MP4 영상
