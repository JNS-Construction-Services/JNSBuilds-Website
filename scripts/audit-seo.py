#!/usr/bin/env python3
"""Quick post-apply SEO validation report."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"header.html", "footer.html"}
pages = sorted(
    p
    for p in list(ROOT.glob("*.html")) + list((ROOT / "services").glob("*.html"))
    if p.name not in SKIP
)

print("JNS SEO VALIDATION")
print("=" * 72)
fail = False
for p in pages:
    t = p.read_text(encoding="utf-8")
    title = re.search(r"<title>([^<]+)</title>", t)
    desc = re.search(r'name="description" content="([^"]+)"', t)
    h1s = re.findall(r"<h1[^>]*>([\s\S]*?)</h1>", t, re.I)
    h1_text = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
    body = re.sub(r"<script[\s\S]*?</script>", "", t, flags=re.I)
    body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    words = len(re.findall(r"\b[\w']+\b", body))
    ti = title.group(1) if title else "MISSING"
    de = desc.group(1) if desc else "MISSING"
    ok_t = len(ti) <= 60
    ok_d = len(de) <= 150
    ok_h1 = len(h1s) == 1
    if not (ok_t and ok_d and ok_h1):
        fail = True
    rel = p.relative_to(ROOT)
    print(f"\n{rel}")
    print(f"  title ({len(ti)}/60): {ti} {'OK' if ok_t else 'FAIL'}")
    print(f"  desc  ({len(de)}/150): {de} {'OK' if ok_d else 'FAIL'}")
    print(f"  H1 x{len(h1s)}: {h1_text[0] if h1_text else 'none'} {'OK' if ok_h1 else 'FAIL'}")
    print(f"  body words ~{words}")
    schema_types = re.findall(r'"@type":\s*"([^"]+)"', t)
    print(f"  schema types: {', '.join(dict.fromkeys(schema_types))}")

print("\n" + "=" * 72)
print("PASS" if not fail else "ISSUES FOUND")
