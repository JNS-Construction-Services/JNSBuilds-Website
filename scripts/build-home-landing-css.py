#!/usr/bin/env python3
"""Port Screen Team home-landing CSS blocks into JNS home-landing.css."""

from pathlib import Path

ST = Path(r"E:\All Client Websites\Screen-Team-LLC-screen-team-website\styles.css")
OUT = Path(__file__).resolve().parents[1] / "CSS" / "home-landing.css"

lines = ST.read_text(encoding="utf-8").splitlines()

# Inclusive line ranges from Screen Team styles.css (1-based in editor, 0-based slices)
RANGES = [
    (2680, 2967),   # hero panels, cutout, overlay, content, strip entrance
    (2989, 3108),   # trust strip, service-card--media, work teaser cta
    (3436, 3595),   # reveals, slide-enter, hero-enter keyframes
    (3597, 3824),   # hero responsive
    (3999, 4200),   # intent strip, process band, route band (partial)
    (4532, 4605),   # reduced motion
]

chunks: list[str] = []
for start, end in RANGES:
    chunks.extend(lines[start - 1 : end])

css = "\n".join(chunks)

replacements = {
    'url("Images/ScreenTeamBanner-mobile.webp")': 'url("../images/jns-construction-services-hero-mobile.webp")',
    "#b8e6f8": "#e8ffb8",
    "#3da8d8": "#a0cc00",
    "#7ec8e8": "#c9ff1f",
    "#e8f4fc": "#edf5e0",
    "#d4e6f2": "#d8e8c8",
    "#e2f0f8": "#e5f0d8",
    "#c5dced": "#c8dcc0",
    "#9fe8ff": "#d4ff66",
    "#c8deef": "#c5d8b8",
    "#d8f1ff": "#e0f5c8",
    "rgba(61, 168, 216, 0.14)": "rgba(201, 255, 31, 0.14)",
    "rgba(61, 168, 216, 0.42)": "rgba(201, 255, 31, 0.42)",
    "rgba(61, 168, 216, 0.08)": "rgba(201, 255, 31, 0.08)",
    "#0b1825": "#0a1008",
    "#0d1c2e": "#0d140a",
    "rgba(4, 9, 20,": "rgba(6, 13, 8,",
    "rgba(7, 13, 24,": "rgba(10, 16, 10,",
}

for old, new in replacements.items():
    css = css.replace(old, new)

header = """:root {
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --st-hero-shift: 0px;
  --st-band-shift: 0px;
  --strip-delay: 0ms;
  --slide-delay: 0ms;
  --eyebrow-accent: var(--accent);
}

body.home-landing .hero {
  background: transparent;
}

"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(header + css + "\n", encoding="utf-8")
print(f"Wrote {OUT} ({len(css.splitlines())} lines)")
