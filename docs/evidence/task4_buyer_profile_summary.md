# Task 4 — Buyer Profile Summary

Summary counts across **all 17 buyer profiles** in `data/buyer_profiles.json`:
the 4 hand-designed profiles (**B001–B004**, unchanged) plus **13
auto-generated** profiles (**B005–B017**) produced deterministically by
`src/generate_profiles.py`.

- **Total profiles:** 17 (4 hand-designed + 13 generated)

## By bedroom count (`min_bedrooms`)

| Min bedrooms | Count |
|---|---|
| 2 | 2 |
| 3 | 12 |
| 4 | 2 |
| 5 | 1 |

- Want **3+ bedrooms:** 15 of 17
- Want **4+ bedrooms:** 3 of 17

## By budget band (`max_budget`)

| Band | Count |
|---|---|
| ≤ $375K | 2 |
| $376K–$425K | 3 |
| $426K–$475K | 8 |
| $476K–$525K | 3 |
| > $525K | 1 |

- **Under $400K:** 3 of 17
- **Under $450K:** 6 of 17
- **$450K and above:** 11 of 17
- **$500K and above:** 4 of 17

## By must-have (`must_haves`, non-exclusive)

| Must-have | Count |
|---|---|
| good school district | 11 |
| garage | 9 |
| safe neighborhood | 5 |

Number of must-haves per buyer: **1 must-have** → 10 buyers, **2 must-haves** →
6 buyers, **3 must-haves** → 1 buyer.

## By preferred city

| City | Count |
|---|---|
| Austin | 15 |
| Round Rock | 2 |

## By rejection history (`session_history.rejected_listings`)

- **Have a non-empty rejection list:** 6 of 17
- **No rejections:** 11 of 17

Rejected listing IDs referenced (all are real IDs from
`data/corpus/listings_corpus.md`):

| Listing ID | Times rejected | Rejected by |
|---|---|---|
| L_ELM_124 | 2 | B001 (Torres), B008 (Sofia Herrera) |
| L_WALNUT_107 | 1 | B006 (Tom & Grace Whitfield) |
| L_MAPLE_105 | 1 | B010 (Robert Osei) |
| L_CEDAR_103 | 1 | B012 (Marcus & Dana Cole) |
| L_WILLOW_109 | 1 | B016 (Victor Chen) |

See each profile's `test_purpose` for the intent behind its rejection.

## Notes

- **B001–B004 are untouched** by the generator; it keeps them verbatim and only
  (re)generates B005+, so re-running `src/generate_profiles.py` is idempotent.
- Every generated profile carries a `test_purpose` beginning with
  `AUTO-GENERATED (Task 4).` so hand-designed and generated profiles are always
  distinguishable.
