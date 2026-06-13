# JNS Construction — SEO / AEO / GEO Audit Report

**Site:** https://jnsbuilds.com  
**Audit date:** 2026-06-12  
**Scope:** 12 public HTML pages (excludes `header.html`, `footer.html` partials)

---

## Executive summary

All 12 indexable pages now meet **title ≤ 60** and **meta description ≤ 150** character limits. Every page has exactly **one H1**, sufficient body copy for indexing (lowest ~693 words on gallery after SEO intro), consistent **GEO tags**, updated **JSON-LD**, a refreshed **sitemap.xml**, **robots.txt**, and new **llms.txt** for AI/answer-engine discovery.

**Verdict:** No pages are too thin to index. Gallery is the lightest page but is strengthened by 25 categorized images, filters, manifest-driven alt text, ItemList schema, and added SEO intro copy.

---

## Meta titles & descriptions (implemented)

| Page | Title (chars) | Description (chars) |
|------|---------------|---------------------|
| Home | General Contractor Palm Harbor FL \| JNS Construction (52) | Licensed contractor Palm Harbor FL (CRC1334879)... (134) |
| About | About JNS Construction \| Palm Harbor Contractor (47) | Licensed Palm Harbor contractor led in the field... (129) |
| Contact | Contact JNS Construction \| Free Estimate Palm Harbor (52) | Request a free estimate... (133) |
| Gallery | Project Gallery \| JNS Construction Palm Harbor (46) | Kitchen & bath remodel photos... (124) |
| General Construction | General Construction Contractor \| Palm Harbor FL (48) | Additions, framing, build-outs... (133) |
| Renovations | Kitchen & Bath Remodel \| Palm Harbor FL \| JNS (45) | Kitchen remodeling, bathroom renovations... (134) |
| Repairs | Home Repairs Contractor \| Palm Harbor FL \| JNS (46) | Code corrections, water & storm damage... (132) |
| Project Coordination | Project Coordination \| Palm Harbor Contractor (45) | Trade scheduling, permit oversight... (125) |
| Payment Policy | Payment Policy \| JNS Construction Services (42) | JNS Construction payment terms... (129) |
| Privacy Policy | Privacy Policy \| JNS Construction Services (42) | How JNS Construction Services LLC collects... (134) |
| Refund Policy | Refund Policy \| JNS Construction Services (41) | Refund and cancellation terms... (135) |
| Terms of Service | Terms of Service \| JNS Construction Services (44) | Terms governing use of jnsbuilds.com... (117) |

**Keyword strategy:** Primary geo terms (Palm Harbor, Pinellas County, Clearwater) + service intent (kitchen remodel, bathroom renovation, general contractor) + trust signal (CRC1334879) without keyword stuffing.

**Source of truth:** `seo/seo-config.json` — re-apply with `python scripts/apply-seo.py`.

---

## Header structure (H1–H6)

| Page | H1 | Structure notes |
|------|-----|-----------------|
| Home | Licensed Contractor Palm Harbor / JNS Construction Services | Hero H1; sections use H2 (Services, Process, Reviews, etc.) |
| About | About JNS Construction | Inner hero H1 → H2 sections (team, expectations, areas) |
| Contact | Contact Us | Inner hero H1 → H2 form / map / FAQ |
| Gallery | Project Gallery | Inner hero H1 → category filters → image cards (H3 titles in cards) |
| Service pages (×4) | Service name | Inner hero H1 → H2 scope, process, FAQ, project photos |
| Legal (×4) | Policy name | Inner hero H1 → H2 policy sections |

**Result:** Logical hierarchy on all pages. No duplicate H1s. Breadcrumb nav is presentational (`<p class="page-breadcrumb">`), not competing headings.

---

## Content depth & indexability

