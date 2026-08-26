"""Generate JNS /areas hub + city pages. Licensed contractor/remodel — not handyman."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from city_page_copy import COPY

ROOT = Path(__file__).resolve().parents[1]
CREDITS = json.loads((ROOT / "data" / "city-photo-credits.json").read_text(encoding="utf-8"))
WORD_MIN = 750

CITIES = [
    {
        "slug": "palm-harbor",
        "name": "Palm Harbor",
        "title": "Kitchen Remodel Palm Harbor FL | Licensed Contractor",
        "description": "Kitchen & bath remodels in Palm Harbor, Ozona & East Lake. Licensed CRC1334879. Free written estimates. Call (727) 265-1120.",
        "h1": "Licensed Contractor in Palm Harbor, FL",
        "sub": "Kitchen remodels, bathroom renovations, and permitted residential work from our Palm Harbor base — CRC1334879.",
        "keywords": "kitchen remodel Palm Harbor, general contractor Palm Harbor FL, bathroom remodel Ozona, East Lake renovation",
        "neighborhoods": "Ozona, Crystal Beach, Innisbrook, East Lake, Lansbrook, Highland Lakes, and US 19 corridor homes",
        "lead": (
            "Palm Harbor is where JNS Construction Services LLC is based. Homeowners here usually call for kitchen remodels, "
            "bathroom gut-outs, and additions that need a licensed residential contractor — not a one-hour punch list. "
            "We write the scope, pull Pinellas permits when the work requires them, and stay on the job through final walkthrough."
        ),
        "body": (
            "Older ranch and split-plan homes along Nebraska Avenue, Tampa Road, and the East Lake side often need layout changes "
            "that affect plumbing, electrical, and load-bearing walls. That is licensed CRC work. We also take kitchen and bath "
            "remodels in Ozona cottages and Crystal Beach properties where salt air and older framing change how finishes last. "
            "If you searched kitchen remodel Palm Harbor or a licensed remodeler for Ozona or East Lake, this is the crew: "
            "Nathanial Combs and Connor McCollum in the field, written exclusions, and a free site consultation before you spend a dollar."
        ),
        "photo_alt": "Saint Luke Church in Palm Harbor, Florida — local landmark near JNS Construction's service base",
        "photo_caption": "Palm Harbor, Florida — local landmark (Saint Luke Church).",
    },
    {
        "slug": "clearwater",
        "name": "Clearwater",
        "title": "Kitchen Remodel Clearwater FL | Licensed Contractor",
        "description": "Kitchen & bath remodeling in Clearwater and Countryside. Licensed CRC1334879, Pinellas permits. Call (727) 265-1120.",
        "h1": "Kitchen & Bath Remodeling in Clearwater, FL",
        "sub": "Licensed residential contractor for Clearwater, Countryside, and Island Estates remodels — not a call-center crew.",
        "keywords": "kitchen remodel Clearwater FL, bathroom renovation Clearwater, licensed contractor Countryside",
        "neighborhoods": "Countryside, Island Estates, downtown Clearwater, Coachman, and mainland neighborhoods off Gulf-to-Bay",
        "lead": (
            "Clearwater homeowners hire JNS for kitchen remodels, bathroom renovations, and interior upgrades that have to survive "
            "Pinellas humidity and, on water-adjacent streets, salt air. We are a Palm Harbor contractor serving Clearwater on "
            "written scopes — CRC1334879 — with permit coordination when walls, plumbing, or electrical change."
        ),
        "body": (
            "Countryside two-story plans and 1970s ranches off Belcher and McMullen Booth are typical JNS calls: open a kitchen, "
            "replace a hall bath, or correct work that failed inspection. Beach-side condos and Island Estates jobs are quoted "
            "only when access, HOA rules, and parking are confirmed in writing. We quote licensed remodels with a written scope — "
            "not a rotating punch-list visit. Call (727) 265-1120 or send photos through the estimate form."
        ),
        "photo_alt": "Pier 60 at Clearwater Beach, Florida looking toward the Gulf",
        "photo_caption": "Pier 60, Clearwater Beach — the landmark most people picture when they say Clearwater.",
    },
    {
        "slug": "dunedin",
        "name": "Dunedin",
        "title": "Contractor Dunedin FL | Kitchen & Bath Remodel | JNS",
        "description": "Licensed kitchen & bath remodeling in downtown Dunedin and nearby Pinellas homes. CRC1334879. Call (727) 265-1120.",
        "h1": "Licensed Remodeling Contractor in Dunedin, FL",
        "sub": "Kitchen, bath, and interior upgrades for downtown Dunedin, the Trail, and marina-adjacent homes.",
        "keywords": "kitchen remodel Dunedin FL, bathroom renovation Dunedin, licensed contractor Dunedin",
        "neighborhoods": "downtown Main Street, Pinellas Trail corridor, marina / Skinner Blvd, and residential streets toward Palm Harbor",
        "lead": (
            "Dunedin jobs are often older cottages and updated bungalows within a few blocks of Main Street. Opening a kitchen "
            "or rebuilding a bath in those footprints means tight access, HOA or historic-adjacent expectations, and Pinellas "
            "permit rules. JNS writes that down before demolition — license CRC1334879."
        ),
        "body": (
            "We schedule Dunedin remodels from Palm Harbor so you are not waiting on a rotating franchise crew. Typical scopes: "
            "kitchen layout, walk-in shower conversions, flooring through connected living rooms, and corrective work after a "
            "failed inspection. Trail-side and marina-adjacent homes get a site visit so we can confirm dumpster, parking, and "
            "material staging. Request a free estimate or call (727) 265-1120."
        ),
        "photo_alt": "Downtown Dunedin, Florida storefronts along Main Street",
        "photo_caption": "Downtown Dunedin — Main Street commercial district.",
    },
    {
        "slug": "tarpon-springs",
        "name": "Tarpon Springs",
        "title": "Contractor Tarpon Springs FL | Kitchen Remodel | JNS",
        "description": "Kitchen & bath remodels in Tarpon Springs and Greektown-area homes. Licensed CRC1334879. Call (727) 265-1120.",
        "h1": "Kitchen Remodeling in Tarpon Springs, FL",
        "sub": "Licensed residential contractor for historic and waterfront-adjacent homes around the sponge docks and Lake Tarpon.",
        "keywords": "kitchen remodel Tarpon Springs, licensed contractor Tarpon Springs FL, bathroom renovation Greektown",
        "neighborhoods": "Greektown / sponge docks historic district, Spring Bayou, Lake Tarpon edge, and residential streets toward Palm Harbor",
        "lead": (
            "Tarpon Springs has a mix of historic cottages near the sponge docks and later ranch homes toward Lake Tarpon. "
            "Kitchen and bath remodels here often hit plaster, older plumbing, and permit questions. JNS is the licensed "
            "Palm Harbor contractor (CRC1334879) that writes the scope before anyone opens a wall."
        ),
        "body": (
            "We take Tarpon Springs remodels that need a residential contractor: kitchens, baths, additions, and code corrections. "
            "Historic-district adjacency and tight downtown streets are confirmed on the site visit — dumpster placement and "
            "parking are part of the written plan, not a surprise on day one. Call (727) 265-1120 for a free consultation."
        ),
        "photo_alt": "Natural sea sponges on a workboat at the Tarpon Springs sponge docks",
        "photo_caption": "Tarpon Springs sponge docks — the city's working waterfront.",
    },
    {
        "slug": "safety-harbor",
        "name": "Safety Harbor",
        "title": "Contractor Safety Harbor FL | Kitchen & Bath | JNS",
        "description": "Licensed kitchen & bath remodeling in Safety Harbor. Pinellas permits, written scopes. CRC1334879. (727) 265-1120.",
        "h1": "Licensed Contractor in Safety Harbor, FL",
        "sub": "Kitchen remodels, bathrooms, and permitted interior work for Safety Harbor and north Tampa Bay waterfront streets.",
        "keywords": "kitchen remodel Safety Harbor, licensed contractor Safety Harbor FL, bathroom renovation Safety Harbor",
        "neighborhoods": "downtown Main Street / spa district, waterfront streets, and residential blocks toward Oldsmar and Clearwater",
        "lead": (
            "Safety Harbor homeowners usually want a licensed remodeler who will deal with Pinellas permitting and still show "
            "up after the deposit. JNS Construction Services LLC does kitchen and bath remodels and corrective residential work "
            "under CRC1334879, with a free site consultation from our Palm Harbor shop."
        ),
        "body": (
            "Downtown lots are tight; waterfront blocks have access and HOA rules. We confirm both before pricing. Typical jobs: "
            "kitchen layout, primary bath rebuild, flooring through connected rooms, and repairs that failed a prior inspection. "
            "This is licensed residential construction with a written scope. Call (727) 265-1120 or use the estimate form."
        ),
        "photo_alt": "Safety Harbor City Hall building and plaza in Safety Harbor, Florida",
        "photo_caption": "Safety Harbor City Hall — downtown civic landmark.",
    },
    {
        "slug": "oldsmar",
        "name": "Oldsmar",
        "title": "Contractor Oldsmar FL | Kitchen & Bath Remodel | JNS",
        "description": "Kitchen & bath remodeling in Oldsmar. Licensed CRC1334879, written scopes, Pinellas permits. Call (727) 265-1120.",
        "h1": "Kitchen & Bath Contractor in Oldsmar, FL",
        "sub": "Licensed residential remodels for Oldsmar homes along Tampa Road, Race Track Road, and Harbor Palms.",
        "keywords": "kitchen remodel Oldsmar FL, licensed contractor Oldsmar, bathroom renovation Oldsmar",
        "neighborhoods": "Harbor Palms, Tampa Road corridor, Race Track Road, and residential streets toward Safety Harbor and Westchase",
        "lead": (
            "Oldsmar sits on the Pinellas–Hillsborough line. Homeowners here call JNS for kitchen remodels, bathroom renovations, "
            "and additions that need a Florida certified residential contractor. We quote from a Palm Harbor base, write the "
            "exclusions, and handle Pinellas permit paths when the scope requires them."
        ),
        "body": (
            "Many Oldsmar houses are 1980s–2000s production homes where a kitchen open-up or hall-bath rebuild is the real job. "
            "We do not bid mystery hourly punch lists. If you need licensed remodeling with a written scope, call (727) 265-1120 "
            "or send photos through the form. Field leadership stays Nathanial Combs and Connor McCollum — not a rotating sub list."
        ),
        "photo_alt": "Historic Mediterranean-style home in Oldsmar, Florida",
        "photo_caption": "Residential architecture in Oldsmar, Florida.",
    },
]

for _city in CITIES:
    extra = COPY[_city["slug"]]
    _city["sections"] = extra["sections"]
    _city["faqs"] = extra["faqs"]


def credit_line(slug: str, caption: str) -> str:
    meta = CREDITS[slug]
    license_name = html.escape(meta.get("license") or "")
    artist = html.escape(meta.get("artist_plain") or "Wikimedia Commons")
    return (
        f"{html.escape(caption)} Photo: {artist}"
        f"{' · ' + license_name if license_name else ''}."
    )


def city_links(current: str | None = None) -> str:
    parts = []
    for city in CITIES:
        if city["slug"] == current:
            parts.append(f'<li><strong>{html.escape(city["name"])}</strong></li>')
        else:
            parts.append(
                f'<li><a href="/areas/{city["slug"]}">{html.escape(city["name"])}</a></li>'
            )
    parts.append("<li>New Port Richey &amp; west Pasco by written quote</li>")
    return "\n            ".join(parts)


def faq_block(city: dict) -> tuple[str, str]:
    items = []
    schema = []
    for i, (q, a) in enumerate(city["faqs"], start=1):
        plain = re.sub(r"<[^>]+>", "", a)
        items.append(
            f"""          <div class="faq-item">
            <button class="faq-question" aria-expanded="false" aria-controls="faq-{city['slug']}-{i}">
              {html.escape(q)}
              <span class="faq-chevron" aria-hidden="true">&#8964;</span>
            </button>
            <div class="faq-answer" id="faq-{city['slug']}-{i}" aria-hidden="true" inert>
              <div class="faq-answer-inner">
                <p>{a}</p>
              </div>
            </div>
          </div>"""
        )
        schema.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": plain},
            }
        )
    return "\n".join(items), json.dumps(schema, ensure_ascii=False)


def city_html(city: dict) -> str:
    slug = city["slug"]
    path = f"/areas/{slug}"
    faq_html, faq_schema = faq_block(city)
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "@id": f"https://jnsbuilds.com{path}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jnsbuilds.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://jnsbuilds.com/areas"},
                    {"@type": "ListItem", "position": 3, "name": city["name"], "item": f"https://jnsbuilds.com{path}"},
                ],
            },
            {
                "@type": "Service",
                "@id": f"https://jnsbuilds.com{path}#service",
                "name": f"Kitchen and bath remodeling in {city['name']}",
                "description": city["description"],
                "provider": {"@id": "https://jnsbuilds.com/#business"},
                "areaServed": {"@type": "City", "name": f"{city['name']}, FL"},
                "url": f"https://jnsbuilds.com{path}",
            },
            {
                "@type": "WebPage",
                "@id": f"https://jnsbuilds.com{path}#webpage",
                "url": f"https://jnsbuilds.com{path}",
                "name": city["title"],
                "description": city["description"],
                "isPartOf": {"@id": "https://jnsbuilds.com/#website"},
                "about": {"@id": f"https://jnsbuilds.com{path}#service"},
                "primaryImageOfPage": {
                    "@type": "ImageObject",
                    "url": f"https://jnsbuilds.com/images/cities/{slug}.webp",
                },
                "inLanguage": "en-US",
            },
            {"@type": "FAQPage", "mainEntity": json.loads(faq_schema)},
        ],
    }
    others = " · ".join(
        f'<a href="/areas/{c["slug"]}">{html.escape(c["name"])}</a>'
        for c in CITIES
        if c["slug"] != slug
    )
    section_html = []
    for i, sec in enumerate(city["sections"]):
        section_html.append(f'        <h2>{html.escape(sec["h2"])}</h2>\n{sec["html"].rstrip()}\n')
        if i == 0:
            section_html.append(
                f"""        <figure class="city-inline-figure">
          <img src="/images/cities/{slug}.webp" alt="{html.escape(city["photo_alt"])}" width="1600" height="900" loading="lazy" decoding="async" />
          <figcaption>{credit_line(slug, city["photo_caption"])}</figcaption>
        </figure>
