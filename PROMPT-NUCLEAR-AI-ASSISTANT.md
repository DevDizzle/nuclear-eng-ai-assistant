# Gemini Coding Task: Nuclear Engineering AI Assistant

## Context
Build a production-grade, open-source Nuclear Engineering AI Assistant on Google Cloud Platform. This is a RAG-powered document assistant purpose-built for nuclear power plant engineering teams. It helps engineers query engineering documents with cited answers, generate preliminary 10 CFR 50.59 screening drafts, summarize large modification packages, and compare vendor bids against specifications.

**Read the full spec first:** `specs/SPEC-NUCLEAR-AI-ASSISTANT.md`

## What to Build

### Phase 1: Core Backend (Priority)

**1. Project scaffolding**
- Python project with pyproject.toml, Dockerfile, cloudbuild.yaml
- FastAPI app with proper project structure (see spec for layout)
- Pydantic models for all data types (documents, queries, screenings, audit entries)
- Config module reading from environment variables (GCP project ID, bucket names, etc.)
- Type hints throughout, Ruff for linting, Black for formatting

**2. Document Ingestion Pipeline (`src/ingestion/`)**
- `pipeline.py` — orchestrates: upload to Cloud Storage → OCR if scanned → chunk → embed → store
- `ocr.py` — Google Document AI integration for scanned PDFs. For native PDFs, use PyPDF2/pdfplumber to extract text with page numbers preserved
- `chunker.py` — overlapping chunk strategy (512 tokens, 50 token overlap). CRITICAL: preserve page numbers and section headers in chunk metadata. Each chunk must carry: `{document_id, page_number, section_header, chunk_index, text}`
- `embedder.py` — Vertex AI Embeddings API (text-embedding-005). Batch embedding for efficiency. Store embeddings in Firestore with vector search index

**3. RAG Retrieval (`src/retrieval/`)**
- `search.py` — vector similarity search over Firestore. Top-k retrieval (k=10), then rerank to top-5
- `reranker.py` — simple relevance reranker using Gemini (score each chunk's relevance to the query, return top-5 by score)

**4. Generation Layer (`src/generation/`)**
- `gemini.py` — Gemini client wrapper. Support for Gemini 3 Flash and Gemini 3.1 Pro. Configurable model selection. Structured output via response_schema
- `citations.py` — Extract and format citations from Gemini responses. Map citations back to source document + page number from chunk metadata. Generate citation tables
- `templates.py` — All prompt templates as constants:
  - Q&A system prompt (answer from context only, cite everything)
  - 50.59 screening system prompt (see spec for full prompt)
  - Summarization system prompt (map phase + reduce phase)
  - Comparison system prompt (extract parameters, compare against spec)

**5. API Endpoints (`src/api/`)**
- `documents.py`:
  - `POST /api/documents` — upload PDF, triggers ingestion pipeline
  - `GET /api/documents` — list all ingested documents
  - `DELETE /api/documents/{id}` — remove document and its embeddings
- `query.py`:
  - `POST /api/query` — RAG Q&A. Input: question + optional document filter. Output: answer + citation table
- `screening.py`:
  - `POST /api/screening` — Input: proposed modification description. Output: preliminary 50.59 screening draft with UFSAR cross-references and citation table
- `summarize.py`:
  - `POST /api/summarize` — Input: document_id. Output: executive summary with section breakdown and page references
- `compare.py`:
  - `POST /api/compare` — Input: spec_document_id + vendor_document_ids[]. Output: comparison table with pass/fail flags
- `POST /api/audit` — query audit log (all endpoints auto-log to BigQuery)

**6. Storage Layer (`src/storage/`)**
- `gcs.py` — Cloud Storage: upload, download, list, delete documents in versioned bucket
- `firestore.py` — Firestore: store/query document chunks with embeddings (vector search), session state for conversations, document metadata
- `bigquery.py` — BigQuery: audit log writes (every query, response, user, timestamp, documents referenced, citations generated)

**7. Agent Layer (`src/agents/`) — Use Google Agent Development Kit (ADK)**
- `retrieval.py` — ADK agent that handles: receive query → search documents → rerank → format citations → return to user
- `screening.py` — ADK agent that orchestrates: receive modification description → search UFSAR → identify affected design functions → generate screening draft → format as structured document
- `summarization.py` — ADK agent: receive document → map chunks to summaries → reduce to executive summary
- `comparison.py` — ADK agent: receive spec + vendor docs → extract parameters from each → build comparison matrix

### Phase 2: Frontend (Next.js)

**Clean, professional UI. This will be demoed to a nuclear engineering hiring manager.**

- **Dashboard** — document count, recent queries, system status
- **Document Management** — upload PDFs (drag and drop), list documents with metadata, delete
- **Q&A Chat Interface** — chat-style interface with citation tables below each response. Conversation history in sidebar.
- **50.59 Screening Wizard** — step-by-step form: describe modification → select relevant documents → generate screening → review with citations → export to PDF
- **Document Summarization** — select document → generate summary → view with section breakdown
- **Vendor Bid Comparison** — upload spec + vendor docs → view side-by-side comparison table with pass/fail
- **Audit Log Viewer** — searchable table of all system interactions

**CRITICAL UI ELEMENT:** Every page that displays AI-generated content must show a prominent banner:
```
⚠️ PRELIMINARY — AI-GENERATED CONTENT — REQUIRES LICENSED ENGINEER REVIEW AND APPROVAL
   This output has zero design authority. All technical decisions remain with qualified engineering personnel.
```
Use a yellow/amber banner, always visible, cannot be dismissed.

### Phase 3: Real Nuclear Documents

Download and include in `data/` directory:

**Regulatory (from NRC.gov — all public domain):**
- 10 CFR 50.59 full text
- NEI 96-07 Rev 1 (10 CFR 50.59 Implementation Guidelines)
- NUREG-2261 (NRC AI Strategic Plan)
- Select NRC Regulatory Guides relevant to design control (RG 1.187, RG 1.189)

**Sample Engineering Documents (from NRC ADAMS — all public):**
- 2-3 License Amendment Requests (LARs) for plant modifications (search ADAMS for recent St. Lucie or Turkey Point LARs)
- 2-3 NRC Safety Evaluation Reports
- Generic Design Control Document sections (AP1000 DCD publicly available)

**For ADAMS documents:** Use the NRC ADAMS public search (https://www.nrc.gov/reading-rm/adams.html) or direct API. Search for recent Turkey Point or St. Lucie modification-related documents.

## Technical Requirements
- Python 3.11+
- FastAPI with async endpoints
- All Pydantic v2 models with strict typing
- Google Cloud SDK (`google-cloud-aiplatform`, `google-cloud-firestore`, `google-cloud-bigquery`, `google-cloud-storage`, `google-cloud-documentai`)
- Google Agent Development Kit (`google-adk`)
- Docker multi-stage build (slim production image)
- GitHub Actions CI (Ruff, Black, mypy, pytest)
- Cloud Build → Cloud Run deployment
- Environment-based config (no hardcoded project IDs or bucket names)

## Repo
Initialize at: `~/nuclear-eng-ai-assistant`
GitHub: Will push to github.com/DevDizzle/nuclear-eng-ai-assistant

## Quality Standards
- Type hints on every function
- Docstrings on every public function and class
- Error handling with proper HTTP status codes
- Structured logging (JSON format for Cloud Logging)
- Unit tests for ingestion, retrieval, and screening logic
- README.md with architecture diagram, setup instructions, and regulatory context explanation
