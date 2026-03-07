# SPEC: Nuclear Engineering AI Assistant
## 50.59 Screening & Document Review Platform

### Overview
A production-grade, open-source AI assistant purpose-built for nuclear engineering teams. Enables engineers to upload engineering documents (modification packages, specifications, procedures), ask natural language questions with cited answers, and generate preliminary 10 CFR 50.59 screening drafts. All outputs are clearly labeled as preliminary and require licensed engineer review and approval.

**Repo name:** `nuclear-eng-ai-assistant`
**Stack:** Google Cloud Platform (Vertex AI, Document AI, BigQuery, Cloud Run, Firestore, Cloud Storage, ADK)
**License:** Apache 2.0

---

### Core Principles

1. **ZERO DESIGN AUTHORITY** — Every AI output is labeled "PRELIMINARY — REQUIRES ENGINEER REVIEW AND APPROVAL." This is non-negotiable and must be visible on every generated document, summary, and screening draft.
2. **Full Traceability** — Every answer includes exact source document, page number, and relevant passage. No unsourced claims.
3. **Audit Trail** — Every query, response, and user action is logged with timestamps, user ID, and document references.
4. **Air-Gap Ready** — Architecture designed so the LLM layer can be swapped for on-prem deployment. No hard dependency on external APIs beyond GCP.
5. **Nuclear Regulatory Alignment** — Built with awareness of NRC (NUREG-2261), EPRI, and INPO standards for AI in nuclear.

---

### Features (MVP)

#### 1. Document Ingestion Pipeline
- Upload PDFs (scanned or native) via web UI or API
- Document AI (GCP) for OCR on scanned documents
- Chunking strategy: overlapping chunks (512 tokens, 50 token overlap) preserving section headers and page numbers
- Embedding generation via Vertex AI Embeddings API (text-embedding-005)
- Store embeddings + metadata in Firestore (vector search) or BigQuery vector index
- Store raw documents in Cloud Storage with versioning
- Supported doc types: modification packages, UFSAR sections, engineering calculations, vendor submittals, specifications, procedures

#### 2. RAG-Powered Q&A with Citations
- Natural language query interface
- Retrieval: semantic search over document embeddings, top-k retrieval with reranking
- Generation: Gemini 2.0 Flash (or latest) with retrieved context
- Output format: answer + structured citation table (document name, page number, relevant passage, confidence)
- Support/Refute table format (per EPRI TS-LLM pattern):
  ```
  | Finding | Source Document | Page | Relevant Passage | Assessment |
  |---------|---------------|------|-----------------|------------|
  | ...     | ...           | ...  | ...             | Support/Refute |
  ```
- Follow-up questions supported via conversation memory (Firestore session state)

#### 3. 50.59 Screening Draft Generator
- Input: plain text description of proposed plant modification
- AI searches uploaded UFSAR sections and licensing documents
- Generates preliminary screening document:
  - Applicability determination (does 50.59 apply?)
  - Identification of affected design functions described in UFSAR
  - Cross-references to relevant UFSAR sections with page citations
  - Preliminary answers to the 8 screening criteria questions
  - List of additional documents that should be reviewed
- Output clearly stamped: "PRELIMINARY DRAFT — NOT FOR REGULATORY SUBMISSION — REQUIRES LICENSED ENGINEER REVIEW"
- Export to PDF with formatting matching standard utility screening templates

#### 4. Document Summarization (Map-Reduce)
- Upload a large engineering package (100+ pages)
- Map phase: chunk document, summarize each chunk preserving technical parameters
- Reduce phase: synthesize chunk summaries into executive summary
- Output: key modifications, impacted systems, safety justifications, open items/action items
- Section-by-section breakdown with page references

#### 5. Vendor Bid Comparison
- Upload engineering specification + one or more vendor submittals
- AI extracts key technical parameters from each document
- Side-by-side comparison table: spec requirement vs. vendor proposed value
- Pass/fail flagging against spec thresholds
- Deviation report highlighting non-conformances