| Page | ~Body words | Index? | Notes |
|------|-------------|--------|-------|
| Home | ~1,009 | Yes | High priority; FAQ + LocalBusiness + OfferCatalog schema |
| About | ~1,112 | Yes | Team, service area, expectations |
| Contact | ~1,041 | Yes | Form, map, FAQ |
| Gallery | ~693 | Yes | 25 images + SEO intro + ItemList schema |
| Service pages | ~1,036–1,195 | Yes | Scope, FAQ, project photos, sidebar CTA |
| Legal pages | ~682–923 | Yes (low priority) | Required trust/compliance pages |

**Not indexed:** `/scripts/`, `/seo/`, `/data/`, `/Gallery/_source/`, partials — blocked in `robots.txt`.

---

## GEO / local SEO

Applied on all pages:

- `geo.region`: US-FL  
- `geo.placename`: Palm Harbor, Florida  
- `geo.position` / `ICBM`: 28.095635, -82.738053  
- Homepage + contact: full **LocalBusiness** / **GeneralContractor** schema with address, hours, `areaServed`, license identifier  
- Service pages: **Service** schema with `areaServed` (Palm Harbor, Pinellas, Pasco)

---

## AEO (Answer Engine Optimization)

- **FAQPage** schema on home, about, contact, and all 4 service pages  
- **llms.txt** at site root — business summary, services, page URLs for GPTBot / AI crawlers  
- Gallery SEO intro answers “what areas / what license / what types of projects” in plain language  
- Phone, email, license, and service area repeated in structured data and visible copy

---

## Schema markup (by page type)

| Page type | JSON-LD |
|-----------|---------|
| Home | WebSite, BreadcrumbList, GeneralContractor/LocalService, OfferCatalog, FAQPage |
| About | @graph: BreadcrumbList, AboutPage + body FAQPage |
| Contact | @graph: BreadcrumbList, ContactPage + body FAQPage |
| Gallery | @graph: BreadcrumbList, CollectionPage, ItemList (25 ImageObjects) |
| Services | @graph: BreadcrumbList, Service, WebPage (about → #service) + body FAQPage |
| Legal | @graph: BreadcrumbList, WebPage |

Entity linking uses stable `@id` anchors: `#website`, `#business`, `#service`, `#webpage`.

---

## Sitemap (`sitemap.xml`)

- 12 URLs, clean paths (no `.html` suffix)  
- `lastmod`: 2026-06-12  
- Priorities: home 1.0, contact + services 0.9, about/gallery 0.8, legal 0.2  
- Homepage `<link rel="sitemap">` added for discoverability

---

## Robots (`robots.txt`)

- Allow all primary crawlers  
- Disallow dev/build paths (`scripts/`, `seo/`, `data/`, `_source/`)  
- Explicit **GPTBot** allow + `llms.txt`  
- **Google-Extended** allowed (AI training opt-in)  
- Sitemap directive: `https://jnsbuilds.com/sitemap.xml`

---

## Files changed / added

- `seo/seo-config.json` — meta config  
- `scripts/apply-seo.py` — apply meta, schema, sitemap, robots, llms  
- `scripts/audit-seo.py` — validation runner  
- All 12 HTML pages — meta, geo, canonical, schema  
- `gallery.html` — SEO intro block  
- `CSS/site-shared.css` — `.gallery-seo-intro` styles  
- `sitemap.xml`, `robots.txt`, `llms.txt` — regenerated  
- `index.html` — sitemap + llms links, WebSite schema, aligned business description

---

## Post-deploy checklist

1. Submit `sitemap.xml` in Google Search Console & Bing Webmaster Tools  
2. Validate rich results: [Google Rich Results Test](https://search.google.com/test/rich-results) on home + one service page + gallery  
3. Confirm clean URLs resolve (`.htaccess` / host rewrites for extensionless paths)  
4. When Google reviews populate, `data/google-reviews.json` will feed the reviews carousel (already wired)

---

## Maintenance

After content changes, run:

```bash
python scripts/apply-seo.py
python scripts/audit-seo.py
```

Update `seo/seo-config.json` first if titles/descriptions change.
