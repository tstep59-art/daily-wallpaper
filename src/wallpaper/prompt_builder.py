"""Build varied, scene-aware 16-bit pixel-art prompts for daily smartphone wallpapers."""

import random
from datetime import date

from .spot_selector import Spot

STYLES = {
    "landscape": ("Premium 16-bit RPG pixel art, refined small-to-medium square pixels, deliberate pixel clusters, "
                  "clean stepped edges, detailed materials, nuanced pixel shading, luminous highlights and "
                  "professional game-background composition. Never use a pixel filter over a normal image."),
    "animal": ("Premium 16-bit RPG pixel art with refined square-pixel clusters, clean stepped silhouettes, "
               "detailed materials and nuanced shading. Any animal is a tiny incidental environmental detail, "
               "never a character portrait or focal subject."),
    "aesthetic": ("Premium 16-bit pixel-art game environment, crisp intentional pixel clusters, clean stepped "
                  "outlines, intricate architecture and objects, cohesive lighting and polished retro game art."),
}
_STYLE_WEIGHTS = {"landscape": 8, "animal": 1, "aesthetic": 1}

_SEASON_PHRASES = {
    "spring": "springtime freshness, delicate blossoms and new foliage",
    "summer": "lush summer growth and a clear, refreshing atmosphere",
    "autumn": "seasonal foliage and drifting fallen leaves",
    "winter": "winter details, frost and delicate snow where appropriate",
}
_TIME_PROFILES = {
    "pre_dawn": {
        "label": "새벽", "range": "04:00-06:00",
        "presets": (
            "silent pre-sunrise streets with a few distant lamps",
            "mist drifting through a quiet harbor before sunrise",
            "moonlit garden with dew and a faint horizon glow",
            "sleepy railway platform beneath a fading star field",
            "cloud sea and floating islands just before first light",
            "peaceful window-lit village wrapped in early fog",
        ),
    },
    "morning": {
        "label": "아침", "range": "06:00-09:00",
        "presets": (
            "soft sunrise spilling across rooftops",
            "fresh morning market preparing to open",
            "sunbeams passing through a leafy garden",
            "quiet countryside station in the first warm light",
            "bright seaside promenade with sparkling water",
            "cozy room with sunlight falling across a desk",
        ),
    },
    "day": {
        "label": "낮", "range": "09:00-14:00",
        "presets": (
            "clear midday sky and crisp architectural shadows",
            "lively shopping street full of small discoveries",
            "sunlit fantasy harbor with boats and distant islands",
            "grand clockwork toy city in bright daylight",
            "vibrant coral garden beneath shafts of sunlight",
            "wide floating-island vista above a sea of clouds",
        ),
    },
    "afternoon": {
        "label": "오후", "range": "14:00-17:00",
        "presets": (
            "lazy afternoon light across a quiet town square",
            "warm sunbeams inside a richly detailed gaming room",
            "breezy seaside boardwalk with long soft shadows",
            "winding garden path with drifting petals",
            "airships crossing a vast layered sky",
            "sunlit bakery street with inviting shop windows",
        ),
    },
    "evening": {
        "label": "저녁", "range": "17:00-20:00",
        "presets": (
            "dramatic sunset above a distant skyline",
            "lantern-lit night market coming alive at dusk",
            "harbor lights beginning to shimmer on the water",
            "warm windows and chimney smoke in a storybook town",
            "twilight clock tower with illuminated gears",
            "quiet train platform beneath the last glow of sunset",
        ),
    },
    "night": {
        "label": "밤", "range": "20:00-04:00",
        "presets": (
            "neon reflections along a lively futuristic street",
            "star-filled observatory above a sleeping city",
            "moonlit garden with tiny floating fireflies",
            "enchanted library with floating books and candlelight",
            "dreamlike spaceport beneath distant planets",
            "rainy downtown alley with glowing signs and reflections",
        ),
    },
}
# Six time families, six distinct scene moods each; the image itself is still freshly composed.
_TIME_PROFILES["pre_dawn"]["hours"] = range(4, 6)
_TIME_PROFILES["morning"]["hours"] = range(6, 9)
_TIME_PROFILES["day"]["hours"] = range(9, 14)
_TIME_PROFILES["afternoon"]["hours"] = range(14, 17)
_TIME_PROFILES["evening"]["hours"] = range(17, 20)
_TIME_PROFILES["night"]["hours"] = tuple(list(range(20, 24)) + list(range(0, 4)))

