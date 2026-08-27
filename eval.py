"""
eval.py — measure the RAG service's answer quality with an LLM-as-judge.

For each question in evals/eval_set.json:
  1. Get the RAG answer (reuses rag.py's answer() — the SAME pipeline the service uses).
  2. Ask a judge model to score it against the reference answer:
       - score 1-5  (correctness vs the reference)
       - grounded   (true if supported by context / not hallucinated)
  3. Print a per-question result and an overall summary (pass rate + average score).

Run:  python eval.py
"""
import json
import sys
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

from rag import answer, retrieve, chunk_ids  # reuse the exact pipeline the deployed service uses

sys.stdout.reconfigure(encoding="utf-8")

JUDGE_MODEL = "claude-sonnet-4-6"
PASS_SCORE = 4  # a case passes if score >= 4 AND it's grounded

client = anthropic.Anthropic()


class Verdict(BaseModel):
    score: int = Field(..., ge=1, le=5, description="1-5, how well the answer matches the reference")
    grounded: bool = Field(..., description="True if factually supported / not hallucinated")
    reasoning: str


JUDGE_PROMPT = """You are grading a RAG system's answer. Be strict and objective.

QUESTION:
{question}

REFERENCE ANSWER (ground truth):
{reference}

SYSTEM'S ANSWER:
{answer}

Grade it:
- score (1-5): correctness/completeness vs the reference. 5 = fully correct, 1 = wrong/irrelevant.
- grounded (true/false): true if factually supported and not hallucinated.
  Special case: if the reference says the topic is OUT OF SCOPE, then a system answer that
  declines or says it lacks context should be grounded=true with score 5; a fabricated answer
  should be grounded=false with a low score.
- reasoning: one short sentence.
"""


def judge(question: str, reference: str, ans: str) -> Verdict:
    resp = client.messages.parse(
        model=JUDGE_MODEL,
        max_tokens=512,
        temperature=0,  # deterministic grading
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            question=question, reference=reference, answer=ans)}],
        output_format=Verdict,
    )
    return resp.parsed_output


def source_recall(expected, retrieved_sources):
    """Fraction of expected source DOCS retrieved (coarse). None = out-of-scope."""
    if not expected:
        return None
    return len(set(expected) & set(retrieved_sources)) / len(set(expected))


def chunk_recall(expected_chunks, retrieved_ids):
    """Fraction of expected CHUNKS (section-level) retrieved. None = out-of-scope.
    An expected label like 'rds-aurora.md::Amazon Aurora' matches a retrieved chunk id
    by prefix, so labels stay stable even if the real heading has a trailing '(...)'."""
    if not expected_chunks:
        return None
    hit = sum(1 for e in expected_chunks if any(cid.startswith(e) for cid in retrieved_ids))
    return hit / len(expected_chunks)


def main():
    eval_set = json.loads(
        (Path(__file__).parent / "evals" / "eval_set.json").read_text(encoding="utf-8"))

    results, doc_recalls, chunk_recalls = [], [], []
    for case in eval_set:
        # Measure retrieval on its own, at BOTH doc level and chunk level.
        hits = retrieve(case["question"])
        retrieved_sources = [src for _, src, _ in hits]
        retrieved_ids = [chunk_ids[i] for i, _, _ in hits]
        dr = source_recall(case.get("expected_sources", []), retrieved_sources)
        cr = chunk_recall(case.get("expected_chunks", []), retrieved_ids)
        if dr is not None:
            doc_recalls.append(dr)
        if cr is not None:
            chunk_recalls.append(cr)

        # Then the full answer + judge (end-to-end quality). show=False keeps the eval output clean.
        ans = answer(case["question"], show=False)
        v = judge(case["question"], case["reference"], ans)
        passed = v.score >= PASS_SCORE and v.grounded
        results.append((case["id"], v, passed))

        mark = "PASS" if passed else "FAIL"
        d = "n/a" if dr is None else f"{dr:.2f}"
        c = "n/a" if cr is None else f"{cr:.2f}"
        print(f"\n[{mark}] {case['id']}  (score={v.score}, doc_recall={d}, chunk_recall={c})")
        print(f"       judge: {v.reasoning}")

    n = len(results)
    passes = sum(1 for _, _, p in results if p)
    avg = sum(v.score for _, v, _ in results) / n
    avg_dr = sum(doc_recalls) / len(doc_recalls) if doc_recalls else 0.0
    avg_cr = sum(chunk_recalls) / len(chunk_recalls) if chunk_recalls else 0.0
    print("\n" + "=" * 60)
    print(f"PASS RATE          : {passes}/{n}  ({round(100 * passes / n)}%)")
    print(f"AVG SCORE          : {avg:.2f} / 5")
    print(f"DOC-LEVEL RECALL   : {avg_dr:.2f}   (right file retrieved)")
    print(f"CHUNK-LEVEL RECALL : {avg_cr:.2f}   (right section retrieved)")
    print("=" * 60)


if __name__ == "__main__":
    main()
