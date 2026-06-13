#!/usr/bin/env python3
"""Convert gallery source images to optimized WebP and write gallery-manifest.json."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "Gallery"
SOURCE = GALLERY / "_source"
MANIFEST = GALLERY / "gallery-manifest.json"

MAX_WIDTH = 1600
WEBP_QUALITY = 82

# source filename -> catalog entry (None source = already webp, rename only)
CATALOG = [
    {
        "source": "Kitchen Remodel (Cabinetry, Countertops, Backsplash, Paint).jpeg",
        "file": "kitchen-remodel-charcoal-cabinets.webp",
        "category": "Kitchen Remodel",
        "title": "Kitchen Remodel — Charcoal Cabinets",
        "description": "Custom cabinetry, quartz countertops, patterned backsplash, and paint in a modern kitchen renovation.",
        "featured": True,
        "carousel_order": 4,
    },
    {
        "source": "Kitchen Remodel (Cabinetry, Countertops, Flooring, Backsplash, Trim, Lighting, Paint, Windows, Doors).jpeg",
        "file": "kitchen-remodel-full-scope.webp",
        "category": "Kitchen Remodel",
        "title": "Kitchen Remodel — Full Scope",
        "description": "Complete kitchen renovation with cabinetry, countertops, flooring, backsplash, trim, lighting, paint, windows, and doors.",
        "featured": False,
    },
    {
        "source": "Kitchen Remodel with Custom Meal Prep Bar  (Cabinetry, Countertops, Flooring, Backsplash, Trim, Lighting, Paint).jpeg",
        "file": "kitchen-remodel-meal-prep-bar.webp",
        "category": "Kitchen Remodel",
        "title": "Kitchen Remodel — Custom Meal Prep Bar",
        "description": "Kitchen renovation featuring a custom meal prep bar, cabinetry, countertops, flooring, backsplash, trim, lighting, and paint.",
        "featured": True,
        "carousel_order": 6,
    },
    {
        "source": "Galley Kitchen Remodel (Cabinetry, Countertops, Flooring, Backsplash, Lighting, Paint).jpeg",
        "file": "galley-kitchen-remodel.webp",
        "category": "Kitchen Remodel",
        "title": "Galley Kitchen Remodel",
        "description": "Galley kitchen renovation with new cabinetry, countertops, flooring, backsplash, lighting, and paint.",
        "featured": False,
    },
    {
        "source": "Full Kitchen Remodel - Before & After.PNG",
        "file": "kitchen-remodel-before-after.webp",
        "category": "Before & After",
        "title": "Full Kitchen Remodel — Before & After",
        "description": "Side-by-side before and after photos of a complete kitchen remodel.",
        "featured": True,
        "carousel_order": 1,
    },
    {
        "source": "Room Remodel (2).jpeg",
        "file": "kitchen-dining-two-tone-remodel.webp",
        "category": "Kitchen Remodel",
        "title": "Kitchen & Dining Remodel — Two-Tone",
        "description": "Open kitchen and dining renovation with charcoal island cabinetry, white uppers, quartz counters, and wood-look flooring.",
        "featured": True,
        "carousel_order": 3,
    },
    {
        "source": "Small Bathroom Remodel (Custom Shower, Vanity, Countertop, Glass Block Window, Lighting, Flooring, Trim, Texture, Paint).jpeg",
        "file": "small-bathroom-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Small Bathroom Remodel",
        "description": "Custom shower, vanity, countertop, glass block window, lighting, flooring, trim, texture, and paint.",
        "featured": True,
        "carousel_order": 5,
    },
    {
        "source": "Main Bathroom Remodel (Walk-In Shower, Custom Vanity, Countertop, Lighting, Flooring, Trim, Texture, Paint).jpeg",
        "file": "main-bathroom-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Main Bathroom Remodel",
        "description": "Walk-in shower, custom vanity, countertop, lighting, flooring, trim, texture, and paint in a main bath renovation.",
        "featured": False,
    },
    {
        "source": "Guest Bathroom Remodel (Shower-Tub, Vanity, Backsplash, Flooring, Lighting, Trim, Texture, Paint).jpeg",
        "file": "guest-bathroom-shower-tub-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Guest Bathroom Remodel — Shower-Tub",
        "description": "Guest bath renovation with shower-tub combo, vanity, backsplash, flooring, lighting, trim, texture, and paint.",
        "featured": False,
    },
    {
        "source": "Guest Bathroom Remodel (Shower, Vanity, Trim, Texture, Paint).jpeg",
        "file": "guest-bathroom-shower-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Guest Bathroom Remodel — Walk-In Shower",
        "description": "Guest bathroom update with walk-in shower, vanity, trim, texture, and paint.",
        "featured": False,
    },
    {
        "source": "Shower Remodel.jpeg",
        "file": "walk-in-shower-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Walk-In Shower Remodel",
        "description": "Modern walk-in shower with textured wall tile, hex floor tile, built-in niche, corner bench, and safety grab bars.",
        "featured": True,
        "carousel_order": 7,
    },
    {
        "source": "bathroom counter.webp",
        "file": "bathroom-vanity-remodel.webp",
        "category": "Bathroom Remodel",
        "title": "Bathroom Vanity Remodel",
        "description": "Bathroom renovation with dark vanity cabinetry, vessel sink, decorative mirror, and wood-look flooring.",
        "featured": False,
    },
    {
        "source": "home-8632.webp",
        "file": "master-bathroom-double-vanity.webp",
        "category": "Bathroom Remodel",
        "title": "Master Bathroom — Double Vanity & Walk-In Shower",
        "description": "Master bath remodel with double vanity, marble-look shower tile, pebble shower floor, and terracotta floor tile.",
        "featured": False,
    },
    {
        "source": "Main Bathroom, Mudroom, and 2 Car Garage Addition - Before & After.PNG",
        "file": "bathroom-garage-addition-before-after.webp",
        "category": "Before & After",
        "title": "Bathroom, Mudroom & Garage Addition — Before & After",
        "description": "Before and after collage of a main bathroom, mudroom, and two-car garage addition project.",
        "featured": True,
        "carousel_order": 2,
    },
    {
        "source": "Grey Modern Home Before After Instagram Post.PNG",
        "file": "home-renovation-before-after-1.webp",
        "category": "Before & After",
        "title": "Home Renovation — Before & After",
        "description": "Before and after comparison of a full home renovation project.",
        "featured": False,
    },
    {
        "source": "Grey Modern Home Before After Instagram Post (1).PNG",
        "file": "home-renovation-before-after-2.webp",
        "category": "Before & After",
        "title": "Home Renovation — Before & After (2)",
        "description": "Before and after collage highlighting interior and exterior renovation results.",
        "featured": False,
    },
    {
        "source": "Gray Minimalist Before After Photo Collage Instagram Post.PNG",
        "file": "home-renovation-before-after-3.webp",
        "category": "Before & After",
        "title": "Renovation Collage — Before & After",
        "description": "Minimalist before and after photo collage from a residential remodel.",
        "featured": False,
    },
    {
        "source": "Gazebo (Concrete Footers, 12' x 12' Gazebo).jpeg",
        "file": "gazebo-12x12-concrete-footers.webp",
        "category": "Outdoor & Additions",
        "title": "12' x 12' Gazebo — Concrete Footers",
        "description": "Custom gazebo build with poured concrete footers and full 12' x 12' structure.",
        "featured": False,
    },
    {
        "source": "Outdoor Cabinets.jpeg",
        "file": "outdoor-kitchen-cabinets.webp",
        "category": "Outdoor & Additions",
        "title": "Outdoor Kitchen Cabinets",
        "description": "Built-in outdoor kitchen with charcoal shaker cabinets, stone countertops, and stainless beverage fridge.",
        "featured": True,
        "carousel_order": 8,
    },
    {
        "source": "Room remodel.jpeg",
        "file": "garage-remodel-workshop.webp",
        "category": "Interior Renovation",
        "title": "Garage Remodel — Cabinets & Workshop",
        "description": "Multi-functional garage renovation with custom cabinetry, epoxy flooring, laundry station, and workshop area.",
        "featured": False,
    },
    {
        "source": "Room Remodel (3).jpeg",
        "file": "living-room-open-concept-remodel.webp",
        "category": "Interior Renovation",
        "title": "Living Room — Open Concept Remodel",
        "description": "Open living and dining renovation with vaulted ceiling, skylight, new flooring, and updated lighting.",
        "featured": False,
    },
    {
        "source": "room remodel2.jpeg",
        "file": "laundry-room-built-in-cabinets.webp",
        "category": "Interior Renovation",
        "title": "Laundry Room — Built-In Cabinets",
        "description": "Laundry room renovation with white shaker built-ins, stone countertop, stacked appliances, and epoxy flooring.",
        "featured": False,
    },
    {
        "source": "Room Remodel (4).jpeg",
        "file": "sunroom-custom-cabinets.webp",
        "category": "Interior Renovation",
        "title": "Sunroom — Custom Cabinets",
        "description": "Sunroom renovation with custom white cabinets, quartz countertop, and tile flooring.",
        "featured": False,
    },
    {
        "source": "Refinished Room.jpeg",
        "file": "interior-remodel-bedroom.webp",
        "category": "Interior Renovation",
        "title": "Interior Remodel — Bedroom Refresh",
        "description": "Room renovation with new flooring, paint, recessed lighting, ceiling fan, and replacement window.",
        "featured": False,
    },
    {
        "source": "Laundry Room Space.jpeg",
        "file": "laundry-room-white-cabinets.webp",
        "category": "Interior Renovation",
        "title": "Laundry Room Renovation",
        "description": "Laundry room update with white shaker cabinets, utility sink, grey tile flooring, and folding station.",
        "featured": False,
    },
]

# Skip known duplicate sources (same bytes as another catalog entry)
SKIP_SOURCES = {
    "Grey Modern Home Before After Instagram Post (2).PNG",
    "Gray Minimalist Before After Photo Collage Instagram Post (1).PNG",
}


def file_hash(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug_alt(title: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", " ", title).strip()
    return f"{base} by JNS Construction Services in Palm Harbor, FL"


def convert_image(source: Path, dest: Path) -> None:
    if source.suffix.lower() == ".webp" and source.resolve() == dest.resolve():
        return

    with Image.open(source) as image:
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        width, height = image.size
        if width > MAX_WIDTH:
            new_height = round(height * (MAX_WIDTH / width))
            image = image.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        if image.mode == "RGBA":
            image.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
        else:
            image.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)


def archive_source(path: Path) -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    target = SOURCE / path.name
    if path.exists() and not target.exists():
        shutil.move(str(path), str(target))


def main() -> None:
    seen_hashes: dict[str, str] = {}
    manifest_items: list[dict] = []

    for entry in CATALOG:
        source_name = entry["source"]
        if source_name in SKIP_SOURCES:
            print(f"skip duplicate: {source_name}")
            continue

        source_path = GALLERY / source_name
        if not source_path.exists():
            source_path = SOURCE / source_name
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source image: {source_name}")

        digest = file_hash(source_path)
        if digest in seen_hashes:
            print(f"skip hash duplicate: {source_name} == {seen_hashes[digest]}")
            continue
        seen_hashes[digest] = source_name

        dest_path = GALLERY / entry["file"]
        convert_image(source_path, dest_path)

        if source_path.parent == GALLERY:
            archive_source(source_path)

        manifest_items.append(
            {
                "file": entry["file"],
                "category": entry["category"],
                "title": entry["title"],
                "description": entry["description"],
                "alt": slug_alt(entry["title"]),
                "featured": entry.get("featured", False),
                "carousel_order": entry.get("carousel_order"),
            }
        )

    # Move skipped duplicates and unlisted loose files to _source
    for path in list(GALLERY.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".jpeg", ".jpg", ".png"} or path.name in SKIP_SOURCES:
            archive_source(path)
        elif path.name.endswith(".webp") and path.name not in {item["file"] for item in manifest_items}:
            archive_source(path)

    manifest = {
        "categories": [
            "Kitchen Remodel",
            "Bathroom Remodel",
            "Before & After",
            "Outdoor & Additions",
            "Interior Renovation",
        ],
        "items": manifest_items,
    }

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(manifest_items)} images to manifest")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
