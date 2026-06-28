#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "src" / "assets" / "images"
HERO_SOURCE = IMAGE_DIR / "hero-digital-forest-original.png"
PEOPLE_DIR = ROOT / "src" / "assets" / "people"
PEOPLE_ORIGINALS = PEOPLE_DIR / "originals"

HERO_VARIANTS = [
    ("hero-digital-forest-960.jpeg", 960, "JPEG", {"quality": 82, "progressive": True, "optimize": True}),
    ("hero-digital-forest-1600.jpeg", 1600, "JPEG", {"quality": 84, "progressive": True, "optimize": True}),
    ("hero-digital-forest-960.webp", 960, "WEBP", {"quality": 78, "method": 6}),
    ("hero-digital-forest-1600.webp", 1600, "WEBP", {"quality": 80, "method": 6}),
]

PEOPLE_SOURCES = [
    "bridget-guo",
    "gregory-paradis",
    "jamie-iversen",
    "jinming-jimmy-ke",
    "kathleen-coupland",
    "rosalia-jaffray",
    "yancun-walter-yan",
    "yunhao-davis-xu",
]


def resize_width(image: Image.Image, width: int) -> Image.Image:
    if image.width <= width:
        return image.copy()
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def square_center_crop(image: Image.Image) -> Image.Image:
    side = min(image.width, image.height)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    return image.crop((left, top, left + side, top + side))


def people_source_path(slug: str) -> Path:
    matches = sorted(PEOPLE_ORIGINALS.glob(f"{slug}.*"))
    if not matches:
        raise SystemExit(f"Missing people source image: {PEOPLE_ORIGINALS / slug}")
    return matches[0]


def main() -> None:
    if not HERO_SOURCE.exists():
        raise SystemExit(f"Missing hero source image: {HERO_SOURCE}")

    with Image.open(HERO_SOURCE) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        for filename, width, image_format, options in HERO_VARIANTS:
            target = IMAGE_DIR / filename
            resized = resize_width(image, width)
            resized.save(target, image_format, **options)

    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    for slug in PEOPLE_SOURCES:
        with Image.open(people_source_path(slug)) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            headshot = square_center_crop(image).resize((360, 360), Image.Resampling.LANCZOS)
            headshot.save(
                PEOPLE_DIR / f"{slug}-360.jpeg",
                "JPEG",
                quality=86,
                progressive=True,
                optimize=True,
            )
            headshot.save(PEOPLE_DIR / f"{slug}-360.webp", "WEBP", quality=82, method=6)


if __name__ == "__main__":
    main()
