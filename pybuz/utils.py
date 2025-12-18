
def extract_album_id(url: str) -> str:
    return url[url.rfind('/') + 1:]