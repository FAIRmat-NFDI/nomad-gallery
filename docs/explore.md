---
title: NOMAD Gallery | Explore
---

![NOMAD Gallery logo](assets/logo.png){ width=520 }

<h2> Explore the NOMAD Gallery </h2>

Browse community-submitted use cases showing how NOMAD is used in real research workflows.
Use the filters below to explore by methodology, research field, or keywords.

<nav class="filter-nav" aria-label="Gallery filters">
  <button class="filter-tab is-active" type="button"
          data-panel="panel-methodology" aria-controls="panel-methodology" aria-expanded="true">
    Methodology
  </button>
  <button class="filter-tab" type="button"
          data-panel="panel-field" aria-controls="panel-field" aria-expanded="false">
    Research field
  </button>
  <button class="filter-tab" type="button"
          data-panel="panel-country" aria-controls="panel-country" aria-expanded="false">
    Country
  </button>
  <button class="filter-tab" type="button"
          data-panel="panel-keywords" aria-controls="panel-keywords" aria-expanded="false">
    Keywords
  </button>

  <div class="filter-nav-spacer"></div>

  <button class="filter-tab" type="button"
          data-panel="panel-sort" aria-controls="panel-sort" aria-expanded="false">
    Sort
  </button>

  <button id="clearGalleryFilters" class="filter-tab" type="button">
    Clear
  </button>
</nav>

<section class="filter-panels" aria-label="Filter options">
  <div id="panel-methodology" class="filter-panel is-open" role="region" aria-label="Methodology filter">
    <label for="filterMethodology">Select methodology</label>
    <select id="filterMethodology">
      <option value="">All</option>
      <option value="Computational">Computational</option>
      <option value="Experimental">Experimental</option>
      <option value="Mixed/Hybrid">Mixed/Hybrid</option>
    </select>
  </div>

  <div id="panel-field" class="filter-panel" role="region" aria-label="Research field filter">
    <label for="filterField">Search research field</label>
    <input id="filterField" type="search" placeholder="e.g., Catalysis" autocomplete="off" list="fieldSuggestions" />
    <datalist id="fieldSuggestions"></datalist>
  </div>

  <div id="panel-country" class="filter-panel" role="region" aria-label="Country filter">
    <label for="filterCountry">Search country</label>
    <input id="filterCountry" type="search" placeholder="e.g., Germany" autocomplete="off" list="countrySuggestions" />
    <datalist id="countrySuggestions"></datalist>
  </div>

  <div id="panel-keywords" class="filter-panel" role="region" aria-label="Keyword filter">
    <label for="filterKeyword">Search keyword</label>
    <input id="filterKeyword" type="search" placeholder="e.g., NeXus" autocomplete="off" list="keywordSuggestions" />
    <datalist id="keywordSuggestions"></datalist>
  </div>

  <div id="panel-sort" class="filter-panel" role="region" aria-label="Sort options">
    <label for="sortGallery">Sort by submission date</label>
    <select id="sortGallery">
      <option value="desc" selected>Newest first</option>
      <option value="asc">Oldest first</option>
    </select>
  </div>

  <p id="galleryResultsCount" class="gallery-results" aria-live="polite"></p>
</section>

<div id="galleryCards" class="gallery-cards">
  {{ render_sorted_cards_macro() }}
</div>

<!-- <div class="grid cards" markdown>

- :file: **NOMAD DOCS** if you have problem with something
- :fontawesome-brands-js: **DISCORD** to collaborate with an awesome community of researchers

</div>

FUNCTIONALITY ADDED IN MKDOCS VERSION 9.5.0-->

