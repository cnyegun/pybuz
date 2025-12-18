from .qobuz_client import QobuzClient
from .service import DownloadService
from .data_models import Album, Track, Quality, DownloadRequest, DownloadOutcome, ProgressEvent, ResolvedDownload
from . import qualities
from .utils import extract_album_id

__all__ = [
    "QobuzClient",
    "DownloadService",
    "Album",
    "Track",
    "Quality",
    "DownloadRequest",
    "DownloadOutcome",
    "ProgressEvent",
    "ResolvedDownload",
    "qualities",
    "extract_album_id",
]
__version__ = "0.1.0"
