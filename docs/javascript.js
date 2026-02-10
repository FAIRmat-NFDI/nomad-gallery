(function () {
  function initGalleryUI() {
    const container = document.getElementById("galleryCards");
    if (!container) return;

    // Prevent double-binding when Material re-renders pages (navigation.instant)
    if (container.dataset.galleryInit === "true") return;
    container.dataset.galleryInit = "true";

    // --- Tabs / panels ---
    const tabs = Array.from(document.querySelectorAll(".filter-tab"));
    const panels = Array.from(document.querySelectorAll(".filter-panel"));

    function openPanel(panelId) {
      for (const tab of tabs) {
        const isTarget = tab.getAttribute("data-panel") === panelId;
        tab.classList.toggle("is-active", isTarget);
        tab.setAttribute("aria-expanded", isTarget ? "true" : "false");
      }
      for (const panel of panels) {
        const isOpen = panel.id === panelId;
        panel.classList.toggle("is-open", isOpen);
      }
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => openPanel(tab.getAttribute("data-panel")));
    });

    // --- Controls ---
    const els = {
      methodology: document.getElementById("filterMethodology"),
      country: document.getElementById("filterCountry"),
      field: document.getElementById("filterField"),
      keyword: document.getElementById("filterKeyword"),
      sort: document.getElementById("sortGallery"),
      clear: document.getElementById("clearGalleryFilters"),
      count: document.getElementById("galleryResultsCount"),
      keywordDatalist: document.getElementById("keywordSuggestions"),
      fieldDatalist: document.getElementById("fieldSuggestions"),
      countryDatalist: document.getElementById("countrySuggestions"),
    };

    function norm(v) {
      return (v || "").toString().trim().toLowerCase();
    }

    function getCards() {
      return Array.from(container.querySelectorAll(".gallery-card"));
    }

    function parseDate(card) {
      const s = card.getAttribute("data-submission-date") || "";
      const t = Date.parse(s);
      return Number.isFinite(t) ? t : 0;
    }

    function buildSuggestions() {
      const cards = getCards();

      // Build keyword suggestions
      if (els.keywordDatalist) {
        const keywordSet = new Set();
        for (const card of cards) {
          const raw = (card.dataset.keywords || "").split(",");
          for (const k of raw) {
            const cleaned = (k || "").trim();
            if (cleaned) keywordSet.add(cleaned);
          }
        }
        const sortedKeywords = Array.from(keywordSet).sort((a, b) => a.localeCompare(b));
        els.keywordDatalist.innerHTML = sortedKeywords
          .map((k) => `<option value="${k.replace(/"/g, "&quot;")}"></option>`)
          .join("");
      }

      // Build research field suggestions
      if (els.fieldDatalist) {
        const fieldSet = new Set();
        for (const card of cards) {
          const field = (card.dataset.researchField || "").trim();
          if (field) fieldSet.add(field);
        }
        const sortedFields = Array.from(fieldSet).sort((a, b) => a.localeCompare(b));
        els.fieldDatalist.innerHTML = sortedFields
          .map((f) => `<option value="${f.replace(/"/g, "&quot;")}"></option>`)
          .join("");
      }

      // Build country suggestions
      if (els.countryDatalist) {
        const countrySet = new Set();
        for (const card of cards) {
          const country = (card.dataset.country || "").trim();
          if (country) countrySet.add(country);
        }
        const sortedCountries = Array.from(countrySet).sort((a, b) => a.localeCompare(b));
        els.countryDatalist.innerHTML = sortedCountries
          .map((c) => `<option value="${c.replace(/"/g, "&quot;")}"></option>`)
          .join("");
      }
    }

    function matches(card) {
      const selectedMethod = norm(els.methodology?.value);
      const queryCountry = norm(els.country?.value);
      const queryField = norm(els.field?.value);
      const queryKeyword = norm(els.keyword?.value);

      const method = norm(card.dataset.methodology);
      const country = norm(card.dataset.country);
      const field = norm(card.dataset.researchField); // data-research-field -> researchField
      const keywords = norm(card.dataset.keywords); // "a,b,c"

      if (selectedMethod && method !== selectedMethod) return false;
      if (queryCountry && !country.includes(queryCountry)) return false;
      if (queryField && !field.includes(queryField)) return false;
      if (queryKeyword && !keywords.includes(queryKeyword)) return false;

      return true;
    }

    function applySort() {
      const order = els.sort?.value || "desc";
      const cards = getCards();

      cards.sort((a, b) => {
        const da = parseDate(a);
        const db = parseDate(b);
        return order === "asc" ? (da - db) : (db - da);
      });

      for (const card of cards) container.appendChild(card);
    }

    function applyFilters() {
      const cards = getCards();
      let shown = 0;

      for (const card of cards) {
        const ok = matches(card);
        card.style.display = ok ? "" : "none";
        if (ok) shown++;
      }

      if (els.count) els.count.textContent = `${shown} of ${cards.length} use cases shown`;
    }

    function refresh() {
      applySort();
      applyFilters();
    }

    function clearAll() {
      if (els.methodology) els.methodology.value = "";
      if (els.country) els.country.value = "";
      if (els.field) els.field.value = "";
      if (els.keyword) els.keyword.value = "";
      if (els.sort) els.sort.value = "desc";
      refresh();
    }

    // Bind events
    els.methodology?.addEventListener("change", refresh);
    els.country?.addEventListener("input", refresh);
    els.field?.addEventListener("input", refresh);
    els.keyword?.addEventListener("input", refresh);
    els.sort?.addEventListener("change", refresh);
    els.clear?.addEventListener("click", clearAll);

    // Default panel open + initial run
    openPanel("panel-methodology");
    buildSuggestions();
    refresh();
  }

  // MkDocs Material (navigation.instant) support
  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => initGalleryUI());
  } else {
    document.addEventListener("DOMContentLoaded", initGalleryUI);
  }
})();


