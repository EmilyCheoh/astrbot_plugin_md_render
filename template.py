"""
Markdown Render Plugin - HTML Template

Generates a self-contained HTML string from markdown content + theme.
The HTML includes all CSS inline so wkhtmltoimage can render it without external deps.
"""

from .themes import get_theme


def build_html(markdown_html: str, theme_name: str = "dark", width: int = 600) -> str:
    """
    Wrap rendered markdown HTML in a fully styled, self-contained HTML page.

    Args:
        markdown_html: Pre-rendered HTML from markdown source
        theme_name: Theme key from themes.py
        width: Content width in pixels

    Returns:
        Complete HTML string ready for wkhtmltoimage
    """
    t = get_theme(theme_name)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background: {t['bg']};
    color: {t['fg']};
    font-family: -apple-system, "Segoe UI", "Noto Sans SC", "PingFang SC",
                 "Microsoft YaHei", sans-serif;
    font-size: 15px;
    line-height: 1.7;
    padding: 28px 32px;
    max-width: {width}px;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    color: {t['heading_color']};
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    line-height: 1.3;
}}
h1 {{ font-size: 1.6em; }}
h2 {{ font-size: 1.35em; }}
h3 {{ font-size: 1.15em; }}
h4, h5, h6 {{ font-size: 1em; }}
h1:first-child, h2:first-child, h3:first-child {{
    margin-top: 0;
}}

/* Paragraphs */
p {{
    margin-bottom: 0.8em;
}}

/* Bold & Italic */
strong {{
    color: {t['bold_color']};
    font-weight: 600;
}}

em {{
    font-style: italic;
}}

del {{
    color: {t['strikethrough_color']};
    text-decoration: line-through;
}}

/* Links */
a {{
    color: {t['link_color']};
    text-decoration: none;
}}

/* Inline code */
code {{
    background: {t['inline_code_bg']};
    color: {t['inline_code_fg']};
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", "Consolas", monospace;
    font-size: 0.88em;
}}

/* Code blocks */
pre {{
    background: {t['code_bg']};
    border: 1px solid {t['border']};
    border-radius: 8px;
    padding: 16px 18px;
    margin: 1em 0;
    overflow-x: auto;
}}

pre code {{
    background: none;
    color: {t['code_fg']};
    padding: 0;
    border-radius: 0;
    font-size: 0.85em;
    line-height: 1.6;
}}

/* Blockquotes */
blockquote {{
    border-left: 3px solid {t['blockquote_border']};
    background: {t['blockquote_bg']};
    padding: 10px 16px;
    margin: 1em 0;
    color: {t['fg_muted']};
}}

blockquote p {{
    margin-bottom: 0.3em;
}}

/* Lists */
ul, ol {{
    padding-left: 1.8em;
    margin-bottom: 0.8em;
}}

li {{
    margin-bottom: 0.3em;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9em;
}}

th {{
    background: {t['table_header_bg']};
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    border-bottom: 2px solid {t['border']};
}}

td {{
    padding: 8px 12px;
    border-bottom: 1px solid {t['border']};
}}

tr:nth-child(even) td {{
    background: {t['table_row_alt_bg']};
}}

/* Horizontal rules */
hr {{
    border: none;
    height: 1px;
    background: {t['hr_color']};
    margin: 1.5em 0;
}}
</style>
</head>
<body>
{markdown_html}
</body>
</html>"""
