# Task 7 — Retrieval Test

> **STATUS: PENDING LIVE RUN.** This test embeds a query and searches ChromaDB,
> which requires an `OPENAI_API_KEY` and a populated store from `src/ingest.py`.
> No usable key was available when the code was written ("write code now, run
> later"). This file is a placeholder describing what will be captured; the
> harness `src/retrieve.py` overwrites it with the real result and judgment.
>
> To generate the real result:
>
> ```
> # with a valid OPENAI_API_KEY in .env:
> python src/ingest.py          # build the store
> python src/retrieve.py        # run the B001 query + write this file
> ```

## Query (B001 Torres Family's exact query)

`3-bed homes under $450K near good schools in Austin`

## Acceptance criteria (auto-checked by src/retrieve.py)

- **L_PINE_101 MUST appear in the top 3.** It is B001's perfect match ($439K,
  3-bed, top-rated 78745 schools, Austin) per `buyer_profiles.json`.
- **L_CEDAR_103** ($510K, over budget) must **not** rank above L_PINE_101.
- **L_WILLOW_109** (Round Rock, wrong city) must **not** rank above L_PINE_101.

The script computes each listing's rank, prints the top-3 chunk IDs and full
chunk text, and writes a `CORRECT`/`INCORRECT` judgment here. If the judgment is
`INCORRECT`, `src/retrieve.py` exits non-zero — chunking/embedding in
`src/ingest.py` must be fixed before proceeding (per the task instruction not to
move on with broken retrieval).

_Note: the semantic query embeds bedrooms, budget, schools, and the city
"Austin"; L_PINE_101's chunk states all four, while L_CEDAR_103 is over budget
and L_WILLOW_109 is explicitly in Round Rock, so both should embed as weaker
matches for this query._
