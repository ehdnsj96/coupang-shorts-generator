import asyncio
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple
import edge_tts
import imageio_ffmpeg
import config


class VoiceGenerator:
    def __init__(self, voice: str = config.TTS_VOICE, rate: str = config.TTS_RATE, pitch: str = getattr(config, "TTS_PITCH", "+0Hz")):
        self.voice = voice
        self.rate = rate
        self.pitch = pitch
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def get_audio_duration(self, audio_path: Path) -> float:
        """FFmpeg로 오디오 파일의 정확한 재생 길이(초) 추출"""
        try:
            res = subprocess.run(
                [self.ffmpeg_exe, "-i", str(audio_path)],
                capture_output=True,
                text=True,
                check=False
            )
            match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = float(match.group(3))
                return hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            print(f"[VoiceGenerator] 길이 확인 에러 ({audio_path}): {e}")
        return 5.0  # 기본 fallback 길이

    async def _generate_slide_audio_async(self, text: str, output_path: Path):
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch)
        await communicate.save(str(output_path))

    def generate_slide_audio(self, text: str, output_path: Path) -> float:
        """단일 슬라이드의 멘트를 음성으로 합성하고 길이(초) 반환"""
        output_path.parent.mkdir(exist_ok=True, parents=True)
        asyncio.run(self._generate_slide_audio_async(text, output_path))
        return self.get_audio_duration(output_path)
