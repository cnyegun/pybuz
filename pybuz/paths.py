from pathlib import Path
from .data_models import Album, DownloadRequest, Track
import re

def sanitize_filename(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    out: list[str] = []
    illegals_ch = {'|', '/', '\\', ':', '*', '?', '\"', '<', '>'}
    for ch in text:
        if ch in illegals_ch:
            out.append('_')
        else:
            out.append(ch)
    return "".join(out).strip()

def album_dir(album: Album, req: DownloadRequest) -> Path:
    return req.dest_dir / sanitize_filename(f"{album.artist} - {album.title}") 

def track_final_path(album_path: Path, track: Track, index: int, ext: str) -> Path:
    return album_path / sanitize_filename(f"{index:02} - {track.title}{ext}")

def temp_path(final_path: Path) -> Path:
    return final_path.with_suffix(final_path.suffix + ".part")