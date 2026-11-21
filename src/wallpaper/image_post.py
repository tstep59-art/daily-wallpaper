"""Turn the raw generated image into an iPhone-sized grayscale JPEG (trim, cover-fit, crop)."""

import io

from PIL import Image, UnidentifiedImageError

from .config import EDGE_TRIM_RATIO

JPEG_QUALITY = 92


class ImageProcessingError(RuntimeError):
    """The generated data could not be read as an image."""


def to_wallpaper(raw: bytes, width: int, height: int) -> bytes:
    try:
        with Image.open(io.BytesIO(raw)) as source:
            image = source.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageProcessingError("generated data is not a valid image") from exc

    margin_x, margin_y = round(image.width * EDGE_TRIM_RATIO), round(image.height * EDGE_TRIM_RATIO)
    image = image.crop((margin_x, margin_y, image.width - margin_x, image.height - margin_y))

    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (max(width, round(image.width * scale)), max(height, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    cropped = resized.crop((left, top, left + width, top + height))

    # Saved as 3-channel JPEG (neutral chroma costs almost nothing) for maximum iOS compatibility.
    output = io.BytesIO()
    cropped.convert("RGB").save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return output.getvalue()
