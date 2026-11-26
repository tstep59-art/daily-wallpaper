
"""History of recently used spots and image styles."""

import logging
import time

import requests

logger = logging.getLogger(__name__)

HISTORY_KEY = "recent_spot_ids"
STYLE_KEY = "previous_style"
THEME_KEY = "previous_theme"
RECENT_THEMES_KEY = "recent_themes"
THEME_HISTORY_LIMIT = 10


def fetch_history(url: str | None, get=requests.get, timeout: int = 10) -> dict:
    """Fetch previous spot and style history from latest.json."""
    if not url:
        return {}

    try:
        response = get(
            url,
            params={"t": int(time.time())},
            headers={"Cache-Control": "no-cache"},
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()

        recent = data.get(HISTORY_KEY, [])
        style = data.get(STYLE_KEY)
        theme = data.get(THEME_KEY)
        recent_themes = data.get(RECENT_THEMES_KEY, [])

        if not isinstance(recent, list) or not all(
            isinstance(item, str) for item in recent
        ):
            raise TypeError(f"{HISTORY_KEY} is not a list of strings")

        if style is not None and not isinstance(style, str):
            raise TypeError(f"{STYLE_KEY} is not a string")
        if theme is not None and not isinstance(theme, str):
            raise TypeError(f"{THEME_KEY} is not a string")
        if not isinstance(recent_themes, list) or not all(
            isinstance(item, str) for item in recent_themes
        ):
            raise TypeError(f"{RECENT_THEMES_KEY} is not a list of strings")

        return {
            HISTORY_KEY: recent,
            STYLE_KEY: style,
            THEME_KEY: theme,
            RECENT_THEMES_KEY: recent_themes[:THEME_HISTORY_LIMIT],
        }

    except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
        logger.warning(
            "history unavailable (%s); choosing without it",
            type(exc).__name__,
        )
        return {}


def fetch_recent_ids(url: str, get=requests.get, timeout: int = 10) -> list[str]:
    """Backward-compatible helper for recent spot IDs."""
    return fetch_history(url, get, timeout).get(HISTORY_KEY, [])


def record(recent: list[str], spot_id: str, limit: int) -> list[str]:
    """Record the newest spot without duplicates."""
    return [spot_id, *(item for item in recent if item != spot_id)][:limit]



def record_theme(recent: list[str], theme: str, limit: int = THEME_HISTORY_LIMIT) -> list[str]:
    """Record the newest theme and retain a bounded, duplicate-free history."""
    return [theme, *(item for item in recent if item != theme)][:limit]
