#!/usr/bin/env python3
"""Replace inline header/footer with dynamic include slots on all JNS HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADER_SLOT = '<div id="site-header-include"></div>'
FOOTER_SLOT = '<div id="site-footer-include"></div>'

HEADER_RE = re.compile(
    r"<header class=\"site-header\"[\s\S]*?</header>",
    re.IGNORECASE,
)
MOBILE_TAIL_RE = re.compile(
    r"\s*(?:<!--[^\n]*MOBILE NAV[^\n]*-->\s*)?"
    r"<div class=\"nav-overlay\"[\s\S]*?</nav>\s*",
    re.IGNORECASE,
)
FOOTER_RE = re.compile(
    r"<footer class=\"site-footer\">[\s\S]*?</footer>",
    re.IGNORECASE,
)

SERVICE_MEDIA = {
    "general-construction": {
        "photos": [
            ("Gallery/garage-remodel-workshop.webp", "Garage remodel and workshop build-out"),
            ("Gallery/kitchen-remodel-before-after.webp", "Residential addition before and after"),
        ],
        "why": [
            "Written scopes before any structural work begins",
            "Permit management included where required",
            "Field-led supervision on every jobsite",
            "Licensed CRC1334879 — DBPR verifiable",
        ],
    },
    "renovations-upgrades": {
        "photos": [
            ("Gallery/kitchen-remodel-charcoal-cabinets.webp", "Kitchen remodel with charcoal cabinets"),
            ("Gallery/small-bathroom-remodel.webp", "Bathroom renovation upgrade"),
        ],
        "why": [
            "Kitchen and bath remodel specialists",
            "Material selections documented in writing",
            "Before-and-after documentation on completed jobs",
            "Serving Pinellas County homeowners",
        ],
    },
    "repairs-corrective-work": {
        "photos": [
            ("Gallery/walk-in-shower-remodel.webp", "Shower repair and remodel"),
            ("Gallery/bathroom-garage-addition-before-after.webp", "Corrective addition and repair work"),
        ],
        "why": [
            "Code corrections handled fully",
            "Damage repair with written scope",
            "No shortcuts on structural fixes",
            "One accountable contractor",
        ],
    },
    "project-coordination": {
        "photos": [
            ("Gallery/living-room-open-concept-remodel.webp", "Open concept interior coordination"),
            ("Gallery/kitchen-dining-two-tone-remodel.webp", "Multi-trade kitchen and dining remodel"),
        ],
        "why": [
            "Single point of contact for all trades",
            "Schedule and budget oversight",
            "Written milestones and updates",
            "Punch-list close-out included",
        ],
    },
}


def depth_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.parent == Path("."):
        return ""
    return "../" * len(rel.parent.parts)


def ensure_assets(html: str, prefix: str) -> str:
    shared = f'{prefix}CSS/site-shared.css'
    if shared in html or "./CSS/site-shared.css" in html or "../CSS/site-shared.css" in html:
        return html
    styles_href = f'{prefix}styles.css' if prefix else "./styles.css"
    needle = f'<link rel="stylesheet" href="{styles_href}" />'
    if needle in html:
        return html.replace(
            needle,
            needle + f'\n  <link rel="stylesheet" href="{shared}" />',
            1,
        )
    return html


def ensure_scripts(html: str, prefix: str) -> str:
    includes_src = f'{prefix}includes.js'
    if includes_src not in html:
        html = html.replace(
            '<script src="',
            f'<script src="{includes_src}" defer></script>\n  <script src="',
            1,
        )
    return html


def gallery_path(prefix: str, rel: str) -> str:
    if rel.startswith("Gallery/"):
        return f"{prefix}{rel}"
    return rel


def service_expansion_block(slug: str, prefix: str) -> str:
    data = SERVICE_MEDIA.get(slug)
    if not data:
        return ""
    photos = data["photos"]
    why_items = "".join(f"              <li>{item}</li>\n" for item in data["why"])
    figures = ""
    for src, cap in photos:
        figures += (
            f"            <figure>\n"
            f"              <img src=\"{gallery_path(prefix, src)}\" alt=\"{cap}\" width=\"800\" height=\"600\" loading=\"lazy\" decoding=\"async\">\n"
            f"              <figcaption>{cap}</figcaption>\n"
            f"            </figure>\n"
        )
    marker = "<!-- See Our Work -->"
    if marker not in open(ROOT / "services" / f"{slug}.html", encoding="utf-8").read():
        return ""
    block = f"""
    <!-- Project photos & why JNS -->
    <section class="inner-section inner-section--panel service-media-section">
      <div class="container service-media-layout">
        <div class="service-media-copy">
          <p class="eyebrow">Proof of work</p>
          <h2>Recent Projects &amp; Field Results</h2>
          <p>Every image below is from a completed JNS Construction Services project in Pinellas County or a nearby community. We document kitchen remodels, bathroom renovations, additions, and corrective work so homeowners know what to expect before signing a scope.</p>
          <div class="service-photo-grid">
{figures}          </div>
          <p class="service-media-note">Want more examples? Browse the <a href="/gallery.html">full project gallery</a> or call <a href="tel:+17272651120">(727) 265-1120</a> to discuss similar work at your property.</p>
        </div>
        <aside class="service-media-aside">
          <div class="about-card">
            <h3>Why JNS for This Service</h3>
            <ul class="about-list">
{why_items}            </ul>
            <a class="btn btn-primary btn-full" href="tel:+17272651120">Call (727) 265-1120</a>
          </div>
        </aside>
      </div>
    </section>

"""
    return block


def patch_service_page(path: Path, prefix: str) -> None:
    slug = path.stem
    text = path.read_text(encoding="utf-8")
    block = service_expansion_block(slug, prefix)
    marker = "    <!-- See Our Work -->"
    if block and marker in text and "service-media-section" not in text:
        text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding="utf-8")


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    prefix = depth_prefix(path)

    if "site-header-include" not in text:
        text = HEADER_RE.sub(HEADER_SLOT, text, count=1)

    if "site-footer-include" not in text:
        text = FOOTER_RE.sub(FOOTER_SLOT, text, count=1)

    text = MOBILE_TAIL_RE.sub("\n", text, count=1)

    text = ensure_assets(text, prefix if prefix else "./")

    script_prefix = prefix or "./"
    if f'{script_prefix}includes.js' not in text:
        text = text.replace(
            '<script src="',
            f'<script src="{script_prefix}includes.js" defer></script>\n  <script src="',
            1,
        )

    path.write_text(text, encoding="utf-8")
    if path.parent.name == "services":
        patch_service_page(path, prefix)


def main() -> None:
    for html in ROOT.rglob("*.html"):
        if html.name in {"header.html", "footer.html"}:
            continue
        patch_file(html)
        print(f"patched {html.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
