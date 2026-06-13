function initSiteChrome() {
	if (document.body.dataset.chromeInit === "1") {
		return;
	}
	document.body.dataset.chromeInit = "1";

	const hamburgerBtn = document.getElementById("hamburger-btn");
	const navOverlay = document.getElementById("nav-overlay");
	const mobileNav = document.getElementById("mobile-nav");
	const mobileNavClose = document.getElementById("mobile-nav-close");
	const mobileServicesToggle = document.querySelector(".mobile-services-toggle");
	const mobileServicesSub = document.getElementById("mobile-services-sub");

	function closeMobileNav() {
		if (!mobileNav) {
			return;
		}

		mobileNav.classList.remove("is-open");
		mobileNav.setAttribute("aria-hidden", "true");

		if (navOverlay) {
			navOverlay.classList.remove("is-open");
			navOverlay.setAttribute("aria-hidden", "true");
		}

		if (hamburgerBtn) {
			hamburgerBtn.classList.remove("is-open");
			hamburgerBtn.setAttribute("aria-expanded", "false");
		}

		document.body.style.overflow = "";
	}

	if (hamburgerBtn) {
		hamburgerBtn.addEventListener("click", function () {
			if (!mobileNav) {
				return;
			}

			mobileNav.classList.add("is-open");
			mobileNav.setAttribute("aria-hidden", "false");

			if (navOverlay) {
				navOverlay.classList.add("is-open");
				navOverlay.setAttribute("aria-hidden", "false");
			}

			hamburgerBtn.classList.add("is-open");
			hamburgerBtn.setAttribute("aria-expanded", "true");
			document.body.style.overflow = "hidden";
		});
	}

	if (mobileNavClose) {
		mobileNavClose.addEventListener("click", closeMobileNav);
	}

	if (navOverlay) {
		navOverlay.addEventListener("click", closeMobileNav);
	}

	if (mobileNav) {
		mobileNav.querySelectorAll("a").forEach(function (link) {
			link.addEventListener("click", closeMobileNav);
		});
	}

	if (mobileServicesToggle && mobileServicesSub) {
		mobileServicesToggle.addEventListener("click", function () {
			const isExpanded = this.getAttribute("aria-expanded") === "true";
			this.setAttribute("aria-expanded", String(!isExpanded));
			mobileServicesSub.classList.toggle("is-open");
		});
	}

	document.querySelectorAll(".nav-dropdown-btn").forEach(function (button) {
		button.addEventListener("click", function (event) {
			event.stopPropagation();
			const isExpanded = this.getAttribute("aria-expanded") === "true";

			document.querySelectorAll(".nav-dropdown-btn").forEach(function (dropdownButton) {
				dropdownButton.setAttribute("aria-expanded", "false");
			});

			this.setAttribute("aria-expanded", String(!isExpanded));
		});
	});

	document.addEventListener("click", function () {
		document.querySelectorAll(".nav-dropdown-btn").forEach(function (button) {
			button.setAttribute("aria-expanded", "false");
		});
	});
}

function initHeaderScroll() {
	const header = document.querySelector(".site-header");
	if (!header || header.dataset.scrollInit === "1") {
		return;
	}

	header.dataset.scrollInit = "1";
	const update = function () {
		header.classList.toggle("scrolled", window.scrollY > 40);
	};
	update();
	window.addEventListener("scroll", update, { passive: true });
}

