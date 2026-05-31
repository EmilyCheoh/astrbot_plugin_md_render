"""
Markdown Render Plugin - Theme Definitions

Each theme is a dictionary containing CSS variables and styles.
To add a new theme, simply add a new entry to the THEMES dict.
"""

THEMES = {
    "dark": {
        "name": "Dark",
        "bg": "#1e1e2e",
        "fg": "#cdd6f4",
        "fg_muted": "#a6adc8",
        "border": "#45475a",
        "code_bg": "#181825",
        "code_fg": "#cdd6f4",
        "inline_code_bg": "#313244",
        "inline_code_fg": "#f38ba8",
        "blockquote_border": "#cba6f7",
        "blockquote_bg": "#1e1e2e",
        "table_header_bg": "#313244",
        "table_row_alt_bg": "#181825",
        "link_color": "#89b4fa",
        "hr_color": "#45475a",
        "heading_color": "#cdd6f4",
        "bold_color": "#f5e0dc",
        "strikethrough_color": "#6c7086",
    },
    "light": {
        "name": "Light",
        "bg": "#ffffff",
        "fg": "#1e1e2e",
        "fg_muted": "#5c5f77",
        "border": "#dce0e8",
        "code_bg": "#f5f5f7",
        "code_fg": "#1e1e2e",
        "inline_code_bg": "#e6e9ef",
        "inline_code_fg": "#d20f39",
        "blockquote_border": "#8839ef",
        "blockquote_bg": "#f9fafb",
        "table_header_bg": "#eff1f5",
        "table_row_alt_bg": "#f5f5f7",
        "link_color": "#1e66f5",
        "hr_color": "#dce0e8",
        "heading_color": "#1e1e2e",
        "bold_color": "#4c4f69",
        "strikethrough_color": "#9ca0b0",
    },
}


def get_theme(name: str) -> dict:
    """Get a theme by name. Falls back to dark if not found."""
    return THEMES.get(name, THEMES["dark"])


def list_themes() -> list:
    """Return list of available theme names."""
    return list(THEMES.keys())
