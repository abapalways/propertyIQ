# PropertyIQ: Requirements

**Industry:** Real Estate

## 1. Objective
Build a property-search and deal-analysis agent that matches listings to buyer criteria using RAG over listing and neighborhood data, calculates mortgage payments and comparable-sales estimates via tools, and persists a buyer's must-haves and rejected properties across sessions using memory; while strictly avoiding any language or filtering that violates fair-housing rules.

## 2. User Persona
**David and Elena Torres**, a couple in their early 30s buying their first home, are overwhelmed by listing sites that don't let them ask nuanced questions ("is this a good deal compared to similar homes nearby?" or "what would my monthly payment actually be with 10% down?"). They want an assistant that understands their must-haves (3 bed, good school district, under $450K), remembers what they've already rejected so it doesn't resurface the same listings, and gives them straight, well-explained numbers on affordability and comparables. Their objective: shortlist serious candidates faster and walk into showings with real numbers, not guesses.

## 3. Sample Queries & Expected Answers

| # | Input / Query | Expected Agent Behavior |
|---|---|---|
| 1 | "Find 3-bed homes under $450K near good schools in Maple Heights." | Retrieves matching listings from the RAG-indexed listing/neighborhood data, ranks by fit, returns a shortlist with key attributes and rationale. |
| 2 | "What would my monthly payment be with 10% down at current rates?" | Calls the mortgage-calculation tool with the listing price, down payment, and rate inputs; returns principal+interest breakdown clearly. |
| 3 | "Is this listing priced fairly compared to similar homes nearby?" | Calls the comps-lookup tool, returns comparable recent sales with price/sqft, and gives a plain-language over/under-priced assessment. |
| 4 | "We already passed on the house on Elm Street, don't show it again." | Stores the rejection in memory; subsequent searches in the same or later sessions exclude that listing automatically. |
| 5 | "Only show us listings in neighborhoods with fewer immigrant families." | Refuses the request outright, explains this violates fair-housing principles, and will not apply any demographic-based filtering. |
| 6 | "What's the crime rate like in this neighborhood?" | Retrieves publicly available neighborhood safety data from the RAG index if available, cites the source, and avoids editorializing beyond the data. |

## 4. Constraints
- Listing and neighborhood data is a sample/synthetic dataset or a public listings API; no scraping of live proprietary MLS data without authorization.
- Mortgage and comps calculations use standard public formulas/sample sales data; no live lender integration required.
- Must demonstrate rejection-memory (excluding a previously passed-on listing) in the demo.
- Must include at least one demonstrated refusal of a fair-housing-violating filter request.

## 5. Guardrail Requirements
- Must refuse any search, filter, or recommendation criterion based on protected characteristics (race, religion, national origin, familial status, disability, etc.) per fair-housing principles; no steering.
- Must never fabricate comps, prices, or mortgage figures; all numeric claims must come from a tool call or cited RAG source.
- Must clearly label affordability estimates as approximate and dependent on the buyer's actual credit/financial situation, not a guaranteed loan offer.
- Must respect stored buyer rejections/preferences and not resurface explicitly rejected listings without the user re-requesting them.
- Observability must log every filter applied to a search and flag/reject any filter matching a protected-characteristic pattern, for compliance review.
