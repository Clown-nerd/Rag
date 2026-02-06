"""
Centralised RAG configuration and system-prompt storage.

All tuneable settings (model names, base URLs, prompt templates) live here
so they can be versioned, reviewed, and swapped without touching RAG logic.
"""

from config.settings import get_settings          # noqa: F401
from config.prompts import SYSTEM_PROMPT, DRAFT_PROMPT  # noqa: F401
