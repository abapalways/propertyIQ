# PropertyIQ Listings Corpus

> **SYNTHETIC DATA.** All 10 listings below are hand-designed for testing the
> PropertyIQ prototype. Prices, addresses, schools, and features are invented.
> Each listing is a deliberate boundary or trap case relative to the buyer
> profiles in `../buyer_profiles.json`. See the "Key Features & Context"
> section of each for the specific trap it encodes. Do not treat as real
> market data. See `SOURCES.md`.

---

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

---

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

---

## L_MAPLE_105 — 755 Maple Rd, Austin, TX 78758

- **Price:** $425,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,540
- **Garage:** No (street parking only)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Maple Rd area (78758)
- **School district:** Austin ISD — assigned schools rated 6–7/10

### Key Features & Context
**Trap: missing must-have (garage).** Affordable ($425K, under budget), correct
bedroom count, and in Austin — so it passes a naive price/beds/city filter. But
it has **no garage**, which disqualifies it for B002 and B003 (garage is an
explicit must-have). Verifies that must-have filtering is applied, not just
budget and bedrooms.

---

## L_OAK_106 — 3320 Oak Bend Dr, Austin, TX 78745

- **Price:** $448,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,700
- **Garage:** Yes (2-car attached)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Pinecrest area (78745)
- **School district:** Austin ISD — assigned schools rated 8/10

### Key Features & Context
A strong **secondary match** in the same well-rated 78745 area as L_PINE_101,
with a garage and good schools, but $9K more expensive and slightly smaller lot.
Designed to sit just below L_PINE_101 in a ranked shortlist for B001 — close
enough to be a legitimate #2, not a trap. Confirms the shortlist can rank
multiple genuine matches sensibly.

---

## L_WALNUT_107 — 6011 Walnut Creek Blvd, Austin, TX 78753

- **Price:** $399,000
- **Bedrooms:** 4
- **Bathrooms:** 2
- **Square feet:** 1,920
- **Garage:** Yes (2-car)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Walnut Creek area (78753)
- **School district:** Austin ISD — assigned schools rated 4–5/10

### Key Features & Context
**Trap: school-district variation.** The cheapest listing ($399K) with the most
bedrooms (4) and a garage — very tempting on price and space. But its assigned
schools are **rated 4–5/10**, so it fails the "good school district" must-have
for B001 and B003. Verifies that "good schools" is evaluated on the
neighborhood's rating, not assumed from the Austin address.

---

## L_PECAN_108 — 210 Pecan Grove Way, Austin, TX 78746

- **Price:** $445,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,600
- **Garage:** Yes (2-car)
- **HOA:** $350/month
- **City:** Austin
- **Neighborhood:** Pecan Grove area (78746)
- **School district:** Eanes ISD — assigned schools rated 9–10/10

### Key Features & Context
**Trap: HOA disqualifier + budget-boundary (just under).** Top-rated Eanes ISD
schools (9–10/10), a garage, and priced at **$445K — just under the $450K
ceiling**, so it passes price for B001/B002. But it carries a **$350/month HOA**
that materially changes affordability and is a common dealbreaker for
first-time buyers. Surface the HOA prominently; do not present the $445K price
as the full monthly cost.

---

## L_WILLOW_109 — 1450 Willow Bend Dr, Round Rock, TX 78664

- **Price:** $415,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,810
- **Garage:** Yes (2-car)
- **HOA:** $45/month
- **City:** Round Rock
- **Neighborhood:** Round Rock (78664)
- **School district:** Round Rock ISD — assigned schools rated 8–9/10

### Key Features & Context
**Trap: geography mismatch.** Under budget ($415K), 3-bed, garage, and good
Round Rock ISD schools — it looks great on every attribute EXCEPT location. It
is in **Round Rock, not Austin**, so it fails the `preferred_city = Austin`
criterion for B001–B004. It must NOT rank above L_PINE_101 for the Torres
Family. Verifies the agent respects city/geography and does not treat "greater
Austin metro" as equivalent to Austin.

---

## L_BIRCH_110 — 88 Birch Hollow Ct, Austin, TX 78753

- **Price:** $380,000
- **Bedrooms:** 2
- **Bathrooms:** 1
- **Square feet:** 1,120
- **Garage:** Yes (1-car)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Walnut Creek area (78753)
- **School district:** Austin ISD — assigned schools rated 5/10

### Key Features & Context
**Trap: bedroom count below minimum.** The cheapest listing overall ($380K) in
Austin with a garage — attractive on price — but it has only **2 bedrooms**,
below the `min_bedrooms = 3` floor for all current profiles. Verifies the
minimum-bedroom filter is enforced and cheap-but-too-small listings are not
surfaced as matches.

---

## L_ELM_124 — 4020 Elm Street, Austin, TX 78745

- **Price:** $435,000
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Square feet:** 1,760
- **Garage:** Yes (2-car attached)
- **HOA:** None
- **City:** Austin
- **Neighborhood:** Pinecrest area (78745)
- **School district:** Austin ISD — assigned schools rated 8/10

### Key Features & Context
**Trap: already-rejected match (memory recall).** On paper this is a near-clone
of L_PINE_101 — 3-bed, $435K (under budget), garage, good 78745 schools, Austin
— so it **would otherwise be a top match for B001**. But the Torres Family has
already passed on it (see `buyer_profiles.json`, B001 `rejected_listings`
contains `L_ELM_124`; cf. requirements.md sample query #4, "the house on Elm
Street"). The agent must NOT resurface it for B001 in this or a later session.
Verifies rejection memory overrides a strong criteria match.

---

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
