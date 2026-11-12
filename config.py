import os
import sys
from pathlib import Path

# 기본 디렉터리
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

OUTPUT_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)

# 쿠팡 파트너스 트래킹 ID
COUPANG_TRACKING_ID = os.getenv("COUPANG_TRACKING_ID", "AF7086198")

# 영상 규격: 유튜브 쇼츠 표준 세로 9:16 (1080 x 1920)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30

# AI 성우 설정 (Microsoft Edge TTS 한국어 고품질 성우)
TTS_VOICE = "ko-KR-SunHiNeural"
TTS_RATE = "+10%"
TTS_PITCH = "+25Hz"  # 쇼츠 템포에 맞춰 약간 빠르게 (+10%)

# 폰트 경로 (Pretendard 최우선 적용)
FONT_BOLD_PATH = str(FONTS_DIR / "Pretendard-Bold.otf")
FONT_EXTRABOLD_PATH = str(FONTS_DIR / "Pretendard-ExtraBold.otf")
