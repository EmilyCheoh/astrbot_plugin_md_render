import os
import re
import tempfile

import markdown
import imgkit

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Image
from astrbot.api import logger, AstrBotConfig

from .template import build_html
from .themes import list_themes

# Patterns that indicate the message contains markdown worth rendering
MD_PATTERNS = [
    re.compile(r"^#{1,6}\s", re.MULTILINE),         # headings
    re.compile(r"\|.+\|.+\|", re.MULTILINE),        # tables
    re.compile(r"```[\s\S]+?```"),                   # fenced code blocks
    re.compile(r"^>\s", re.MULTILINE),               # blockquotes
    re.compile(r"^[-*]\s", re.MULTILINE),            # unordered lists
    re.compile(r"^\d+\.\s", re.MULTILINE),           # ordered lists
    re.compile(r"\*\*.+?\*\*"),                      # bold
    re.compile(r"~~.+?~~"),                          # strikethrough
    re.compile(r"^---+$", re.MULTILINE),             # horizontal rules
]

# Minimum number of markdown patterns that must match to trigger auto-render
AUTO_RENDER_THRESHOLD = 1


def _has_rich_markdown(text: str) -> bool:
    """Check if text contains any markdown elements worth rendering."""
    return any(p.search(text) for p in MD_PATTERNS)


def _render_to_image(md_text: str, theme: str, width: int) -> str:
    """
    Convert markdown text to a PNG image.

    Returns the path to the generated temporary image file.
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_text,
        extensions=[
            "tables",
            "fenced_code",
            "codehilite",
            "nl2br",
            "sane_lists",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": True,
                "noclasses": True,
                "pygments_style": "monokai" if theme == "dark" else "default",
            }
        },
    )

    # Wrap in full HTML page with theme
    full_html = build_html(html_content, theme_name=theme, width=width)

    # Render to image
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()

    options = {
        "format": "png",
        "width": str(width),
        "encoding": "UTF-8",
        "quiet": "",
        "enable-local-file-access": "",
    }

    try:
        imgkit.from_string(full_html, tmp.name, options=options)
    except Exception as e:
        # Clean up on failure
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
        raise e

    return tmp.name


@register("md_render", "Abyss AI", "Render markdown messages as images", "1.0.0")
class MdRenderPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.after_message_sent()
    async def auto_render_after_send(self, event: AstrMessageEvent):
        """Hook: after text message is sent, render and send image separately."""
        mode = self.config.get("mode", "auto")
        if mode != "auto":
            return

        # Get the plain text content from the result chain
        result = event.get_result()
        if not result or not result.chain:
            return

        # Extract text from the chain
        from astrbot.api.message_components import Plain
        text_parts = []
        for seg in result.chain:
            if isinstance(seg, Plain):
                text_parts.append(seg.text)

        full_text = "".join(text_parts)
        if not full_text or not _has_rich_markdown(full_text):
            return

        # Render and send as separate message
        theme = self.config.get("theme", "dark")
        width = self.config.get("width", 600)

        try:
            img_path = _render_to_image(full_text, theme, width)
            from astrbot.api.event import MessageChain
            chain = MessageChain().file_image(img_path)
            await self.context.send_message(event.unified_msg_origin, chain)
            logger.info(f"[md_render] Auto-rendered markdown image ({theme} theme)")
            # Cleanup
            if os.path.exists(img_path):
                os.unlink(img_path)
        except Exception as e:
            logger.error(f"[md_render] Render failed: {e}")

    @filter.command("render")
    async def render_command(self, event: AstrMessageEvent):
        """
        /render dark     — switch to dark theme
        /render light    — switch to light theme
        /render <content> — render markdown as image
        """
        text = event.message_str.strip()

        if not text:
            yield event.plain_result(
                "Usage:\n/render dark|light — switch theme\n/render <markdown> — render as image"
            )
            return

        # Theme switching
        available = list_themes()
        if text.lower() in available:
            self.config["theme"] = text.lower()
            self.config.save_config()
            yield event.plain_result(f"Theme set to: {text.lower()}")
            return

        # Render markdown
        theme = self.config.get("theme", "dark")
        width = self.config.get("width", 600)

        try:
            img_path = _render_to_image(text, theme, width)
            yield event.image_result(img_path)
            if os.path.exists(img_path):
                os.unlink(img_path)
        except Exception as e:
            logger.error(f"[md_render] Manual render failed: {e}")
            yield event.plain_result(f"Render failed: {e}")
