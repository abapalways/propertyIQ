"""Task 4: auto-generate additional buyer profiles.

Reads data/buyer_profiles.json, KEEPS the four hand-designed profiles
(B001-B004) exactly as they are, and (re)generates a deterministic set of
additional profiles B005+ in the identical schema. Deterministic: no RNG, so
re-running produces the same file (idempotent).

Variety is spread across budget bands, bedroom counts, must-have combinations,
preferred city, and rejection history (some referencing real listing IDs from
data/corpus/listings_corpus.md).

Run:  python src/generate_profiles.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "buyer_profiles.json"

# Real listing IDs from data/corpus/listings_corpus.md (for rejection history).
REAL_LISTING_IDS = [
    "L_PINE_101", "L_CEDAR_103", "L_MAPLE_105", "L_OAK_106", "L_WALNUT_107",
    "L_PECAN_108", "L_WILLOW_109", "L_BIRCH_110", "L_ELM_124", "L_ASPEN_112",
]

# Each tuple: (name, min_bedrooms, max_budget, must_haves, city, rejected, purpose)
GENERATED = [
    ("Aisha Rahman", 2, 350000, ["garage"], "Austin", [],
     "Low budget band ($350K) + small home; most Austin 3-beds are out of reach, "
     "exercises the bottom of the budget range."),
    ("Tom & Grace Whitfield", 3, 375000, ["good school district"], "Austin", ["L_WALNUT_107"],
     "Tight budget ($375K) with a good-schools must-have; has already rejected "
     "L_WALNUT_107 (cheap but low-rated schools), so rejection recall must keep it out."),
    ("Daniel Kim", 3, 400000, ["garage", "good school district"], "Austin", [],
     "Sub-$400K band with two must-haves; stresses affordability against the "
     "good-schools + garage combination."),
    ("Sofia Herrera", 3, 425000, ["good school district"], "Austin", ["L_ELM_124"],
     "Mid budget; independently rejected L_ELM_124 as well, verifying rejection "
     "recall works for a buyer other than B001."),
    ("The Nguyen Family", 4, 450000, ["garage"], "Austin", [],
     "Wants 4 bedrooms at the $450K ceiling; L_WALNUT_107 (4-bed, $399K) fits beds/"
     "budget/garage but schools are weak -- tests four-bed demand at the cap."),
    ("Robert Osei", 3, 460000, ["garage", "safe neighborhood"], "Austin", ["L_MAPLE_105"],
     "Safety-focused buyer; rejected L_MAPLE_105 (no garage). Combines a safety "
     "must-have with garage and a rejection."),
    ("Lena Petrov", 3, 475000, ["good school district", "safe neighborhood"], "Austin", [],
     "Higher budget with both schools and safety must-haves; L_PECAN_108/L_ASPEN_112 "
     "(Eanes ISD) become reachable, exercising the upper-mid band."),
    ("Marcus & Dana Cole", 3, 500000, ["garage", "good school district"], "Austin", ["L_CEDAR_103"],
     "$500K ceiling; rejected L_CEDAR_103 ($510K, over budget) -- so both budget "
     "logic AND rejection recall should keep it out."),
    ("Priyanka Desai", 4, 525000, ["good school district"], "Austin", [],
     "Above the standard cap ($525K); most listings qualify on price, isolating the "
     "bedroom (4) and schools filters."),
    ("The Alvarez Family", 5, 600000, ["garage", "safe neighborhood", "good school district"], "Austin", [],
     "Top budget band ($600K) and 5 bedrooms with three must-haves; no current "
     "listing fully satisfies -- tests graceful 'no strong match' behavior."),
    ("Hannah Brooks", 3, 430000, ["garage"], "Round Rock", [],
     "Geography variation: prefers Round Rock, so L_WILLOW_109 (Round Rock, $415K, "
     "garage) becomes the strong match instead of a trap."),
    ("Victor Chen", 3, 450000, ["safe neighborhood"], "Round Rock", ["L_WILLOW_109"],
     "Round Rock buyer who has already rejected the main Round Rock listing "
     "(L_WILLOW_109); exercises rejection recall shrinking a thin candidate pool."),
    ("Olivia Santos", 2, 390000, ["good school district"], "Austin", [],
     "Two-bedroom buyer on a modest budget; L_BIRCH_110 (2-bed, $380K) fits beds/"
     "budget but has weak schools -- tests the 2-bed segment."),
]


def main() -> None:
    data = json.loads(PROFILES_PATH.read_text())
    kept = [p for p in data["profiles"] if p["buyer_id"] in {"B001", "B002", "B003", "B004"}]
    if len(kept) != 4:
        raise SystemExit(f"Expected B001-B004 intact, found {[p['buyer_id'] for p in kept]}")

    generated = []
    for i, (name, beds, budget, must_haves, city, rejected, purpose) in enumerate(GENERATED):
        bid = f"B{5 + i:03d}"
        for lid in rejected:
            if lid not in REAL_LISTING_IDS:
                raise SystemExit(f"{bid} references unknown listing {lid}")
        generated.append({
            "buyer_id": bid,
            "name": name,
            "preferences": {
                "min_bedrooms": beds,
                "max_budget": budget,
                "must_haves": must_haves,
                "preferred_city": city,
            },
            "session_history": {
                "current_session_id": f"s-{bid.lower()}-001",
                "rejected_listings": rejected,
            },
            "test_purpose": "AUTO-GENERATED (Task 4). " + purpose,
        })

    data["profiles"] = kept + generated
    PROFILES_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {len(data['profiles'])} profiles "
          f"(4 hand-designed B001-B004 + {len(generated)} generated B005-B{4 + len(generated):03d}).")


if __name__ == "__main__":
    main()
