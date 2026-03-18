# JNS Construction Services — Site Structure

## Pages

### Root (`jns-v2/`)

| File | Canonical URL | Description |
|------|---------------|-------------|
| `index.html` | `https://jnsbuilds.com/` | Homepage — hero, about, services overview, contact/estimate form, reviews |
| `privacy-policy.html` | `https://jnsbuilds.com/privacy-policy` | Privacy policy for website visitors |
| `terms-of-service.html` | `https://jnsbuilds.com/terms-of-service` | Terms of service for site use |
| `payment-policy.html` | `https://jnsbuilds.com/payment-policy` | Contractor payment terms, deposits, billing |

### Services (`jns-v2/services/`)

| File | Canonical URL | Description |
|------|---------------|-------------|
| `general-construction.html` | `https://jnsbuilds.com/services/general-construction` | New builds, room additions, structural framing, accessory structures, light commercial |
| `renovations-upgrades.html` | `https://jnsbuilds.com/services/renovations-upgrades` | Kitchen, bathroom, flooring, whole-home renovations |
| `repairs-corrective-work.html` | `https://jnsbuilds.com/services/repairs-corrective-work` | Water/storm damage, code corrections, structural repairs, drywall/carpentry |
| `project-coordination.html` | `https://jnsbuilds.com/services/project-coordination` | GC role, subcontractor management, permit coordination, scheduling, budget oversight |

---

## Navigation Structure

```
Home (index.html)
├── About → index.html#about
├── Services ▼
│   ├── General Construction → services/general-construction.html
│   ├── Renovations & Upgrades → services/renovations-upgrades.html
│   ├── Repairs & Corrective Work → services/repairs-corrective-work.html
│   └── Project Coordination → services/project-coordination.html
├── Reviews → index.html#reviews
└── Contact → index.html#contact
```

---

## Footer Links

| Label | Target |
|-------|--------|
| Privacy Policy | `privacy-policy.html` (or `../privacy-policy.html` from services/) |
| Terms of Service | `terms-of-service.html` (or `../terms-of-service.html` from services/) |
| Payment Policy | `payment-policy.html` (or `../payment-policy.html` from services/) |

---

## Shared Stylesheet

All pages share `jns-v2/styles.css`. Relative path by location:

| Page location | CSS path |
|---------------|----------|
| `jns-v2/` (index, policy pages) | `./styles.css` |
| `jns-v2/services/` | `../styles.css` |

---

## Assets

Located one level above `jns-v2/` at the site root:

| Asset | Path from `jns-v2/` | Path from `jns-v2/services/` |
|-------|---------------------|-------------------------------|
| `Logo_WHITE-01.png` | `../Logo_WHITE-01.png` | `../../Logo_WHITE-01.png` |
| `hero-placementimage.png` | `../hero-placementimage.png` | (not used on service pages) |

---

## Placeholders Still Needing Real Data

| Location | Placeholder | Replace With |
|----------|-------------|--------------|
| All pages nav + footer | `(555) 010-0000` / `+15550100000` | Real phone number |
| `index.html` form | `YOUR_FORM_ID` in Formspree action URL | Real Formspree form ID |
| `index.html` JSON-LD schema | `[REPLACE WITH REAL PHONE]` | Real phone number |
| All pages footer | `href="#"` on Facebook, Instagram, LinkedIn | Real social media URLs |

---

## Copilot / Development Notes

- No build system — all static HTML/CSS/JS
- Inner pages use `.inner-hero` header class (dark panel, no background image)
- Shared CSS classes for inner pages: `.inner-section`, `.inner-section--panel`, `.feature-grid`, `.feature-card`, `.process-steps`, `.process-step`, `.step-num`, `.step-body`, `.inner-cta`, `.policy-content`
- The `.top-nav` hamburger and mobile nav work identically on all pages (same JS, same CSS)
- Service cards on `index.html#services` link to the dedicated service pages
- All 4 service pages use `aria-current="page"` on their own dropdown link
