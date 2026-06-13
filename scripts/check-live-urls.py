#!/usr/bin/env python3
import re
import urllib.request

URLS = [
    "https://jnsbuilds.com/about.html",
    "https://jnsbuilds.com/about",
    "https://jnsbuilds.com/contact.html",
    "https://jnsbuilds.com/contact",
    "https://jnsbuilds.com/gallery.html",
    "https://jnsbuilds.com/gallery",
    "http://jnsbuilds.com/",
    "https://jnsbuilds.com/sitemap.xml",
]

for u in URLS:
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            final = r.geturl()
            body = r.read(12000).decode("utf-8", errors="ignore")
            m = re.search(r'rel="canonical" href="([^"]+)"', body)
            canon = m.group(1) if m else "none"
            print(u)
            print(f"  final={final} status={r.status}")
            print(f"  canonical={canon}")
            if "sitemap" in u:
                locs = re.findall(r"<loc>([^<]+)</loc>", body)
                print(f"  sitemap locs ({len(locs)}): {locs[:3]}...")
    except Exception as e:
        print(f"{u} ERROR: {e}")
