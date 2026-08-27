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

# --- 1. Load the knowledge base -------------------------------------------------
KB_DIR = Path(__file__).parent / "kb"
doc_paths = [p for p in KB_DIR.glob("*.md") if p.name != "README.md"]
docs = [p.read_text(encoding="utf-8") for p in doc_paths]
print(f"Loaded {len(docs)} KB documents from {KB_DIR}")

# --- 2. Embed locally + 3. Build the FAISS index --------------------------------
print("Embedding docs (first run downloads the model, ~90 MB)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
doc_vecs = embedder.encode(docs, convert_to_numpy=True, normalize_embeddings=True)
# Vectors are L2-normalized (unit length), so inner product == cosine similarity:
# a score in ~[0, 1] where higher = more similar. This is more interpretable than
# raw L2 distance and is the standard metric for embedding search.
index = faiss.IndexFlatIP(doc_vecs.shape[1])
index.add(doc_vecs)

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


# --- 4. Retrieve + answer -------------------------------------------------------
# Only keep retrieved docs whose cosine similarity clears this floor. Weak matches
# (an off-topic question) get dropped so we don't feed Claude irrelevant context.
MIN_SCORE = 0.25

# How many docs to retrieve per query. Configurable via env var so we can test retrieval
# sensitivity (e.g. RAG_TOP_K=1 starves multi-hop questions) without changing code. Default 3.
TOP_K = int(os.environ.get("RAG_TOP_K", "3"))


def answer(question: str, k: int = TOP_K) -> str:
    q_vec = embedder.encode([question], convert_to_numpy=True, normalize_embeddings=True)
    scores, idx = index.search(q_vec, k)

    # Pair each hit with its score, keep only those above the relevance floor.
    hits = [(doc_paths[i].name, i, s) for i, s in zip(idx[0], scores[0]) if s >= MIN_SCORE]
    if not hits:
        return "No KB document is relevant enough to answer this confidently."

    print("  retrieved:")
    for name, _, s in hits:
        print(f"    {s:.3f}  {name}")
    context = "\n\n---\n\n".join(docs[i] for _, i, _ in hits)

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
