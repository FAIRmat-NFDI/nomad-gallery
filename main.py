import html
import os
from datetime import datetime
from pathlib import Path

import yaml

MIN_FRONT_MATTER_PARTS = 3


def esc(x):
    """HTML-escape any value safely."""
    return html.escape("" if x is None else str(x), quote=True)

CARD_GRADIENTS = [
    "linear-gradient(135deg, #a8c8f0 0%, #7baad8 50%, #5a92c6 100%)",
    "linear-gradient(135deg, #b0d0f4 0%, #85b5e0 50%, #6a9ed0 100%)",
    "linear-gradient(135deg, #9ec4ee 0%, #72a4d4 50%, #5890c2 100%)",
    "linear-gradient(135deg, #b8d6f6 0%, #90bee4 50%, #74a8d4 100%)",
    "linear-gradient(135deg, #a4caf2 0%, #7eb0dc 50%, #6298c8 100%)",
]


def _read_front_matter_from_docs(file_path):
    """Read YAML front matter from docs/<file_path> safely."""
    with open(f"docs/{file_path}", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError(f"{file_path} does not start with YAML front matter.")

    parts = content.split("---", MIN_FRONT_MATTER_PARTS)
    if len(parts) < MIN_FRONT_MATTER_PARTS:
        raise ValueError(f"{file_path} has invalid YAML front matter.")

    metadata = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return metadata, body


def _normalize_use_case_info(data, body=""):
    """Normalize richer use-case metadata without affecting old card logic."""
    def _to_line_list(value):
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            return [line.strip() for line in value.splitlines() if line.strip()]
        return []

    coauthors = data.get("coauthors", [])
    if isinstance(coauthors, str):
        coauthors = [c.strip() for c in coauthors.split(",") if c.strip()]

    keywords = data.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    image_path = (data.get("image_path") or data.get("image") or "").strip()
    if "github.com" in image_path:
        image_path = (
            image_path.replace("github.com", "raw.githubusercontent.com")
            .replace("/blob/", "/")
        )

    entry_link = (
        data.get("entry_link") or data.get("external_url") or ""
    ).strip()

    publication_references = (
        _to_line_list(data.get("publication_references"))
    )
    repository_references = (
        _to_line_list(data.get("repository_references"))
    )
    nomad_resource_links = _to_line_list(data.get("nomad_resource_links"))
    funding_references = (
        _to_line_list(data.get("funding_references"))
    )
    media_urls = (
        _to_line_list(data.get("media_urls"))
    )

    return {
        "title": data.get("title", "Untitled Submission"),
        "submitter": (
            data.get("submitter") or data.get("submitted_by") or "Unknown Submitter"
        ),
        "description": data.get("description")
        or data.get("summary")
        or body
        or "No description available.",
        "submission_date": data.get("submission_date")
        or data.get("submitted_date")
        or "",
        "institution": (data.get("institution", "") or "").strip(),
        "country": (data.get("country", "") or "").strip(),
        "research_field": (data.get("research_field", "") or "").strip(),
        "methodology": (data.get("methodology_type", "") or "").strip(),
        "technique": (
            data.get("technique") or data.get("specific_technique") or ""
        ).strip(),
        "data_size": (data.get("data_size", "") or "").strip(),
        "active_users": data.get("estimated_active_users", None),
        "downloads": data.get("downloads", None),
        "primary_media": media_urls[0] if media_urls else "",
        "media_urls": media_urls,
        "coauthors": coauthors,
        "keywords": keywords,
        "primary_publication": (
            publication_references[0] if publication_references else ""
        ),
        "publication_references": publication_references,
        "primary_funding": funding_references[0] if funding_references else "",
        "funding_references": funding_references,
        "nomad_resource_links": nomad_resource_links,
        "image_name": data.get("image_name", data.get("title", "Image")),
        "image_path": image_path,
        "primary_repository": (
            repository_references[0] if repository_references else ""
        ),
        "repository_references": repository_references,
        "repo_name": (data.get("repo_name", "") or "").strip(),
        "entry_link": (
            entry_link
            or (nomad_resource_links[0] if nomad_resource_links else "")
        ),
        "entry_name": (data.get("entry_name", "") or "").strip() or entry_link,
    }

def _icon_calendar():
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" aria-hidden="true">\n'
        '      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>\n'
        '      <line x1="16" y1="2" x2="16" y2="6"></line>\n'
        '      <line x1="8" y1="2" x2="8" y2="6"></line>\n'
        '      <line x1="3" y1="10" x2="21" y2="10"></line>\n'
        '    </svg>'
    )


