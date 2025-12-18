from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Track:
    track_id: str
    track_number: int
    title: str
    artist: str
    release_date: datetime

@dataclass(frozen=True, slots=True)
class Album:
    album_id: str
    title: str
    artist: str
    release_date: datetime | None
    tracks: tuple[Track, ...]

@dataclass(frozen=True, slots=True)
class Quality:
    code: str
    description: str

@dataclass(frozen=True, slots=True)
class DownloadRequest:
    dest_dir: Path
    quality: Quality
    overwrite: bool = True

@dataclass(frozen=True, slots=True)
class ResolvedDownload:
    url: str
    ext: str

@dataclass(frozen=True,slots=True)
class DownloadOutcome:
    item_id: str
    status: str
    path: Path | None
    error: str | None

@dataclass(frozen=True,slots=True)
class ProgressEvent:
    phase: str # "resolving" | "downloading" | "finished"
    track_name: str | None
    track_number: int | None
    bytes_done: int | None
    bytes_total: int | None

