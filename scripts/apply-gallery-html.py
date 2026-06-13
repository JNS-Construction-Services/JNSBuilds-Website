#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "Gallery" / "gallery-manifest.json").read_text(encoding="utf-8"))


def text(value: str) -> str:
    cleaned = value.replace(" \u2014 ", " - ").replace("\u2014", " - ")
    return html.escape(cleaned)


def build_filters() -> str:
    lines = [
        '<div class="gallery-filters" role="toolbar" aria-label="Filter project gallery">',
        '  <button type="button" class="gallery-filter is-active" data-filter="all">All Projects</button>',
    ]
    for category in manifest["categories"]:
        lines.append(
            f'  <button type="button" class="gallery-filter" data-filter="{text(category)}">{text(category)}</button>'
        )
    lines.append("</div>")
    return "\n".join(lines)


def build_grid() -> str:
    lines = []
    for item in manifest["items"]:
        title = item["title"].replace("\u2014", " - ")
        description = item["description"]
        caption = f"{title} - {description}"
        lines.append(
            f'          <figure class="gallery-item" data-category="{text(item["category"])}">'
            f'<a class="gallery-img-link" href="Gallery/{text(item["file"])}" data-caption="{text(caption)}">'
            f'<img src="Gallery/{text(item["file"])}" alt="{text(item["alt"])}" loading="lazy"></a>'
            f'<figcaption><strong>{text(title)}</strong><span>{text(description)}</span></figcaption></figure>'
        )
    return "\n".join(lines)


def build_carousel() -> str:
    featured = sorted(
        [item for item in manifest["items"] if item.get("featured")],
        key=lambda item: item.get("carousel_order") or 99,
    )
    lines = []
    for item in featured:
        title = item["title"].replace("\u2014", " - ")
        lines.append(
            f'              <figure class="gallery-item carousel-slide"><a class="gallery-img-link" href="/gallery.html">'
            f'<img src="Gallery/{text(item["file"])}" alt="{text(item["alt"])}" loading="lazy" decoding="async"></a>'
            f'<figcaption>{text(title)}</figcaption></figure>'
        )
    return "\n".join(lines)


def replace_between(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = content.index(start_marker)
    end = content.index(end_marker, start)
    return content[:start] + replacement + content[end:]


gallery_path = ROOT / "gallery.html"
gallery = gallery_path.read_text(encoding="utf-8")
gallery = replace_between(
    gallery,
    '        <div class="section-heading">',
    '        </div>\n      </div>\n    </section>\n\n    <section class="inner-cta">',
    f'''        <div class="section-heading">
          <p class="eyebrow">Real project photos</p>
          <h2>Completed Remodels &amp; Renovations</h2>
          <p>Browse kitchen remodels, bathroom renovations, before-and-after projects, outdoor builds, and interior upgrades completed by JNS in Palm Harbor and surrounding areas.</p>
        </div>
{build_filters()}
        <div class="gallery-grid" id="gallery-grid">
{build_grid()}
        </div>''',
)
gallery_path.write_text(gallery, encoding="utf-8")

index_path = ROOT / "index.html"
index = index_path.read_text(encoding="utf-8")
index = replace_between(
    index,
    '            <div class="carousel-track">\n',
    '            </div>\n          </div>\n          <button class="carousel-btn carousel-next"',
    f'            <div class="carousel-track">\n{build_carousel()}\n',
)
index_path.write_text(index, encoding="utf-8")
print("Updated gallery.html and index.html")