WEATHER_PHRASES = {
    "clear": "clear open sky and crisp natural light",
    "partly_cloudy": "drifting clouds and gentle breaks of sunlight",
    "overcast": "layered clouds and soft diffused light",
    "fog": "soft atmospheric mist and layered depth",
    "rain": "gentle rainfall, tiny droplets and reflective surfaces",
    "snow": "delicate falling snow and quiet winter details",
    "thunderstorm": "distant storm clouds and occasional faraway lightning",
    "unknown": "balanced ambient light and a calm atmosphere",
}
THEMES = {
    "nature": "an expansive natural world of forests, lakes, coastlines, gardens, rivers and countryside",
    "city": "a lively modern city with distinctive streets, rooftops, transit and layered skyline",
    "cyberpunk": "a dense futuristic city with neon signs, elevated trains, rain-slick streets and layered architecture",
    "cozy_room": "a richly detailed cozy retro-gaming room, vintage computer desk, CRT monitor showing a colorful miniature pixel game, keyboard, books, plants and a large window",
    "toy_village": "a grand fantastical clockwork toy city with monumental clock towers, enormous exposed gears, winding keys, spring mechanisms, stacked toy-block buildings, toy trains and mechanical bridges",
    "spirit_realm": "an enchanted spirit garden with luminous plants, ancient trees, floating wisps and magical ponds",
    "cosmic": "an imaginative outer-space vista with planets, nebulae, orbital structures and distant galaxies",
    "fantasy": "a grand fantasy realm with castles, impossible waterfalls, magical bridges and floating islands",
    "underwater": "a tranquil underwater world with coral gardens, sunken ruins, tiny fish and shafts of light",
    "steampunk": "a detailed steampunk town with brass machinery, airships, clockwork towers and intricate rooftops",
    "desert": "a vast desert oasis with sculpted dunes, palm groves, caravan paths and monumental architecture",
    "snow_globe": "a miniature winter town inside a snow globe, warm windows and handcrafted scenery",
    "night_market": "a lively traditional night market with paper lanterns, food stalls, shop signs and narrow lanes",
    "seaside_harbor": "a Mediterranean harbor town with sailboats, waterfront buildings, docks and open sea",
    "magic_library": "a grand magical library interior with towering shelves, spiral stairs, floating books and reading alcoves",
    "retro_arcade": "a vibrant retro arcade interior filled with classic cabinets, vintage game machines and patterned floors",
    "countryside_station": "a quiet Japanese countryside railway station with tracks, crossing signals, utility poles and distant homes",
    "sky_islands": "a fantastical sky-island world with waterfalls spilling into clouds, airships and suspended bridges",
    "storybook_village": "a storybook village with timber cottages, bakery, cobblestone lanes, flower boxes and inviting windows",
    "onsen_town": "a Japanese hot-spring town with wooden inns, steaming baths, stone paths and lanterns",
    "floating_city": "an immense floating city with suspended districts, sky bridges, elevators and layered towers",
    "botanical_dome": "a vast glass botanical dome with exotic plants, winding walkways, water features and intricate glass architecture",
    "aquarium_tunnel": "a spectacular underwater aquarium tunnel surrounded by giant sea creatures, coral and glowing exhibits",
    "mountain_cablecar": "a scenic mountain cable-car station with suspended cabins, dramatic peaks and distant valleys",
    "festival": "a joyful town festival with decorations, food carts, parade floats and illuminated stalls",
    "canal_city": "a picturesque canal city with arched bridges, narrow boats, waterside homes and reflections",
    "lighthouse_coast": "a dramatic lighthouse coast with sea cliffs, small boats, tide pools and distant islands",
    "enchanted_greenhouse": "an enchanted greenhouse filled with unusual plants, glass roofs, hanging vines and tiny magical lights",
    "mushroom_realm": "a whimsical giant mushroom realm with winding paths, oversized fungi, tiny houses and glowing ponds",
    "clockwork_station": "a fantastical railway terminal with giant clocks, brass mechanisms, platforms and miniature locomotives",
    "space_colony": "a lived-in space colony with glass biodomes, orbital walkways, landing pads and a vast planet view",
    "arcane_academy": "a magical academy campus with towers, courtyards, observatories and floating spell fragments",
    "coastal_cliffs": "a bright coastal landscape with layered sea cliffs, hidden coves, beaches and winding paths",
    "waterfall_grotto": "a lush waterfall grotto with stepped cascades, hidden pools, mossy ruins and shafts of light",
    "desert_caravan": "an ancient desert trade route with caravanserai, fabric canopies, market courtyards and monumental gates",
    "medieval_port": "a bustling medieval port with tall ships, stone quays, warehouses, cranes and distant fortifications",
    "winter_village": "a lively winter village with snow-covered roofs, frozen canals, warm shops and festive details",
    "cloud_cafe": "a whimsical cafe floating among clouds with terraces, tiny airships and a vast sky panorama",
    "mechanical_garden": "a fantastical garden of intricate mechanical flowers, turning gears, water channels and tiny automata",
    "dream_train": "a magical night train traveling through impossible landscapes, illuminated carriages and distant stations",
    "abandoned_ruins": "beautifully overgrown ancient ruins with arches, courtyards, fountains and climbing greenery",
    "rainy_alley": "a detailed urban backstreet with awnings, puddles, shopfronts, overhead cables and glowing windows",
    "harbor_festival": "a festive waterfront celebration with boats, lanterns, stalls, bridges and reflections",
    "miniature_world": "a detailed handcrafted miniature world with tiny buildings, winding roads, layered props and playful scale",
}

