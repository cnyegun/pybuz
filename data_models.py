from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Track:
    track_id: str
    title: str
    artist: str
    year: int | None

@dataclass(frozen=True, slots=True)
class Album:
    album_id: str
    title: str
    artist: str
    year: int | None
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
    item_id: str
    phase: str
    bytes_done: int | None
    bytes_total: int | None

