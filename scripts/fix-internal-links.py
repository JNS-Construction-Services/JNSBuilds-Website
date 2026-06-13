#!/usr/bin/env python3
"""Normalize internal page links to extensionless clean URLs."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"header.html", "footer.html"}

# href="/about.html" -> href="/about" ; keep assets, tel, mailto, external, anchors
PATTERN = re.compile(
    r'href="(/(?:about|contact|gallery|payment-policy|privacy-policy|refund-policy|terms-of-service|services/[a-z0-9-]+))\.html("|[?#])',
    re.I,
)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = PATTERN.sub(r'href="\1\2', text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name in SKIP:
            continue
        if fix_file(path):
            changed.append(path.relative_to(ROOT))
    for path in [ROOT / "header.html", ROOT / "footer.html"]:
        if path.exists() and fix_file(path):
            changed.append(path.relative_to(ROOT))
    print(f"Updated {len(changed)} files:")
    for c in changed:
        print(f"  {c}")


if __name__ == "__main__":
    main()
