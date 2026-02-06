"""
Runtime settings loaded from environment variables / .env file.

Defaults point at a local Ollama instance so the system works out of the
box without any cloud API keys.
"""

import os


def get_settings() -> dict:
    """Return a dict of all configuration values used by the RAG pipeline."""
    return {
        # --- Ollama / local-model connection ---
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),

        # --- Model names (must be pulled into Ollama first) ---
        "chat_model": os.getenv("CHAT_MODEL", "mistral"),
        "embed_model": os.getenv("EMBED_MODEL", "nomic-embed-text"),

        # --- Retrieval tunables ---
        "chunk_tokens": int(os.getenv("CHUNK_TOKENS", "450")),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "80")),
        "retrieval_k": int(os.getenv("RETRIEVAL_K", "4")),
    }
