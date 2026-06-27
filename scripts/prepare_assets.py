#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "src" / "assets" / "images"
HERO_SOURCE = IMAGE_DIR / "hero-forest-operations-original.jpeg"

HERO_VARIANTS = [
    ("hero-forest-operations-960.jpeg", 960, "JPEG", {"quality": 82, "progressive": True, "optimize": True}),
    ("hero-forest-operations-1600.jpeg", 1600, "JPEG", {"quality": 84, "progressive": True, "optimize": True}),
    ("hero-forest-operations-960.webp", 960, "WEBP", {"quality": 78, "method": 6}),
    ("hero-forest-operations-1600.webp", 1600, "WEBP", {"quality": 80, "method": 6}),
]


def resize_width(image: Image.Image, width: int) -> Image.Image:
    if image.width <= width:
        return image.copy()
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    if not HERO_SOURCE.exists():
        raise SystemExit(f"Missing hero source image: {HERO_SOURCE}")

    with Image.open(HERO_SOURCE) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        for filename, width, image_format, options in HERO_VARIANTS:
            target = IMAGE_DIR / filename
            resized = resize_width(image, width)
            resized.save(target, image_format, **options)


if __name__ == "__main__":
    main()
