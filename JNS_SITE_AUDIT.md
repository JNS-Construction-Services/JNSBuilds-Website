# JNS Construction Services Site Audit

Date: May 20, 2026
Site: https://jnsbuilds.com/
Local folder: `C:\Users\nknig\Downloads\JNSConstruction\jnsconstructionservicesllcwebiste`

## Completed In This Pass

- Refreshed the visual direction to follow the stronger Screen Team structure while keeping the JNS green/black brand.
- Added a more professional homepage rhythm: stronger hero, trust metrics, services, project gallery teaser, contact/map, reviews, FAQ, and footer links.
- Added `gallery.html` using the supplied project images from `Gallery/`.
- Added `script.js` for reveal states, FAQ accordion behavior, and gallery lightbox behavior.
- Added Gallery links to primary navigation and footer navigation across site pages.
- Updated `sitemap.xml` with `/gallery` and fresh lastmod dates for primary pages.
- Expanded `robots.txt` with sitemap reference and basic private-folder disallows.
- Preserved the existing Google map embed, estimate forms, phone links, email links, service pages, policy pages, analytics, and business identity.

## Highest-Impact Remaining Improvements

1. Image optimization
   - The gallery source images are large, many between 1 MB and 8 MB.
   - Generate compressed WebP/AVIF derivatives at practical sizes, such as 480, 900, and 1400 px.
   - Keep originals archived, but serve compressed images in `gallery.html` and homepage teasers.
   - This is likely the biggest remaining performance win.

2. Favicon package
   - Current favicon links use the full logo PNG rather than a complete favicon set.
   - Add `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, and Android icons.
   - Update all pages to reference the final icons consistently.

3. JavaScript consolidation
   - Most pages still include inline hamburger scripts.
   - Move the repeated mobile menu logic into `script.js` and include it globally.
   - This will reduce maintenance risk and make future navigation changes easier.

4. Analytics loading
   - Google Analytics and Microsoft Clarity load in the head on most pages.
   - Consider deferring Clarity until after initial page load to protect first paint and LCP.
   - Keep GA as-is if reporting continuity matters, but defer nonessential scripts.

5. Structured data cleanup
   - The homepage has multiple schema blocks. Some are helpful, but the `SiteLinksSearchBox` pattern is not useful because the site has no real search page.
   - Replace that with a cleaner graph: `GeneralContractor`, `WebSite`, `WebPage`, `BreadcrumbList`, `OfferCatalog`, and `FAQPage`.
   - Add `ImageGallery` schema to `gallery.html`.

6. Service page design consistency
   - Service pages are content-rich and valuable, but their layout is denser than the refreshed homepage.
   - Apply the new header/section/card polish consistently across all service pages.
   - Add small project-gallery strips on service pages where relevant.

7. Policy and footer cleanup
   - Footer links now include the gallery, but policy pages still have older page structure.
   - Bring policy pages onto the same compact header/footer and typography system.
   - Consider reducing policy page visual weight so they feel official but not over-designed.

8. Accessibility
   - Add skip-to-content link.
   - Ensure every interactive dropdown has keyboard-friendly behavior.
   - Replace emoji icons in service cards with inline SVG or accessible icon markup.
   - Confirm color contrast on muted green text, especially in dark cards.

9. Conversion tracking
   - Add click tracking for phone calls, email clicks, estimate form submissions, and Google review clicks.
   - Define GA4 events such as `click_call`, `submit_estimate_request`, `click_email`, `click_review`.

10. Local SEO additions
   - Add stronger city/service copy blocks without creating new service pages.
   - Add visible service area content to the homepage and contact page.
   - Add DBPR/license verification language near CTAs.

## Technical Notes

- The site is static HTML/CSS/JS and does not require a build step.
- Local test server used: `http://127.0.0.1:4173/`.
- Basic HTTP checks returned 200 for `/`, `/gallery.html`, and `/services/general-construction.html`.
- Local file-link validation found no missing local assets apart from `/#services`, which is a valid homepage anchor route.
- Because this session did not expose the Browser plugin's required Node control tool and Playwright is not installed locally, final visual QA was limited to static server and markup/link checks.

## Suggested Next Pass

1. Compress and resize gallery images.
2. Refactor repeated inline navigation scripts into `script.js`.
3. Apply the refreshed layout system across service and policy pages.
4. Add a complete favicon set.
5. Run a Lighthouse pass after image compression.
