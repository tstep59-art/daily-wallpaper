"""Build scenic, high-quality 16-bit pixel-art prompts for daily smartphone wallpapers."""

import random
from datetime import date

from .spot_selector import Spot


# All three variants remain within the same restrained, detailed pixel-art direction.
STYLES = {
    "landscape": (
        "Authentic 16-bit retro RPG game background pixel art, with clearly visible medium-sized square pixels "
        "and deliberate block-by-block pixel clusters. Distinct stepped pixel edges, tile-like foliage, "
        "pixel-shaped highlights, layered mountains, forests and reflective water. "
        "Limited cohesive game-era color palette, carefully grouped shades, strong readable light and shadow. "
        "Looks hand-crafted pixel by pixel, not a painting with a pixel filter."
    ),
    "animal": (
        "Authentic 16-bit retro RPG environment pixel art, made from clearly visible square pixels "
        "and deliberate blocky pixel clusters. Distinct stepped silhouettes, pixel-shaped foliage, "
        "layered mountains, forests and reflective water, with a limited cohesive game-era palette "
        "and readable pixel shading. One tiny animal may appear as a subtle environmental discovery, "
        "never a focal point. It must look hand-crafted pixel by pixel, not filtered artwork."
    ),
    "aesthetic": (
        "Authentic 16-bit pixel-art game scenery, with clearly visible square pixels, chunky deliberate "
        "pixel clusters, stepped outlines and block-built environmental details. Layered natural depth, "
        "small cottages and landscape details, restrained limited palette and carefully grouped pixel shading. "
        "Polished classic retro RPG background art, never abstract poster art or painterly illustration."
    ),
}

# Keep the image overwhelmingly scenery-led; animal appearances are occasional accents.
_STYLE_WEIGHTS = {
    "landscape": 8,
    "animal": 1,
    "aesthetic": 1,
}

_SEASON_PHRASES = {
    "spring": "spring scenery, fresh foliage, delicate blossoms and a gentle seasonal atmosphere",
    "summer": "lush summer scenery, dense foliage and clear, refreshing atmosphere",
    "autumn": "autumn foliage, fallen leaves and a calm seasonal atmosphere",
    "winter": "winter scenery, snow-covered details and crisp, peaceful atmosphere",
}

_TIME_PHRASES = {
    "day": "daytime atmosphere, natural sunlight and clear environmental details",
    "night": "nighttime atmosphere, subtle glowing lights, stars and peaceful ambient lighting",
}

_WEATHER_PHRASES = {
    "clear": {
        "day": "clear sky and crisp natural light",
        "night": "clear night sky, visible stars and gentle moonlight",
    },
    "partly_cloudy": {
        "day": "scattered clouds and soft sunlight",
        "night": "clouds drifting across a moonlit sky",
    },
    "overcast": {
        "day": "layered clouds and soft diffused daylight",
        "night": "cloudy night sky and quiet ambient lighting",
    },
    "fog": {
        "day": "light morning mist and atmospheric depth",
        "night": "soft night fog and mysterious ambient lighting",
    },
    "rain": {
        "day": "gentle rainfall, reflective surfaces and fresh atmosphere",
        "night": "rainy night, tiny reflections and quiet ambient lighting",
    },
    "snow": {
        "day": "gentle snowfall and fresh snow across the scenery",
        "night": "snow falling softly under quiet nighttime lights",
    },
    "thunderstorm": {
        "day": "dramatic storm clouds and distant rainfall",
        "night": "distant lightning behind dramatic storm clouds",
    },
    "unknown": {
        "day": "peaceful natural atmosphere and balanced daylight",
        "night": "peaceful nighttime atmosphere and subtle ambient lighting",
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

    subject = (
        f"Scene inspiration: {spot.visual}. "
        "Interpret this as a wide, immersive environment rather than a literal close-up. "
        "Vary the setting naturally across generations: quiet lakes, forests, coastlines, "
        "mountain villages, riversides, gardens and peaceful countryside."
    )

    if style_name == "animal":
        subject += (
            " Include at most one small animal, such as a cat, fox, rabbit, deer or bird, "
            "occupying only a tiny part of the scene (about 5 to 10 percent of the frame). "
            "It should feel like a quiet discovery within the landscape, not a character portrait."
        )
    else:
        subject += (
            " If any animal or small object appears, keep it tiny and incidental, "
            "never larger than a minor detail in the environment."
        )

    return (
        f"{style_phrase} {subject} "
        f"Season: {season_phrase}. Weather: {weather_phrase}. Time: {time_phrase}. "
        "Vertical 9:16 smartphone wallpaper composition. "
        "Scenery should occupy approximately 80 to 90 percent of the image. "
        "Make the pixel structure unmistakable: visible square pixels at a consistent medium-to-large scale, "
        "chunky grouped pixel clusters, stepped diagonal edges, simplified block-shaped foliage and rocks, "
        "pixel-by-pixel highlights and shadows, and a limited cohesive 16-bit palette. "
        "Avoid tiny noisy dithering and avoid smooth gradients. Absolutely no anti-aliasing, "
        "blur, painterly brushwork, watercolor texture, or smooth digital illustration. "
        "It must look like an authentic classic 16-bit RPG game screenshot, not a normal image with a pixel filter; "
        "not photorealistic, not 3D, not vector art, not chibi, not childish cartoon. "
        "Keep the upper area visually calm enough for the phone clock and notifications. "
        "No large characters, no close-up animals, no text, no letters, no watermark, "
        "no logo, no border, no frame."
    )


def _lookup(table: dict, key: str, label: str):
    try:
        return table[key]
    except KeyError:
        raise ValueError(f"unknown {label}: {key!r}") from None
