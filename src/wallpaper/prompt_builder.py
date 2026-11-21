
"""Build varied, weather-aware image prompts for daily wallpapers."""

import random
from datetime import date

from .spot_selector import Spot

STYLES = {
    "landscape": (
        "Photorealistic landscape photography, breathtaking natural scenery, "
        "realistic camera details, beautiful atmospheric lighting, rich natural colors, "
        "professional travel photography."
    ),
    "animal": (
        "A beautiful animal as the main subject, lifelike fur or feather details, "
        "natural behavior, expressive eyes, beautifully composed wildlife photography, "
        "soft realistic lighting, high photographic quality."
    ),
    "aesthetic": (
        "A visually stunning artistic scene, imaginative composition, vibrant harmonious "
        "colors, dreamy atmosphere, beautiful light and shadows, refined color grading, "
        "creative fine-art photography."
    ),
}

_STYLE_WEIGHTS = {
    "landscape": 5,
    "animal": 3,
    "aesthetic": 2,
}

_SEASON_PHRASES = {
    "spring": "spring atmosphere, fresh green leaves, delicate blossoms and gentle sunlight",
    "summer": "summer atmosphere, lush green nature, vivid colors and warm sunlight",
    "autumn": "autumn atmosphere, golden and red foliage, warm rich colors",
    "winter": "winter atmosphere, crisp air, snowy scenery and beautiful cool tones",
}

_TIME_PHRASES = {
    "day": (
        "daytime lighting, natural sunlight, clear visual details, "
        "balanced exposure and beautiful bright colors"
    ),
    "night": (
        "nighttime atmosphere, cinematic low-light photography, "
        "beautiful ambient lights, deep rich colors and realistic night lighting"
    ),
}

_WEATHER_PHRASES = {
    "clear": {
        "day": "clear sky, bright sunshine and crisp natural light",
        "night": "clear night sky, visible stars and peaceful moonlight",
    },
    "partly_cloudy": {
        "day": "beautiful scattered clouds and soft sunlight",
        "night": "a partly cloudy sky with moonlight between the clouds",
    },
    "overcast": {
        "day": "soft diffused daylight, dramatic cloudy sky and muted atmosphere",
        "night": "cloudy night sky and atmospheric low-light scenery",
    },
    "fog": {
        "day": "mysterious morning mist, atmospheric fog and soft diffused light",
        "night": "dreamlike night fog and mysterious atmospheric lighting",
    },
    "rain": {
        "day": "fresh rain, wet surfaces, reflections and moody natural lighting",
        "night": "rainy night, glowing reflections and cinematic lighting",
    },
    "snow": {
        "day": "beautiful snowfall, fresh white snow and soft winter light",
        "night": "snow falling under gentle nighttime lights",
    },
    "thunderstorm": {
        "day": "dramatic storm clouds, powerful rain and cinematic atmosphere",
        "night": "dramatic thunderstorm, dark clouds and distant lightning",
    },
    "unknown": {
        "day": "peaceful natural atmosphere and balanced daylight",
        "night": "peaceful nighttime atmosphere and soft ambient lighting",
    },
}


def season_of(day: date) -> str:
    if day.month in (3, 4, 5):
        return "spring"
    if day.month in (6, 7, 8):
        return "summer"
    if day.month in (9, 10, 11):
        return "autumn"
    return "winter"


def choose_style(previous_style: str | None = None, rng=None) -> str:
    """Choose a style while avoiding the immediately previous style."""
    rng = rng or random
    choices = [
        style
        for style, weight in _STYLE_WEIGHTS.items()
        for _ in range(weight)
    ]

    if previous_style in STYLES and len(STYLES) > 1:
        choices = [style for style in choices if style != previous_style]

    return rng.choice(choices)


def build_prompt(
    spot: Spot,
    slot: str,
    season: str,
    condition: str,
    previous_style: str | None = None,
    rng=None,
) -> str:
    style_name = choose_style(previous_style, rng)
    style_phrase = STYLES[style_name]

    time_phrase = _lookup(_TIME_PHRASES, slot, "slot")
    season_phrase = _lookup(_SEASON_PHRASES, season, "season")
    weather_phrase = _lookup(
        _lookup(_WEATHER_PHRASES, condition, "weather condition"),
        slot,
        "slot",
    )

    if style_name == "landscape":
        subject = f"Scene: {spot.visual}."
    elif style_name == "animal":
        subject = (
            "Create a beautiful animal-centered scene. Choose an animal and natural "
            "environment that fit the current season and weather. Do not include a "
            "human or a city as the main subject."
        )
    else:
        subject = (
            "Create an original visually captivating scene inspired by the current "
            "season and weather. Use an imaginative subject and artistic composition."
        )

    return (
        f"{style_phrase} {subject} "
        f"Season: {season_phrase}. "
        f"Weather: {weather_phrase}. "
        f"Time: {time_phrase}. "
        "Vertical smartphone wallpaper composition, edge-to-edge image, "
        "high detail, beautiful professional quality. "
        "No text, no letters, no watermark, no logo, no borders."
    )


def _lookup(table: dict, key: str, label: str):
    try:
        return table[key]
    except KeyError:
        raise ValueError(f"unknown {label}: {key!r}") from None
