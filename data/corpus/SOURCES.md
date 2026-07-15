# RAG Corpus — Sources & Provenance

## Provenance

Both files in this corpus are **synthetic**, hand-generated for the PropertyIQ
project. They do not come from any live MLS, listings API, crime database, or
other external source. No proprietary or scraped data is included.

| File | Contents | Status |
|---|---|---|
| `listings_corpus.md` | 10 property listings (L_PINE_101 … L_ASPEN_112) | Synthetic — hand-designed boundary/trap cases |
| `neighborhood_data.md` | Safety/crime summaries for 6 neighborhoods | Synthetic — invented figures vs. a synthetic metro baseline |

Prices, addresses, school ratings, HOA fees, and crime rates are all invented to
exercise the buyer profiles in `../buyer_profiles.json`. They must never be
presented to a user as real market or public-safety statistics.

## Sample-query coverage verification

For each of the six sample queries in `requirements.md` §3, confirmation that
the corpus contains content that could answer it:

| # | Query (paraphrased) | Corpus content that answers it | Covered? |
|---|---|---|---|
| 1 | 3-bed homes under $450K near good schools in [city] | `listings_corpus.md` — every listing has bedrooms, price, city, and a school-district rating, so matches can be retrieved and ranked (e.g. L_PINE_101). | ✅ Yes (RAG) |
| 2 | Monthly payment with 10% down at current rates | Numeric answer comes from the **mortgage tool** (not yet built), but the corpus supplies the required **listing price** input for every listing. | ⚠️ Inputs in corpus; figure requires the mortgage tool |
| 3 | Is this listing priced fairly vs. nearby homes? | Numeric comps come from the **comps tool** (not yet built), but the corpus supplies **price and square footage** for all 10 listings, enough to compute price/sqft comparisons. | ⚠️ Inputs in corpus; assessment requires the comps tool |
| 4 | We passed on the house on Elm Street — don't show it | `listings_corpus.md` contains **L_ELM_124 (4020 Elm Street)**; the rejection lives in `buyer_profiles.json` (B001). Both pieces exist to satisfy rejection recall. | ✅ Yes (RAG + memory) |
| 5 | Only show neighborhoods with fewer immigrant families | **Correctly NOT answerable:** the corpus deliberately contains **no demographic data** to filter on. This query must be refused per fair-housing rules — the absence of such data is intentional. | ✅ Yes (by refusal; no such data exists) |
| 6 | What's the crime rate like in this neighborhood? | `neighborhood_data.md` — property/violent crime rates and a metro-baseline comparison for all 6 neighborhoods referenced by the listings. | ✅ Yes (RAG) |

**Summary:** Queries 1, 4, 5, and 6 are fully supported by the RAG corpus (with
#5 supported by the deliberate *absence* of demographic data). Queries 2 and 3
need the mortgage/comps tools that are out of scope for the week-1 RAG
prototype, but the corpus already carries the numeric inputs (prices, square
footage) those tools will consume.
