import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from models import ShortsScript
from episode_builder import get_next_dynamic_episode
from slide_renderer import SlideRenderer
from video_builder import VideoBuilder
from voice_generator import VoiceGenerator
from youtube_uploader import YouTubeUploader
from web_updater import update_link_page
import config

STATE_FILE = config.BASE_DIR / "daily_state.json"
DAILY_OUTPUT_DIR = config.OUTPUT_DIR / "daily"
DAILY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 유튜브 쇼츠 알고리즘 최적 3대 골든 타임 슬롯 (기본: 아침 8시, 점심 12시, 저녁 18시)
DEFAULT_SLOTS = [8, 12, 18]


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"completed_slots": [], "history": []}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_video_to_telegram(video_path: Path, caption: str) -> bool:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "9156774396:AAFJqnKnvHVdy1nYOesY1nn9QQuqn7oEHo0")
    channel_id = os.getenv("TELEGRAM_CHANNEL", "@ym_hotdeal")

    if not bot_token or not channel_id:
        print("[Telegram] 봇 토큰 또는 채널 ID가 설정되지 않아 건너뜁니다.")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    print(f"📲 텔레그램 채널({channel_id})로 영상 자동 전송 중...")

    try:
        import mimetypes
        import ssl

        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        data = []

        def add_field(name, value):
            data.append(f"--{boundary}".encode("utf-8"))
            data.append(f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"))
            data.append(b"")
            data.append(str(value).encode("utf-8"))

        def add_file(name, filepath):
            filename = os.path.basename(filepath)
            mimetype = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
            data.append(f"--{boundary}".encode("utf-8"))
            data.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode("utf-8"))
            data.append(f"Content-Type: {mimetype}".encode("utf-8"))
            data.append(b"")
            with open(filepath, "rb") as f:
                data.append(f.read())

        add_field("chat_id", channel_id)
        add_field("caption", caption[:1024])
        add_field("supports_streaming", "true")
        add_file("video", video_path)

        data.append(f"--{boundary}--".encode("utf-8"))
        data.append(b"")
        body = b"\r\n".join(data)

        req = urllib.request.Request(url, data=body)
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
            res = json.loads(response.read().decode())
            if res.get("ok"):
                print("✅ 텔레그램 영상 전송 성공!")
                return True
            else:
                print(f"❌ 텔레그램 전송 실패: {res}")
                return False
    except Exception as e:
        print(f"⚠️ 텔레그램 전송 중 오류 발생: {e}")
        return False


