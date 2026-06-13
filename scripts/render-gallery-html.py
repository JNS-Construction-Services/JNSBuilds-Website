#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "Gallery" / "gallery-manifest.json").read_text(encoding="utf-8"))
OUT = ROOT / "_gallery-html.txt"


def text(value: str) -> str:
    return html.escape(value.replace("\u2014", " - "))


lines: list[str] = []
lines.append("=== FILTERS ===")
lines.append('<div class="gallery-filters" role="toolbar" aria-label="Filter project gallery">')
lines.append('  <button type="button" class="gallery-filter is-active" data-filter="all">All Projects</button>')
for category in manifest["categories"]:
    lines.append(f'  <button type="button" class="gallery-filter" data-filter="{text(category)}">{text(category)}</button>')
lines.append("</div>")
lines.append("")
lines.append("=== GRID ===")
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
lines.append("")
lines.append("=== CAROUSEL ===")
featured = sorted(
    [item for item in manifest["items"] if item.get("featured")],
    key=lambda item: item.get("carousel_order") or 99,
)
for item in featured:
    title = item["title"].replace("\u2014", " - ")
    lines.append(
        f'              <figure class="gallery-item carousel-slide"><a class="gallery-img-link" href="/gallery.html">'
        f'<img src="Gallery/{text(item["file"])}" alt="{text(item["alt"])}" loading="lazy" decoding="async"></a>'
        f'<figcaption>{text(title)}</figcaption></figure>'
    )

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
