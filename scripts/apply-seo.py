#!/usr/bin/env python3
"""Apply SEO meta, geo tags, schema, and fix head markup across JNS HTML pages."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "seo" / "seo-config.json").read_text(encoding="utf-8"))
SITE = CONFIG["site"]
PAGES = CONFIG["pages"]
MANIFEST = json.loads((ROOT / "Gallery" / "gallery-manifest.json").read_text(encoding="utf-8"))
TODAY = date.today().isoformat()

TITLE_MAX = 60
DESC_MAX = 150


def validate_lengths() -> None:
    errors = []
    for rel, page in PAGES.items():
        t = len(page["title"])
        d = len(page["description"])
        if t > TITLE_MAX:
            errors.append(f"{rel}: title {t} chars ({page['title']!r})")
        if d > DESC_MAX:
            errors.append(f"{rel}: description {d} chars")
    if errors:
        raise SystemExit("SEO length validation failed:\n" + "\n".join(errors))


def geo_block() -> str:
    return f"""  <meta name="geo.region" content="US-FL" />
  <meta name="geo.placename" content="{SITE['locality']}, Florida" />
  <meta name="geo.position" content="{SITE['geo_position']}" />
  <meta name="ICBM" content="{SITE['geo_position'].replace(';', ', ')}" />