---

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                  │
│  - Document upload   - Q&A chat    - 50.59 wizard   │
│  - Bid comparison    - Doc summary - Audit log view  │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────┐
│              Backend (FastAPI on Cloud Run)           │
│  - /api/documents    - /api/query     - /api/screen  │
│  - /api/summarize    - /api/compare   - /api/audit   │
└──┬───────┬───────┬───────┬───────┬──────────────────┘
   │       │       │       │       │
   ▼       ▼       ▼       ▼       ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Doc AI││Vertex││Fire- ││Big   ││Cloud │
│(OCR) ││AI    ││store ││Query ││Storage│
│      ││Gemini││Vector││Audit ││Docs  │
│      ││Embed ││Search││Log   ││Raw   │
└──────┘└──────┘└──────┘└──────┘└──────┘
```

**Agent Layer (ADK):**
- **Retrieval Agent** — handles document search, reranking, citation extraction
- **Screening Agent** — orchestrates 50.59 screening workflow (search UFSAR → identify affected functions → generate screening draft)
- **Summarization Agent** — map-reduce document summarization
- **Comparison Agent** — vendor bid extraction and comparison

---

### Data: Real Nuclear Documents (Publicly Available)

All sourced from NRC's public ADAMS database (https://www.nrc.gov/reading-rm/adams.html) and public regulatory documents:

#### UFSAR Sections (publicly available for decommissioned/reference plants)
- NRC NUREG series documents (design basis references)
- Generic UFSAR chapter templates from NRC regulatory guides

#### Regulatory Documents
- 10 CFR 50.59 full regulatory text
- NEI 96-07 Rev 1 — "Guidelines for 10 CFR 50.59 Implementation" (industry standard guidance)
- NUREG-2261 — NRC AI Strategic Plan
- NRC Regulatory Guides (publicly available)
- NRC Generic Letters and Information Notices

#### Sample Engineering Documents
- NRC inspection reports (contain modification descriptions, findings)
- License Amendment Requests (LAR) — publicly filed, contain engineering justifications
- Safety Evaluation Reports (SERs) — NRC's own analysis of modifications
- Generic Design Control Documents (DCDs) for AP1000, ABWR (publicly available)

#### EPRI Public Resources
- EPRI nuclear AI publications and white papers
- NILLM (Nuclear Industry LLM) public documentation

---

### Project Structure

```
nuclear-eng-ai-assistant/
├── README.md
├── LICENSE (Apache 2.0)
├── pyproject.toml
├── Dockerfile
├── cloudbuild.yaml
├── .github/
│   └── workflows/
│       ├── ci.yaml (lint, type check, test)
│       └── deploy.yaml (Cloud Build → Cloud Run)
├── docs/
│   ├── architecture.md
│   ├── regulatory-context.md
│   └── deployment.md
├── data/
│   ├── regulatory/          # 10 CFR 50.59 text, NEI 96-07, NUREG-2261
│   ├── sample_documents/    # NRC public docs for demo
│   └── templates/           # 50.59 screening templates
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Environment config, GCP project settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── documents.py     # Upload, list, delete documents
│   │   ├── query.py         # RAG Q&A endpoint
│   │   ├── screening.py     # 50.59 screening generator
│   │   ├── summarize.py     # Map-reduce summarization
│   │   └── compare.py       # Vendor bid comparison
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── retrieval.py     # ADK retrieval agent
│   │   ├── screening.py     # ADK 50.59 screening agent
│   │   ├── summarization.py # ADK summarization agent
│   │   └── comparison.py    # ADK comparison agent
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pipeline.py      # Document processing pipeline
│   │   ├── ocr.py           # Document AI integration
│   │   ├── chunker.py       # Overlapping chunk strategy
│   │   └── embedder.py      # Vertex AI embeddings
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── search.py        # Vector search (Firestore/BQ)
│   │   └── reranker.py      # Result reranking
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── gemini.py        # Gemini client wrapper
│   │   ├── citations.py     # Citation extraction and formatting
│   │   └── templates.py     # Prompt templates (50.59, summary, comparison)
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── gcs.py           # Cloud Storage operations
│   │   ├── firestore.py     # Firestore operations (vectors, sessions)
│   │   └── bigquery.py      # BigQuery audit log
│   └── models/
│       ├── __init__.py
│       ├── document.py      # Pydantic models for documents
│       ├── query.py         # Pydantic models for Q&A
│       ├── screening.py     # Pydantic models for 50.59
│       └── audit.py         # Pydantic models for audit trail
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Landing/dashboard
│   │   │   ├── documents/
│   │   │   │   └── page.tsx       # Document management
│   │   │   ├── query/
│   │   │   │   └── page.tsx       # Q&A interface
│   │   │   ├── screening/
│   │   │   │   └── page.tsx       # 50.59 screening wizard
│   │   │   ├── summarize/
│   │   │   │   └── page.tsx       # Document summarization
│   │   │   ├── compare/
│   │   │   │   └── page.tsx       # Vendor bid comparison
│   │   │   └── audit/
│   │   │       └── page.tsx       # Audit log viewer
│   │   └── components/
│   │       ├── CitationTable.tsx
│   │       ├── DocumentUpload.tsx
│   │       ├── ChatInterface.tsx
│   │       ├── ScreeningForm.tsx
│   │       └── PreliminaryBanner.tsx  # "REQUIRES ENGINEER REVIEW" banner
│   └── public/
│       └── nrc-logo.svg
└── tests/
    ├── test_ingestion.py
    ├── test_retrieval.py
    ├── test_screening.py
    └── test_api.py
