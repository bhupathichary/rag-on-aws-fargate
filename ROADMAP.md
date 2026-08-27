# Roadmap — from demo to production AI

This project started as a working RAG service deployed on AWS Fargate. This roadmap tracks its
evolution toward a **production-grade AI workflow**. Each milestone adds a real production
capability (not a tutorial), measured and documented.

| # | Milestone | Production skill |
|---|-----------|------------------|
| 1 | **Evaluation harness** — labeled question set + LLM-as-judge scoring correctness & groundedness | Evals — measuring AI quality, catching regressions |
| 2 | **Retrieval quality** — chunking, hybrid (keyword + vector) search, reranking; measured with #1 | RAG engineering, data-driven iteration |
| 3 | **Observability** — per-request logging of retrieved docs, latency, tokens, cost; CloudWatch dashboard | Production monitoring for AI |
| 4 | **IaC + CI/CD** — Terraform for the full Fargate stack; GitHub Actions build → eval → deploy | Reproducible production deployment |
| 5 | **Hardening** — Secrets Manager, ALB + HTTPS, private subnets, autoscaling, caching, guardrails, API auth | Production-grade security & reliability |
| 6 | **Agentic patterns** *(stretch)* — tool use, multi-step, streaming | Advanced AI system design |

**Status:** ✅ Base deploy · ✅ Milestone 1 — Evaluation (validated via a retrieval-sensitivity test) · 🚧 Milestone 2 — Retrieval quality
