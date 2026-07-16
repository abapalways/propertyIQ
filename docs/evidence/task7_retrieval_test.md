# Task 7 — Retrieval Test (Ollama / nomic-embed-text)

**Query (B001 Torres Family's exact query):** `3-bed homes under $450K near good schools in Austin`

Retrieved from the persistent ChromaDB store (`chroma_db`, collection
`propertyiq_corpus`, 16 chunks) via OllamaEmbeddings
(`nomic-embed-text`).

## Top-3 retrieved chunks (full text)

### Rank 1: L_PINE_101 (distance 0.5201, source listings_corpus.md)

```
## L_PINE_101 — 4212 Pinecrest Ln, Austin, TX 78745

- **Price:** $439,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,780
- **Garage:** Yes (2-car attached)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Pinecrest area (78745)
- **School district:** Austin ISD — assigned schools rated 8–9/10

### Key Features & Context
The intended **perfect match for B001 (Torres Family)**: a 3-bedroom in Austin,
under the $450K ceiling, with a 2-car garage and highly-rated assigned schools.
Move-in ready, no HOA, single owner. This is the listing that should rank #1 for
the Torres Family's core query ("3-bed homes under $450K near good schools in
Austin"). No trap here — it is the clean positive case every other listing is
designed to be compared against.
```

### Rank 2: L_ASPEN_112 (distance 0.5518, source listings_corpus.md)

```
## L_ASPEN_112 — 9 Aspen Ridge, Austin, TX 78746

- **Price:** $498,000
- **Bedrooms:** 4
- **Bathrooms:** 3
- **Square feet:** 2,240
- **Garage:** Yes (2-car attached)
- **HOA:** $120/month
- **City:** Austin
- **Neighborhood:** Pecan Grove area (78746)
- **School district:** Eanes ISD — assigned schools rated 9–10/10

### Key Features & Context
**Higher-budget match for B004.** A larger 4-bed in top-rated Eanes ISD, priced
at **$498K — just under B004's $500K ceiling** but over B001/B002/B003's lower
ceilings. Safe, well-regarded neighborhood (see `neighborhood_data.md`, 78746).
Serves as a legitimate match for B004's higher budget and "safe neighborhood /
good schools" must-haves, while remaining out of reach for the sub-$460K
buyers. Confirms budget bands separate the buyer pool correctly.
```

### Rank 3: L_CEDAR_103 (distance 0.5541, source listings_corpus.md)

```
## L_CEDAR_103 — 1908 Cedar Ave, Austin, TX 78704

- **Price:** $510,000
- **Bedrooms:** 3
- **Bathrooms:** 2.5
- **Square feet:** 1,650
- **Garage:** Yes (1-car)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Cedar Ave area (78704)
- **School district:** Austin ISD — assigned schools rated 7–8/10

### Key Features & Context
**Trap: budget boundary.** Attractive, walkable 78704 location with good
schools and a garage — but priced at **$510,000, which is over the $450K
ceiling** for B001 and B002. It should be excluded or ranked below in-budget
options for those buyers. It is also $10K over B004's $500K budget, making it an
over-budget case for every current profile. Do not surface it as affordable
without flagging the overage.
```


## Spot-check ranks (over the full 16-chunk ranking)

- **L_PINE_101** (B001's perfect match): rank **1**
- **L_CEDAR_103** ($510K, over budget): rank **3**
- **L_WILLOW_109** (Round Rock, wrong city): rank **7**

## Judgment: CORRECT

- L_PINE_101 in top 3: **True**
- L_CEDAR_103 does NOT rank above L_PINE_101: **True**
- L_WILLOW_109 does NOT rank above L_PINE_101: **True**

_Embedding model note: this run uses `nomic-embed-text` (768-dim). Chunking is
one whole section per listing (unchanged from the OpenAI-embedding setup); no
chunking change was needed for L_PINE_101 to rank in the top 3._
