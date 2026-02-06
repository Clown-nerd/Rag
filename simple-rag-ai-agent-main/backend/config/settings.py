"""
Runtime settings loaded from environment variables / .env file.

Defaults point at a local Ollama instance so the system works out of the
box without any cloud API keys.
"""

import os


def _int_env(name: str, default: int) -> int:
    """Read an environment variable as an integer with a clear error message."""
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(
            f"Environment variable {name} must be an integer, got '{raw}'"
        )


def get_settings() -> dict:
    """Return a dict of all configuration values used by the RAG pipeline."""
    return {
        # --- Ollama / local-model connection ---
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),

        # --- Model names (must be pulled into Ollama first) ---
        "chat_model": os.getenv("CHAT_MODEL", "mistral"),
        "embed_model": os.getenv("EMBED_MODEL", "nomic-embed-text"),

        # --- Retrieval tunables ---
        "chunk_tokens": _int_env("CHUNK_TOKENS", 450),
        "chunk_overlap": _int_env("CHUNK_OVERLAP", 80),
        "retrieval_k": _int_env("RETRIEVAL_K", 4),

        # --- Server binding (0.0.0.0 allows LAN access) ---
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": _int_env("PORT", 8000),
    }
