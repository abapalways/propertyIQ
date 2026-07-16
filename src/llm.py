"""Shared local-LLM wiring for PropertyIQ (Ollama via langchain-ollama).

Centralizes model config, a reachability check, and factories for the chat
model and embeddings, so every script (ingest, retrieve, prototype, app, tests)
talks to the local model the same way. No OpenAI calls anywhere.

LangSmith tracing stays wired: we load .env (which may set LANGCHAIN_TRACING_V2
/ LANGCHAIN_API_KEY / LANGCHAIN_PROJECT) and never disable it, so traces are
captured whenever a LangSmith key is present -- it works fine with a local model.
"""

import os
import urllib.request
import urllib.error
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


class OllamaUnavailable(RuntimeError):
    """Raised when the local Ollama server can't be reached or lacks a model."""


def check_ollama(require_models=True) -> list:
    """Verify Ollama is reachable at OLLAMA_BASE_URL. Returns the list of
    available model names. Raises OllamaUnavailable with a clear message if the
    server is down or (when require_models) a configured model is missing."""
    url = OLLAMA_BASE_URL.rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            import json
            data = json.loads(resp.read().decode())
    except (urllib.error.URLError, OSError) as exc:
        raise OllamaUnavailable(
            f"Ollama is not reachable at {OLLAMA_BASE_URL}. Start it with "
            f"`ollama serve` and ensure the models are pulled "
            f"(`ollama pull {OLLAMA_CHAT_MODEL}`, `ollama pull {OLLAMA_EMBED_MODEL}`). "
            f"Underlying error: {exc}"
        )

    names = [m.get("name", "") for m in data.get("models", [])]

    def present(want: str) -> bool:
        # Match with or without an explicit :tag (":latest" is implicit).
        return any(n == want or n.split(":")[0] == want.split(":")[0] for n in names)

    if require_models:
        missing = [m for m in (OLLAMA_CHAT_MODEL, OLLAMA_EMBED_MODEL) if not present(m)]
        if missing:
            raise OllamaUnavailable(
                f"Ollama is up at {OLLAMA_BASE_URL} but these models are missing: "
                f"{missing}. Pull them with: "
                + "; ".join(f"ollama pull {m}" for m in missing)
                + f". Available: {names}"
            )
    return names


def make_chat(temperature: float = 0.0):
    """ChatOllama for the configured chat model. reasoning=False keeps qwen3's
    <think> traces out of the visible answer for clean, deterministic output."""
    from langchain_ollama import ChatOllama
    return ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        reasoning=False,
    )


def make_embeddings():
    from langchain_ollama import OllamaEmbeddings
    return OllamaEmbeddings(model=OLLAMA_EMBED_MODEL, base_url=OLLAMA_BASE_URL)
