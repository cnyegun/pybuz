from .data_models import Quality

MP3_320 = Quality(code="5", description="MP3 320kbps")
CD_QUALITY = Quality(code="6", description="FLAC 16-bit/44.1kHz")
HIRES = Quality(code="7", description="FLAC 24-bit ≤96kHz")
HIRES_MAX = Quality(code="27", description="FLAC 24-bit ≤192kHz")

# Alias
LOSSLESS = CD_QUALITY
MP3 = MP3_320
BEST = HIRES_MAX

class Qualities:
    MP3_320 = MP3_320
    MP3 = MP3
    CD_QUALITY = CD_QUALITY
    LOSSLESS = LOSSLESS
    HIRES = HIRES
    HIRES_MAX = HIRES_MAX
    BEST = BEST