/* =========================================================
   Featured highlights rotator (NOMAD Gallery)
   ========================================================= */
(function () {
  function initRotators() {
    document.querySelectorAll(".featured-rotator").forEach((rotator) => {
      // Prevent double-binding when Material re-renders pages (navigation.instant)
      if (rotator.dataset.rotatorInit === "true") return;
      rotator.dataset.rotatorInit = "true";

      const slides = Array.from(rotator.querySelectorAll(".featured-rotator__slide"));

      if (slides.length <= 1) {
        if (slides[0]) slides[0].classList.add("is-active");
        return;
      }

      const rotateMs = Number(rotator.dataset.rotateMs || 6000);
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      let index = 0;
      slides.forEach((s) => s.classList.remove("is-active"));
      slides[0].classList.add("is-active");

      let timer = null;

      // Create navigation controls
      const controlsDiv = document.createElement("div");
      controlsDiv.className = "rotator-controls";
      controlsDiv.setAttribute("role", "group");
      controlsDiv.setAttribute("aria-label", "Carousel controls");

      // Previous button
      const prevBtn = document.createElement("button");
      prevBtn.className = "rotator-btn";
      prevBtn.innerHTML = "‹";
      prevBtn.setAttribute("aria-label", "Previous slide");
      prevBtn.type = "button";

      // Dots container
      const dotsDiv = document.createElement("div");
      dotsDiv.className = "rotator-dots";
      dotsDiv.setAttribute("role", "tablist");
      dotsDiv.setAttribute("aria-label", "Slide indicators");

      const dots = [];
      for (let i = 0; i < slides.length; i++) {
        const dot = document.createElement("button");
        dot.className = "rotator-dot";
        dot.setAttribute("role", "tab");
        dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
        dot.setAttribute("aria-selected", i === 0 ? "true" : "false");
        dot.type = "button";
        if (i === 0) dot.classList.add("is-active");
        dots.push(dot);
        dotsDiv.appendChild(dot);
      }

      // Next button
      const nextBtn = document.createElement("button");
      nextBtn.className = "rotator-btn";
      nextBtn.innerHTML = "›";
      nextBtn.setAttribute("aria-label", "Next slide");
      nextBtn.type = "button";

      controlsDiv.appendChild(prevBtn);
      controlsDiv.appendChild(dotsDiv);
      controlsDiv.appendChild(nextBtn);
      rotator.appendChild(controlsDiv);

      function goToSlide(newIndex) {
        if (newIndex === index) return;
        
        slides[index].classList.remove("is-active");
        dots[index].classList.remove("is-active");
        dots[index].setAttribute("aria-selected", "false");
        
        index = newIndex;
        
        slides[index].classList.add("is-active");
        dots[index].classList.add("is-active");
        dots[index].setAttribute("aria-selected", "true");
        
        stop();
        start();
      }

      const start = () => {
        if (reduceMotion) return;
        timer = window.setInterval(() => {
          slides[index].classList.remove("is-active");
          dots[index].classList.remove("is-active");
          dots[index].setAttribute("aria-selected", "false");
          
          index = (index + 1) % slides.length;
          
          slides[index].classList.add("is-active");
          dots[index].classList.add("is-active");
          dots[index].setAttribute("aria-selected", "true");
        }, rotateMs);
      };

      const stop = () => {
        if (timer) window.clearInterval(timer);
        timer = null;
      };

      // Button event handlers
      prevBtn.addEventListener("click", () => {
        const newIndex = (index - 1 + slides.length) % slides.length;
        goToSlide(newIndex);
      });

      nextBtn.addEventListener("click", () => {
        const newIndex = (index + 1) % slides.length;
        goToSlide(newIndex);
      });

      // Dot event handlers
      dots.forEach((dot, i) => {
        dot.addEventListener("click", () => goToSlide(i));
      });

      rotator.addEventListener("mouseenter", stop);
      rotator.addEventListener("mouseleave", start);
      rotator.addEventListener("focusin", stop);
      rotator.addEventListener("focusout", start);

      start();
    });
  }

  // MkDocs Material (navigation.instant) support
  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => initRotators());
  } else {
    document.addEventListener("DOMContentLoaded", initRotators);
  }
})();
