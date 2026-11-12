import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from models import ShortsScript
from slide_renderer import SlideRenderer
from templates import get_preset_scripts
from video_builder import VideoBuilder
from voice_generator import VoiceGenerator
import config


def generate_shorts(script: ShortsScript) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = config.OUTPUT_DIR / f"temp_{timestamp}"
    work_dir.mkdir(parents=True, exist_ok=True)

    renderer = SlideRenderer()
    voice_gen = VoiceGenerator()
    video_builder = VideoBuilder()

    slide_items = []
    total_duration = 0.0

    print(f"\n=======================================================")
    print(f"🎬 쿠팡 쇼츠 자동 생성 시작: [{script.topic}]")
    print(f"=======================================================\n")

    for i, slide in enumerate(script.slides):
        print(f"[{i+1}/{len(script.slides)}] {slide.step_name} 슬라이드 처리 중...")

        # 1. 슬라이드 이미지 렌더링
        img_path = work_dir / f"slide_{i:02d}.png"
        renderer.render_slide(slide, img_path)

        # 2. AI 성우 음성 생성
        audio_path = work_dir / f"voice_{i:02d}.mp3"
        duration = voice_gen.generate_slide_audio(slide.voice_script, audio_path)
        total_duration += duration

        print(f"   -> 음성 길이: {duration:.2f}초 | 멘트: \"{slide.voice_script[:25]}...\"")
        slide_items.append((img_path, audio_path, duration))

    # 3. 비디오 인코딩 및 병합
    output_video_path = config.OUTPUT_DIR / f"shorts_{timestamp}.mp4"
    print(f"\n🎥 영상 인코딩 및 최종 병합 중 (예상 길이: 약 {int(total_duration)}초)...")

    success = video_builder.build_shorts_video(slide_items, output_video_path)

    # 임시 디렉터리 정리
    import shutil
    shutil.rmtree(work_dir, ignore_errors=True)

    if not success:
        print("❌ 비디오 생성에 실패했습니다.")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"✨ 쇼츠 영상 제작 완료!")
    print(f"📁 파일 위치: {output_video_path.resolve()}")
    print(f"⏱️ 영상 길이: 약 {int(total_duration)}초 (세로 1080x1920)")
    print(f"=======================================================\n")

    print("📋 [유튜브 업로드용 복사/붙여넣기 정보]")
    print("-------------------------------------------------------")
    print(f"📌 제목:\n{script.youtube_title}\n")
    print(f"📝 설명란:\n{script.youtube_description}\n")
    print(f"🏷️ 해시태그:\n{' '.join(script.hashtags)}")
    print("-------------------------------------------------------\n")

    return output_video_path


def main():
    parser = argparse.ArgumentParser(description="쿠팡 파트너스 유튜브 쇼츠 자동 생성기")
    parser.add_argument("--preset", type=int, default=1, help="프리셋 번호 (1: 자취생 꿀템, 2: 직장인 데스크테리어)")
    args = parser.parse_args()

    presets = get_preset_scripts()
    idx = args.preset - 1
    if idx < 0 or idx >= len(presets):
        idx = 0

    selected_script = presets[idx]
    generate_shorts(selected_script)


if __name__ == "__main__":
    main()
