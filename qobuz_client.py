from typing import Protocol
from data_models import Album, Quality, ResolvedDownload

class QobuzClient(Protocol):
    def get_album(self, album_id: str) -> Album:
        ...

    def resolve_download(self, track_id: str, quality: Quality) -> ResolvedDownload:
        ...