from typing import Callable
from requests import Session
from pathlib import Path

from data_models import ProgressEvent

class HttpDownloader:
    def __init__(self, session: Session | None = None):
        if not session:
            self.session = Session()
        else:
            self.session = session

    def download(self, url: str, dest_tmp: Path, item_id: str, progress_cb: Callable[[ProgressEvent], None] | None) -> int:
        ...