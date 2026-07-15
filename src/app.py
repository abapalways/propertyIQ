"""PropertyIQ — Gradio ChatInterface wired to the RAG prototype (Task 9).

Real buyer criteria in, grounded shortlist out: the chat takes a buyer (selected
by buyer_id) plus a free-text query, runs the Task-8 prototype
(retrieve -> deterministic rejection filter -> grounded LLM shortlist), and
returns the ranked shortlist. Rejected listings (e.g. L_ELM_124 for B001) are
filtered in code and never resurface.

Run:  python src/app.py         # launches with a public share link
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "src"))  # so `import prototype`/`retrieve` work

PROFILES_PATH = ROOT / "data" / "buyer_profiles.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KEY_CONFIGURED = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip() and "your-openai-api-key" not in OPENAI_API_KEY)


def _buyer_choices():
    data = json.loads(PROFILES_PATH.read_text())
    return [f"{p['buyer_id']} — {p['name']}" for p in data["profiles"]]


def _buyer_id(choice: str) -> str:
    return choice.split(" — ", 1)[0].strip()


def respond(message: str, history: list, buyer_choice: str) -> str:
    del history  # each shortlist is computed fresh from the buyer profile + query

    if not KEY_CONFIGURED:
        return (
            "⚠️ **OPENAI_API_KEY is not configured.** Copy `.env.example` to "
            "`.env`, set your key, run `python src/ingest.py`, then relaunch."
        )

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

    return gr.ChatInterface(
        fn=respond,
        title="PropertyIQ",
        description=(
            "Property-search assistant. Pick a buyer, ask for a shortlist "
            "(e.g. \"Find 3-bed homes under $450K near good schools in Austin\"). "
            "Results are grounded in the RAG corpus; rejected listings are never "
            "resurfaced."
        ),
        additional_inputs=[
            gr.Dropdown(choices=_buyer_choices(), value=_buyer_choices()[0], label="Buyer profile")
        ],
    )


def main():
    status = "configured ✅" if KEY_CONFIGURED else "NOT configured ⚠️ (shortlists disabled)"
    print(f"[PropertyIQ] OPENAI_API_KEY is {status}")
    demo = build_demo()
    demo.launch(share=True)


if __name__ == "__main__":
    main()