def run_daily_job(
    slot_id: Optional[str] = None,
    force: bool = False,
    theme: str = "bright_room_minimal",
    send_telegram: bool = True,
    upload_youtube: bool = False
) -> Optional[Path]:
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_hour_slot = slot_id or f"{today_str}_{now.hour:02d}"

    state = load_state()
    completed_slots = state.get("completed_slots", [])

    if not force and current_hour_slot in completed_slots:
        print(f"ℹ️ 현재 슬롯({current_hour_slot})의 쇼츠는 이미 생성되었습니다.")
        print("💡 강제 재실행하려면 --force 플래그를 붙여 실행하세요.")
        if state.get("history"):
            return Path(state["history"][-1]["video_path"])
        return None

    # 다음 순번 에피소드 자동 선택 (테마 및 상품 자동 회전)
    selected_script, state = get_next_dynamic_episode(state)

    timestamp = now.strftime("%Y%m%d_%H%M%S")
    work_dir = config.OUTPUT_DIR / f"temp_{timestamp}"
    work_dir.mkdir(parents=True, exist_ok=True)

    renderer = SlideRenderer(theme=theme)
    voice_gen = VoiceGenerator()
    video_builder = VideoBuilder()

    slide_items = []
    total_duration = 0.0

    print(f"\n=======================================================")
    print(f"🚀 쇼츠 자동 생성 슬롯 [{current_hour_slot}]: [{selected_script.topic}]")
    print(f"🎨 디자인 모드: 화사한 룸 미니멀 클린 (아이 목소리 적용)")
    print(f"=======================================================\n")

    for i, slide in enumerate(selected_script.slides):
        print(f"[{i+1}/{len(selected_script.slides)}] {slide.step_name} 슬라이드 처리 중...")

        # 1. 슬라이드 이미지 렌더링
        img_path = work_dir / f"slide_{i:02d}.png"
        renderer.render_slide(slide, img_path)

        # 2. AI 성우 음성 생성
        audio_path = work_dir / f"voice_{i:02d}.mp3"
        duration = voice_gen.generate_slide_audio(slide.voice_script, audio_path)
        total_duration += duration

        print(f"   -> 음성 길이: {duration:.2f}초 | 멘트: \"{slide.voice_script[:25]}...\"")
        slide_items.append((img_path, audio_path, duration))

    # 3. 비디오 인코딩 및 최종 병합
    safe_topic = "".join([c for c in selected_script.topic if c.isalnum() or c in (" ", "_")]).rstrip().replace(" ", "_")
    output_filename = f"Shorts_{safe_topic}_{timestamp}.mp4"
    output_video_path = DAILY_OUTPUT_DIR / output_filename

    print(f"\n🎥 영상 인코딩 및 최종 병합 중 (예상 길이: 약 {int(total_duration)}초)...")
    success = video_builder.build_shorts_video(slide_items, output_video_path)

    # 임시 디렉터리 정리
    import shutil
    shutil.rmtree(work_dir, ignore_errors=True)

    if not success:
        print("❌ 비디오 생성에 실패했습니다.")
        return None

    print(f"\n=======================================================")
    print(f"✨ 슬롯 [{current_hour_slot}] 쇼츠 영상 자동 제작 완료!")
    print(f"📁 파일 위치: {output_video_path.resolve()}")
    print(f"⏱️ 영상 길이: 약 {int(total_duration)}초 (세로 1080x1920)")
    print(f"=======================================================\n")

    youtube_url = None
    uploader = YouTubeUploader()

    # 유튜브 자동 업로드 시도
    if upload_youtube or uploader.is_configured():
        print("\n📺 YouTube 자동 업로드 모듈 가동...")
        youtube_url = uploader.upload(
            video_path=output_video_path,
            title=selected_script.youtube_title,
            description=selected_script.youtube_description,
            tags=selected_script.hashtags,
            privacy_status="public"
        )

    caption_text = (
        f"🎬 [{current_hour_slot}] 오늘의 쇼츠 완성!\n\n"
        f"📌 제목:\n{selected_script.youtube_title}\n\n"
        f"📝 설명란:\n{selected_script.youtube_description}\n\n"
        f"🏷️ 해시태그:\n{' '.join(selected_script.hashtags)}"
    )

    if youtube_url:
        caption_text = f"✨ 유튜브 쇼츠 자동 업로드 완료!\n🔗 {youtube_url}\n\n" + caption_text

    print(caption_text)
    print("\n-------------------------------------------------------")

    # 텔레그램 채널로 전송
    if send_telegram:
        send_video_to_telegram(output_video_path, caption_text)

    # 모바일 웹 링크 페이지(GitHub Pages) 자동 갱신
    if selected_script.items:
        print("\n🌐 모바일 링크 페이지(GitHub Pages) 자동 갱신 중...")
        try:
            update_link_page(theme_name=selected_script.topic, items=selected_script.items, auto_push=True)
            print("✅ 모바일 웹페이지 최신 꿀템 링크 자동 반영 완료!")
        except Exception as e:
            print(f"⚠️ 모바일 웹페이지 갱신 중 오류: {e}")

    # 상태 업데이트
    if "completed_slots" not in state:
        state["completed_slots"] = []
    if current_hour_slot not in state["completed_slots"]:
        state["completed_slots"].append(current_hour_slot)

    # 오래된 슬롯 기록 정리 (최근 30일 유지)
    if len(state["completed_slots"]) > 90:
        state["completed_slots"] = state["completed_slots"][-90:]

    state["last_run_date"] = today_str
    history_entry = {
        "slot": current_hour_slot,
        "date": today_str,
        "topic": selected_script.topic,
        "video_path": str(output_video_path)
    }
    if youtube_url:
        history_entry["youtube_url"] = youtube_url
    if "history" not in state:
        state["history"] = []
    state["history"].append(history_entry)
    save_state(state)

    return output_video_path


