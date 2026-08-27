"""
rag.py — a minimal Retrieval-Augmented Generation service over the AWS KB docs.

Pipeline:
  1. Load every .md in kb/ as a document.
  2. Embed them locally with sentence-transformers (free, no API cost).
  3. Index the embeddings with FAISS for fast similarity search.
  4. On a question: embed it, retrieve the top-k most similar docs,
     hand them to Claude as context, and get a grounded answer.

Run:  python rag.py
Then type questions at the prompt (e.g. "difference between multi-az and read replicas?").
"""

import os
import sys
from pathlib import Path

import anthropic
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Windows consoles default to cp1252, which can't print em-dashes/arrows that
# Claude may return. Force UTF-8 so answers print cleanly.
sys.stdout.reconfigure(encoding="utf-8")

# --- 1. Load the knowledge base and split into CHUNKS ---------------------------
# Instead of embedding each whole file as one coarse vector, we split every doc into
# section-level chunks (one per "## " heading, plus the intro). Each chunk is prefixed
# with its doc title so it stays self-contained and embeds with topic context.
KB_DIR = Path(__file__).parent / "kb"
doc_paths = [p for p in KB_DIR.glob("*.md") if p.name != "README.md"]


def split_markdown(text: str):
    """Split a markdown doc into (heading, section_text) pairs — the intro plus one
    chunk per '## ' section. heading is 'intro' for content before the first '## '."""
    sections, heading, current = [], "intro", []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections.append((heading, "\n".join(current).strip()))
            heading = line[3:].strip()
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append((heading, "\n".join(current).strip()))
    return [(h, t) for h, t in sections if t]


# Parallel lists: chunk text (embedded + fed to the LLM), source file, and a stable
# chunk id "file::heading" used to evaluate retrieval at the section level.
chunk_texts, chunk_sources, chunk_ids = [], [], []
for path in doc_paths:
    text = path.read_text(encoding="utf-8")
    title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), path.stem)
    for heading, section in split_markdown(text):
        chunk_texts.append(f"[{title}]\n{section}")   # title prefix = topic context per chunk
        chunk_sources.append(path.name)
        chunk_ids.append(f"{path.name}::{heading}")
print(f"Loaded {len(doc_paths)} docs -> {len(chunk_texts)} chunks from {KB_DIR}")

# --- 2. Embed locally + 3. Build the FAISS index --------------------------------
# Vectors are L2-normalized, so inner product == cosine similarity (~0-1, higher = closer).
print("Embedding chunks (first run downloads the model, ~90 MB)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vecs = embedder.encode(chunk_texts, convert_to_numpy=True, normalize_embeddings=True)
index = faiss.IndexFlatIP(chunk_vecs.shape[1])
index.add(chunk_vecs)

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


# --- 4. Retrieve + answer -------------------------------------------------------
# Only keep retrieved docs whose cosine similarity clears this floor. Weak matches
# (an off-topic question) get dropped so we don't feed Claude irrelevant context.
MIN_SCORE = 0.25

# How many docs to retrieve per query. Configurable via env var so we can test retrieval
# sensitivity (e.g. RAG_TOP_K=1 starves multi-hop questions) without changing code. Default 3.
TOP_K = int(os.environ.get("RAG_TOP_K", "3"))


def retrieve(question: str, k: int = TOP_K):
    """Retrieve the top-k chunks above the relevance floor.
    Returns a list of (chunk_index, source_filename, score) — retrieval only, no LLM.
    Kept separate from answer() so it can be evaluated on its own (retrieval recall)."""
    q_vec = embedder.encode([question], convert_to_numpy=True, normalize_embeddings=True)
    scores, idx = index.search(q_vec, k)
    return [(int(i), chunk_sources[i], float(s))
            for i, s in zip(idx[0], scores[0]) if s >= MIN_SCORE]


def answer(question: str, k: int = TOP_K, show: bool = True) -> str:
    hits = retrieve(question, k)
    if not hits:
        return "No KB document is relevant enough to answer this confidently."

    if show:  # interactive CLI prints what was retrieved; the eval suppresses it for clean output
        print("  retrieved:")
        for _, src, s in hits:
            print(f"    {s:.3f}  {src}")
    context = "\n\n---\n\n".join(chunk_texts[i] for i, _, _ in hits)

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Answer the question using ONLY the context below. "
                       f"If the context doesn't cover it, say so.\n\n"
                       f"CONTEXT:\n{context}\n\nQUESTION: {question}",
        }],
    )
    return next(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    print("\nAsk a question about AWS (or press Enter to quit).\n")
    while True:
        q = input("Q: ").strip()
        if not q:
            break
        print(f"\nA: {answer(q)}\n")