```

---

### Prompt Templates

#### 50.59 Screening System Prompt
```
You are a nuclear engineering document assistant supporting 10 CFR 50.59 screening workflows. You help engineers determine whether a proposed plant modification requires prior NRC approval.

CRITICAL CONSTRAINTS:
- You have ZERO design authority. All outputs are preliminary drafts.
- Every claim must cite a specific source document and page number.
- If you cannot find a relevant source, say "No relevant source found — requires manual review."
- Never fabricate regulatory references or document citations.
- Never make definitive safety determinations. Use language like "based on the retrieved documentation, this appears to..." or "the following UFSAR sections may be affected..."

Your outputs will be reviewed by a licensed nuclear engineer before any action is taken.
```

#### Q&A System Prompt
```
You are a nuclear engineering document assistant. Answer questions using ONLY the provided document context. For every claim in your answer, provide:
1. The source document name
2. The specific page number
3. The relevant passage

If the provided context does not contain sufficient information to answer the question, say so explicitly. Do not speculate or use knowledge outside the provided documents.

Format citations as: [Source: {document_name}, Page {page_number}]
```

---

### Deployment

#### Local Development
```bash
# Backend
cd nuclear-eng-ai-assistant
pip install -e ".[dev]"
uvicorn src.main:app --reload --port 8080

# Frontend
cd frontend
npm install
npm run dev
```

#### GCP Deployment
```bash
# Deploy backend to Cloud Run
gcloud builds submit --config cloudbuild.yaml

# Deploy frontend to Firebase Hosting or Cloud Run
cd frontend && npm run build
firebase deploy --only hosting
```

---

### Success Metrics (for the interview demo)
1. Upload a 50+ page NRC document → fully indexed in < 60 seconds
2. Ask a technical question → cited answer in < 5 seconds
3. Generate 50.59 screening draft → complete preliminary document in < 30 seconds
4. Every output shows "PRELIMINARY — REQUIRES ENGINEER REVIEW" banner
5. Audit log captures every interaction with timestamps

---

### Why This Wins the Interview
- Built on GCP (NextEra's new partner)
- Addresses the #1 engineering time sink (50.59 screening)
- Uses real NRC public documents, not fake data
- Shows production architecture (Docker, CI/CD, Cloud Run, ADK)
- Respects the prime directive (zero design authority, full traceability)
- Open source — demonstrates thought leadership, not just technical skill
- Scalable from demo to enterprise deployment