def _icon_chevron_down():
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" aria-hidden="true">\n'
        '      <polyline points="6 9 12 15 18 9"></polyline>\n'
        '    </svg>'
    )


def _icon_nomad():
    return (
        '<img src="assets/images/page/nomad-logo.png" alt="NOMAD" aria-hidden="true">'
    )


def _icon_document():
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" aria-hidden="true">\n'
        '      <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12'
        'a2 2 0 0 0 2-2V9z"></path>\n'
        '      <polyline points="13 2 13 9 20 9"></polyline>\n'
        '      <line x1="8" y1="13" x2="16" y2="13"></line>\n'
        '      <line x1="8" y1="17" x2="16" y2="17"></line>\n'
        '    </svg>'
    )


def _icon_github():
    _gh_path = (
        "M12 0C5.373 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387"
        ".599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416"
        "-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745"
        ".083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07"
        " 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604"
        "-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381"
        " 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322"
        " 3.301 1.23A11.48 11.48 0 0 1 12 6.844c1.02.005 2.047.138"
        " 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242"
        " 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609"
        "-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293"
        "c0 .319.192.694.801.576C20.566 21.799 24 17.302 24 12"
        " 24 5.373 18.627 0 12 0z"
    )
    return (
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">\n'
        f'      <path d="{_gh_path}"></path>\n'
        '    </svg>'
    )


def _icon_play():
    return """
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <polygon points="5 3 19 12 5 21 5 3"></polygon>
    </svg>
    """


def _icon_share():
    return """
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         aria-hidden="true">
      <circle cx="18" cy="5" r="3"></circle>
      <circle cx="6" cy="12" r="3"></circle>
      <circle cx="18" cy="19" r="3"></circle>
      <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
      <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
    </svg>
    """


def _icon_users():
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" aria-hidden="true">\n'
        '      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>\n'
        '      <circle cx="9" cy="7" r="4"></circle>\n'
        '      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>\n'
        '      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>\n'
        '    </svg>'
    )


def _icon_download():
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" aria-hidden="true">\n'
        '      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>\n'
        '      <polyline points="7 10 12 15 17 10"></polyline>\n'
        '      <line x1="12" y1="15" x2="12" y2="3"></line>\n'
        '    </svg>'
    )