function initStGoogleReviews() {
	const carousels = document.querySelectorAll("[data-st-review-carousel]");
	if (!carousels.length) {
		return;
	}

	carousels.forEach(function (carousel) {
		if (carousel.dataset.reviewsInit === "1") {
			return;
		}
		carousel.dataset.reviewsInit = "1";

		const track = carousel.querySelector(".st-review-carousel-track");
		const prevBtn = carousel.querySelector(".st-review-carousel-btn.prev");
		const nextBtn = carousel.querySelector(".st-review-carousel-btn.next");
		const showcase = carousel.closest(".st-google-reviews-showcase");
		const dotsContainer = showcase ? showcase.querySelector(".st-review-carousel-dots") : null;
		const summaryEl = document.getElementById("st-review-summary");
		const mapRatingEl = document.getElementById("st-map-rating");
		const seedEl = showcase ? showcase.querySelector("#google-reviews-seed") : null;

		if (!track || !prevBtn || !nextBtn || !dotsContainer || !showcase) {
			return;
		}

		let cards = [];
		let currentIndex = 0;
		let reviews = [];

		function escapeHtml(value) {
			return String(value || "")
				.replace(/&/g, "&amp;")
				.replace(/</g, "&lt;")
				.replace(/>/g, "&gt;")
				.replace(/"/g, "&quot;")
				.replace(/'/g, "&#39;");
		}

		function getInitial(name) {
			const clean = String(name || "").trim();
			return clean ? clean.charAt(0).toUpperCase() : "?";
		}

		function formatStars(count) {
			const stars = Math.max(0, Math.min(5, Number(count) || 0));
			return "\u2605".repeat(stars);
		}

		function reviewCardMarkup(review) {
			return (
				'<article class="st-review-card">' +
				'<div class="st-review-card-header">' +
				'<span class="st-review-avatar" style="background:' +
				escapeHtml(review.avatarColor || "#3a6b12") +
				';" aria-hidden="true">' +
				escapeHtml(getInitial(review.name)) +
				"</span>" +
				"<div>" +
				'<div class="st-review-name">' +
				escapeHtml(review.name) +
				"</div>" +
				'<div class="st-review-meta">' +
				escapeHtml(review.meta || "") +
				"</div>" +
				"</div>" +
				"</div>" +
				'<div class="st-review-card-stars" role="img" aria-label="' +
				escapeHtml(String(Number(review.stars) || 5)) +
				' stars">' +
				formatStars(review.stars) +
				"</div>" +
				'<p class="st-review-text">' +
				escapeHtml(review.text || "") +
				"</p>" +
				'<div class="st-review-date">' +
				escapeHtml(review.date || "") +
				"</div>" +
				"</article>"
			);
		}

		function applySummary(payload) {
			const count = Number(payload.reviewCount || reviews.length || 0);
			const rating = count > 0 ? Number(payload.ratingValue || 5).toFixed(1) : "—";
			const label = count === 1 ? " review" : " reviews";
			const summaryText = count > 0 ? rating + " \u00b7 " + count + label : "No Google reviews yet";
			if (summaryEl) {
				summaryEl.textContent = summaryText;
			}
			if (mapRatingEl) {
				mapRatingEl.textContent =
					count > 0
						? formatStars(payload.ratingValue || 5) + " " + rating + " \u00b7 " + count + " Google review" + (count === 1 ? "" : "s")
						: "Be the first to review JNS on Google";
			}
		}

		function visibleCount() {
			if (window.innerWidth <= 720) {
				return 1;
			}
			if (window.innerWidth <= 1060) {
				return 2;
			}
			return 3;
		}

		function pageCount() {
			return Math.max(1, Math.ceil(cards.length / visibleCount()));
		}

		function maxIndex() {
			return Math.max(0, cards.length - visibleCount());
		}

		function cardSpan() {
			if (!cards.length) {
				return 0;
			}
			const styles = window.getComputedStyle(track);
			const gap = parseFloat(styles.columnGap || styles.gap || "0");
			return cards[0].getBoundingClientRect().width + gap;
		}

		function updateButtons() {
			const singlePage = pageCount() <= 1 || cards.length === 0;
			prevBtn.disabled = singlePage || currentIndex <= 0;
			nextBtn.disabled = singlePage || currentIndex >= maxIndex();
		}

		function update() {
			currentIndex = Math.max(0, Math.min(currentIndex, maxIndex()));
			track.style.transform = "translateX(" + -currentIndex * cardSpan() + "px)";

			const activePage = Math.floor(currentIndex / visibleCount());
			dotsContainer.querySelectorAll(".st-review-carousel-dot").forEach(function (dot, index) {
				const isActive = index === activePage;
				dot.classList.toggle("active", isActive);
				if (isActive) {
					dot.setAttribute("aria-current", "true");
				} else {
					dot.removeAttribute("aria-current");
				}
			});

			updateButtons();
		}

		function buildDots() {
			dotsContainer.innerHTML = "";
			for (let index = 0; index < pageCount(); index += 1) {
				const dot = document.createElement("button");
				dot.type = "button";
				dot.className = "st-review-carousel-dot" + (index === 0 ? " active" : "");
				dot.setAttribute("aria-label", "Go to review page " + (index + 1));
				if (index === 0) {
					dot.setAttribute("aria-current", "true");
				}
				dot.addEventListener("click", function () {
					currentIndex = index * visibleCount();
					update();
				});
				dotsContainer.appendChild(dot);
			}
		}

		function renderReviews(payload) {
			reviews = Array.isArray(payload.reviews) ? payload.reviews.slice() : [];
			applySummary(payload);

			if (!reviews.length) {
				track.innerHTML =
					'<article class="st-reviews-empty">' +
					"<p>We're building our Google review presence. If JNS Construction has completed work for you, we'd appreciate your feedback.</p>" +
					'<a class="btn btn-primary" href="https://g.page/r/CZ_HHTzVN4xTEBM/review" target="_blank" rel="noopener noreferrer">Leave a Google Review</a>' +
					"</article>";
			} else {
				track.innerHTML = reviews.map(reviewCardMarkup).join("");
			}

			cards = Array.from(track.querySelectorAll(".st-review-card, .st-reviews-empty"));
			currentIndex = 0;
			carousel.classList.toggle("single-review", cards.length <= 1);
			buildDots();
			update();
		}

		function parseSeedPayload() {
			if (!seedEl) {
				return null;
			}
			try {
				return JSON.parse(seedEl.textContent || "{}");
			} catch (error) {
				console.warn("Google review seed parse failed:", error);
				return null;
			}
		}

		async function loadReviews() {
			let payload = null;
			const feedPath = "/data/google-reviews.json";

			try {
				const response = await fetch(feedPath, { cache: "no-store" });
				if (response.ok) {
					payload = await response.json();
				}
			} catch (error) {
				console.warn("Google review feed fetch failed, using seed data:", error);
			}

			if (!payload) {
				payload = parseSeedPayload();
			}
			if (!payload || !Array.isArray(payload.reviews)) {
				payload = { ratingValue: 0, reviewCount: 0, reviews: [] };
			}

			renderReviews(payload);
		}

		prevBtn.addEventListener("click", function () {
			currentIndex -= 1;
			update();
		});
		nextBtn.addEventListener("click", function () {
			currentIndex += 1;
			update();
		});
		window.addEventListener("resize", function () {
			buildDots();
			update();
		});

		loadReviews();
	});
}

document.addEventListener("DOMContentLoaded", function () {
	function prefersReducedMotion() {
		return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
	}

	function initScrollReveal() {
		const revealEls = document.querySelectorAll(
			".reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-photo, .slide-enter, [data-reveal], .eyebrow:not(.hero-enter), .card-eyebrow:not(.hero-enter)"
		);

		if (!revealEls.length) {
			return;
		}

		if ("IntersectionObserver" in window) {
			const revealObserver = new IntersectionObserver(
				function (entries, observer) {
					entries.forEach(function (entry) {
						if (!entry.isIntersecting) {
							return;
						}

						entry.target.classList.add("visible", "is-visible");
						observer.unobserve(entry.target);
					});
				},
				{
					threshold: 0.12,
					rootMargin: "0px 0px -40px 0px"
				}
			);

			revealEls.forEach(function (item) {
				revealObserver.observe(item);
			});
		} else {
			revealEls.forEach(function (item) {
				item.classList.add("visible", "is-visible");
			});
		}
	}

	function initHeroPanels() {
		document.querySelectorAll(".hero-panels").forEach(function (panels) {
			const hero = panels.closest(".hero");
			if (!hero || hero.dataset.panelsInit) {
				return;
			}

			hero.dataset.panelsInit = "1";
			requestAnimationFrame(function () {
				hero.classList.add("hero-panels-ready");
			});
		});
	}

	function initHomeStripEntrance() {
		if (!document.body.classList.contains("home-landing")) {
			return;
		}

		const items = document.querySelectorAll(
			".trust-strip .strip-slide, .st-intent-strip .strip-slide"
		);
		if (!items.length) {
			return;
		}

		const reveal = function () {
			items.forEach(function (item) {
				item.classList.add("is-visible");
			});
		};

		if (prefersReducedMotion()) {
			reveal();
			return;
		}

		const start = function () {
			setTimeout(reveal, 1850);
		};
		const hero = document.querySelector(".hero");

		if (hero && hero.classList.contains("hero-panels-ready")) {
			start();
			return;
		}

		if (!hero) {
			start();
			return;
		}

		const observer = new MutationObserver(function () {
			if (!hero.classList.contains("hero-panels-ready")) {
				return;
			}

			observer.disconnect();
			start();
		});

		observer.observe(hero, { attributes: true, attributeFilter: ["class"] });
	}

	function initHeroParallax() {
		if (prefersReducedMotion()) {
			return;
		}

		const hero = document.querySelector("body.home-landing .hero");
		if (!hero) {
			return;
		}

		const layers = hero.querySelectorAll(".hero-panels, .hero-cutout-wrap, .hero-overlay");
		if (!layers.length) {
			return;
		}

		let ticking = false;

		function update() {
			ticking = false;
			const heroTop = hero.offsetTop;
			const heroHeight = hero.offsetHeight;
			const offset = Math.max(0, window.scrollY - heroTop);
			const shift = Math.min(offset * 0.4, heroHeight);

			layers.forEach(function (layer) {
				layer.style.setProperty("--st-hero-shift", Math.round(shift) + "px");
			});
		}

		function queue() {
			if (ticking) {
				return;
			}

			ticking = true;
			requestAnimationFrame(update);
		}

		update();
		window.addEventListener("scroll", queue, { passive: true });
		window.addEventListener("resize", queue, { passive: true });
	}

	function initParallaxBands() {
		if (prefersReducedMotion()) {
			return;
		}

		const backgrounds = document.querySelectorAll(".st-parallax-bg");
		if (!backgrounds.length) {
			return;
		}

		let ticking = false;

		function getOverscanPx(band) {
			if (band.dataset.parallaxOverscan) {
				return band.offsetHeight * Number(band.dataset.parallaxOverscan);
			}

			if (band.classList.contains("st-process-band")) {
				return band.offsetHeight * 0.08;
			}

			if (band.classList.contains("st-route-band--parallax")) {
				return band.offsetHeight * 0.28;
			}

			return band.offsetHeight * 0.3;
		}

		function clampShift(shift, maxShift) {
			return Math.round(Math.max(-maxShift, Math.min(maxShift, shift)));
		}

		function applyParallax(target, band) {
			const vh = Math.max(window.innerHeight, 1);
			const rect = band.getBoundingClientRect();
			if (rect.bottom < 0 || rect.top > vh) {
				return;
			}

			const maxShift = getOverscanPx(band);
			let shift;

			if (band.classList.contains("st-process-band")) {
				shift = (rect.top - vh) * 0.35 + 56;
			} else if (band.classList.contains("st-route-band--parallax")) {
				shift = (rect.top - vh) * 0.28;
			} else {
				shift = (rect.top - vh) * 0.45;
			}

			target.style.setProperty("--st-band-shift", clampShift(shift, maxShift) + "px");
		}

		function update() {
			ticking = false;

			backgrounds.forEach(function (bg) {
				const band = bg.closest(".work-teaser--parallax, .map-section--parallax, .st-process-band, .st-route-band--parallax");
				if (!band) {
					return;
				}

				applyParallax(bg, band);
			});
		}

		function queue() {
			if (ticking) {
				return;
			}

			ticking = true;
			requestAnimationFrame(update);
		}

		update();
		window.addEventListener("scroll", queue, { passive: true });
		window.addEventListener("resize", queue, { passive: true });
	}

	initScrollReveal();
	initHeroPanels();
	initHomeStripEntrance();
	initHeroParallax();
	initParallaxBands();
	initStGoogleReviews();
	initHeaderScroll();

	if (document.querySelector(".site-header") && !document.getElementById("site-header-include")) {
		initSiteChrome();
	}

	document.querySelectorAll(".faq-question").forEach(function (button) {
		button.addEventListener("click", function () {
			const isExpanded = this.getAttribute("aria-expanded") === "true";
			const panel = document.getElementById(this.getAttribute("aria-controls"));

			document.querySelectorAll(".faq-question").forEach(function (question) {
				if (question === button) {
					return;
				}

				question.setAttribute("aria-expanded", "false");
				const siblingPanel = document.getElementById(question.getAttribute("aria-controls"));
				if (siblingPanel) {
					siblingPanel.setAttribute("aria-hidden", "true");
					siblingPanel.setAttribute("inert", "");
				}
			});

			this.setAttribute("aria-expanded", String(!isExpanded));

			if (panel) {
				panel.setAttribute("aria-hidden", String(isExpanded));
				if (isExpanded) {
					panel.setAttribute("inert", "");
				} else {
					panel.removeAttribute("inert");
				}
			}
		});
	});

	if (window.location.hash === "#success") {
		const formSuccess = document.getElementById("form-success");
		const heroContactForm = document.getElementById("hero-contact-form");
		if (formSuccess && heroContactForm) {
			heroContactForm.hidden = true;
			formSuccess.hidden = false;
		}
	}

	const homepageCarousel = document.getElementById("gallery-carousel");
	if (homepageCarousel) {
		const overflow = homepageCarousel.querySelector(".carousel-overflow");
		const track = homepageCarousel.querySelector(".carousel-track");
		const slides = Array.from(homepageCarousel.querySelectorAll(".carousel-slide"));
		const prevButton = homepageCarousel.querySelector(".carousel-prev");
		const nextButton = homepageCarousel.querySelector(".carousel-next");
		const dots = homepageCarousel.querySelector(".carousel-dots");
		let currentIndex = 0;
		let scrollFrame = null;

		function slidesPerView() {
			return window.innerWidth <= 600 ? 1 : 2;
		}

		function maxIndex() {
			return Math.max(0, slides.length - slidesPerView());
		}

		function slideOffset(index) {
			const slide = slides[index];
			return slide ? slide.offsetLeft - track.offsetLeft : 0;
		}

		function updateControls() {
			if (prevButton) {
				prevButton.disabled = currentIndex <= 0;
			}

			if (nextButton) {
				nextButton.disabled = currentIndex >= maxIndex();
			}

			if (dots) {
				dots.querySelectorAll(".carousel-dot").forEach(function (dot, index) {
					const isActive = index === currentIndex;
					dot.classList.toggle("is-active", isActive);
					dot.setAttribute("aria-pressed", String(isActive));
				});
			}
		}

		function renderDots() {
			if (!dots) {
				return;
			}

			dots.innerHTML = "";
			for (let index = 0; index <= maxIndex(); index += 1) {
				const dot = document.createElement("button");
				dot.type = "button";
				dot.className = "carousel-dot";
				dot.setAttribute("aria-label", "Show project slide " + (index + 1));
				dot.setAttribute("aria-pressed", String(index === currentIndex));
				dot.addEventListener("click", function () {
					goToSlide(index);
				});
				dots.appendChild(dot);
			}

			updateControls();
		}

		function goToSlide(index, behavior) {
			const targetIndex = Math.max(0, Math.min(index, maxIndex()));
			currentIndex = targetIndex;

			if (overflow) {
				overflow.scrollTo({
					left: slideOffset(targetIndex),
					behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : (behavior || "smooth")
				});
			}

			updateControls();
		}

		function syncFromScroll() {
			let closestIndex = 0;
			let closestDistance = Number.POSITIVE_INFINITY;

			for (let index = 0; index <= maxIndex(); index += 1) {
				const distance = Math.abs(overflow.scrollLeft - slideOffset(index));
				if (distance < closestDistance) {
					closestDistance = distance;
					closestIndex = index;
				}
			}

			currentIndex = closestIndex;
			updateControls();
		}

		if (prevButton) {
			prevButton.addEventListener("click", function () {
				goToSlide(currentIndex - 1);
			});
		}

		if (nextButton) {
			nextButton.addEventListener("click", function () {
				goToSlide(currentIndex + 1);
			});
		}

		if (overflow) {
			overflow.addEventListener(
				"scroll",
				function () {
					if (scrollFrame) {
						window.cancelAnimationFrame(scrollFrame);
					}

					scrollFrame = window.requestAnimationFrame(function () {
						scrollFrame = null;
						syncFromScroll();
					});
				},
				{ passive: true }
			);
		}

		window.addEventListener("resize", function () {
			renderDots();
			goToSlide(currentIndex, "auto");
		});

		renderDots();
		goToSlide(0, "auto");
	}

	const lightbox = document.getElementById("gallery-lightbox");
	const galleryFilters = document.querySelectorAll(".gallery-filter");
	const galleryItems = document.querySelectorAll("#gallery-grid .gallery-item");

	if (galleryFilters.length > 0 && galleryItems.length > 0) {
		galleryFilters.forEach(function (button) {
			button.addEventListener("click", function () {
				const selected = button.getAttribute("data-filter");

				galleryFilters.forEach(function (filterButton) {
					filterButton.classList.toggle("is-active", filterButton === button);
				});

				galleryItems.forEach(function (item) {
					const category = item.getAttribute("data-category");
					const show = selected === "all" || category === selected;
					item.classList.toggle("is-hidden", !show);
				});
			});
		});
	}

	if (lightbox) {
		const lightboxImage = lightbox.querySelector("img");
		const lightboxCaption = lightbox.querySelector(".lightbox-caption");
		const closeButton = lightbox.querySelector(".lightbox-close");
		const prevLightboxButton = lightbox.querySelector(".lightbox-prev");
		const nextLightboxButton = lightbox.querySelector(".lightbox-next");
		const galleryLinks = Array.from(document.querySelectorAll(".gallery-img-link"));
		let currentImageIndex = 0;

		function openLightbox(index) {
			const link = galleryLinks[index];
			currentImageIndex = index;

			if (!link || !lightboxImage) {
				return;
			}

			const previewImage = link.querySelector("img");
			lightboxImage.src = link.href;
			lightboxImage.alt = previewImage ? previewImage.alt : "";

			if (lightboxCaption) {
				lightboxCaption.textContent = link.getAttribute("data-caption") || lightboxImage.alt;
			}

			lightbox.hidden = false;
			document.body.style.overflow = "hidden";
		}

		function closeLightbox() {
			lightbox.hidden = true;
			document.body.style.overflow = "";

			if (lightboxImage) {
				lightboxImage.src = "";
			}
		}

		function changeImage(direction) {
			if (!galleryLinks.length) {
				return;
			}

			const nextIndex = (currentImageIndex + direction + galleryLinks.length) % galleryLinks.length;
			openLightbox(nextIndex);
		}

		galleryLinks.forEach(function (link, index) {
			link.addEventListener("click", function (event) {
				event.preventDefault();
				openLightbox(index);
			});
		});

		if (closeButton) {
			closeButton.addEventListener("click", closeLightbox);
		}

		if (prevLightboxButton) {
			prevLightboxButton.addEventListener("click", function () {
				changeImage(-1);
			});
		}

		if (nextLightboxButton) {
			nextLightboxButton.addEventListener("click", function () {
				changeImage(1);
			});
		}

		const backdrop = lightbox.querySelector(".lightbox-backdrop");
		if (backdrop) {
			backdrop.addEventListener("click", closeLightbox);
		}

		document.addEventListener("keydown", function (event) {
			if (lightbox.hidden) {
				return;
			}

			if (event.key === "Escape") {
				closeLightbox();
			}
			if (event.key === "ArrowLeft") {
				changeImage(-1);
			}
			if (event.key === "ArrowRight") {
				changeImage(1);
			}
		});
	}
});

document.addEventListener("site:includes-loaded", function () {
	initSiteChrome();
	initHeaderScroll();
}, { once: true });