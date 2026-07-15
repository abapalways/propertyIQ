# PropertyIQ — Team

## Members & Responsibilities

All three of us are **developers with shared responsibility across every area** of
the project. There are no single-owner silos — anyone can pick up and work in any
area, and we review each other's work across boundaries.

| Member | Role | Areas |
|---|---|---|
| Haritha K | Developer **+ Lead** | RAG, tools/MCP, memory, guardrails/caching, observability/UI |
| Shree | Developer | RAG, tools/MCP, memory, guardrails/caching, observability/UI |
| Avanish | Developer | RAG, tools/MCP, memory, guardrails/caching, observability/UI |

### Work areas (everyone can work in any of these)
- **RAG** — listing/neighborhood indexing and retrieval over ChromaDB.
- **Tools / MCP** — mortgage-payment calculator and comparable-sales (comps) lookup.
- **Memory** — persisting buyer must-haves and rejected listings across sessions.
- **Guardrails / Caching** — fair-housing refusals, no-fabrication rules, response caching.
- **Observability / UI** — LangSmith tracing, filter audit logging, and the Gradio UI.

### Lead role — Haritha K
"Lead" means **coordination, final calls on architecture, and unblocking the team** —
not a separate technical lane. Specifically, Haritha K owns:
- **Coordination** — planning, task tracking, keeping work areas in sync.
- **Architecture decisions** — the final call when the team needs one.
- **Removing blockers** — unsticking anyone who is stuck.

## Tech Stack

| Concern | Choice |
|---|---|
| Language | Python |
| Agent / orchestration framework | LangChain |
| Vector store (RAG) | ChromaDB |
| Observability / tracing | LangSmith |
| UI | Gradio |
| LLM provider | OpenAI |
| Source control | GitHub |

## Key Guardrails (from requirements.md §5)

These are non-negotiable and every work area must uphold them:

1. **Fair-housing refusal** — Refuse any search, filter, or recommendation criterion
   based on protected characteristics (race, religion, national origin, familial
   status, disability, etc.). No steering.
2. **No fabricated numbers** — Never fabricate comps, prices, or mortgage figures.
   Every numeric claim must come from a tool call or a cited RAG source. Affordability
   estimates are labeled approximate and not a guaranteed loan offer.
3. **Rejection-memory persistence** — Respect stored buyer rejections/preferences;
   do not resurface explicitly rejected listings across sessions unless the user
   re-requests them.
4. **Filter audit logging** — Observability must log every filter applied to a search
   and flag/reject any filter matching a protected-characteristic pattern, for
   compliance review.

## Sign-off Checklist

Each developer confirms they have read `requirements.md` in full:

- [ ] Haritha K has read requirements.md
- [ ] Shree has read requirements.md
- [ ] Avanish has read requirements.md