COMPOSITIONS = (
    "wide panoramic establishing view with generous open space",
    "winding path leading the eye into a deep layered background",
    "elevated viewpoint looking across rooftops and distant scenery",
    "intimate street-level view with a richly detailed environment",
    "waterside composition with reflections and a broad visible horizon",
    "dramatic vertical depth with foreground framing and distant landmarks",
    "peaceful centered composition with balanced visual breathing room",
    "diagonal leading lines and asymmetrical environmental framing",
    "isometric-inspired layered environment viewed from a gentle elevated angle",
    "wide view framed by architecture, foliage or environmental details",
)
MOODS = (
    "peaceful and welcoming", "dreamlike and quietly magical",
    "bright, lively and full of discovery", "serene with soft atmospheric depth",
    "adventurous and expansive", "warm and cozy", "mysterious but inviting",
    "playful and full of tiny environmental stories",
)
AMBIENT_EFFECTS = (
    "tiny drifting square pixel motes and delicate light fragments",
    "subtle floating dust particles caught in shafts of light",
    "gentle wind moving leaves, banners, hanging signs or curtains",
    "small petals drifting across the scene",
    "fireflies and tiny luminous particles near the ground",
    "soft volumetric light rays and carefully placed pixel highlights",
    "small ripples and sparkling reflections on visible water",
    "distant birds or tiny airships as scale-setting details",
    "occasional glowing windows and subtle environmental animation cues",
    "fine rain streaks and crisp puddle reflections where appropriate",
    "delicate snowflakes and soft accumulation where appropriate",
    "thin drifting clouds and layered atmospheric haze",
)
INDOOR_THEMES = {
    "cozy_room", "magic_library", "retro_arcade", "botanical_dome",
    "aquarium_tunnel", "enchanted_greenhouse", "arcane_academy",
}
WEATHER_SENSITIVE_THEMES = set(THEMES) - INDOOR_THEMES - {"cosmic", "space_colony", "underwater"}

def choose_theme(previous_theme: str | None = None, rng=None) -> str:
    rng = rng or random
    choices = [theme for theme in THEMES if theme != previous_theme]
    return rng.choice(choices)

def season_of(day: date) -> str:
    if day.month in (3, 4, 5):
        return "spring"
    if day.month in (6, 7, 8):
        return "summer"
    if day.month in (9, 10, 11):
        return "autumn"
    return "winter"

def choose_style(previous_style: str | None = None, rng=None) -> str:
    rng = rng or random
    choices = [style for style, weight in _STYLE_WEIGHTS.items() for _ in range(weight)]
    if previous_style in STYLES and len(STYLES) > 1:
        choices = [style for style in choices if style != previous_style]
    return rng.choice(choices)

