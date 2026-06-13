#!/usr/bin/env python3
"""Rebuild gallery.html grid from gallery-manifest.json."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "Gallery" / "gallery-manifest.json").read_text(encoding="utf-8"))


def text(value: str) -> str:
    return html.escape(value.replace("\u2014", " - "))


def build_filters() -> str:
    lines = [
        '        <div class="gallery-filters" role="toolbar" aria-label="Filter project gallery">',
        '          <button type="button" class="gallery-filter is-active" data-filter="all">All Projects</button>',
    ]
    for category in manifest["categories"]:
        lines.append(
            f'          <button type="button" class="gallery-filter" data-filter="{text(category)}">{text(category)}</button>'
        )
    lines.append("        </div>")
    return "\n".join(lines)


def build_grid() -> str:
    lines = []
    for item in manifest["items"]:
        title = item["title"].replace("\u2014", " - ")
        caption = f"{title} - {item['description']}"
        lines.append(
            f'          <figure class="gallery-item" data-category="{text(item["category"])}">'
            f'<a class="gallery-img-link" href="Gallery/{text(item["file"])}" data-caption="{text(caption)}">'
            f'<img src="Gallery/{text(item["file"])}" alt="{text(item["alt"])}" loading="lazy" decoding="async"></a>'
            f"<figcaption><strong>{text(title)}</strong><span>{text(item['description'])}</span></figcaption></figure>"
        )
    return "\n".join(lines)


gallery_path = ROOT / "gallery.html"
content = gallery_path.read_text(encoding="utf-8")
start = content.index('<div class="section-heading">')
end = content.index('<section class="inner-cta">')

replacement = f"""        <div class="section-heading">
          <p class="eyebrow">Real project photos</p>
          <h2>Completed Remodels &amp; Renovations</h2>
          <p>Browse kitchen remodels, bathroom renovations, before-and-after projects, outdoor builds, and interior upgrades completed by JNS in Palm Harbor and surrounding areas.</p>
        </div>
{build_filters()}
        <div class="gallery-grid" id="gallery-grid">
{build_grid()}
        </div>
      </div>
    </section>

    """

gallery_path.write_text(content[:start] + replacement + content[end:], encoding="utf-8")
print(f"Updated gallery.html with {len(manifest['items'])} images")
