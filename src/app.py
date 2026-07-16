"""PropertyIQ — Gradio ChatInterface wired to the RAG prototype (Task 9, Ollama).

Real buyer criteria in, grounded shortlist out: the chat takes a buyer (selected
by buyer_id) plus a free-text query, runs the Task-8 prototype
(retrieve -> deterministic rejection filter -> grounded ChatOllama shortlist),
and returns the ranked shortlist. Rejected listings (e.g. L_ELM_124 for B001)
are filtered in code and never resurface.

Run:  python src/app.py         # launches with a public share link
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import llm  # noqa: E402  (shared Ollama wiring; also loads .env)

PROFILES_PATH = ROOT / "data" / "buyer_profiles.json"

try:
    llm.check_ollama()
    OLLAMA_STATUS = f"reachable ✅ ({llm.OLLAMA_CHAT_MODEL} / {llm.OLLAMA_EMBED_MODEL} @ {llm.OLLAMA_BASE_URL})"
    OLLAMA_ERROR = None
except llm.OllamaUnavailable as exc:
    OLLAMA_STATUS = "NOT reachable ⚠️ (shortlists disabled)"
    OLLAMA_ERROR = str(exc)


def _buyer_choices():
    data = json.loads(PROFILES_PATH.read_text())
    return [f"{p['buyer_id']} — {p['name']}" for p in data["profiles"]]


def _buyer_id(choice: str) -> str:
    return choice.split(" — ", 1)[0].strip()


def respond(message: str, history: list, buyer_choice: str) -> str:
    del history  # each shortlist is computed fresh from the buyer profile + query

    if OLLAMA_ERROR:
        return f"⚠️ **Ollama is not reachable.**\n\n{OLLAMA_ERROR}"

    buyer_id = _buyer_id(buyer_choice)
    try:
        import prototype
        r = prototype.generate_shortlist(buyer_id, query=message or None)
    except Exception as exc:  # surface setup issues (e.g. missing Chroma store)
        return (
            f"⚠️ Could not produce a shortlist: `{exc}`\n\n"
            "Make sure the corpus is ingested: `python src/ingest.py`."
        )

    prefs = r["prefs"]
    header = (
        f"**Buyer {r['buyer_id']} ({r['name']})** — "
        f"{prefs['min_bedrooms']}+ bed, ≤ ${prefs['max_budget']:,}, "
        f"{prefs['preferred_city']}, must-haves: {', '.join(prefs['must_haves']) or 'none'}\n\n"
    )
    if r["dropped"]:
        header += f"_Rejection memory removed (not shown): {', '.join(r['dropped'])}_\n\n"
    return header + r["shortlist"]


def build_demo():
    import gradio as gr

    description = (
        "Property-search assistant, powered by a local model via Ollama. Pick a "
        "buyer, ask for a shortlist (e.g. \"Find 3-bed homes under $450K near "
        "good schools in Austin\"). Results are grounded in the RAG corpus; "
        "rejected listings are never resurfaced.\n\n"
        f"Ollama status: {OLLAMA_STATUS}"
    )
    if OLLAMA_ERROR:
        description += f"\n\n⚠️ {OLLAMA_ERROR}"

    return gr.ChatInterface(
        fn=respond,
        title="PropertyIQ",
        description=description,
        additional_inputs=[
            gr.Dropdown(choices=_buyer_choices(), value=_buyer_choices()[0], label="Buyer profile")
        ],
    )


def main():
    print(f"[PropertyIQ] Ollama is {OLLAMA_STATUS}")
    demo = build_demo()
    demo.launch(share=True)


if __name__ == "__main__":
    main()