"""
            )
    sections_joined = "\n".join(section_html)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(city["title"])}</title>
  <meta name="description" content="{html.escape(city["description"])}" />
  <meta name="keywords" content="{html.escape(city["keywords"])}" />
  <meta name="geo.region" content="US-FL" />
  <meta name="geo.placename" content="{html.escape(city["name"])}, Florida" />
  <meta name="geo.position" content="28.095635;-82.738053" />
  <meta name="ICBM" content="28.095635, -82.738053" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <link rel="canonical" href="https://jnsbuilds.com{path}" />
  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI discovery file" />
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary" />
  <meta property="og:title" content="{html.escape(city["title"])}" />
  <meta property="og:description" content="{html.escape(city["description"])}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://jnsbuilds.com{path}" />
  <meta property="og:image" content="https://jnsbuilds.com/images/cities/{slug}.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(city["title"])}" />
  <meta name="twitter:description" content="{html.escape(city["description"])}" />
  <meta name="twitter:image" content="https://jnsbuilds.com/images/cities/{slug}.webp" />
  <meta name="theme-color" content="#060d08" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/CSS/site-shared.css" />
  <link rel="icon" href="/images/Logo_CMYK-01.png" type="image/png" />
  <script type="application/ld+json">
{json.dumps(graph, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <div id="site-header-include"></div>

  <section class="inner-hero inner-hero--city">
    <img class="city-hero-img" src="/images/cities/{slug}.webp" alt="{html.escape(city["photo_alt"])}" width="1600" height="900" fetchpriority="high" />
    <div class="container">
      <div class="page-title-bar">
        <p class="page-breadcrumb">
          <a href="/">Home</a><span>&rsaquo;</span>
          <a href="/areas">Service Areas</a><span>&rsaquo;</span>
          {html.escape(city["name"])}
        </p>
        <h1>{html.escape(city["h1"])}</h1>
        <p class="page-sub">{html.escape(city["sub"])}</p>
      </div>
    </div>
  </section>

  <main class="service-page-main">
    <div class="service-layout">
    <div class="service-main">

    <section class="inner-section inner-section--panel">
      <div class="container">
{sections_joined}
        <p class="city-related-label">Related JNS pages</p>
        <ul>
          <li><a href="/services/renovations-upgrades">Kitchen &amp; bath remodels</a></li>
          <li><a href="/services/general-construction">Additions and general construction</a></li>
          <li><a href="/services/repairs-corrective-work">Repairs and code corrections</a></li>
          <li><a href="/services/project-coordination">Project coordination</a></li>
          <li><a href="/gallery">Project gallery</a> — real JNS jobs, not stock interiors</li>
          <li><a href="/about">About JNS</a> — license, field leadership, how we work</li>
        </ul>
      </div>
    </section>

    <section class="inner-section">
      <div class="container">
        <h2>Other cities we serve</h2>
        <p>{others}</p>
        <p>Also by written quote: New Port Richey and nearby west Pasco. See the <a href="/areas">service areas hub</a>.</p>
      </div>
    </section>

    <section class="inner-section inner-section--panel">
      <div class="container">
        <h2>{html.escape(city["name"])} remodeling FAQ</h2>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>

    <section class="inner-cta">
      <div class="container">
        <h2>Get a written estimate in {html.escape(city["name"])}</h2>
        <p>Free site consultation. License CRC1334879. Call or send project photos.</p>
        <div class="cta-row">
          <a href="/contact" class="btn btn-primary">Request a Free Estimate</a>
          <a href="tel:+17272651120" class="btn btn-ghost">Call (727) 265-1120</a>
        </div>
      </div>
    </section>

    </div>

    <aside class="service-sidebar">
      <div class="service-sidebar-inner">
        <div class="sidebar-cta-card">
          <p class="sidebar-heading">Work in {html.escape(city["name"])}?</p>
          <p class="sidebar-sub">Free walkthrough. Written scope before we touch a thing.</p>
          <div class="sidebar-cta-buttons">
            <a href="tel:+17272651120" class="btn btn-primary">Call (727) 265-1120</a>
            <a href="/contact" class="btn btn-ghost">Request Free Estimate</a>
          </div>
        </div>
        <div class="sidebar-card">
          <p class="sidebar-card-label">Service Areas</p>
          <ul class="sidebar-area-list">
            {city_links(slug)}
          </ul>
        </div>
        <div class="sidebar-card sidebar-form-card">
          <p class="sidebar-card-label">Request a Free Estimate</p>
          <form class="estimate-form sidebar-form" action="https://formspree.io/f/xaqgqgyg" method="POST">
            <label class="visually-hidden" for="{slug}-hp">Leave this field blank</label>
            <input type="text" id="{slug}-hp" name="address_2" class="hp" tabindex="-1" autocomplete="off" />
            <input type="hidden" name="_subject" value="JNS Construction — {html.escape(city["name"])} Estimate Request" />
            <input type="hidden" name="request_type" value="{html.escape(city["name"])} city page estimate" />
            <input type="hidden" name="_next" value="https://jnsbuilds.com/thank-you" />
            <label>Name *<input type="text" name="fullName" required /></label>
            <label>Phone *<input type="tel" name="phone" required /></label>
            <label>Email *<input type="email" name="email" required /></label>
            <label>Project Details *<textarea name="projectDetails" rows="3" required placeholder="Kitchen, bath, addition..."></textarea></label>
            <button type="submit" class="btn btn-primary">Send Request</button>
          </form>
        </div>
      </div>
    </aside>

    </div>
  </main>

  <div id="site-footer-include"></div>
  <script src="/includes.js" defer></script>
  <script src="/script.js" defer></script>
</body>
</html>
"""


