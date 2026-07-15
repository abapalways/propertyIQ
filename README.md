# PropertyIQ

A property-search and deal-analysis agent for first-time home buyers. PropertyIQ
matches listings to buyer criteria using **RAG** over listing and neighborhood
data, calculates **mortgage payments** and **comparable-sales estimates** via
tools, and **remembers** a buyer's must-haves and rejected properties across
sessions — all while strictly upholding **fair-housing** rules (no filtering or
steering on protected characteristics, and no fabricated numbers).

- 📋 Full spec: [requirements.md](requirements.md)
- 👥 Team & responsibilities: [docs/team.md](docs/team.md)

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

## Quickstart

```bash
# 1. Clone
git clone <your-repo-url> PropertyIQ
cd PropertyIQ

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env               # then edit .env and add your keys

# 5. Run the app
python src/app.py
```

Gradio prints a local URL (e.g. `http://127.0.0.1:7860`) — open it in a browser.
The current app is a **scaffold**: it echoes your messages with an "agent logic
not wired up yet" placeholder. If `OPENAI_API_KEY` is missing it still runs, in
echo-only mode, and tells you the key is not configured.

## Project Structure

```
PropertyIQ/
├── docs/
│   └── team.md            # Team, roles, tech stack, guardrails, sign-off
├── src/
│   └── app.py             # Gradio ChatInterface stub (runnable scaffold)
├── requirements.md        # Product/functional spec
├── requirements.txt       # Python dependencies
├── .env.example           # Template for required environment variables
├── .gitignore
└── README.md
```

## Branch Strategy

- **`main`** — protected and always deployable. No direct pushes; changes land
  only via reviewed pull requests.
- **Feature branches** — one branch per work item, named `feature/<area>`
  (e.g. `feature/rag-pipeline`, `feature/guardrails`).
- **PR + review before merge** — open a pull request into `main`, get at least
  one teammate review, ensure the app still runs, then merge.

Active feature branches:

| Branch | Work item |
|---|---|
| `feature/rag-pipeline` | RAG indexing & retrieval over listings/neighborhoods |
| `feature/mortgage-comps-tools` | Mortgage calculator & comparable-sales tools |
| `feature/memory-store` | Persistent buyer preferences & rejection memory |
| `feature/guardrails` | Fair-housing guardrails & response caching |
| `feature/ui-observability` | Gradio UI & LangSmith observability/audit logging |
