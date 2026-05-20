/* ─── JNS Construction Services — script.js ─────────────────── */

document.addEventListener("DOMContentLoaded", function () {

  /* =============================================================
     MOBILE NAV DRAWER
     ============================================================= */
  var hamburger      = document.getElementById("hamburger-btn");
  var overlay        = document.getElementById("nav-overlay");
  var mobileNav      = document.getElementById("mobile-nav");
  var mobileClose    = document.getElementById("mobile-nav-close");
  var servicesToggle = document.querySelector(".mobile-services-toggle");
  var servicesSub    = document.getElementById("mobile-services-sub");

  function openNav() {
    if (!mobileNav) return;
    mobileNav.classList.add("is-open");
    if (overlay)   overlay.classList.add("is-open");
    if (hamburger) {
      hamburger.classList.add("is-open");
      hamburger.setAttribute("aria-expanded", "true");
    }
    mobileNav.setAttribute("aria-hidden", "false");
    if (overlay) overlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeNav() {
    if (!mobileNav) return;
    mobileNav.classList.remove("is-open");
    if (overlay)   overlay.classList.remove("is-open");
    if (hamburger) {
      hamburger.classList.remove("is-open");
      hamburger.setAttribute("aria-expanded", "false");
    }
    mobileNav.setAttribute("aria-hidden", "true");
    if (overlay) overlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  if (hamburger)   hamburger.addEventListener("click", openNav);
  if (mobileClose) mobileClose.addEventListener("click", closeNav);
  if (overlay)     overlay.addEventListener("click", closeNav);

  if (mobileNav) {
    mobileNav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });
  }

  if (servicesToggle && servicesSub) {
    servicesToggle.addEventListener("click", function () {
      var expanded = this.getAttribute("aria-expanded") === "true";
      this.setAttribute("aria-expanded", String(!expanded));
      servicesSub.classList.toggle("is-open");
    });
  }

  /* =============================================================
     DESKTOP DROPDOWN NAV
     ============================================================= */
  document.querySelectorAll(".nav-dropdown-btn").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var expanded = this.getAttribute("aria-expanded") === "true";
      // Close all
      document.querySelectorAll(".nav-dropdown-btn").forEach(function (b) {
        b.setAttribute("aria-expanded", "false");
      });
      this.setAttribute("aria-expanded", String(!expanded));
    });
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".nav-dropdown-btn").forEach(function (b) {
      b.setAttribute("aria-expanded", "false");
    });
  });

  /* =============================================================
     SCROLL-REVEAL (IntersectionObserver)
     ============================================================= */
  var revealItems = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealItems.length > 0) {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    revealItems.forEach(function (el) { observer.observe(el); });
  } else {
    revealItems.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* =============================================================
     FAQ ACCORDION
     ============================================================= */
  document.querySelectorAll(".faq-question").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var expanded  = this.getAttribute("aria-expanded") === "true";
      var answerId  = this.getAttribute("aria-controls");
      var answer    = document.getElementById(answerId);

      // Close all others first
      document.querySelectorAll(".faq-question").forEach(function (other) {
        if (other === btn) return;
        other.setAttribute("aria-expanded", "false");
        var otherAnswer = document.getElementById(other.getAttribute("aria-controls"));
        if (otherAnswer) {
          otherAnswer.setAttribute("aria-hidden", "true");
          otherAnswer.setAttribute("inert", "");
        }
      });

      this.setAttribute("aria-expanded", String(!expanded));
      if (answer) {
        answer.setAttribute("aria-hidden", String(expanded));
        if (expanded) {
          answer.setAttribute("inert", "");
        } else {
          answer.removeAttribute("inert");
        }
      }
    });
  });

  /* =============================================================
     HERO FORM SUCCESS (formsubmit redirect alternative)
     Show inline success message if hash is set after redirect
     ============================================================= */
  if (window.location.hash === "#success") {
    var successEl = document.getElementById("form-success");
    var formEl    = document.getElementById("hero-contact-form");
    if (successEl && formEl) {
      formEl.hidden    = true;
      successEl.hidden = false;
    }
  }

  /* =============================================================
     LIGHTBOX (gallery page)
     ============================================================= */
  var lightbox = document.getElementById("gallery-lightbox");
  if (!lightbox) return;

  var lbImage   = lightbox.querySelector("img");
  var lbCaption = lightbox.querySelector(".lightbox-caption");
  var lbClose   = lightbox.querySelector(".lightbox-close");
  var lbPrev    = lightbox.querySelector(".lightbox-prev");
  var lbNext    = lightbox.querySelector(".lightbox-next");
  var lbLinks   = Array.prototype.slice.call(document.querySelectorAll(".gallery-img-link"));
  var lbIndex   = 0;

  function openLightbox(index) {
    lbIndex = index;
    var link = lbLinks[lbIndex];
    if (!link || !lbImage) return;
    lbImage.src = link.href;
    lbImage.alt = (link.querySelector("img") || {}).alt || "";
    if (lbCaption) lbCaption.textContent = link.getAttribute("data-caption") || lbImage.alt;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.style.overflow = "";
    if (lbImage) lbImage.src = "";
  }

  function moveLightbox(dir) {
    if (!lbLinks.length) return;
    lbIndex = (lbIndex + dir + lbLinks.length) % lbLinks.length;
    openLightbox(lbIndex);
  }

  lbLinks.forEach(function (link, i) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      openLightbox(i);
    });
  });

  if (lbClose)   lbClose.addEventListener("click", closeLightbox);
  if (lbPrev)    lbPrev.addEventListener("click", function () { moveLightbox(-1); });
  if (lbNext)    lbNext.addEventListener("click", function () { moveLightbox(1); });

  lightbox.querySelector(".lightbox-backdrop").addEventListener("click", closeLightbox);

  document.addEventListener("keydown", function (e) {
    if (lightbox.hidden) return;
    if (e.key === "Escape")      closeLightbox();
    if (e.key === "ArrowLeft")   moveLightbox(-1);
    if (e.key === "ArrowRight")  moveLightbox(1);
  });

  /* =============================================================
     GALLERY CAROUSEL (homepage)
     ============================================================= */
  (function () {
    var carousel  = document.getElementById("gallery-carousel");
    if (!carousel) return;

    var track    = document.getElementById("carousel-track");
    var prevBtn  = document.getElementById("carousel-prev");
    var nextBtn  = document.getElementById("carousel-next");
    var dotsWrap = document.getElementById("carousel-dots");
    var items    = Array.prototype.slice.call(track.querySelectorAll(".gallery-item"));
    var current  = 0;

    function getVisible() {
      return window.innerWidth <= 600 ? 1 : window.innerWidth <= 960 ? 2 : 4;
    }
    function getMax() { return Math.max(0, items.length - getVisible()); }

    function buildDots() {
      dotsWrap.innerHTML = "";
      var pages = Math.ceil(items.length / getVisible());
      for (var i = 0; i < pages; i++) {
        var dot = document.createElement("button");
        dot.className = "carousel-dot";
        dot.setAttribute("aria-label", "Slide " + (i + 1));
        dot.setAttribute("data-page", i);
        dot.addEventListener("click", function () {
          goTo(parseInt(this.getAttribute("data-page")) * getVisible());
        });
        dotsWrap.appendChild(dot);
      }
      updateDots();
    }

    function updateDots() {
      var page = Math.floor(current / getVisible());
      dotsWrap.querySelectorAll(".carousel-dot").forEach(function (d, i) {
        d.classList.toggle("is-active", i === page);
      });
    }

    function goTo(idx) {
      current = Math.max(0, Math.min(idx, getMax()));
      var itemW = items[0].getBoundingClientRect().width + 16;
      track.style.transform = "translateX(-" + (current * itemW) + "px)";
      prevBtn.disabled = current === 0;
      nextBtn.disabled = current >= getMax();
      updateDots();
    }

    prevBtn.addEventListener("click", function () { goTo(current - 1); });
    nextBtn.addEventListener("click", function () { goTo(current + 1); });

    buildDots();
    goTo(0);

    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        buildDots();
        goTo(Math.min(current, getMax()));
      }, 120);
    });
  }());
});
