from typing import Callable
from requests import Session
from pathlib import Path

from data_models import ProgressEvent

class HttpDownloader:
    def __init__(self, session: Session | None = None):
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def download(self, url: str, dest_tmp: Path, item_id: str,
                 progress_cb: Callable[[ProgressEvent], None] | None) -> int:
        byte_count = 0
        with self.session.get(url, stream=True) as res:
            if res.status_code != 200:
                res.close()
                raise ConnectionError(res.status_code)
            with open(dest_tmp, 'wb') as file:
                report_every = 1024 * 1024
                last_reported = 0
                for chunk in res.iter_content(chunk_size=4096):
                    if not chunk:
                        continue
                    byte_count += len(chunk)
                    file.write(chunk)
                    if progress_cb is not None and (byte_count - last_reported) >= report_every:
                        last_reported = byte_count
                        progress_cb(ProgressEvent(
                            item_id,
                            "downloading",
                            byte_count,
                            None))
        if progress_cb is not None:
            progress_cb(ProgressEvent(
                item_id,
                "finished",
                byte_count,
                None))
        return byte_count