def time_profile_for(hour: int) -> str:
    if not 0 <= hour <= 23:
        raise ValueError(f"hour must be between 0 and 23: {hour!r}")
    for name, profile in _TIME_PROFILES.items():
        if hour in profile["hours"]:
            return name
    raise ValueError(f"no time profile for hour: {hour}")

def build_prompt(
    spot: Spot,
    slot: str,
    season: str,
    condition: str,
    previous_style: str | None = None,
    rng=None,
    previous_theme: str | None = None,
    theme_override: str | None = None,
    hour: int | None = None,
) -> str:
    rng = rng or random
    style_name = choose_style(previous_style, rng)
    theme_name = theme_override or choose_theme(previous_theme, rng)
    if theme_name not in THEMES:
        raise ValueError(f"unknown theme: {theme_name!r}")
    if slot not in ("day", "night"):
        raise ValueError(f"unknown slot: {slot!r}")
    if season not in _SEASON_PHRASES:
        raise ValueError(f"unknown season: {season!r}")
    if condition not in WEATHER_PHRASES:
        raise ValueError(f"unknown weather condition: {condition!r}")

    profile_name = time_profile_for(hour) if hour is not None else ("day" if slot == "day" else "night")
    profile = __TIME_PROFILES[profile_name]
    time_scene = rng.choice(profile["presets"])
    composition = rng.choice(COMPOSITIONS)
    mood = rng.choice(MOODS)
    effect = rng.choice(AMBIENT_EFFECTS)

    subject = f"World: {THEMES[theme_name]}. Moment: {time_scene}. "
    subject += f"Location inspiration (minor detail only): {spot.visual}. "
    subject += f"Season: {season} — {_SEASON_PHRASES[season]}. "
    if theme_name in WEATHER_SENSITIVE_THEMES:
        subject += f"Ambient weather: {WEATHER_PHRASES[condition]}. "
        if condition == "rain" and slot == "night":
            subject += "Rainy night atmosphere. "
        if condition == "snow":
            subject += "gentle snowfall. "
        if season == "winter":
            subject += "winter scenery details. "
    else:
        subject += "Keep the selected setting coherent; do not force outdoor weather into an indoor, underwater or space scene. "
    if theme_name == "cozy_room":
        subject += ("Show a colorful miniature pixel game visibly playing on the CRT, not a blank screen or app icons. "
                    "Capture a lively instant: floating square pixel motes, tiny light fragments and subtle trails. ")
    if theme_name == "toy_village":
        subject += ("Make the clockwork toy-city identity unmistakable: monumental clock tower, oversized interlocking gears, "
                    "toy-block architecture, spring mechanisms and a visible miniature railway. Never depict an ordinary village. ")
    subject += f"Composition: {composition}. Mood: {mood}. Ambient detail: {effect}. "
    subject += "Use a distinct viewpoint, varied scale and layered environmental storytelling. "
    if style_name == "animal":
        subject += "At most one tiny animal may appear as an incidental detail, never a focal point. "
    else:
        subject += "Any small characters or animals must remain tiny incidental details. "

    return (
        f"{STYLES[style_name]} {subject}"
        "16-bit pixel art. Vertical 9:16 smartphone wallpaper, immersive environment, scenery-led composition. "
        "Scenery should occupy 80 to 90 percent of the frame. no large characters. "
        "Keep the upper area visually calm for the phone clock and notifications. "
        "Use crisp small-to-medium square pixels, precise clusters, clean stepped edges, pixel-by-pixel highlights "
        "and shadows, nuanced lighting, intricate materials and premium classic 16-bit RPG game-art finish. "
        "Bright, inviting, luminous exposure with rich variation and clear visual hierarchy. "
        "Avoid oversized coarse pixels, excessive dithering, muddy blocks, blur, painterly brushwork, watercolor, "
        "photorealism, 3D rendering, vector art, chibi or childish cartoon styling. "
        "Dark cliffs and heavy shadow masses must not dominate the foreground. "
        "No large characters, close-up animals, no text, no letters, watermark, logo, border or frame."
    )

def _lookup(table: dict, key: str, label: str):
    try:
        return table[key]
    except KeyError:
        raise ValueError(f"unknown {label}: {key!r}") from None
