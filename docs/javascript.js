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

    function buildKeywordSuggestions() {
      if (!els.keywordDatalist) return;

      const set = new Set();
      for (const card of getCards()) {
        const raw = (card.dataset.keywords || "").split(",");
        for (const k of raw) {
          const cleaned = (k || "").trim();
          if (cleaned) set.add(cleaned);
        }
      }

      const sorted = Array.from(set).sort((a, b) => a.localeCompare(b));
      els.keywordDatalist.innerHTML = sorted
        .map((k) => `<option value="${k.replace(/"/g, "&quot;")}"></option>`)
        .join("");
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
    buildKeywordSuggestions();
    refresh();
  }

  // MkDocs Material (navigation.instant) support
  if (typeof window.document$ !== "undefined" && window.document$?.subscribe) {
    window.document$.subscribe(() => initGalleryUI());
  } else {
    document.addEventListener("DOMContentLoaded", initGalleryUI);
  }
})();
