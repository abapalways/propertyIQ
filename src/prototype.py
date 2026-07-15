"""Task 8: minimal criteria-to-shortlist prototype (no mortgage/comps tools yet).

Given a buyer_id from data/buyer_profiles.json:
  1. Build a search query from the buyer's preferences.
  2. Retrieve candidate corpus chunks from ChromaDB (src/retrieve.py).
  3. DETERMINISTICALLY drop any listing in the buyer's rejected list BEFORE the
     LLM sees it -- rejection filtering is done in code, not left to the model,
     so a rejected listing (e.g. L_ELM_124 for B001) can never be resurfaced.
  4. Ask the LLM (with src/prompts/system_prompt.md) to produce a ranked
     shortlist with a short grounded rationale, citing listing IDs.

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


def run(buyer_id: str = "B001") -> int:
    key = os.getenv("OPENAI_API_KEY")
    if not key or "your-openai-api-key" in key:
        print("OPENAI_API_KEY not configured. Add it to .env, run `python src/ingest.py`, "
              "then re-run:  python src/prototype.py " + buyer_id)
        return 1

    from openai import OpenAI
    from retrieve import retrieve  # same directory

    profile = load_profile(buyer_id)
    prefs = profile["preferences"]
    rejected = set(profile["session_history"]["rejected_listings"])
    query = build_query(profile)

    print(f"=== PropertyIQ prototype — buyer {buyer_id} ({profile['name']}) ===")
    print(f"Preferences: {prefs}")
    print(f"Rejected listings (from memory): {sorted(rejected) or 'none'}")
    print(f"Search query: {query}\n")

    candidates = retrieve(query, k=CANDIDATE_K)
    retrieved_ids = [c["id"] for c in candidates]
    print(f"Retrieved {len(candidates)} candidate chunks: {retrieved_ids}")

    # DETERMINISTIC rejection filter (code-level, before the LLM).
    kept = [c for c in candidates if c["id"] not in rejected]
    dropped = [c["id"] for c in candidates if c["id"] in rejected]
    if dropped:
        print(f"Rejection filter removed (never shown to LLM): {dropped}")
    else:
        print("Rejection filter removed: none (no rejected listing was retrieved)")
    print(f"Candidates passed to LLM: {[c['id'] for c in kept]}\n")

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

    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_PATH.read_text()},
            {"role": "user", "content": user_msg},
        ],
    )
    shortlist = resp.choices[0].message.content
    print("=== Ranked shortlist ===\n")
    print(shortlist)

    # Automated acceptance checks.
    print("\n=== Acceptance checks ===")
    kept_ids = {c["id"] for c in kept}
    rejected_absent_from_candidates = rejected.isdisjoint(kept_ids)
    rejected_absent_from_shortlist = all(rid not in shortlist for rid in rejected)
    print(f"Rejected listings never passed to LLM: {rejected_absent_from_candidates} "
          f"(rejected={sorted(rejected) or 'none'})")
    print(f"Rejected listings absent from shortlist text: {rejected_absent_from_shortlist}")
    if buyer_id == "B001":
        elm_retrieved = "L_ELM_124" in retrieved_ids
        print(f"  - L_ELM_124 was retrieved by similarity: {elm_retrieved}")
        print(f"  - L_ELM_124 dropped by rejection filter: {'L_ELM_124' in dropped}")
        print(f"  - L_ELM_124 absent from final shortlist: {'L_ELM_124' not in shortlist}")
        print(f"  - L_PINE_101 present as a match: {'L_PINE_101' in shortlist}")
    return 0


def main() -> int:
    buyer_id = sys.argv[1] if len(sys.argv) > 1 else "B001"
    return run(buyer_id)


if __name__ == "__main__":
    sys.exit(main())
