import os
from datetime import datetime
from pathlib import Path
import html
import yaml


def esc(x):
    """HTML-escape any value safely."""
    return html.escape("" if x is None else str(x), quote=True)


def extract_metadata(data):
    """Extracts and cleans all fields from the YAML data."""
    # Handle lists (Coauthors, Keywords)
    coauthors = data.get("coauthors", [])
    if isinstance(coauthors, str):
        coauthors = [c.strip() for c in coauthors.split(",") if c.strip()]

    keywords = data.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    # Handle Images
    image_path = (data.get("image_path", "") or "").strip()
    if "github.com" in image_path:
        image_path = image_path.replace("github.com", "raw.githubusercontent.com").replace(
            "/blob/", "/"
        )

    # Handle Links with Fallbacks
    repo_link = (data.get("repo_link", "") or "").strip()
    repo_name = (data.get("repo_name", "") or "").strip() or repo_link
    entry_link = (data.get("entry_link", "") or "").strip()
    entry_name = (data.get("entry_name", "") or "").strip() or entry_link

    return {
        "title": data.get("title", "Untitled Submission"),
        "submitter": data.get("submitter", "Unknown Submitter"),
        "description": data.get("description", "No description available."),
        "submission_date": data.get("submission_date", "Unknown date"),
        "institution": (data.get("institution", "") or "").strip(),
        "country": (data.get("country", "") or "").strip(),
        "research_field": (data.get("research_field", "") or "").strip(),
        "methodology": (data.get("methodology_type", "") or "").strip(),
        "technique": (data.get("technique", "") or "").strip(),
        "data_size": (data.get("data_size", "") or "").strip(),
        "active_users": data.get("estimated_active_users", None),
        "downloads": data.get("downloads", None),
        "media_url": (data.get("media_url", "") or "").strip(),
        "coauthors": coauthors,
        "keywords": keywords,
        "publication": (data.get("publication_reference", "") or "").strip(),
        "funding": (data.get("funding_reference", "") or "").strip(),
        "image_name": data.get("image_name", "Image"),
        "image_path": image_path,
        "repo_link": repo_link,
        "repo_name": repo_name,
        "entry_link": entry_link,
        "entry_name": entry_name,
    }


def _build_header(info):
    title = esc(info.get("title", "Untitled Submission"))
    description = esc(info.get("description", "No description available."))

    meta_parts = []
    if info.get("research_field"):
        meta_parts.append(f"<strong>Field</strong>: {esc(info['research_field'])}")
    if info.get("institution"):
        meta_parts.append(f"<strong>Inst</strong>: {esc(info['institution'])}")
    if info.get("country"):
        meta_parts.append(f"({esc(info['country'])})")

    meta_line = f'<div class="card-meta">{" , ".join(meta_parts)}</div>' if meta_parts else ""

    return (
        f'<h3 class="card-title">{title}</h3>'
        f"{meta_line}"
        f'<p class="card-description">{description}</p>'
    )


def _build_details(info):
    rows = []
    rows.append(f"<div><strong>Submitter</strong>: {esc(info.get('submitter', 'Unknown Submitter'))}</div>")

    if info.get("coauthors"):
        rows.append(f"<div><strong>Coauthors</strong>: {esc(', '.join(info['coauthors']))}</div>")
    if info.get("methodology"):
        rows.append(f"<div><strong>Methodology</strong>: {esc(info['methodology'])}</div>")
    if info.get("technique"):
        rows.append(f"<div><strong>Technique</strong>: {esc(info['technique'])}</div>")
    if info.get("data_size"):
        rows.append(f"<div><strong>Data Size</strong>: {esc(info['data_size'])}</div>")

    return f'<div class="card-details">{"".join(rows)}</div>'


def _build_metrics_and_refs(info):
    blocks = []

    impact = []
    if info.get("active_users"):
        impact.append(f"{esc(info['active_users'])} Users")
    if info.get("downloads"):
        impact.append(f"{esc(info['downloads'])} Downloads")
    if impact:
        blocks.append(f'<div><strong>Impact</strong>: {", ".join(impact)}</div>')

    if info.get("funding"):
        blocks.append(f"<div><strong>Funding</strong>: {esc(info['funding'])}</div>")

    if info.get("publication"):
        pub = (info.get("publication") or "").strip()
        if pub:
            blocks.append(
                f'<div><strong>Publication</strong>: <a href="{esc(pub)}">{esc(pub)}</a></div>'
            )

    if info.get("keywords"):
        badges = " ".join([f'<span class="kw-badge">{esc(k)}</span>' for k in info["keywords"]])
        blocks.append(f'<div class="card-keywords"><strong>Keywords</strong>: {badges}</div>')

    return f'<div class="card-metrics">{"".join(blocks)}</div>'


