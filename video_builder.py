import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple
import imageio_ffmpeg
import config


class VideoBuilder:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def build_shorts_video(self, slide_items: List[Tuple[Path, Path, float]], output_video_path: Path) -> bool:
        """
        slide_items: List of (image_png_path, audio_mp3_path, duration_seconds)
        output_video_path: 최종 완성될 mp4 파일 경로
        """
        output_video_path.parent.mkdir(exist_ok=True, parents=True)
        temp_dir = Path(tempfile.mkdtemp(prefix="shorts_build_"))

        try:
            clip_paths = []
            for i, (img_p, aud_p, dur) in enumerate(slide_items):
                clip_p = temp_dir / f"clip_{i:03d}.mp4"

                # 100만 쇼츠 미니멀 클린 인코딩 (화사한 룸 + 제품 집중)
                cmd = [
                    self.ffmpeg_exe, "-y",
                    "-loop", "1",
                    "-framerate", str(config.VIDEO_FPS),
                    "-i", str(img_p),
                    "-i", str(aud_p),
                    "-t", f"{dur:.3f}",
                    "-c:v", "libx264",
                    "-crf", "24",
                    "-preset", "veryfast",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-pix_fmt", "yuv420p",
                    str(clip_p)
                ]

                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if res.returncode != 0:
                    print(f"[VideoBuilder] 클립 {i} 생성 실패: {res.stderr[-500:]}")
                    return False
                clip_paths.append(clip_p)

            # concat 리스트 파일 작성
            concat_list_file = temp_dir / "concat_list.txt"
            with open(concat_list_file, "w", encoding="utf-8") as f:
                for cp in clip_paths:
                    f.write(f"file '{cp.resolve()}'\n")

            # 전체 클립 무손실 병합
            concat_cmd = [
                self.ffmpeg_exe, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_file),
                "-c", "copy",
                str(output_video_path)
            ]
            concat_res = subprocess.run(concat_cmd, capture_output=True, text=True, check=False)
            if concat_res.returncode != 0:
                print(f"[VideoBuilder] 최종 병합 실패: {concat_res.stderr[:200]}")
                return False

            return True
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
