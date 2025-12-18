from .data_models import Quality, ResolvedDownload, Track, Album
import requests
import hashlib
import time
from datetime import datetime
from .utils import extract_album_id

class QobuzClient:
    def __init__(
        self,
        user_id: str,
        auth_token: str,
    ):
        self.app_secret = "abb21364945c0583309667d13ca3d93a"
        self.app_id = "798273057"
        self.user_id = user_id
        self.auth_token = auth_token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
                "X-App-Id": self.app_id,
                "X-User-Auth-Token": self.auth_token,
                "Content-Type": "application/json;charset=UTF-8"
            }
        )
        self.base = "https://www.qobuz.com/api.json/0.2/"
        self._auth()

    def _auth(self):
        endpoint = "user/login"
        params = {
            "app_id": self.app_id
        }
        response = self.session.get(self.base + endpoint, params=params)
        if response.status_code != 200:
            raise Exception("Invalid credentials.")

    def _get_request_sig(self, format_id: str, track_id: str, timestamp: int) -> str:
        to_hash = f"trackgetFileUrlformat_id{format_id}intentstreamtrack_id{track_id}{timestamp}{self.app_secret}"
        return hashlib.md5(to_hash.encode()).hexdigest()

    def get_album(self, album_id: str):
        endpoint = "album/get"
        params = {
            "album_id": extract_album_id(album_id)
        }
        response = self.session.get(self.base + endpoint, params=params)
        response.raise_for_status()

        data = response.json()
        print(data)

        artist_name = data["artist"]["name"]

        try:
            release_date = datetime.strptime(data["release_date_original"],"%Y-%m-%d")
        except (KeyError, ValueError):
            release_date = None

        tracks = []
        for track_data in data["tracks"]["items"]:
            track = Track(
                track_id=str(track_data["id"]),
                track_number=int(track_data["track_number"]),
                title=track_data["title"].strip(),
                artist=artist_name,
                release_date=release_date
            )
            tracks.append(track)

        return Album(
            album_id=album_id,
            title=data["title"],
            artist=artist_name,
            release_date=release_date,
            tracks=tuple(tracks)
        )

    def resolve_download(self, track_id: str, quality: Quality) -> ResolvedDownload:
        endpoint = "track/getFileUrl"
        timestamp = int(time.time())

        params = {
            "request_ts": timestamp,
            "request_sig": self._get_request_sig(quality.code, track_id, timestamp),
            "track_id": track_id,
            "format_id": quality.code,
            "intent": "stream"
        }

        response = self.session.get(self.base + endpoint, params=params)
        response.raise_for_status()

        data = response.json()

        mime = data.get('mime_type', '')
        ext = '.flac' if 'flac' in mime else '.mp3'

        return ResolvedDownload(url=data['url'], ext=ext)