def hub_html() -> str:
    cards = []
    for i, city in enumerate(CITIES):
        loading = 'fetchpriority="high"' if i < 2 else 'loading="lazy" decoding="async"'
        cards.append(
            f"""        <a class="city-card" href="/areas/{city["slug"]}">
          <img src="/images/cities/{city["slug"]}.webp" alt="{html.escape(city["photo_alt"])}" width="800" height="450" {loading} />
          <div class="city-card-body">
            <h2>{html.escape(city["name"])}</h2>
            <p>{html.escape(city["sub"])}</p>
          </div>
        </a>"""
        )
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "@id": "https://jnsbuilds.com/areas#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jnsbuilds.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://jnsbuilds.com/areas"},
                ],
            },
            {
                "@type": "CollectionPage",
                "@id": "https://jnsbuilds.com/areas#webpage",
                "url": "https://jnsbuilds.com/areas",
                "name": "Service Areas | Palm Harbor to Clearwater | JNS",
                "description": "Licensed kitchen & bath remodeling across Palm Harbor, Clearwater, Dunedin, Tarpon Springs, Safety Harbor, and Oldsmar. CRC1334879.",
                "isPartOf": {"@id": "https://jnsbuilds.com/#website"},
                "inLanguage": "en-US",
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Service Areas | Palm Harbor to Clearwater | JNS</title>
  <meta name="description" content="Licensed kitchen & bath remodeling across Palm Harbor, Clearwater, Dunedin, Tarpon Springs, Safety Harbor, and Oldsmar. CRC1334879." />
  <meta name="keywords" content="contractor Palm Harbor, kitchen remodel Clearwater, licensed contractor Pinellas County" />
  <meta name="geo.region" content="US-FL" />
  <meta name="geo.placename" content="Palm Harbor, Florida" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <link rel="canonical" href="https://jnsbuilds.com/areas" />
  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI discovery file" />
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary" />
  <meta property="og:title" content="Service Areas | Palm Harbor to Clearwater | JNS" />
  <meta property="og:description" content="Licensed kitchen & bath remodeling across north Pinellas. CRC1334879." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://jnsbuilds.com/areas" />
  <meta property="og:image" content="https://jnsbuilds.com/images/jns-og-image.jpg" />
  <meta name="theme-color" content="#060d08" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/CSS/site-shared.css" />
  <link rel="icon" href="/images/Logo_CMYK-01.png" type="image/png" />
  <script type="application/ld+json">
{json.dumps(graph, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <div id="site-header-include"></div>
  <section class="inner-hero">
    <div class="container">
      <div class="page-title-bar">
        <p class="page-breadcrumb"><a href="/">Home</a><span>&rsaquo;</span>Service Areas</p>
        <h1>Pinellas Service Areas</h1>
        <p class="page-sub">Licensed kitchen, bath, and residential remodeling from Palm Harbor — CRC1334879. City pages below use real local photos, not generic stock skylines.</p>
      </div>
    </div>
  </section>
  <main>
    <section class="inner-section inner-section--panel">
      <div class="container">
        <h2>Where JNS takes licensed remodel work</h2>
        <p>JNS Construction Services LLC is a Florida certified residential contractor based in Palm Harbor. These pages are for homeowners searching a licensed kitchen or bath remodel in a specific city. Each city page names the housing stock, streets, and access constraints we actually quote &mdash; not a copied paragraph with the city name swapped.</p>
        <p>Start here, then open the city that matches the house: <a href="/areas/palm-harbor">Palm Harbor</a> (shop base, Ozona, East Lake), <a href="/areas/clearwater">Clearwater</a> (Countryside and mainland), <a href="/areas/dunedin">Dunedin</a> (Main Street and the Trail), <a href="/areas/tarpon-springs">Tarpon Springs</a> (Greektown and Lake Tarpon), <a href="/areas/safety-harbor">Safety Harbor</a> (spa district and waterfront streets), and <a href="/areas/oldsmar">Oldsmar</a> (Harbor Palms and the county line). Kitchen and bath scopes are detailed on <a href="/services/renovations-upgrades">renovations and upgrades</a>; additions on <a href="/services/general-construction">general construction</a>; finished jobs in the <a href="/gallery">gallery</a>.</p>
        <div class="city-card-grid">
{chr(10).join(cards)}
        </div>
        <p>West Pasco (including New Port Richey) is quoted when the scope is licensed remodeling or construction, not a punch-list visit. Call <a href="tel:+17272651120">(727) 265-1120</a> or <a href="/contact">request a free estimate</a>.</p>
      </div>
    </section>
  </main>
  <div id="site-footer-include"></div>
  <script src="/includes.js" defer></script>
  <script src="/script.js" defer></script>
</body>
</html>
"""


def seo_entries() -> dict:
    pages = {
        "areas/index.html": {
            "path": "/areas",
            "title": "Service Areas | Palm Harbor to Clearwater | JNS",
            "description": "Licensed kitchen & bath remodeling across Palm Harbor, Clearwater, Dunedin, Tarpon Springs, Safety Harbor, and Oldsmar. CRC1334879.",
            "keywords": "contractor Palm Harbor, kitchen remodel Clearwater, licensed contractor Pinellas County",
            "og_title": "Service Areas | Palm Harbor to Clearwater | JNS",
            "index": True,
            "priority": "0.8",
            "changefreq": "monthly",
        }
    }
    for city in CITIES:
        pages[f"areas/{city['slug']}.html"] = {
            "path": f"/areas/{city['slug']}",
            "title": city["title"],
            "description": city["description"],
            "keywords": city["keywords"],
            "og_title": city["title"],
            "index": True,
            "priority": "0.8",
            "changefreq": "monthly",
        }
    return pages


def city_word_count(city: dict) -> int:
    chunks = [city["h1"], city["sub"], city["neighborhoods"]]
    for sec in city["sections"]:
        chunks.append(sec["h2"])
        chunks.append(sec["html"])
    for q, a in city["faqs"]:
        chunks.append(q)
        chunks.append(a)
    text = re.sub(r"<[^>]+>", " ", " ".join(chunks))
    return len(re.findall(r"[A-Za-z0-9']+", text))


def validate() -> None:
    errors = []
    for city in CITIES:
        if len(city["title"]) > 60:
            errors.append(f"{city['slug']} title {len(city['title'])}: {city['title']}")
        if len(city["description"]) > 150:
            errors.append(f"{city['slug']} desc {len(city['description'])}")
        words = city_word_count(city)
        city["_words"] = words
        if words < WORD_MIN:
            errors.append(f"{city['slug']} word count {words} < {WORD_MIN}")
    hub_t = "Service Areas | Palm Harbor to Clearwater | JNS"
    hub_d = "Licensed kitchen & bath remodeling across Palm Harbor, Clearwater, Dunedin, Tarpon Springs, Safety Harbor, and Oldsmar. CRC1334879."
    if len(hub_t) > 60:
        errors.append(f"hub title {len(hub_t)}")
    if len(hub_d) > 150:
        errors.append(f"hub desc {len(hub_d)}")
    if errors:
        raise SystemExit("SEO length failed:\n" + "\n".join(errors))


def main() -> None:
    validate()
    out = ROOT / "areas"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(hub_html(), encoding="utf-8")
    print("wrote areas/index.html")
    for city in CITIES:
        dest = out / f"{city['slug']}.html"
        dest.write_text(city_html(city), encoding="utf-8")
        print("wrote", dest.relative_to(ROOT), f"title={len(city['title'])} desc={len(city['description'])} words={city['_words']}")
    (ROOT / "data" / "city-pages.json").write_text(
        json.dumps({"cities": [{k: c[k] for k in ("slug", "name", "title", "description")} for c in CITIES]}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
