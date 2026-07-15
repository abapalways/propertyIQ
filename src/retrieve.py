"""Task 7: retrieval over the ChromaDB corpus.

Embeds a query and similarity-searches the persistent Chroma store built by
src/ingest.py, returning the top-k chunks. `retrieve()` is reused by
src/prototype.py.

Run (self-judging test on B001 Torres Family's exact query):
    python src/retrieve.py

Writes docs/evidence/task7_retrieval_test.md with the query, the full text of
the top-3 chunks, and a correct/incorrect judgment (L_PINE_101 must be top-3;
L_CEDAR_103 over-budget and L_WILLOW_109 wrong-city must not rank above it).
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
COLLECTION_NAME = "propertyiq_corpus"
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

B001_QUERY = "3-bed homes under $450K near good schools in Austin"


def _require_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key or "your-openai-api-key" in key:
        raise SystemExit(
            "OPENAI_API_KEY not configured. Add it to .env, run `python src/ingest.py`, "
            "then re-run this script."
        )
    return key


def retrieve(query: str, k: int = 3):
    """Return the top-k corpus chunks for `query` as a list of dicts:
    {id, document, metadata, distance}, best match first."""
    key = _require_key()

    import chromadb
    from langchain_openai import OpenAIEmbeddings

    embedder = OpenAIEmbeddings(model=EMBED_MODEL, api_key=key)
    qvec = embedder.embed_query(query)

    db_path = str((ROOT / CHROMA_DB_DIR).resolve())
    client = chromadb.PersistentClient(path=db_path)
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise SystemExit(
            f"Collection '{COLLECTION_NAME}' not found in {db_path}. "
            f"Run `python src/ingest.py` first. ({exc})"
        )

    k = min(k, collection.count())
    res = collection.query(query_embeddings=[qvec], n_results=k)
    out = []
    for i in range(len(res["ids"][0])):
        out.append({
            "id": res["ids"][0][i],
            "document": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i],
        })
    return out


def main() -> int:
    _require_key()

    import chromadb
    client = chromadb.PersistentClient(path=str((ROOT / CHROMA_DB_DIR).resolve()))
    total = client.get_collection(COLLECTION_NAME).count()

    # Full ranking so we can spot-check where the trap listings land.
    full = retrieve(B001_QUERY, k=total)
    ranked_ids = [r["id"] for r in full]
    top3 = full[:3]

    def rank_of(cid):
        return ranked_ids.index(cid) + 1 if cid in ranked_ids else None

    pine_rank = rank_of("L_PINE_101")
    cedar_rank = rank_of("L_CEDAR_103")
    willow_rank = rank_of("L_WILLOW_109")

    pine_in_top3 = pine_rank is not None and pine_rank <= 3
    cedar_ok = cedar_rank is None or (pine_rank is not None and cedar_rank > pine_rank)
    willow_ok = willow_rank is None or (pine_rank is not None and willow_rank > pine_rank)
    verdict = "CORRECT" if (pine_in_top3 and cedar_ok and willow_ok) else "INCORRECT"

    print(f"Query: {B001_QUERY}\n")
    print("Top-3 retrieved chunk IDs:", [r["id"] for r in top3])
    print(f"L_PINE_101 rank: {pine_rank} | L_CEDAR_103 rank: {cedar_rank} | "
          f"L_WILLOW_109 rank: {willow_rank}")
    print(f"JUDGMENT: {verdict}")

    def block(r):
        return (
            f"### Rank {ranked_ids.index(r['id']) + 1}: {r['id']} "
            f"(distance {r['distance']:.4f}, source {r['metadata']['source']})\n\n"
            f"```\n{r['document']}\n```\n"
        )

    md = f"""# Task 7 — Retrieval Test

**Query (B001 Torres Family's exact query):** `{B001_QUERY}`

Retrieved from the persistent ChromaDB store (`{CHROMA_DB_DIR}`, collection
`{COLLECTION_NAME}`, {total} chunks) via OpenAI embeddings (`{EMBED_MODEL}`).

## Top-3 retrieved chunks (full text)

{chr(10).join(block(r) for r in top3)}

## Spot-check ranks

- **L_PINE_101** (B001's perfect match): rank **{pine_rank}**
- **L_CEDAR_103** ($510K, over budget): rank **{cedar_rank}**
- **L_WILLOW_109** (Round Rock, wrong city): rank **{willow_rank}**

## Judgment: {verdict}

- L_PINE_101 in top 3: **{pine_in_top3}**
- L_CEDAR_103 does NOT rank above L_PINE_101: **{cedar_ok}**
- L_WILLOW_109 does NOT rank above L_PINE_101: **{willow_ok}**
"""
    evidence = ROOT / "docs" / "evidence" / "task7_retrieval_test.md"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(md)
    print(f"\nWrote {evidence.relative_to(ROOT)}")

    if verdict != "CORRECT":
        print("\nRetrieval FAILED the acceptance check. Fix chunking/embedding in "
              "src/ingest.py before proceeding (do not move on with broken retrieval).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
