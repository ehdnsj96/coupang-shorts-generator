import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional
import config

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = config.BASE_DIR / "client_secrets.json"
TOKEN_FILE = config.BASE_DIR / "token.json"


class YouTubeUploader:
    def __init__(self, client_secrets_path: Path = CLIENT_SECRETS_FILE, token_path: Path = TOKEN_FILE):
        self.client_secrets_path = Path(client_secrets_path)
        self.token_path = Path(token_path)
        self.service = None

    def is_configured(self) -> bool:
        return self.client_secrets_path.exists() or self.token_path.exists()

    def authenticate(self) -> bool:
        if not GOOGLE_API_AVAILABLE:
            print("❌ google-api-python-client 라이브러리가 설치되지 않았습니다.")
            print("👉 'pip install google-api-python-client google-auth-oauthlib' 실행이 필요합니다.")
            return False

        creds = None

        # 1. 기존 인증 토큰이 있으면 로드
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            except Exception as e:
                print(f"⚠️ 토큰 파일 읽기 실패: {e}")

        # 2. 토큰이 유효하지 않거나 만료된 경우 리프레시 또는 신규 인증
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("🔄 YouTube OAuth 인증 토큰 갱신 완료")
                except Exception as e:
                    print(f"⚠️ 토큰 갱신 실패, 재인증 필요: {e}")
                    creds = None

            if not creds:
                if not self.client_secrets_path.exists():
                    print("\n" + "=" * 60)
                    print("⚠️ [안내] YouTube 업로드를 위한 'client_secrets.json' 파일이 없습니다.")
                    print("=" * 60)
                    print("1. Google Cloud Console(console.cloud.google.com) 접속")
                    print("2. 프로젝트 생성 -> 'YouTube Data API v3' 활성화")
                    print("3. [사용자 인증 정보] -> [OAuth 2.0 클라이언트 ID] (데스크톱 앱) 생성")
                    print("4. JSON 다운로드 후 파일명을 'client_secrets.json'으로 프로젝트 폴더에 저장")
                    print("=" * 60 + "\n")
                    return False

                try:
                    print("🌐 웹 브라우저를 열어 Google 계정 1회 로그인을 진행합니다...")
                    flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets_path), SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"❌ OAuth 인증 실패: {e}")
                    return False

            # 새 토큰 저장 (다음부터는 로그인 창 없이 영구 자동 구동)
            try:
                with open(self.token_path, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
                print(f"💾 인증 토큰 저장 완료: {self.token_path}")
            except Exception as e:
                print(f"⚠️ 토큰 파일 저장 실패: {e}")

        self.service = build("youtube", "v3", credentials=creds)
        return True

    def upload(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        category_id: str = "22",  # 22: People & Blogs, 24: Entertainment, 26: Howto & Style
        privacy_status: str = "public",  # 'public', 'unlisted', 'private'
        thumbnail_path: Optional[Path] = None
    ) -> Optional[str]:
        video_path = Path(video_path)
        if not video_path.exists():
            print(f"❌ 업로드할 영상 파일이 없습니다: {video_path}")
            return None

        if not self.service:
            if not self.authenticate():
                return None

        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        print(f"\n🚀 유튜브 업로드 시작: [{title}]")
        print(f"📁 파일: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
        print(f"🔒 공개 상태: {privacy_status}")

        try:
            media = MediaFileUpload(
                str(video_path),
                chunksize=-1,
                resumable=True,
                mimetype="video/*"
            )

            request = self.service.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   -> 업로드 진행률: {progress}%")

            video_id = response.get("id")
            shorts_url = f"https://youtube.com/shorts/{video_id}"
            print(f"✨ 유튜브 쇼츠 업로드 성공!")
            print(f"🔗 쇼츠 링크: {shorts_url}")

            # 맞춤 썸네일 자동 등록
            if thumbnail_path and Path(thumbnail_path).exists():
                try:
                    thumb_media = MediaFileUpload(str(thumbnail_path), mimetype="image/png")
                    self.service.thumbnails().set(
                        videoId=video_id,
                        media_body=thumb_media
                    ).execute()
                    print(f"🖼️ 유튜브 맞춤 썸네일 자동 등록 완료: {Path(thumbnail_path).name}")
                except Exception as te:
                    print(f"⚠️ 맞춤 썸네일 자동 등록 안내 (채널 1회 전화번호 인증 필요시 스튜디오에서 적용): {te}")

            return shorts_url

        except HttpError as e:
            print(f"❌ YouTube API HTTP 에러 발생: {e}")
            return None
        except Exception as e:
            print(f"❌ 업로드 중 예상치 못한 에러: {e}")
            return None