def _build_media_and_links(info):
    parts = []

    # Image
    if info.get("image_path"):
        parts.append(
            f'<div class="click-zoom" style="margin-top: 10px;">'
            f'  <label>'
            f'    <input type="checkbox">'
            f'    <img src="{esc(info["image_path"])}" alt="{esc(info.get("image_name","Image"))}" '
            f'         width="100%" title="Click to zoom in">'
            f'  </label>'
            f"</div>"
        )

    # Icon-based Links
    link_items = []
    if info.get("repo_link"):
        link_items.append(
            f'<a href="{esc(info["repo_link"])}" class="icon-link" '
            f'aria-label="View Repository" target="_blank" rel="noopener">'
            f'<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
            f'</a>'
        )
    if info.get("entry_link"):
        link_items.append(
            f'<a href="{esc(info["entry_link"])}" class="icon-link" '
            f'aria-label="Open in NOMAD" target="_blank" rel="noopener">'
            f'<img src="assets/nomad-icon.png" alt="NOMAD" onerror="this.parentElement.innerHTML=\'<span class=&quot;emoji-icon&quot;>🚀</span>\'" />'
            f'</a>'
        )
    if info.get("media_url"):
        link_items.append(
            f'<a href="{esc(info["media_url"])}" class="icon-link" '
            f'aria-label="Watch Media" target="_blank" rel="noopener">'
            f'<span class="emoji-icon">🎥</span>'
            f'</a>'
        )
    if info.get("publication"):
        link_items.append(
            f'<a href="{esc(info["publication"])}" class="icon-link" '
            f'aria-label="View Publication" target="_blank" rel="noopener">'
            f'<span class="emoji-icon">📄</span>'
            f'</a>'
        )

    # Create footer with icons and date
    if link_items or info.get("submission_date"):
        footer_html = '<div class="card-icon-links">'
        if link_items:
            footer_html += '<div class="card-icons-group">' + "".join(link_items) + '</div>'
        if info.get("submission_date"):
            submitted = esc(info.get("submission_date", "") or "")
            footer_html += f'<div class="card-submitted-inline">Submitted: {submitted}</div>'
        footer_html += '</div>'
        parts.append(footer_html)

    return parts


def build_card_html(info):
    """Constructs a single card as HTML with data-* attributes for filtering."""
    keywords_csv = ",".join(info.get("keywords", [])) if info.get("keywords") else ""

    parts = [
        f'<article class="gallery-card" '
        f'data-submission-date="{esc(info.get("submission_date",""))}" '
        f'data-methodology="{esc(info.get("methodology",""))}" '
        f'data-country="{esc(info.get("country",""))}" '
        f'data-research-field="{esc(info.get("research_field",""))}" '
        f'data-keywords="{esc(keywords_csv)}">'
    ]

    parts.append(_build_header(info))
    parts.append(_build_details(info))
    parts.append(_build_metrics_and_refs(info))
    parts.extend(_build_media_and_links(info))

    parts.append("</article>")
    return "\n".join(parts)


def render_card_from_file(file_path):
    """Reads front matter from a file and renders a formatted card."""
    try:
        with open(f"docs/{file_path}", encoding="utf-8") as f:
            content = f.read()
            metadata, _ = content.split("---", 2)[1:]  # Extract front matter
            data = yaml.safe_load(metadata)  # Parse YAML

        info = extract_metadata(data)
        return build_card_html(info)

    except Exception as e:
        return f"**Error loading card from {file_path}: {str(e)}**"


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
                                date_obj = datetime.strptime(submission_date, "%Y-%m-%d")
                            except ValueError:
                                date_obj = datetime.min
                        else:
                            date_obj = submission_date if isinstance(submission_date, datetime) else datetime.min

                        card_files.append((file_path, date_obj))
                    except Exception as e:
                        print(f"Error parsing {filename}: {e}")

    card_files.sort(key=lambda x: x[1] if x[1] else datetime.min, reverse=True)

    rendered_cards = ""
    docs_dir = Path("docs").resolve()

    for file_path, _ in card_files:
        clean_path = str(Path(file_path).resolve().relative_to(docs_dir))
        rendered_cards += render_card_from_file(clean_path) + "\n"

    return rendered_cards


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
    def render_card_from_file_macro(file_path):
        return render_card_from_file(file_path)

    @env.macro
    def render_sorted_cards_macro(cards_dir="docs/cards"):
        return render_sorted_cards(cards_dir)
