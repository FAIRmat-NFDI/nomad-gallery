/* =========================================================
   ZIP-style gallery filter
   ========================================================= */
(function () {
  function initZipStyleGalleryFilter() {
    const container = document.getElementById("galleryCards");
    const filterRoot = document.getElementById("galleryFilter");

    if (!container || !filterRoot) return;
    if (filterRoot.dataset.galleryInit === "true") return;
    filterRoot.dataset.galleryInit = "true";

    const chips = Array.from(filterRoot.querySelectorAll(".gallery-filter__chip"));
    const controlRow = document.getElementById("galleryFilterControlRow");
    const clearBtn = document.getElementById("clearGalleryFilters");
    const sortBtn = document.getElementById("sortGallery");
    const countEl = document.getElementById("galleryResultsCount");
    const keywordDatalist = document.getElementById("galleryKeywordSuggestions");

    let activeFilter = "methodology";
    let sortOrder = "desc"; // desc = newest first

    const state = {
      methodology: "All",
      field: "All",
      country: "All",
      keywords: ""
    };

    function norm(value) {
      return (value || "").toString().trim().toLowerCase();
    }

    function getCards() {
      return Array.from(container.querySelectorAll(".gallery-card"));
    }

    function parseDate(card) {
      const raw = card.getAttribute("data-submission-date") || "";
      const ts = Date.parse(raw);
      return Number.isFinite(ts) ? ts : 0;
    }

    function uniqueSorted(values) {
      return Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b));
    }

    function getOptionsFromCards() {
      const cards = getCards();

      const methodologies = uniqueSorted(
        cards.map((card) => (card.dataset.methodology || "").trim())
      );

      const fields = uniqueSorted(
        cards.map((card) => (card.dataset.researchField || "").trim())
      );

      const countries = uniqueSorted(
        cards.map((card) => (card.dataset.country || "").trim())
      );

      const keywords = uniqueSorted(
        cards.flatMap((card) =>
          (card.dataset.keywords || "")
            .split(",")
            .map((k) => k.trim())
            .filter(Boolean)
        )
      );

      return { methodologies, fields, countries, keywords };
    }

    function buildKeywordSuggestions() {
      if (!keywordDatalist) return;
      const { keywords } = getOptionsFromCards();
      keywordDatalist.innerHTML = keywords
        .map((k) => `<option value="${k.replace(/"/g, "&quot;")}"></option>`)
        .join("");
    }

    function renderSelect(options, value, labelText, onChange) {
      const wrapper = document.createElement("div");
      wrapper.className = "gallery-filter__control";

      const label = document.createElement("label");
      label.className = "gallery-filter__label";
      label.textContent = labelText;

      const select = document.createElement("select");
      select.className = "gallery-filter__input";
      select.innerHTML = [
        `<option value="All">All</option>`,
        ...options.map(
          (option) => `<option value="${option.replace(/"/g, "&quot;")}">${option}</option>`
        )
      ].join("");

      select.value = value;
      select.addEventListener("change", onChange);

      wrapper.appendChild(label);
      wrapper.appendChild(select);
      return wrapper;
    }

    function renderKeywordInput(value, onInput) {
      const wrapper = document.createElement("div");
      wrapper.className = "gallery-filter__control";

      const label = document.createElement("label");
      label.className = "gallery-filter__label";
      label.textContent = "Search keywords";

      const input = document.createElement("input");
      input.className = "gallery-filter__input";
      input.type = "text";
      input.placeholder = "e.g., NeXus, perovskite, DFT...";
      input.value = value;
      input.setAttribute("list", "galleryKeywordSuggestions");
      input.addEventListener("input", onInput);

      wrapper.appendChild(label);
      wrapper.appendChild(input);
      return wrapper;
    }

    function renderControlRow() {
      if (!controlRow) return;

      const { methodologies, fields, countries } = getOptionsFromCards();
      controlRow.innerHTML = "";

      let control;

      if (activeFilter === "methodology") {
        control = renderSelect(
          methodologies,
          state.methodology,
          "Select methodology",
          (e) => {
            state.methodology = e.target.value;
            refresh();
          }
        );
      } else if (activeFilter === "field") {
        control = renderSelect(
          fields,
          state.field,
          "Select research field",
          (e) => {
            state.field = e.target.value;
            refresh();
          }
        );
      } else if (activeFilter === "country") {
        control = renderSelect(
          countries,
          state.country,
          "Select country",
          (e) => {
            state.country = e.target.value;
            refresh();
          }
        );
      } else {
        control = renderKeywordInput(state.keywords, (e) => {
          state.keywords = e.target.value;
          refresh();
        });
      }

      controlRow.appendChild(control);
    }

    function matches(card) {
      const methodology = norm(card.dataset.methodology);
      const field = norm(card.dataset.researchField);
      const country = norm(card.dataset.country);
      const keywords = norm(card.dataset.keywords);

      if (state.methodology !== "All" && methodology !== norm(state.methodology)) {
        return false;
      }

      if (state.field !== "All" && field !== norm(state.field)) {
        return false;
      }

      if (state.country !== "All" && country !== norm(state.country)) {
        return false;
      }

      if (state.keywords && !keywords.includes(norm(state.keywords))) {
        return false;
      }

      return true;
    }

    function applySort() {
      const cards = getCards();

      cards.sort((a, b) => {
        const da = parseDate(a);
        const db = parseDate(b);
        return sortOrder === "asc" ? da - db : db - da;
      });

      cards.forEach((card) => container.appendChild(card));
    }

    function applyFilters() {
      const cards = getCards();
      let visible = 0;

      cards.forEach((card) => {
        const show = matches(card);
        card.style.display = show ? "" : "none";
        if (show) visible += 1;
      });

      if (countEl) {
        countEl.textContent = `${visible} of ${cards.length}`;
      }
    }

    function refresh() {
      applySort();
      applyFilters();
    }

    function setActiveChip(filterName) {
      activeFilter = filterName;

      chips.forEach((chip) => {
        chip.classList.toggle("is-active", chip.dataset.filter === filterName);
      });

      renderControlRow();
    }

    function clearAll() {
      state.methodology = "All";
      state.field = "All";
      state.country = "All";
      state.keywords = "";
      sortOrder = "desc";

      if (sortBtn) sortBtn.textContent = "Sort: Newest";

      renderControlRow();
      refresh();
    }

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        setActiveChip(chip.dataset.filter || "methodology");
      });
    });

    sortBtn?.addEventListener("click", () => {
      sortOrder = sortOrder === "desc" ? "asc" : "desc";
      sortBtn.textContent = sortOrder === "desc" ? "Sort: Newest" : "Sort: Oldest";
      refresh();
    });

    clearBtn?.addEventListener("click", clearAll);

    buildKeywordSuggestions();
    setActiveChip("methodology");
    refresh();
  }

  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => {
      initZipStyleGalleryFilter();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initZipStyleGalleryFilter);
  } else {
    initZipStyleGalleryFilter();
  }
})();

