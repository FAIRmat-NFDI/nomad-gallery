import os
from datetime import datetime

import yaml


def render_card_from_file(file_path):
    """Reads front matter from a file and renders a formatted card."""
    try:
        with open(f'docs/{file_path}', encoding='utf-8') as f:
            content = f.read()
            metadata, _ = content.split('---', 2)[1:]  # Extract front matter
            data = yaml.safe_load(metadata)  # Parse YAML

        # Values with defaults
        title = data.get('title', 'Untitled Submission')
        submitter = data.get('submitter', 'Unknown Submitter')
        description = data.get('description', 'No description available.')
        submission_date = data.get('submission_date', 'Unknown date')
        image_name = data.get('image_name', 'Image')

        # Values with dynamic removal
        image_path = data.get('image_path', '').strip()
        # Handling image paths (relative and absolute)
        if 'github.com' in image_path:
            # Convert GitHub page URL to raw content URL
            image_path = image_path.replace(
                'github.com', 'raw.githubusercontent.com'
            ).replace('/blob/', '/')
        repo_link = data.get('repo_link', '').strip()
        repo_name = data.get('repo_name', '').strip()
        entry_link = data.get('entry_link', '').strip()
        entry_name = data.get('entry_name', '').strip()

        # Start building the HTML card
        card_content = [
            '<div markdown="block" style="background-color: white;\
                  padding: 20px; border-radius: 10px; '
            'box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;">\n'
        ]

        # Always add fields with defaults
        card_content.append(f'## {title}\n')
        card_content.append(f'**Submitter**: {submitter}\n')
        card_content.append(f'**Description**: {description}\n')
        card_content.append(f'**Submission date**: {submission_date}\n')

        # Conditional additions
        if image_path:
            card_content.append(
                f'<div class="click-zoom">\n'
                f'    <label>\n'
                f'        <input type="checkbox">\n'
                f'        <img src="{image_path}" alt="{image_name}" width="100%"\
                      title="Click to zoom in">\n'
                f'    </label>\n'
                f'</div>\n'
            )
        if repo_link:
            if not repo_name:
                repo_name = repo_link
            card_content.append(f'**Link to repo**: [{repo_name}]({repo_link})\n')
        if entry_link:
            if not entry_name:
                entry_name = entry_link
            card_content.append(
                f'**Link to entry/page/app/dataset/upload**:\
                      [{entry_name}]({entry_link})\n'
            )

        # Close the div
        card_content.append('</div>\n')

        # Return the final HTML card as a string
        return '\n'.join(card_content)

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

                        # Check submission_date is already a datetime object or a string
                        if isinstance(submission_date, datetime):
                            date_obj = submission_date
                        elif isinstance(submission_date, str):
                            try:
                                # Try to parse the date string into a datetime object
                                date_obj = datetime.strptime(
                                    submission_date, '%Y-%m-%d'
                                )
                            except ValueError:
                                # If parsing fails, set to a default date (optional)
                                date_obj = datetime.min
                        else:
                            # If no valid date, use the earliest date (optional)
                            date_obj = datetime.min

                        card_files.append((file_path, date_obj))
                    except Exception as e:
                        print(f'Error parsing {filename}: {e}')

    # Sort by submission_date (newest first)
    card_files.sort(key=lambda x: x[1] if x[1] else datetime.min, reverse=True)

    # Now render each card using the render_card_from_file function
    rendered_cards = ''
    for file_path, _ in card_files:
        # Strip 'docs/' from the front of the file path
        # FIX: used a new variable name 'clean_path' instead of overwriting 'file_path'
        clean_path = file_path.replace('docs/', '', 1)
        rendered_cards += render_card_from_file(clean_path) + '\n'

    print(rendered_cards)

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
