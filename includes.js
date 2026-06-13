const SERVICE_PAGES = [
  "general-construction",
  "renovations-upgrades",
  "repairs-corrective-work",
  "project-coordination",
];

const NAV_ACTIVE_SELECTORS = {
  home: [".site-header .brand", ".mobile-nav-links a[href='/']"],
  about: [".site-nav > a[href='/about']", ".mobile-nav-links a[href='/about']"],
  gallery: [".site-nav > a[href='/gallery']", ".mobile-nav-links a[href='/gallery']"],
  contact: [".site-nav > a[href='/contact']", ".mobile-nav-links a[href='/contact']"],
  "general-construction": [
    ".nav-dropdown-menu a[href='/services/general-construction']",
    ".mobile-services-sub a[href='/services/general-construction']",
  ],
  "renovations-upgrades": [
    ".nav-dropdown-menu a[href='/services/renovations-upgrades']",
    ".mobile-services-sub a[href='/services/renovations-upgrades']",
  ],
  "repairs-corrective-work": [
    ".nav-dropdown-menu a[href='/services/repairs-corrective-work']",
    ".mobile-services-sub a[href='/services/repairs-corrective-work']",
  ],
  "project-coordination": [
    ".nav-dropdown-menu a[href='/services/project-coordination']",
    ".mobile-services-sub a[href='/services/project-coordination']",
  ],
  "privacy-policy": [".footer-nav a[href='/privacy-policy']"],
  "terms-of-service": [".footer-nav a[href='/terms-of-service']"],
  "payment-policy": [".footer-nav a[href='/payment-policy']"],
  "refund-policy": [".footer-nav a[href='/refund-policy']"],
};

function getIncludeBase() {
  const script = document.querySelector('script[src*="includes.js"]');
  if (!script || !script.src) return "";
  return script.src.replace(/includes\.js(?:\?.*)?$/, "");
}

function getCurrentNavPage() {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  if (path === "/" || path.endsWith("/index.html")) return "home";
  const segment = path.split("/").pop() || "";
  return segment.replace(/\.html$/, "");
}

function isHomePage() {
  return (
    document.body.classList.contains("home-landing") ||
    window.location.pathname === "/" ||
    window.location.pathname.endsWith("/index.html")
  );
}

function applyHeaderAdjustments() {
  const brand = document.querySelector(".site-header .brand");
  if (brand) {
    brand.setAttribute("href", isHomePage() ? "#top" : "/");
  }

  document.querySelectorAll('[aria-current="page"]').forEach((el) => {
    el.removeAttribute("aria-current");
  });

  const page = getCurrentNavPage();
  (NAV_ACTIVE_SELECTORS[page] || []).forEach((selector) => {
    document.querySelectorAll(selector).forEach((link) => {
      link.setAttribute("aria-current", "page");
    });
  });

  if (SERVICE_PAGES.includes(page)) {
    const servicesBtn = document.querySelector(".nav-dropdown-wrap .nav-dropdown-btn");
    if (servicesBtn) servicesBtn.setAttribute("aria-current", "page");
  }
}

async function fetchInclude(path) {
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to load ${path} (${response.status})`);
  }
  return response.text();
}

function injectInclude(slot, html) {
  if (!slot || !html) return;
  slot.insertAdjacentHTML("afterend", html.trim());
  slot.remove();
}

async function loadSiteIncludes() {
  const base = getIncludeBase();
  const headerSlot = document.getElementById("site-header-include");
  const footerSlot = document.getElementById("site-footer-include");
  const tasks = [];

  if (headerSlot) {
    tasks.push(
      fetchInclude(`${base}header.html`).then((html) => injectInclude(headerSlot, html)),
    );
  }

  if (footerSlot) {
    tasks.push(
      fetchInclude(`${base}footer.html`).then((html) => injectInclude(footerSlot, html)),
    );
  }

  await Promise.all(tasks);

  if (!document.querySelector(".site-header")) {
    console.warn("Site header was not injected. Check header.html and includes.js.");
    return;
  }

  applyHeaderAdjustments();
  document.dispatchEvent(new CustomEvent("site:includes-loaded"));
}

function initSiteIncludes() {
  loadSiteIncludes().catch((error) => {
    console.error("Site includes failed to load:", error);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSiteIncludes);
} else {
  initSiteIncludes();
}