/* =========================================================
   Featured rotator (track-based version)
   ========================================================= */
(function () {
  function initFeaturedRotators() {
    document.querySelectorAll(".featured-rotator").forEach((rotator) => {
      if (rotator.dataset.rotatorInit === "true") return;
      rotator.dataset.rotatorInit = "true";

      const template = rotator.querySelector(".featured-rotator__slides-template");
      const track = rotator.querySelector(".featured-rotator__track");
      const prevButton = rotator.querySelector(".featured-rotator__arrow--prev");
      const nextButton = rotator.querySelector(".featured-rotator__arrow--next");
      const dots = Array.from(rotator.querySelectorAll(".featured-rotator__dot"));

      if (!template || !track) return;

      const sourceSlides = Array.from(
        template.content.querySelectorAll(".featured-rotator__slide-source")
      );

      if (!sourceSlides.length) return;

      let activeIndex = 0;
      const total = sourceSlides.length;
      const rotateMs = parseInt(rotator.dataset.rotateMs || "5000", 10);
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      let intervalId = null;

      const normalizeIndex = (index) => ((index % total) + total) % total;

      const buildCard = (index, className) => {
        const item = document.createElement("div");
        item.className = `featured-rotator__item ${className}`;
        item.innerHTML = sourceSlides[normalizeIndex(index)].innerHTML;
        return item;
      };

      const render = () => {
        track.innerHTML = "";

        const prevIndex = normalizeIndex(activeIndex - 1);
        const nextIndex = normalizeIndex(activeIndex + 1);

        track.appendChild(buildCard(prevIndex, "is-prev"));
        track.appendChild(buildCard(activeIndex, "is-active"));
        track.appendChild(buildCard(nextIndex, "is-next"));

        dots.forEach((dot, index) => {
          const isActive = index === activeIndex;
          dot.classList.toggle("is-active", isActive);
          dot.setAttribute("aria-selected", isActive ? "true" : "false");
        });
      };

      const stop = () => {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
      };

      const start = () => {
        if (reduceMotion) return;
        stop();
        intervalId = setInterval(() => {
          activeIndex = normalizeIndex(activeIndex + 1);
          render();
        }, rotateMs);
      };

      const restart = () => {
        stop();
        start();
      };

      const goNext = () => {
        activeIndex = normalizeIndex(activeIndex + 1);
        render();
        restart();
      };

      const goPrev = () => {
        activeIndex = normalizeIndex(activeIndex - 1);
        render();
        restart();
      };

      prevButton?.addEventListener("click", goPrev);
      nextButton?.addEventListener("click", goNext);

      dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
          activeIndex = index;
          render();
          restart();
        });
      });

      rotator.addEventListener("mouseenter", stop);
      rotator.addEventListener("mouseleave", start);
      rotator.addEventListener("focusin", stop);
      rotator.addEventListener("focusout", start);

      // Delegated click for "View in Gallery" buttons inside the track
      track.addEventListener("click", (e) => {
        const btn = e.target.closest(".featured-rotator-card__explore-btn");
        if (!btn) return;

        const card = btn.closest("[data-explore-target]");
        if (!card) return;

        const targetCard = document.getElementById(card.dataset.exploreTarget);
        if (!targetCard) return;

        // Expand via the toggle button (reuses all existing expand logic)
        if (!targetCard.classList.contains("is-expanded")) {
          const toggleBtn = targetCard.querySelector(".grid-use-case-card__toggle");
          if (toggleBtn) toggleBtn.click();
        }

        // Scroll to card after layout settles
        requestAnimationFrame(() => {
          targetCard.scrollIntoView({ behavior: "smooth", block: "start" });
        });
      });

      render();
      start();
    });
  }

  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => {
      initFeaturedRotators();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFeaturedRotators);
  } else {
    initFeaturedRotators();
  }
})();


