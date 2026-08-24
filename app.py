"""
app.py — FastAPI wrapper around the RAG pipeline in rag.py.

Turns the local RAG script into an HTTP service (Week 3 of the project):
  GET  /health                  -> {"status": "ok"}          (used by load balancers)
  POST /ask   {"question": ...} -> {"answer": ..., "sources": [...]}

Importing rag builds the FAISS index ONCE at startup (module-level code in rag.py),
so each /ask request just embeds the question and retrieves — fast.

Run locally:
  uvicorn app:app --reload
  open http://127.0.0.1:8000/docs   (interactive Swagger UI — try /ask there)
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field

from rag import answer  # side effect: loads KB + builds the FAISS index at import time

app = FastAPI(
    title="Support Triage / RAG Assistant",
    description="Ask questions grounded in the kb/ knowledge base.",
    version="1.0.0",
)


class Ask(BaseModel):
    question: str = Field(..., min_length=1, examples=["Difference between Multi-AZ and read replicas?"])


class Answer(BaseModel):
    answer: str


@app.get("/health")
def health():
    """Liveness probe — the ALB/ECS health check hits this."""
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
def ask(body: Ask):
    """Retrieve relevant KB docs and answer the question with Claude."""
    return {"answer": answer(body.question)}
