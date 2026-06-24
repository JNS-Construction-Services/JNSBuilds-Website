# JNS Construction Services — Site Structure

Repo root = GitHub Pages site root (`https://jnsbuilds.com`).

## Production pages

| File | Canonical URL | Description |
|------|---------------|-------------|
| `index.html` | `https://jnsbuilds.com/` | **Live homepage** — hero, about, services, gallery carousel, reviews, estimate form |
| `about.html` | `https://jnsbuilds.com/about` | About the company |
| `contact.html` | `https://jnsbuilds.com/contact` | Contact + estimate form + map |
| `gallery.html` | `https://jnsbuilds.com/gallery` | Full project gallery |
| `services/general-construction.html` | `.../services/general-construction` | Service detail |
| `services/renovations-upgrades.html` | `.../services/renovations-upgrades` | Service detail |
| `services/repairs-corrective-work.html` | `.../services/repairs-corrective-work` | Service detail |
| `services/project-coordination.html` | `.../services/project-coordination` | Service detail |
| `privacy-policy.html` | `https://jnsbuilds.com/privacy-policy` | Privacy policy |
| `thank-you.html` | `https://jnsbuilds.com/thank-you` | Form submission confirmation (noindex) |
| `terms-of-service.html` | `https://jnsbuilds.com/terms-of-service` | Terms |
| `payment-policy.html` | `https://jnsbuilds.com/payment-policy` | Payment terms |
| `refund-policy.html` | `https://jnsbuilds.com/refund-policy` | Refund policy |

## Not deployed

| Path | Notes |
|------|--------|
| `_archive/homepage-drafts/` | Retired `index_carousel.html` and `index_prev.html` — see README there |

## Navigation (production)

```
Home (index.html)
├── About → about.html
├── Our Work → gallery.html
├── Services ▼
│   ├── General Construction
│   ├── Renovations & Upgrades
│   ├── Repairs & Corrective Work
│   └── Project Coordination
├── Reviews → index.html#reviews
└── Contact → contact.html / index.html#contact
```

## Forms

Processor: **Formspree** → `https://formspree.io/f/xaqgqgyg`

**Account:** JNS owns their own Formspree account (not shared with Knight Group, Knight Logics, or other client sites). Same model as Screen Team and Faith Works.

**Client setup (JNS):** Form `xaqgqgyg` is live. If replacing in the future, find/replace `xaqgqgyg` in all six HTML forms.

Notification email: `projects@jnsconstructionfl.com`

Used on: `index.html` (hero), `contact.html`, sidebar forms on service pages. Redirects to `thank-you.html` via `_next`.

## Shared assets

| Asset | Location |
|-------|----------|
| Styles | `styles.css` (root); `../styles.css` from `services/` |
| Scripts | `script.js` (root); `../script.js` from `services/` |
| Logos / hero | `images/` |
| Gallery photos | `Gallery/*.webp` |

## Development notes

- No build step — static HTML/CSS/JS only.
- Inner pages use `.inner-hero`, `.inner-section`, `.feature-grid`, etc.
- Service pages set `aria-current="page"` on their nav item.
- See `.github/copilot-instructions.md` for agent/editor rules.