/* =========================================================
   Explore grid cards
   ========================================================= */
(function () {
  function initGridUseCaseCards() {
    document.querySelectorAll(".grid-use-case-card").forEach((card) => {
      if (card.dataset.gridCardInit === "true") return;
      card.dataset.gridCardInit = "true";

      const button = card.querySelector(".grid-use-case-card__toggle");
      if (!button) return;

      button.addEventListener("click", () => {
        const grid = card.parentElement;
        const expanded = card.classList.toggle("is-expanded");
        button.setAttribute("aria-expanded", expanded ? "true" : "false");

        // Collapse every other expanded card in the same grid
        if (expanded) {
          grid.querySelectorAll(".grid-use-case-card.is-expanded").forEach((other) => {
            if (other === card) return;
            other.classList.remove("is-expanded");
            const otherBtn = other.querySelector(".grid-use-case-card__toggle");
            if (otherBtn) {
              otherBtn.setAttribute("aria-expanded", "false");
              const otherLabel = otherBtn.querySelector(".grid-use-case-card__toggle-label");
              if (otherLabel) otherLabel.textContent = "View Details";
            }
            const otherDesc = other.querySelector(".grid-use-case-card__description");
            if (otherDesc) otherDesc.classList.add("is-collapsed");
            const otherKwRow = other.querySelector(".grid-use-case-card__body .grid-use-case-card__keywords");
            if (otherKwRow) {
              Array.from(otherKwRow.children).forEach((el, i) => {
                if (el.classList.contains("grid-use-case-card__keyword-more")) {
                  el.style.display = "";
                } else if (i >= 4) {
                  el.style.display = "none";
                }
              });
            }
            // Restore DOM position if it was swapped
            if (other._origNextSibling !== undefined && other._origNextSibling !== null) {
              grid.insertBefore(other, other._origNextSibling);
            } else if (other._origNextSibling === null) {
              grid.appendChild(other);
            }
            other._origNextSibling = undefined;
          });
        }

        if (expanded) {
          // Remember the node that comes after this card so we can restore later
          card._origNextSibling = card.nextElementSibling;
          // If this card is in the right column (odd DOM index), move it before
          // its left-column neighbor so grid-column: 1/-1 expands in-place
          const siblings = Array.from(grid.children);
          const idx = siblings.indexOf(card);
          if (idx % 2 === 1) {
            grid.insertBefore(card, siblings[idx - 1]);
          }
        } else {
          // Restore original DOM position
          if (card._origNextSibling) {
            grid.insertBefore(card, card._origNextSibling);
          } else {
            grid.appendChild(card);
          }
          card._origNextSibling = null;
        }

        // Scroll the top of the card to the top of the viewport
        if (expanded) {
          requestAnimationFrame(() => {
            card.scrollIntoView({ behavior: "smooth", block: "start" });
          });
        }

        const label = button.querySelector(".grid-use-case-card__toggle-label");
        if (label) {
          label.textContent = expanded ? "Show Less" : "View Details";
        }

        // Uncollapse / recollapse description
        const desc = card.querySelector(".grid-use-case-card__description");
        if (desc) desc.classList.toggle("is-collapsed", !expanded);

        // Show all keywords when expanded, hide extras when collapsed
        const kwRow = card.querySelector(".grid-use-case-card__body .grid-use-case-card__keywords");
        if (kwRow) {
          Array.from(kwRow.children).forEach((el, i) => {
            if (el.classList.contains("grid-use-case-card__keyword-more")) {
              el.style.display = expanded ? "none" : "";
            } else if (i >= 4) {
              el.style.display = expanded ? "" : "none";
            }
          });
        }
      });
    });
  }

  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => {
      initGridUseCaseCards();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGridUseCaseCards);
  } else {
    initGridUseCaseCards();
  }
})();