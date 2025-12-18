from typing import Callable
from requests import Session
from pathlib import Path

from .data_models import ProgressEvent

class HttpDownloader:
    def __init__(self, session: Session):
        self.session = session

    def _download_once(
            self,
            url: str,
            dest_tmp: Path,
            track_name: str,
            track_number: int,
            progress_cb: Callable[[ProgressEvent], None] | None,
    ) -> int:
        byte_count = 0
        with self.session.get(url, stream=True, timeout=30) as res:
            if res.status_code != 200:
                res.close()
                raise ConnectionError(res.status_code)
            with open(dest_tmp, 'wb') as file:
                report_every = 1024 * 1024
                last_reported = 0
                for chunk in res.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    byte_count += len(chunk)
                    file.write(chunk)
                    if progress_cb is not None and (byte_count - last_reported) >= report_every:
                        last_reported = byte_count
                        progress_cb(ProgressEvent(
                            phase="downloading",
                            track_name=track_name,
                            track_number=track_number,
                            bytes_done=byte_count,
                            bytes_total=None
                        ))
        if progress_cb is not None:
            progress_cb(ProgressEvent(
                phase="finished",
                track_name=track_name,
                track_number=track_number,
                bytes_done=byte_count,
                bytes_total=None
            ))
        return byte_count

    def download(
        self,
        url: str,
        dest_tmp: Path,
        track_name: str,
        track_number: int,
        progress_cb: Callable[[ProgressEvent], None] | None,
        max_retries: int = 5
    ) -> int | None:
        for attempt in range(max_retries):
            try:
                return self._download_once(url, dest_tmp, track_name, track_number, progress_cb)
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    raise
        return None
