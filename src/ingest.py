"""Task 6: RAG ingestion pipeline (Ollama / nomic-embed-text).

Chunks data/corpus/*.md by markdown section (one chunk per `## ` heading), so a
single listing's "Key Features & Context" is never split across chunks and each
listing / neighborhood is retrieved whole and coherent. Embeds each chunk with
OllamaEmbeddings (nomic-embed-text via langchain-ollama) and writes them to a
persistent ChromaDB store at CHROMA_DB_DIR (default ./chroma_db).

Run:
    python src/ingest.py            # embed + persist (needs Ollama running)
    python src/ingest.py --dry-run  # chunk + report counts only, no embed/write

Prints the final chunk count and embedding count.
"""

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import llm  # noqa: E402  (shared Ollama wiring; also loads .env)

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "data" / "corpus"
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
COLLECTION_NAME = "propertyiq_corpus"

# Files that are metadata about the corpus, not corpus content to index.
SKIP_FILES = {"SOURCES.md"}

LISTING_ID_RE = re.compile(r"\b(L_[A-Z]+_\d+)\b")


def split_sections(text: str):
    """Split markdown into one section per level-2 (`## `) heading.

    Everything from a `## ` line up to (but not including) the next `## ` line
    is one section, including its full body. Content before the first `## `
    (the `# ` title and the synthetic-data blockquote) is dropped.
    """
    sections = []
    current = None
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            if current is not None:
                sections.append(current)
            current = line
        elif current is not None:
            current += line
    if current is not None:
        sections.append(current)

    cleaned = []
    for s in sections:
        s = re.sub(r"\n-{3,}\s*$", "", s).strip()  # drop trailing --- separators
        if s:
            cleaned.append(s)
    return cleaned


def build_chunks():
    """Return (ids, documents, metadatas) for every corpus section."""
    ids, documents, metadatas = [], [], []
    for md in sorted(CORPUS_DIR.glob("*.md")):
        if md.name in SKIP_FILES:
            continue
        for section in split_sections(md.read_text()):
            heading = section.splitlines()[0].lstrip("# ").strip()
            m = LISTING_ID_RE.search(heading)
            if m:
                cid = m.group(1)
                section_type = "listing"
            else:
                cid = re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")
                section_type = "neighborhood" if md.name == "neighborhood_data.md" else "other"
            ids.append(cid)
            documents.append(section)
            metadatas.append({
                "source": md.name,
                "section_title": heading,
                "section_type": section_type,
            })
    return ids, documents, metadatas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Chunk and report counts only; no embeddings, no DB write.")
    args = parser.parse_args()

    ids, documents, metadatas = build_chunks()
    chunk_count = len(documents)
    print(f"Corpus files: {[p.name for p in sorted(CORPUS_DIR.glob('*.md')) if p.name not in SKIP_FILES]}")
    print(f"Chunked into {chunk_count} sections (1 per listing/neighborhood):")
    for cid, md in zip(ids, metadatas):
        print(f"  - {cid}  [{md['section_type']}]  ({md['source']})")

    if args.dry_run:
        print(f"\n[dry-run] Final chunk count: {chunk_count}")
        print("[dry-run] No embeddings computed and nothing written.")
        return 0

    try:
        llm.check_ollama()
    except llm.OllamaUnavailable as exc:
        print(f"\nERROR: {exc}")
        return 1

    print(f"\nEmbedding {chunk_count} chunks with '{llm.OLLAMA_EMBED_MODEL}' "
          f"@ {llm.OLLAMA_BASE_URL} ...")
    embedder = llm.make_embeddings()
    vectors = embedder.embed_documents(documents)
    embedding_count = len(vectors)
    dim = len(vectors[0]) if vectors else 0

    import chromadb
    db_path = str((ROOT / CHROMA_DB_DIR).resolve())
    print(f"Writing to persistent ChromaDB at {db_path} (collection '{COLLECTION_NAME}') ...")
    client = chromadb.PersistentClient(path=db_path)
    try:
        client.delete_collection(COLLECTION_NAME)  # rebuild -> idempotent re-ingest
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(ids=ids, embeddings=vectors, documents=documents, metadatas=metadatas)

    stored = collection.count()
    print("\n=== Ingestion complete ===")
    print(f"Embedding model:       {llm.OLLAMA_EMBED_MODEL} (dim {dim})")
    print(f"Final chunk count:     {chunk_count}")
    print(f"Embedding count:       {embedding_count}")
    print(f"Stored in collection:  {stored}")
    if not (chunk_count == embedding_count == stored):
        print("WARNING: chunk / embedding / stored counts do not match!")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
