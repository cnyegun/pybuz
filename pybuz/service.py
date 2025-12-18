from typing import Callable
import os
from pathlib import Path

from .data_models import DownloadRequest, ProgressEvent, DownloadOutcome, Track, Quality
from .downloader import HttpDownloader
from .paths import album_dir, track_final_path, temp_path
from .qobuz_client import QobuzClient

class DownloadService:
    """
    - create destination directories
    - enforce overwrite/skip behavior
    - download to a temp file (.part) and atomically move into place
    - translate exceptions into DownloadOutcome entries
    """
    def __init__(self, client: QobuzClient):
        self.client = client
        self.downloader = HttpDownloader(client.session)

    def download_album(
        self,
        album_id: str,
        dest_dir: str,
        quality: Quality,
        overwrite: bool = False,
        progress_cb: Callable[[ProgressEvent], None] | None = None,
    ) -> list[DownloadOutcome]:
        dl_request = DownloadRequest(
            dest_dir=Path(dest_dir),
            quality=quality,
            overwrite=overwrite
        )
        if progress_cb is not None:
            progress_cb(ProgressEvent("resolving", None, None, None, None))

        # Get album info from Qobuz
        album = self.client.get_album(album_id)

        # Create album folder
        album_path = album_dir(album, dl_request)
        album_path.mkdir(parents=True, exist_ok=True)

        # Download each track
        outcomes: list[DownloadOutcome] = []

        for index, track in enumerate(album.tracks, start=1):
            outcome = self.download_track(
                track=track,
                index=index,
                album_path=album_path,
                req=dl_request,
                progress_cb=progress_cb
            )
            outcomes.append(outcome)

        return outcomes
    def download_track(
        self,
        track: Track,
        index: int,
        album_path: Path,
        req: DownloadRequest,
        progress_cb: Callable[[ProgressEvent], None] | None = None
    ) -> DownloadOutcome:
        try:
            # Get download URL from Qobuz
            resolved = self.client.resolve_download(track.track_id, req.quality)

            final_path = track_final_path(
                album_path=album_path,
                track=track,
                index=index,
                ext=resolved.ext
            )

            if final_path.exists() and not req.overwrite:
                return DownloadOutcome(
                    item_id=track.track_id,
                    status="skipped",
                    path=final_path,
                    error=None
                )

            temp_file = temp_path(final_path)
            self.downloader.download(
                url=resolved.url,
                dest_tmp=temp_file,
                track_name=track.title,
                track_number=track.track_number,
                progress_cb=progress_cb
            )

            # Change the file extension
            os.replace(temp_file, final_path)


            return DownloadOutcome(
                item_id=track.track_id,
                status="downloaded",
                path=final_path,
                error=None
            )


        except Exception as e:
            return DownloadOutcome(
                item_id=track.track_id,
                status="failed",
                path=None,
                error=str(e)
            )
