"""Task 8: minimal criteria-to-shortlist prototype (no mortgage/comps tools yet).

Given a buyer_id from data/buyer_profiles.json:
  1. Build a search query from the buyer's preferences.
  2. Retrieve candidate corpus chunks from ChromaDB (src/retrieve.py).
  3. DETERMINISTICALLY drop any listing in the buyer's rejected list BEFORE the
     LLM sees it -- rejection filtering is done in code, not left to the model,
     so a rejected listing (e.g. L_ELM_124 for B001) can never be resurfaced.
  4. Ask the LLM (with src/prompts/system_prompt.md) to produce a ranked
     shortlist with a short grounded rationale, citing listing IDs.

`generate_shortlist()` is the reusable core, shared by this CLI and the Gradio
UI (src/app.py).

Run:
    python src/prototype.py            # defaults to B001 (Torres Family)
    python src/prototype.py B003
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

PROFILES_PATH = ROOT / "data" / "buyer_profiles.json"
SYSTEM_PROMPT_PATH = ROOT / "src" / "prompts" / "system_prompt.md"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
CANDIDATE_K = 8


def has_key() -> bool:
    key = os.getenv("OPENAI_API_KEY")
    return bool(key and "your-openai-api-key" not in key)


def load_profile(buyer_id: str) -> dict:
    data = json.loads(PROFILES_PATH.read_text())
    for p in data["profiles"]:
        if p["buyer_id"] == buyer_id:
            return p
    raise SystemExit(f"{buyer_id} not found in {PROFILES_PATH}")


def build_query(profile: dict) -> str:
    p = profile["preferences"]
    musts = ", ".join(p["must_haves"]) if p["must_haves"] else "no specific must-haves"
    return (
        f"{p['min_bedrooms']}-bed homes under ${p['max_budget']:,} in "
        f"{p['preferred_city']} with {musts}"
    )


def generate_shortlist(buyer_id: str, query: str | None = None) -> dict:
    """Core RAG-to-shortlist path shared by the CLI and the Gradio UI.

    Returns a dict: {buyer_id, name, prefs, rejected, query, retrieved_ids,
    dropped, kept_ids, shortlist}. Rejection filtering is deterministic and
    happens before the LLM call.
    """
    if not has_key():
        raise RuntimeError("OPENAI_API_KEY not configured — set it in .env.")

    from openai import OpenAI
    from retrieve import retrieve  # same directory

    profile = load_profile(buyer_id)
    prefs = profile["preferences"]
    rejected = set(profile["session_history"]["rejected_listings"])
    query = query or build_query(profile)

    candidates = retrieve(query, k=CANDIDATE_K)
    retrieved_ids = [c["id"] for c in candidates]

    # DETERMINISTIC rejection filter (code-level, before the LLM).
    kept = [c for c in candidates if c["id"] not in rejected]
    dropped = [c["id"] for c in candidates if c["id"] in rejected]

    context = "\n\n".join(
        f"[{c['id']}] (source {c['metadata']['source']})\n{c['document']}" for c in kept
    )
    musts = ", ".join(prefs["must_haves"]) if prefs["must_haves"] else "none"
    user_msg = (
        f"Buyer {buyer_id} ({profile['name']}) is looking for: at least "
        f"{prefs['min_bedrooms']} bedrooms, budget up to ${prefs['max_budget']:,}, "
        f"in {prefs['preferred_city']}, must-haves: {musts}.\n\n"
        f"Here are the ONLY candidate listings/neighborhood records you may use "
        f"(do not invent others, do not use any figure not present here):\n\n"
        f"{context}\n\n"
        f"Produce a ranked shortlist of the best-fitting listings (best first). "
        f"For each, give a one-line rationale grounded in the record above and "
        f"cite its listing ID. If a listing fails a hard criterion (over budget, "
        f"wrong city, too few bedrooms, missing a must-have), either exclude it or "
        f"clearly flag why it falls short. Do not include any listing not in the "
        f"list above."
    )

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_PATH.read_text()},
            {"role": "user", "content": user_msg},
        ],
    )

    return {
        "buyer_id": buyer_id,
        "name": profile["name"],
        "prefs": prefs,
        "rejected": sorted(rejected),
        "query": query,
        "retrieved_ids": retrieved_ids,
        "dropped": dropped,
        "kept_ids": [c["id"] for c in kept],
        "shortlist": resp.choices[0].message.content,
    }


def run(buyer_id: str = "B001") -> int:
    if not has_key():
        print("OPENAI_API_KEY not configured. Add it to .env, run `python src/ingest.py`, "
              "then re-run:  python src/prototype.py " + buyer_id)
        return 1

    r = generate_shortlist(buyer_id)
    print(f"=== PropertyIQ prototype — buyer {r['buyer_id']} ({r['name']}) ===")
    print(f"Preferences: {r['prefs']}")
    print(f"Rejected listings (from memory): {r['rejected'] or 'none'}")
    print(f"Search query: {r['query']}\n")
    print(f"Retrieved {len(r['retrieved_ids'])} candidate chunks: {r['retrieved_ids']}")
    if r["dropped"]:
        print(f"Rejection filter removed (never shown to LLM): {r['dropped']}")
    else:
        print("Rejection filter removed: none (no rejected listing was retrieved)")
    print(f"Candidates passed to LLM: {r['kept_ids']}\n")
    print("=== Ranked shortlist ===\n")
    print(r["shortlist"])

    print("\n=== Acceptance checks ===")
    rejected = set(r["rejected"])
    print(f"Rejected listings never passed to LLM: {rejected.isdisjoint(set(r['kept_ids']))} "
          f"(rejected={r['rejected'] or 'none'})")
    print(f"Rejected listings absent from shortlist text: "
          f"{all(rid not in r['shortlist'] for rid in rejected)}")
    if buyer_id == "B001":
        print(f"  - L_ELM_124 was retrieved by similarity: {'L_ELM_124' in r['retrieved_ids']}")
        print(f"  - L_ELM_124 dropped by rejection filter: {'L_ELM_124' in r['dropped']}")
        print(f"  - L_ELM_124 absent from final shortlist: {'L_ELM_124' not in r['shortlist']}")
        print(f"  - L_PINE_101 present as a match: {'L_PINE_101' in r['shortlist']}")
    return 0


def main() -> int:
    buyer_id = sys.argv[1] if len(sys.argv) > 1 else "B001"
    return run(buyer_id)


if __name__ == "__main__":
    sys.exit(main())
