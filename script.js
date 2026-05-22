document.addEventListener("DOMContentLoaded", function () {
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

	const revealItems = document.querySelectorAll("[data-reveal]");
	if ("IntersectionObserver" in window && revealItems.length > 0) {
		const revealObserver = new IntersectionObserver(
			function (entries, observer) {
				entries.forEach(function (entry) {
					if (!entry.isIntersecting) {
						return;
					}

					entry.target.classList.add("is-visible");
					observer.unobserve(entry.target);
				});
			},
			{
				threshold: 0.12,
				rootMargin: "0px 0px -40px 0px"
			}
		);

		revealItems.forEach(function (item) {
			revealObserver.observe(item);
		});
	} else {
		revealItems.forEach(function (item) {
			item.classList.add("is-visible");
		});
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