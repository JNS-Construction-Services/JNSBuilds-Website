# JNS Construction Services Website — Copilot Instructions

## Project Overview
Static HTML/CSS/JS website for JNS Construction Services LLC. Deployed on GitHub Pages at **jnsbuilds.com** via the `JNS-Construction-Services/JNSBuilds-Website` repo, `main` branch. DNS managed in Namecheap (4 A records + CNAME www).

## File Structure
```
jns-v2/
  index.html              # Homepage (hero, about, services, contact)
  about.html              # About page
  contact.html            # Contact form + Direct Contact cards
  services/
    general-construction.html
    renovations-upgrades.html
    repairs-corrective-work.html
    project-coordination.html
  policy_pages/
    privacy-policy.html
    terms-of-service.html
    cookie-policy.html
    disclaimer.html
    refund-policy.html
  styles.css              # Single global stylesheet — all responsive styles here
  script.js               # Nav hamburger, dropdown, scroll behavior
  images/
    hero.webp             # Compressed hero (197KB) — DO NOT replace with PNG
    Logo_WHITE-01.png
    Logo_BLACK-01.png
    Logo_CMYK-01.png
  CNAME                   # jnsbuilds.com
  sitemap.xml
  robots.txt
```

## Critical Rules
- **NEVER create new HTML files** without explicit approval. All pages already exist.
- **NEVER create new CSS files.** All styles go in `styles.css`.
- **Edit existing files only** — no duplicates, no new utility files.
- **Do not auto-push to GitHub.** Always show the user the changes and wait for confirmation before staging or pushing anything.
- All image paths must use `images/` (relative, no `../`) since the site root is `jns-v2/`.

## CSS Conventions
- CSS custom properties (variables) defined at `:root` — use them, don't hardcode colors.
- Responsive breakpoints: `720px`, `600px`, `420px`, `400px` — mobile-first adjustments.
- Use `clamp()` for fluid font sizes, never fixed px at a single breakpoint.
- `.container` base padding: `0 36px`; override for mobile in the `≤600px` query.
- High-specificity section containers (e.g. `.section-services .container`, `.inner-section .container`) must have their own mobile padding overrides — generic `.container` mobile rules won't reach them.
- Modifier classes (e.g. `.feature-grid--4`) have higher specificity than `.feature-grid` — always include modifier variants in every breakpoint rule.
- Hero: `min-height: 60vh`, NO `max-height` — content must be able to expand on mobile.

## Deployment
```bash
git add <files>
git commit -m "description"
git push origin main
```
GitHub Pages rebuilds automatically (~1 min). Always wait for user to confirm the changes work locally before pushing.

## Known Placeholder Values (to fix before launch)
- Phone number: `(555) 010-0000` — needs real number from client
- Email: `projects@jnsconstructionfl.com` — confirmed by client
- Social links: placeholder `#` hrefs in footer — need real URLs
- Google Maps embed: placeholder `src` — needs real embed URL

## SEO / Metadata
- Every page has: `<title>`, `<meta description>`, canonical `<link>`, OG tags, favicon.
- Homepage has `GeneralContractor` JSON-LD schema.
- Service pages have `Service` JSON-LD schema.
- `sitemap.xml` covers all 11 pages.
- Google Search Console verified via TXT DNS record.
- `og:image` uses `https://jnsbuilds.com/images/hero-placementimage.png`.
