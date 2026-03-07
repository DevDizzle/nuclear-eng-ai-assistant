# ⚛️ Nuclear Engineering AI Assistant

> AI-powered document assistant for nuclear engineering teams. RAG-based Q&A with citations, 10 CFR 50.59 screening drafts, document summarization, and vendor bid comparison.

**⚠️ All AI outputs are PRELIMINARY and require licensed engineer review and approval. This system has zero design authority.**

---

## What It Does

| Feature | Description |
|---------|-------------|
| **Document Q&A** | Ask questions about engineering documents. Get cited answers with source document, page number, and relevant passage. |
| **50.59 Screening** | Generate preliminary 10 CFR 50.59 screening drafts from a modification description. Cross-references UFSAR sections automatically. |
| **Summarization** | Summarize 100+ page engineering packages into executive summaries with section breakdowns and page references. |
| **Bid Comparison** | Compare vendor submittals against engineering specifications. Automated pass/fail flagging. |
| **Audit Trail** | Every interaction logged with timestamps, user ID, documents referenced, and citations generated. |

## Why

Nuclear engineering teams spend thousands of hours annually on document review, regulatory screening, and vendor evaluation. This tool returns that time to high-value engineering judgment by automating the administrative burden — while keeping all technical authority with licensed engineers.

## Architecture

```
Frontend (Next.js) → FastAPI (Cloud Run) → Vertex AI (Gemini + Embeddings)
                                         → Firestore (vectors + sessions)
                                         → BigQuery (audit log)
                                         → Cloud Storage (documents)
                                         → Document AI (OCR)
                                         → ADK (agent orchestration)
```

## Built With

- **Google Cloud Platform** — Vertex AI, BigQuery, Cloud Run, Firestore, Cloud Storage, Document AI
- **Google Agent Development Kit (ADK)** — Agent orchestration
- **Gemini 2.0 Flash / 2.5 Pro** — Generation and reasoning
- **FastAPI** — Backend API
- **Next.js** — Frontend

## Quick Start

```bash
# Clone
git clone https://github.com/DevDizzle/nuclear-eng-ai-assistant.git
cd nuclear-eng-ai-assistant

# Install
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env with your GCP project details

# Run
uvicorn src.main:app --reload --port 8080
```

## Regulatory Context

This tool is designed with awareness of:
- **10 CFR 50.59** — Changes, Tests, and Experiments
- **NEI 96-07 Rev 1** — 50.59 Implementation Guidelines
- **NUREG-2261** — NRC AI Strategic Plan
- **10 CFR 50, Appendix B** — Quality Assurance

All sample documents are sourced from NRC's public ADAMS database.

## License

Apache 2.0

## Author

**Evan Parra** — AI/ML Engineer | [LinkedIn](https://linkedin.com/in/evanparra) | [GitHub](https://github.com/DevDizzle)
