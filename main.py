import os
from datetime import datetime

import yaml


def extract_metadata(data):
    """Extracts and cleans all fields from the YAML data."""
    # Handle lists (Coauthors, Keywords)
    coauthors = data.get('coauthors', [])
    if isinstance(coauthors, str):
        coauthors = [c.strip() for c in coauthors.split(',')]

    keywords = data.get('keywords', [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(',')]

    # Handle Images
    image_path = data.get('image_path', '').strip()
    if 'github.com' in image_path:
        image_path = image_path.replace(
            'github.com', 'raw.githubusercontent.com'
        ).replace('/blob/', '/')

    # Handle Links with Fallbacks
    repo_link = data.get('repo_link', '').strip()
    repo_name = data.get('repo_name', '').strip() or repo_link
    entry_link = data.get('entry_link', '').strip()
    entry_name = data.get('entry_name', '').strip() or entry_link

    return {
        'title': data.get('title', 'Untitled Submission'),
        'submitter': data.get('submitter', 'Unknown Submitter'),
        'description': data.get('description', 'No description available.'),
        'submission_date': data.get('submission_date', 'Unknown date'),
        'institution': data.get('institution', '').strip(),
        'country': data.get('country', '').strip(),
        'research_field': data.get('research_field', '').strip(),
        'methodology': data.get('methodology_type', '').strip(),
        'technique': data.get('technique', '').strip(),
        'data_size': data.get('data_size', '').strip(),
        'active_users': data.get('estimated_active_users', None),
        'downloads': data.get('downloads', None),
        'media_url': data.get('media_url', '').strip(),
        'coauthors': coauthors,
        'keywords': keywords,
        'publication': data.get('publication_reference', '').strip(),
        'funding': data.get('funding_reference', '').strip(),
        'image_name': data.get('image_name', 'Image'),
        'image_path': image_path,
        'repo_link': repo_link,
        'repo_name': repo_name,
        'entry_link': entry_link,
        'entry_name': entry_name,
    }


def _build_header(info):
    html = [f'## {info["title"]}\n']
    meta = []
    if info['research_field']:
        meta.append(f'**Field**: {info["research_field"]}')
    if info['institution']:
        meta.append(f'**Inst**: {info["institution"]}')
    if info['country']:
        meta.append(f'({info["country"]})')

    if meta:
        html.append(f'{", ".join(meta)}  \n')

    html.append(f'\n{info["description"]}\n<br>\n')
    return html


def _build_details(info):
    html = []
    html.append(f'**Submitter**: {info["submitter"]}  \n')

    if info['coauthors']:
        html.append(f'**Coauthors**: {", ".join(info["coauthors"])}  \n')
    if info['methodology']:
        html.append(f'**Methodology**: {info["methodology"]}  \n')
    if info['technique']:
        html.append(f'**Technique**: {info["technique"]}  \n')
    if info['data_size']:
        html.append(f'**Data Size**: {info["data_size"]}  \n')
    return html


def _build_metrics_and_refs(info):
    html = []
    # Metrics
    metrics = []
    if info['active_users']:
        metrics.append(f'{info["active_users"]} Users')
    if info['downloads']:
        metrics.append(f'{info["downloads"]} Downloads')
    if metrics:
        html.append(f'**Impact**: {", ".join(metrics)}  \n')

    # Funding & Pubs
    if info['funding']:
        html.append(f'**Funding**: {info["funding"]}  \n')
    if info['publication']:
        html.append(f'**Publication**: {info["publication"]}  \n')

    # Keywords
    if info['keywords']:
        badges = [f'`{k}`' for k in info['keywords']]
        html.append(f'\n**Keywords**: {" ".join(badges)}  \n')

    html.append(f'\n*Submitted: {info["submission_date"]}*\n')
    return html


def _build_media_and_links(info):
    html = []
    # Image
    if info['image_path']:
        html.append(
            f'<div class="click-zoom" style="margin-top: 10px;">\n'
            f'    <label>\n'
            f'        <input type="checkbox">\n'
            f'        <img src="{info["image_path"]}" alt="{info["image_name"]}" \
                  width="100%" title="Click to zoom in">\n'
            f'    </label>\n'
            f'</div>\n'
        )

    # Links
    if info['repo_link']:
        html.append(f'\n**Repo**: [{info["repo_name"]}]({info["repo_link"]})\n')
    if info['entry_link']:
        html.append(f'**Launch**: [{info["entry_name"]}]({info["entry_link"]})\n')
    if info['media_url']:
        html.append(f'**Media/Video**: [Watch Demo]({info["media_url"]})\n')

    return html


def build_card_html(info):
    """Constructs the HTML for a single card by composing helper functions."""
    html = [
        '<div markdown="block" style="background-color: white;\
              padding: 20px; border-radius: 10px; '
        'box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;">\n'
    ]

    html.extend(_build_header(info))
    html.extend(_build_details(info))
    html.extend(_build_metrics_and_refs(info))
    html.extend(_build_media_and_links(info))

    html.append('</div>\n')
    return ''.join(html)


def render_card_from_file(file_path):
    """Reads front matter from a file and renders a formatted card."""
    try:
        with open(f'docs/{file_path}', encoding='utf-8') as f:
            content = f.read()
            metadata, _ = content.split('---', 2)[1:]  # Extract front matter
            data = yaml.safe_load(metadata)  # Parse YAML

        info = extract_metadata(data)
        return build_card_html(info)

    except Exception as e:
        return f'**Error loading card from {file_path}: {str(e)}**'


def render_sorted_cards(cards_dir='docs/cards'):
    """Render all cards from the specified directory, sorted by submission date."""
    card_files = []

    # List all files in the specified directory and filter only .md files
    if os.path.exists(cards_dir):
        for filename in os.listdir(cards_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(cards_dir, filename)

                # Read the front matter to extract the date
                with open(file_path, encoding='utf-8') as f:
                    try:
                        # Load YAML front matter
                        front_matter = yaml.safe_load(f.read().split('---')[1])
                        submission_date = front_matter.get('submission_date', '')

                        # Check submission_date
                        if isinstance(submission_date, str):
                            try:
                                date_obj = datetime.strptime(
                                    submission_date, '%Y-%m-%d'
                                )
                            except ValueError:
                                date_obj = datetime.min
                        else:
                            is_date = isinstance(submission_date, datetime)
                            date_obj = submission_date if is_date else datetime.min

                        card_files.append((file_path, date_obj))
                    except Exception as e:
                        print(f'Error parsing {filename}: {e}')

    # Sort by submission_date (newest first)
    card_files.sort(key=lambda x: x[1] if x[1] else datetime.min, reverse=True)

    # Now render each card using the render_card_from_file function
    rendered_cards = ''
    for file_path, _ in card_files:
        # Strip 'docs/' from the front of the file path
        clean_path = file_path.replace('docs/', '', 1)
        rendered_cards += render_card_from_file(clean_path) + '\n'

    return rendered_cards


def define_env(env):
    """Define macros for MkDocs."""

    @env.macro
    def include_raw_markdown(file_path):
        """Reads and returns raw markdown content from a file without rendering."""
        try:
            with open(f'docs/{file_path}', encoding='utf-8') as f:
                content = f.read()
                # Escape the content by using `|safe` to treat it as raw text
                return f'```markdown\n{content}\n```'
        except Exception as e:
            return f'**Error loading file {file_path}: {str(e)}**'

    @env.macro
    def render_card_from_file_macro(file_path):
        return render_card_from_file(file_path)

    @env.macro
    def render_sorted_cards_macro(cards_dir='docs/cards'):
        return render_sorted_cards(cards_dir)