"""


def keywords_block(keywords: str) -> str:
    return f'  <meta name="keywords" content="{keywords}" />\n'


def replace_title_desc(content: str, page: dict) -> str:
    content = re.sub(r"<title>[^<]*</title>", f"<title>{page['title']}</title>", content, count=1)
    content = re.sub(
        r'<meta name="description" content="[^"]*"\s*/>',
        f'<meta name="description" content="{page["description"]}" />',
        content,
        count=1,
    )
    if 'name="keywords"' in content:
        content = re.sub(
            r'<meta name="keywords" content="[^"]*"\s*/>',
            keywords_block(page.get("keywords", "")).strip(),
            content,
            count=1,
        )
    elif page.get("keywords"):
        content = content.replace(
            f'<meta name="description" content="{page["description"]}" />',
            f'<meta name="description" content="{page["description"]}" />\n{keywords_block(page["keywords"]).rstrip()}',
            1,
        )

    og_title = page.get("og_title", page["title"])
    content = re.sub(
        r'<meta property="og:title" content="[^"]*"\s*/>',
        f'<meta property="og:title" content="{og_title}" />',
        content,
        count=1,
    )
    content = re.sub(
        r'<meta property="og:description" content="[^"]*"\s*/>',
        f'<meta property="og:description" content="{page["description"]}" />',
        content,
        count=1,
    )
    if 'name="twitter:title"' in content:
        content = re.sub(
            r'<meta name="twitter:title" content="[^"]*"\s*/>',
            f'<meta name="twitter:title" content="{og_title}" />',
            content,
            count=1,
        )
        content = re.sub(
            r'<meta name="twitter:description" content="[^"]*"\s*/>',
            f'<meta name="twitter:description" content="{page["description"]}" />',
            content,
            count=1,
        )
    return content


def ensure_geo(content: str) -> str:
    if 'name="geo.region"' in content:
        return content
    insert_after = '<meta name="robots"'
    if insert_after in content:
        return content.replace(insert_after, geo_block() + insert_after, 1)
    return content.replace("<head>", "<head>\n" + geo_block(), 1)


def fix_broken_comments(content: str) -> str:
    return content.replace("--> -->", "").replace("-->-->", "")


def breadcrumb_schema(path: str, crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{SITE['domain']}{path}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": SITE["domain"] + item if item.startswith("/") else item,
            }
            for i, (name, item) in enumerate(crumbs)
        ],
    }


def webpage_schema(path: str, page: dict, page_type: str = "WebPage", about_id: str | None = None) -> dict:
    return {
        "@type": page_type,
        "@id": f"{SITE['domain']}{path}#webpage",
        "url": f"{SITE['domain']}{path}",
        "name": page["title"],
        "description": page["description"],
        "isPartOf": {"@id": SITE["website_id"]},
        "about": {"@id": about_id or SITE["business_id"]},
        "inLanguage": "en-US",
    }


def service_schema(path: str, page: dict) -> dict:
    return {
        "@type": "Service",
        "@id": f"{SITE['domain']}{path}#service",
        "name": page["service_name"],
        "description": page["service_description"],
        "provider": {"@id": SITE["business_id"]},
        "areaServed": [
            {"@type": "City", "name": "Palm Harbor"},
            {"@type": "AdministrativeArea", "name": "Pinellas County, FL"},
            {"@type": "AdministrativeArea", "name": "Pasco County, FL"},
        ],
        "url": f"{SITE['domain']}{path}",
    }


def gallery_itemlist_schema() -> dict:
    items = []
    for i, entry in enumerate(MANIFEST["items"], start=1):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "ImageObject",
                    "contentUrl": f"{SITE['domain']}/Gallery/{entry['file']}",
                    "name": entry["title"],
                    "description": entry["description"],
                    "caption": entry["alt"],
                },
            }
        )
    return {
        "@type": "ItemList",
        "@id": f"{SITE['domain']}/gallery#itemlist",
        "name": "JNS Construction Project Gallery",
        "description": "Completed kitchen remodels, bathroom renovations, and construction projects in Pinellas County.",
        "numberOfItems": len(items),
        "itemListElement": items[:25],
    }


def schema_graph_for(rel: str, page: dict) -> str:
    path = page["path"]
    graphs: list[dict] = []

    if rel == "index.html":
        graphs.append(
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "@id": SITE["website_id"],
                "url": SITE["domain"] + "/",
                "name": SITE["name"],
                "publisher": {"@id": SITE["business_id"]},
                "inLanguage": "en-US",
            }
        )
        return ""  # homepage keeps existing rich schema; only meta updated

    if rel == "about.html":
        wp = webpage_schema(path, page, "AboutPage")
        graphs.extend(
            [
                breadcrumb_schema(path, [("Home", "/"), ("About", path)]),
                wp,
            ]
        )
    elif rel == "contact.html":
        wp = webpage_schema(path, page, "ContactPage")
        graphs.extend(
            [
                breadcrumb_schema(path, [("Home", "/"), ("Contact", path)]),
                wp,
            ]
        )
    elif rel == "gallery.html":
        wp = webpage_schema(path, page, "CollectionPage")
        graphs.extend(
            [
                breadcrumb_schema(path, [("Home", "/"), ("Gallery", path)]),
                wp,
                gallery_itemlist_schema(),
            ]
        )
    elif rel.startswith("services/"):
        name = page["service_name"]
        service_id = f"{SITE['domain']}{path}#service"
        graphs.extend(
            [
                breadcrumb_schema(
                    path,
                    [
                        ("Home", "/"),
                        ("Services", "/#services"),
                        (name, path),
                    ],
                ),
                service_schema(path, page),
                webpage_schema(path, page, about_id=service_id),
            ]
        )
    elif rel.endswith("-policy.html") or rel == "terms-of-service.html":
        graphs.extend(
            [
                breadcrumb_schema(
                    path,
                    [("Home", "/"), (page["title"].split("|")[0].strip(), path)],
                ),
                webpage_schema(path, page),
            ]
        )

    if not graphs:
        return ""

    payload = graphs[0] if len(graphs) == 1 else {"@context": "https://schema.org", "@graph": graphs}
    return (
        '  <script type="application/ld+json">\n'
        + json.dumps(payload, indent=2, ensure_ascii=False)
        + "\n  </script>\n"
    )


def inject_schema(content: str, rel: str, page: dict) -> str:
    if rel == "index.html":
        # Add WebSite to existing @graph if present, else skip (homepage already has business schema)
        if '"@type": "WebSite"' not in content:
            website = {
                "@type": "WebSite",
                "@id": SITE["website_id"],
                "url": SITE["domain"] + "/",
                "name": SITE["name"],
                "publisher": {"@id": SITE["business_id"]},
                "inLanguage": "en-US",
            }
            # Insert before closing of first ld+json if it's a single object - homepage uses separate scripts
            website_script = (
                '  <script type="application/ld+json">\n'
                + json.dumps({"@context": "https://schema.org", **website}, indent=2)
                + "\n  </script>\n"
            )
            content = content.replace(
                "  <!-- Breadcrumb Schema -->",
                website_script + "  <!-- Breadcrumb Schema -->",
                1,
            )
        return content

    new_schema = schema_graph_for(rel, page)
    if not new_schema:
        return content

    # Replace prior @graph schema block when re-applying
    content = re.sub(
        r'  <script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@graph":[\s\S]*?</script>\s*',
        "",
        content,
        count=1,
    )

    # Remove legacy BreadcrumbList-only script block
    content = re.sub(
        r'  <script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BreadcrumbList"[\s\S]*?</script>\s*',
        "",
        content,
        count=1,
    )

    anchor = "  <meta name=\"theme-color\""
    if anchor in content and new_schema not in content:
        return content.replace(anchor, new_schema + anchor, 1)
    anchor = "  <!-- Analytics intentionally disabled"
    if anchor in content:
        return content.replace(anchor, new_schema + anchor, 1)
    return content.replace("</head>", new_schema + "</head>", 1)


def patch_canonical(content: str, page: dict) -> str:
    canonical = SITE["domain"] + page["path"]
    if page["path"] == "/":
        canonical = SITE["domain"] + "/"
    content = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/>',
        f'<link rel="canonical" href="{canonical}" />',
        content,
        count=1,
    )
    if 'property="og:url"' in content:
        content = re.sub(
            r'<meta property="og:url" content="[^"]*"\s*/>',
            f'<meta property="og:url" content="{canonical}" />',
            content,
            count=1,
        )
    return content


def patch_page(rel: str, page: dict) -> None:
    path = ROOT / rel
    if not path.exists():
        print(f"skip missing {rel}")
        return
    content = path.read_text(encoding="utf-8")
    content = fix_broken_comments(content)
    content = replace_title_desc(content, page)
    content = ensure_geo(content)
    content = patch_canonical(content, page)
    content = inject_schema(content, rel, page)
    path.write_text(content, encoding="utf-8")
    print(f"patched {rel} (title={len(page['title'])}, desc={len(page['description'])})")


def write_sitemap() -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "",
    ]
    for rel, page in PAGES.items():
        if not page.get("index", True):
            continue
        loc = SITE["domain"] + page["path"]
        if page["path"] == "/":
            loc = SITE["domain"] + "/"
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{TODAY}</lastmod>",
                f"    <changefreq>{page.get('changefreq', 'monthly')}</changefreq>",
                f"    <priority>{page.get('priority', '0.5')}</priority>",
                "  </url>",
                "",
            ]
        )
    lines.append("</urlset>")
    lines.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print("wrote sitemap.xml")


def write_robots() -> None:
    text = """User-agent: *
