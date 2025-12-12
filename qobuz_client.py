from typing import Protocol
from data_models import Album, Quality, ResolvedDownload

class QobuzClient(Protocol):
    def get_album(album_id: str) -> Album:
        pass

    def resolve_download(track_id: str, quality: Quality) -> ResolvedDownload:
        pass