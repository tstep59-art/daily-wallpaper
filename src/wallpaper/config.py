"""Constants shared across modules. Spot data lives in data/spots.json."""

from datetime import timedelta, timezone

KST = timezone(timedelta(hours=9))
# Kept as day/night command-line compatibility values; fine-grained ambience is selected by KST hour.
SLOTS = ("day", "night")

SEOUL_LATITUDE = 37.5665
SEOUL_LONGITUDE = 126.9780
GEN_WIDTH = 880
GEN_HEIGHT = 1920
EDGE_TRIM_RATIO = 0.07
WALLPAPER_WIDTH = 1179
WALLPAPER_HEIGHT = 2556
DEFAULT_MODEL = "@cf/black-forest-labs/flux-2-klein-4b"
MAX_ATTEMPTS = 3
