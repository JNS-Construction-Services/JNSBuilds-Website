"""Download Wikimedia Commons photos that actually show each JNS service city."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "cities"
CREDITS = ROOT / "data" / "city-photo-credits.json"
UA = {"User-Agent": "JNSCityPages/1.0 (https://jnsbuilds.com; seo)"}

# Exact Commons filenames — verified as that city, commercial-ok licenses.
FILES = {
    "palm-harbor": "Saint Luke Church (Palm Harbor, Florida) - exterior.jpg",
    "clearwater": "Clearwater Beach, Florida (34733793384).jpg",
    "dunedin": "Dunedin FL downtown01.jpg",
    "tarpon-springs": "Sponge fishing Tarpon Springs FL.jpg",
    "safety-harbor": "Safety harbor city hall pmr 01a.jpg",
    "oldsmar": "Aerial view of Oldsmar, Florida.jpg",
}


def commons_info(filename: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": f"File:{filename}",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime",
            "iiurlwidth": 1800,
        }
    )
    req = urllib.request.Request(
        f"https://commons.wikimedia.org/w/api.php?{params}", headers=UA
    )
    data = json.loads(urllib.request.urlopen(req, timeout=45).read().decode())
    page = next(iter(data["query"]["pages"].values()))
    info = page["imageinfo"][0]
    meta = info.get("extmetadata") or {}
    artist_html = (meta.get("Artist") or {}).get("value", "Wikimedia Commons")
    license_name = (meta.get("LicenseShortName") or {}).get("value", "")
    credit = (meta.get("Credit") or {}).get("value", "")
    thumb = info.get("thumburl") or info.get("url")
    return {
        "file": filename,
        "url": thumb,
        "license": license_name,
        "artist_html": artist_html,
        "credit_html": credit,
        "width": info.get("thumbwidth") or info.get("width"),
        "height": info.get("thumbheight") or info.get("height"),
        "commons": f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(filename)}",
    }


def crop_cover(img: Image.Image, w: int = 1600, h: int = 900) -> Image.Image:
    img = img.convert("RGB")
    src_w, src_h = img.size
    target_ratio = w / h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize((w, h), Image.Resampling.LANCZOS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    credits = {}
    for slug, filename in FILES.items():
        info = commons_info(filename)
        print(f"fetch {slug}: {filename} ({info['license']})")
        req = urllib.request.Request(info["url"], headers=UA)
        raw = urllib.request.urlopen(req, timeout=60).read()
        img = Image.open(BytesIO(raw))
        cover = crop_cover(img)
        dest = OUT / f"{slug}.webp"
        cover.save(dest, "WEBP", quality=82, method=6)
        credits[slug] = {
            "file": filename,
            "local": f"images/cities/{slug}.webp",
            "license": info["license"],
            "commons": info["commons"],
            "artist_html": info["artist_html"],
        }
        print(f"  wrote {dest} {dest.stat().st_size} bytes")
    CREDITS.parent.mkdir(parents=True, exist_ok=True)
    CREDITS.write_text(json.dumps(credits, indent=2), encoding="utf-8")
    print("wrote", CREDITS)


if __name__ == "__main__":
    main()