def render_sorted_cards(cards_dir="docs/cards"):
    """Render all cards from the specified directory, sorted by submission date."""
    card_files = []

    if os.path.exists(cards_dir):
        for filename in os.listdir(cards_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(cards_dir, filename)

                with open(file_path, encoding="utf-8") as f:
                    try:
                        front_matter = yaml.safe_load(f.read().split("---")[1])
                        submission_date = front_matter.get("submission_date", "")

                        if isinstance(submission_date, str):
                            try:
                                date_obj = datetime.strptime(
                                    submission_date, "%Y-%m-%d"
                                )
                            except ValueError:
                                date_obj = datetime.min
                        else:
                            date_obj = (
                                submission_date
                                if isinstance(submission_date, datetime)
                                else datetime.min
                            )

                        card_files.append((file_path, date_obj))
                    except Exception as e:
                        print(f"Error parsing {filename}: {e}")

    card_files.sort(key=lambda x: x[1] if x[1] else datetime.min, reverse=True)

    rendered_cards = ""
    docs_dir = Path("docs").resolve()

    for i, (file_path, _) in enumerate(card_files):
        clean_path = str(Path(file_path).resolve().relative_to(docs_dir))
        rendered_cards += _render_grid_use_case_card(clean_path, index=i) + "\n"

    return rendered_cards


def _build_action_buttons(
    info,
    primary_nomad_resource_link,
    primary_publication,
    primary_repository,
    primary_media,
):
    """Build icon-button anchor tags for a grid use-case card."""
    cls = "grid-use-case-card__icon-button"
    buttons = []
    if info["nomad_resource_links"]:
        buttons.append(
            f'<a class="{cls}" href="{primary_nomad_resource_link}"'
            f' target="_blank" rel="noopener"'
            f' title="Open in NOMAD">{_icon_nomad()}</a>'
        )
    if info["primary_publication"]:
        buttons.append(
            f'<a class="{cls}" href="{primary_publication}"'
            f' target="_blank" rel="noopener"'
            f' title="View Publication">{_icon_document()}</a>'
        )
    if info["primary_repository"]:
        buttons.append(
            f'<a class="{cls}" href="{primary_repository}"'
            f' target="_blank" rel="noopener"'
            f' title="View Repository">{_icon_github()}</a>'
        )
    if info["primary_media"]:
        buttons.append(
            f'<a class="{cls}" href="{primary_media}"'
            f' target="_blank" rel="noopener"'
            f' title="Watch Media">{_icon_play()}</a>'
        )
    return buttons


def _build_stats_html(info):
    """Build usage-statistics HTML block for a grid use-case card."""
    stat_parts = []
    if info["active_users"]:
        stat_parts.append(
            '<div class="grid-use-case-card__stat">'
            f'{_icon_users()}'
            f'<span>{esc(info["active_users"])} active users</span>'
            '</div>'
        )
    if info["downloads"]:
        stat_parts.append(
            '<div class="grid-use-case-card__stat">'
            f'{_icon_download()}'
            f'<span>{esc(info["downloads"])} downloads</span>'
            '</div>'
        )
    if not stat_parts:
        return ""
    return f'''
            <div class="grid-use-case-card__detail">
              <h4>Usage Statistics</h4>
              <div class="grid-use-case-card__stats">
                {"".join(stat_parts)}
              </div>
            </div>
            '''


def _build_left_column(info, data_size, technique, stats_html, coauthors_html):
    """Build the left column detail blocks for a grid use-case card."""
    col = []
    if info["data_size"]:
        col.append(f'''
            <div class="grid-use-case-card__detail">
              <h4>Data Size</h4>
              <p>{data_size}</p>
            </div>
            ''')
    if info["technique"]:
        col.append(f'''
            <div class="grid-use-case-card__detail">
              <h4>Technique</h4>
              <p>{technique}</p>
            </div>
            ''')
    if stats_html:
        col.append(stats_html)
    if coauthors_html:
        col.append(coauthors_html)
    return col


def _build_right_column(info, escaped):
    """Build the right column detail blocks for a grid use-case card."""
    publication_references = escaped["publication_references"]
    repository_references = escaped["repository_references"]
    nomad_resource_links = escaped["nomad_resource_links"]
    funding_references = escaped["funding_references"]
    media_urls = escaped["media_urls"]
    col = []

    def _link_reference_block(title, references):
        items = "".join(
            f'<li><a href="{ref}" target="_blank" rel="noopener">{ref}</a></li>'
            for ref in references
        )
        body = f"<ul>{items}</ul>"
        return f'''
            <div class="grid-use-case-card__detail">
              <h4>{title}</h4>
              {body}
            </div>
            '''

    def _text_reference_block(title, references):
        items = "".join(f"<li>{ref}</li>" for ref in references)
        body = f"<ul>{items}</ul>"
        return f'''
            <div class="grid-use-case-card__detail">
              <h4>{title}</h4>
              {body}
            </div>
            '''

    if info["primary_publication"]:
        col.append(
            _link_reference_block(
                "Publication References",
                publication_references,
            )
        )
    if info["primary_repository"]:
        col.append(
            _link_reference_block(
                "Repository References",
                repository_references,
            )
        )
    if info["nomad_resource_links"]:
        col.append(
            _link_reference_block(
                "NOMAD Resource Links",
                nomad_resource_links,
            )
        )
    if info["primary_funding"]:
        col.append(
            _text_reference_block(
                "Funding References",
                funding_references,
            )
        )
    if info["primary_media"]:
        col.append(_link_reference_block("Media URLs", media_urls))
    return col


def _render_grid_use_case_card(file_path, index=0):
    """Grid card renderer for the Explore section."""
    try:
        data, body = _read_front_matter_from_docs(file_path)
        info = _normalize_use_case_info(data, body)

        title = esc(info["title"])
        description = esc(info["description"])
        institution = esc(info["institution"])
        country = esc(info["country"])
        research_field = esc(info["research_field"])
        methodology = esc(info["methodology"])
        submitter = esc(info["submitter"])
        submission_date = esc(info["submission_date"])
        technique = esc(info["technique"])
        data_size = esc(info["data_size"])
        primary_publication = esc(info["primary_publication"])
        primary_repository = esc(info["primary_repository"])
        primary_nomad_resource_link = (
            esc(info["nomad_resource_links"][0])
            if info["nomad_resource_links"]
            else ""
        )
        primary_media = esc(info["primary_media"])
        image_path = esc(info["image_path"])
        image_name = esc(info["image_name"])

        gradient = CARD_GRADIENTS[index % len(CARD_GRADIENTS)]
        keywords_csv = ",".join(info["keywords"]) if info["keywords"] else ""
        slug = Path(file_path).stem.lower().replace("_", "-").replace(" ", "-")

        image_html = ""
        if info["image_path"]:
            image_html = f'''
            <div class="grid-use-case-card__hero-image">
              <img src="{image_path}" alt="{image_name}">
            </div>
            '''

        action_buttons = _build_action_buttons(
            info,
            primary_nomad_resource_link,
            primary_publication,
            primary_repository,
            primary_media,
        )

        keyword_items = []
        for kw in info["keywords"]:
            keyword_items.append(
                f'<span class="grid-use-case-card__keyword">#{esc(kw)}</span>'
            )

        stats_html = _build_stats_html(info)

        coauthors_html = ""
        coauthors = info.get("coauthors", [])
        if coauthors:
            coauthors_html = f'''
            <div class="grid-use-case-card__detail">
              <h4>Contributors</h4>
              <p>{esc(", ".join(coauthors))}</p>
            </div>
            '''

        left_column = _build_left_column(
            info, data_size, technique, stats_html, coauthors_html
        )
        escaped_vals = {
            "publication_references": [
                esc(v) for v in info.get("publication_references", [])
            ],
            "repository_references": [
                esc(v) for v in info.get("repository_references", [])
            ],
            "nomad_resource_links": [
                esc(v) for v in info.get("nomad_resource_links", [])
            ],
            "funding_references": [
                esc(v) for v in info.get("funding_references", [])
            ],
            "media_urls": [esc(v) for v in info.get("media_urls", [])],
        }
        right_column = _build_right_column(info, escaped_vals)

        return f'''
<article class="grid-use-case-card gallery-card"
  id="grid-card-{slug}"
  data-submission-date="{submission_date}"
  data-methodology="{methodology}"
  data-country="{country}"
  data-research-field="{research_field}"
  data-keywords="{esc(keywords_csv)}"
  style="--grid-card-gradient: {gradient};">

  <div class="grid-use-case-card__hero" style="background: {gradient};">
    {image_html}
    <div class="grid-use-case-card__pattern"></div>
    <div class="grid-use-case-card__shade"></div>

    <div class="grid-use-case-card__hero-actions">
      {"".join(action_buttons)}
    </div>
  </div>

  <div class="grid-use-case-card__hero-content">
    <p class="grid-use-case-card__title">{title}</p>
    <div class="grid-use-case-card__institution-line">
      <span>{institution}</span>
      <span>•</span>
      <span>{country}</span>
    </div>
  </div>

  <div class="grid-use-case-card__body">
    <div class="grid-use-case-card__pills">
      <span class="grid-use-case-card__pill
            grid-use-case-card__pill--field">{research_field}</span>
      <span class="grid-use-case-card__pill
            grid-use-case-card__pill--method">{methodology}</span>
    </div>

    <p class="grid-use-case-card__description is-collapsed">{description}</p>

    <div class="grid-use-case-card__keywords">
      {"".join(keyword_items)}
    </div>

    <div class="grid-use-case-card__meta">
      <span>By {submitter}</span>
      <div class="grid-use-case-card__meta-right">
        {_icon_calendar()}
        <span>{submission_date}</span>
      </div>
    </div>

    <div class="grid-use-case-card__controls">
      <button class="grid-use-case-card__toggle" type="button"
              aria-expanded="false">
        <span class="grid-use-case-card__toggle-label">View Details</span>
        {_icon_chevron_down()}
      </button>
      <button class="grid-use-case-card__share" type="button"
              aria-label="Copy link to {title}" title="Copy link">
        {_icon_share()}
      </button>
    </div>
  </div>

  <div class="grid-use-case-card__expanded">
    <div class="grid-use-case-card__expanded-grid">
      <div class="grid-use-case-card__section">
        {"".join(left_column)}
      </div>
      <div class="grid-use-case-card__section">
        {"".join(right_column)}
      </div>
    </div>
  </div>
</article>
'''
    except Exception as e:
        return f"**Error loading grid use case card from {file_path}: {str(e)}**"

def _render_featured_rotator_card(file_path, index=0):
    """Compact Figma-style thumbnail card for the featured-highlights carousel."""
    try:
        data, body = _read_front_matter_from_docs(file_path)
    except Exception as exc:
        return f'<div class="featured-rotator-card">Error: {esc(str(exc))}</div>'

    info = _normalize_use_case_info(data, body)
    gradient = CARD_GRADIENTS[index % len(CARD_GRADIENTS)]
    title = esc(info["title"])
    research_field = esc(info["research_field"])
    image_path = esc(info["image_path"])
    image_name = esc(info.get("image_name", title))

    image_html = ""
    if info["image_path"]:
        image_html = (
            f'<img class="featured-rotator-card__img"'
            f' src="{image_path}" alt="{image_name}">'
        )

    slug = Path(file_path).stem.lower().replace("_", "-").replace(" ", "-")

    return (
        f'<div class="featured-rotator-card"'
        f' data-explore-target="grid-card-{slug}">\n'
        f'  <div class="featured-rotator-card__hero"'
        f' style="background: {gradient};">\n'
        f'    {image_html}\n'
        f'    <div class="featured-rotator-card__pattern"></div>\n'
        f'  </div>\n'
        f'  <div class="featured-rotator-card__body">\n'
        f'    <p class="featured-rotator-card__title">{title}</p>\n'
        f'    <span class="featured-rotator-card__field">{research_field}</span>\n'
        '    <button class="featured-rotator-card__explore-btn"'
        ' type="button">View in Gallery</button>\n'
        f'  </div>\n'
        f'</div>'
    )


def define_env(env):
    """Define macros for MkDocs."""

    @env.macro
    def include_raw_markdown(file_path):
        """Reads and returns raw markdown content from a file without rendering."""
        try:
            with open(f"docs/{file_path}", encoding="utf-8") as f:
                content = f.read()
                return f"```markdown\n{content}\n```"
        except Exception as e:
            return f"**Error loading file {file_path}: {str(e)}**"

    @env.macro
    def render_sorted_cards_macro(cards_dir="docs/cards"):
        return render_sorted_cards(cards_dir)

    @env.macro
    def render_featured_rotator_card(file_path, index=0):
        return _render_featured_rotator_card(file_path, index)

    @env.macro
    def render_grid_use_case_card(file_path, index=0):
        return _render_grid_use_case_card(file_path, index)
