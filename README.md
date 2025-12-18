# Pybuz

Minimalistic python library for downloading high-quality music from Qobuz.

## Installation
```bash
git clone https://github.com/cnyegun/pybuz/
pip install -e .
```

## Usage

```python
from pybuz import QobuzClient, DownloadService, qualities

client = QobuzClient(user_id="your_user_id", auth_token="your_auth_token")
service = DownloadService(client)

outcomes = service.download_album(
    album_id="https://www.qobuz.com/album/xyz123",
    dest_dir="./music",
    quality=qualities.BEST,
    overwrite=False
)
```

## Quality Options

```python
from pybuz import qualities

qualities.MP3_320    # MP3 320kbps
qualities.CD_QUALITY # FLAC 16-bit/44.1kHz
qualities.HIRES      # FLAC 24-bit ≤96kHz
qualities.HIRES_MAX  # FLAC 24-bit ≤192kHz
```

## Progress Tracking

```python
def progress_callback(event):
    print(f"{event.phase}: {event.track_name}")

service.download_album(..., progress_cb=progress_callback)
```

## Features

- Multiple quality levels (MP3 to FLAC 24-bit/192kHz)
- Automatic folder organization and file naming
- Progress callbacks and retry logic
- Skip existing files with `overwrite=False`

## File Structure

```
music/
└── Artist - Album/
    ├── 01 - Track One.flac
    └── 02 - Track Two.flac
```

## Requirements

Python 3.10+, requests