def daemon_loop(slots: List[int] = DEFAULT_SLOTS, theme: str = "bright_room_minimal", send_telegram: bool = True, upload_youtube: bool = False):
    slot_desc = ", ".join([f"{h:02d}:00" for h in sorted(slots)])
    print(f"🕒 데일리 쇼츠 하루 3회 무인 자동화 백그라운드 데몬 가동 중...")
    print(f"⏰ 지정된 슬롯 시각: 매일 [{slot_desc}] 총 {len(slots)}회 자동 생성 및 업로드")
    print("💡 중단하려면 Ctrl+C를 누르세요.\n")

    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        current_hour = now.hour

        if current_hour in slots:
            slot_id = f"{today_str}_{current_hour:02d}"
            state = load_state()
            completed_slots = state.get("completed_slots", [])

            if slot_id not in completed_slots:
                # 오늘 완료된 슬롯 수 계산
                today_done = [s for s in completed_slots if s.startswith(today_str)]
                print(f"\n[알림] ⏰ {current_hour:02d}:00 슬롯 도달! (오늘 {len(today_done) + 1}/{len(slots)}번째 영상 생성 시작)")
                run_daily_job(slot_id=slot_id, force=False, theme=theme, send_telegram=send_telegram, upload_youtube=upload_youtube)

        time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description="쿠팡 파트너스 하루 3회 쇼츠 무인 자동화 러너")
    parser.add_argument("--now", action="store_true", help="지금 즉시 1회 생성")
    parser.add_argument("--batch", type=int, default=0, help="한 번에 연속 N개 영상 일괄 생성 (예: --batch 3)")
    parser.add_argument("--force", action="store_true", help="현재 슬롯이 이미 완료되었어도 강제 재실행")
    parser.add_argument("--theme", default="bright_room_minimal", help="디자인 테마")
    parser.add_argument("--no-telegram", action="store_true", help="텔레그램 전송 건너뛰기")
    parser.add_argument("--youtube", action="store_true", help="생성 완료 후 YouTube Data API로 자동 업로드")
    parser.add_argument("--daemon", action="store_true", help="하루 3회 지정 슬롯에 자동 실행하는 데몬 모드")
    parser.add_argument("--slots", type=int, nargs="+", default=DEFAULT_SLOTS, help="실행 시각 슬롯 목록 (기본: 8 12 18)")

    args = parser.parse_args()
    send_telegram = not args.no_telegram

    if args.batch > 0:
        print(f"🎬 연속 {args.batch}개 영상 일괄 배치 생성을 시작합니다...\n")
        for i in range(args.batch):
            now = datetime.now()
            batch_slot_id = f"batch_{now.strftime('%Y%m%d_%H%M%S')}_{i+1}"
            print(f"\n>>> [배치 {i+1}/{args.batch}] 생성 시작 <<<")
            run_daily_job(slot_id=batch_slot_id, force=True, theme=args.theme, send_telegram=send_telegram, upload_youtube=args.youtube)
            if i < args.batch - 1:
                time.sleep(2)
        print(f"\n🎉 총 {args.batch}개 영상 일괄 배치 제작 완료!")
    elif args.daemon:
        daemon_loop(slots=args.slots, theme=args.theme, send_telegram=send_telegram, upload_youtube=args.youtube)
    else:
        run_daily_job(force=args.force or args.now, theme=args.theme, send_telegram=send_telegram, upload_youtube=args.youtube)


if __name__ == "__main__":
    main()