Allow: /
Disallow: /.git/
Disallow: /.github/
Disallow: /.vscode/
Disallow: /_archive/
Disallow: /scripts/
Disallow: /seo/
Disallow: /data/
Disallow: /Gallery/_source/
Disallow: /_gallery-html.txt

User-agent: GPTBot
Allow: /
Allow: /llms.txt

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://jnsbuilds.com/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(text, encoding="utf-8")
    print("wrote robots.txt")


def write_llms_txt() -> None:
    text = f"""# JNS Construction Services LLC

> Licensed general contractor in Palm Harbor, Florida (CRC1334879) serving Pinellas County and surrounding areas with kitchen remodels, bathroom renovations, general construction, repairs, and project coordination.

## Business
- Name: JNS Construction Services LLC
- Website: {SITE['domain']}
- Phone: (727) 265-1120
- Email: projects@jnsconstructionfl.com
- Address: 35595 US Hwy 19 N, Suite 621, Palm Harbor, FL 34684
- License: Florida Certified Residential Contractor CRC1334879
- Service area: Palm Harbor, Dunedin, Clearwater, Tarpon Springs, Safety Harbor, Oldsmar, New Port Richey, Pinellas County, Pasco County

## Primary pages
- Home: {SITE['domain']}/
- About: {SITE['domain']}/about
- Contact / free estimate: {SITE['domain']}/contact
- Project gallery: {SITE['domain']}/gallery
- General construction: {SITE['domain']}/services/general-construction
- Renovations & upgrades: {SITE['domain']}/services/renovations-upgrades
- Repairs & corrective work: {SITE['domain']}/services/repairs-corrective-work
- Project coordination: {SITE['domain']}/services/project-coordination

## Services summary
JNS provides written scopes and free site consultations for residential remodels, room additions, structural repairs, code corrections, and trade coordination. Field leadership is provided by Nathanial Combs and Connor McCollum.

## Optional
- Privacy policy: {SITE['domain']}/privacy-policy
- Payment policy: {SITE['domain']}/payment-policy
- Sitemap: {SITE['domain']}/sitemap.xml
"""
    (ROOT / "llms.txt").write_text(text, encoding="utf-8")
    print("wrote llms.txt")


def expand_gallery_seo_copy() -> None:
    path = ROOT / "gallery.html"
    content = path.read_text(encoding="utf-8")
    intro = """        <div class="gallery-seo-intro reveal">
          <p>JNS Construction Services LLC documents completed kitchen remodels, bathroom renovations, room additions, and corrective repair work across <strong>Palm Harbor</strong>, <strong>Clearwater</strong>, <strong>Dunedin</strong>, and greater <strong>Pinellas County</strong>. Every photo in this gallery is from a real client project — not stock imagery.</p>
          <p>Whether you are planning a full kitchen remodel, a walk-in shower upgrade, or a before-and-after renovation, these photos show the finish quality, scope depth, and field standards JNS brings to licensed residential construction under Florida license <strong>CRC1334879</strong>.</p>
          <p>Use the category filters to browse kitchen remodels, bathroom projects, before-and-after collages, outdoor builds, and interior upgrades. Ready to discuss a similar project? <a href="/contact.html">Request a free estimate</a> or call <a href="tel:+17272651120">(727) 265-1120</a>.</p>
        </div>
"""
    if "gallery-seo-intro" not in content:
        content = content.replace(
            '        <div class="gallery-filters"',
            intro + '        <div class="gallery-filters"',
            1,
        )
        path.write_text(content, encoding="utf-8")
        print("expanded gallery.html SEO copy")


def main() -> None:
    validate_lengths()
    for rel, page in PAGES.items():
        patch_page(rel, page)
    expand_gallery_seo_copy()
    write_sitemap()
    write_robots()
    write_llms_txt()
    print("SEO apply complete.")


if __name__ == "__main__":
    main()
