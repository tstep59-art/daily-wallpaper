
"""Build varied, colorful, weather-aware prompts for daily smartphone wallpapers."""

import random
from datetime import date

from .spot_selector import Spot


STYLES = {
    "landscape": (
        "Premium photorealistic landscape photography, breathtaking natural scenery, "
        "cinematic composition, realistic camera details, rich vivid natural colors, "
        "beautiful atmospheric lighting, deep blues, emerald greens and warm golden tones. "
        "Create a sophisticated and visually immersive scene."
    ),
    "animal": (
        "High-quality colorful wildlife and nature photography. Feature a charming, "
        "adorable animal with realistic anatomy, detailed natural fur or feathers, "
        "and a gentle expressive personality. The animal should look naturally cute, "
        "not cartoonish or childish. Use rich natural colors and beautiful cinematic light. "
        "Show the animal's full body or at least most of its body in its environment. "
        "The animal should occupy approximately 30 to 50 percent of the image. "
        "Never use an extreme close-up, face-only portrait, or oversized head."
    ),
    "aesthetic": (
        "Sophisticated contemporary digital art and fine-art visual design. "
        "Creative surrealism, cinematic 3D art, imaginative architecture, "
        "abstract forms, futuristic scenery and artistic landscapes. "
        "Use bold yet harmonious colors, deep blue, emerald, charcoal, orange, "
        "violet and tasteful contrasting accents. "
        "A refined, modern, visually striking atmosphere, not overly cute or childish."
    ),
}

# Approximate distribution: landscape 40%, animal 30%, aesthetic 30%.
_STYLE_WEIGHTS = {
    "landscape": 4,
    "animal": 3,
    "aesthetic": 3,
}

_SEASON_PHRASES = {
    "spring": (
        "spring atmosphere, fresh green leaves, blooming trees, "
        "clear gentle sunlight and lively natural colors"
    ),
    "summer": (
        "summer atmosphere, lush green nature, vivid colors, "
        "bright sunlight and refreshing scenery"
    ),
    "autumn": (
        "autumn atmosphere, golden and red foliage, "
        "warm rich colors and crisp air"
    ),
    "winter": (
        "winter atmosphere, beautiful snow, crisp air, "
        "cool blue tones and peaceful winter scenery"
    ),
}

_TIME_PHRASES = {
    "day": (
        "daytime lighting, natural sunlight, clear visual details, "
        "balanced exposure and beautiful vibrant colors"
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
        "night": "partly cloudy sky with moonlight between the clouds",
    },
    "overcast": {
        "day": "dramatic cloudy sky and soft diffused daylight",
        "night": "cloudy night sky and atmospheric low-light scenery",
    },
    "fog": {
        "day": "mysterious morning mist, atmospheric fog and soft light",
        "night": "dreamlike night fog and mysterious atmospheric lighting",
    },
    "rain": {
        "day": "fresh rain, wet surfaces, reflections and moody natural lighting",
        "night": "rainy night, glowing reflections and cinematic lighting",
    },
    "snow": {
        "day": "beautiful snowfall, fresh white snow and soft winter light",
        "night": "snow falling under beautiful nighttime lights",
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
        subject = (
            f"Scene: {spot.visual}. "
            "Show a wide, immersive view of the surrounding environment. "
            "The scenery is the main subject, not a close-up object."
        )
    elif style_name == "animal":
        subject = (
            "Create a charming wildlife scene. Choose an appealing animal such as "
            "a fox, red panda, otter, rabbit, squirrel, cat, dog, deer or other "
            "interesting animal. Vary the animal between generations. "
            "Show it naturally walking, sitting, playing, exploring or resting "
            "in a beautiful environment such as a forest, meadow, riverside or snowy landscape. "
            "Include plenty of visible scenery around the animal. "
            "Avoid extreme close-ups, face-only portraits and studio backgrounds."
        )
    else:
        subject = (
            "Create an original artistic wallpaper with a strong visual concept. "
            "Explore imaginative landscapes, surreal architecture, futuristic cities, "
            "cinematic 3D environments, abstract geometry or visually striking natural forms. "
            "Use a sophisticated and balanced color palette. "
            "Avoid overly feminine decorations, excessive pink, excessive pastel colors, "
            "floral patterns and childish cartoon aesthetics."
        )

    return (
        f"{style_phrase} {subject} "
        f"Season: {season_phrase}. "
        f"Weather: {weather_phrase}. "
        f"Time: {time_phrase}. "
        "Vertical 9:16 smartphone wallpaper composition. "
        "Carefully balanced composition with some calm visual space near the top "
        "for the phone clock and notifications. "
        "The main subject must be clearly visible without filling the entire frame. "
        "Full color image only. Absolutely no black and white, monochrome, "
        "grayscale, ink wash or desaturated treatment. "
        "High detail, beautiful professional quality. "
        "No text, no letters, no watermark, no logo, no borders."
    )


def _lookup(table: dict, key: str, label: str):
    try:
        return table[key]
    except KeyError:
        raise ValueError(f"unknown {label}: {key!r}") from None
