---
title: NOMAD Gallery | Home
---

<div class="page-banner">
  <img src="assets/images/page/nomad-gallery-logo.png" alt="NOMAD Gallery" class="page-banner__logo">
  <p>Welcome to <strong>NOMAD Gallery</strong> &mdash; a space to showcase innovative features, uploads, and use cases created with the NOMAD platform. Whether you want to share your latest work or explore what&rsquo;s possible, this is the place to <strong>engage, discover, and inspire.</strong></p>
</div>

<p class="section-title">
  <span class="section-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
      <path d="M20 3v4"/>
      <path d="M22 5h-4"/>
      <path d="M4 17v2"/>
      <path d="M5 18H3"/>
    </svg>
  </span>
  Featured highlights
</p>

<p class="section-subtitle">
  Hand-picked examples that demonstrate what's possible with NOMAD — from large-scale databases to innovative workflows.
</p>

<div class="featured-rotator" data-rotate-ms="5000">
  <div class="featured-rotator__viewport">

    <div class="featured-rotator__track"></div>

    <button class="featured-rotator__arrow featured-rotator__arrow--prev" type="button" aria-label="Previous highlight">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>

    <button class="featured-rotator__arrow featured-rotator__arrow--next" type="button" aria-label="Next highlight">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>

  <div class="featured-rotator__dots">
    <button class="featured-rotator__dot is-active" type="button" aria-label="Go to slide 1"></button>
    <button class="featured-rotator__dot" type="button" aria-label="Go to slide 2"></button>
    <button class="featured-rotator__dot" type="button" aria-label="Go to slide 3"></button>
  </div>

  <template class="featured-rotator__slides-template">
    <div class="featured-rotator__slide-source">
      {{ render_featured_rotator_card("special_cards/Alexandria.md", index=0) }}
    </div>
    <div class="featured-rotator__slide-source">
      {{ render_featured_rotator_card("special_cards/perovskite_database.md", index=1) }}
    </div>
    <div class="featured-rotator__slide-source">
      {{ render_featured_rotator_card("cards/CG_bilayer.md", index=2) }}
    </div>
  </template>
</div>

<p class="section-title">
  <span class="section-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"/>
      <line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  </span>
  Explore the NOMAD Gallery
</p>

<p class="section-subtitle">
  Browse community-submitted use cases showing how NOMAD is used in real research workflows. Use the filters below to explore by methodology, research field, or keywords.
</p>

<div class="gallery-filter" id="galleryFilter">
  <div class="gallery-filter__bar">
    <div class="gallery-filter__chips" role="tablist" aria-label="Gallery filters">
      <button class="gallery-filter__chip is-active" type="button" data-filter="methodology">Methodology</button>
      <button class="gallery-filter__chip" type="button" data-filter="field">Research field</button>
      <button class="gallery-filter__chip" type="button" data-filter="country">Country</button>
      <button class="gallery-filter__chip" type="button" data-filter="keywords">Keywords</button>
    </div>

    <div class="gallery-filter__spacer"></div>

    <p class="gallery-filter__count" id="galleryResultsCount">0 of 0</p>

    <button class="gallery-filter__action" type="button" id="sortGallery">Sort: Newest</button>
    <button class="gallery-filter__action" type="button" id="clearGalleryFilters">Clear</button>
  </div>

  <div class="gallery-filter__control-row" id="galleryFilterControlRow"></div>

  <datalist id="galleryKeywordSuggestions"></datalist>
</div>

<div id="galleryCards" class="gallery-cards">

{{ render_sorted_cards_macro("docs/cards") }}

</div>