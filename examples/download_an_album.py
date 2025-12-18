from pybuz import QobuzClient, DownloadService
from pybuz import qualities
from pybuz import extract_album_id

# 1. Setup your credentials
USER_ID = "your-user-id"
AUTH_TOKEN = "your-token"

# 2. Create client
client = QobuzClient(user_id=USER_ID, auth_token=AUTH_TOKEN)

# 3. Create download service
service = DownloadService(client)

# 4. Download an album
album_id = extract_album_id("your-album-url")

def progress_handler(event):
    if event.phase == "finished":
        mb = event.bytes_done / (1024 * 1024)
        print(f"  ✅ {event.track_number:02d}. {event.track_name}: {mb:.1f} MB")

service.download_album(
    album_id=album_id,
    dest_dir="./downloads",
    quality=qualities.HIRES_MAX,
    progress_cb=progress_handler
)
