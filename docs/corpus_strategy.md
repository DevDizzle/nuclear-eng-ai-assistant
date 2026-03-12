# Corpus Indexing and Grounding Strategy

## Data Model
Chunks now have extensive metadata for filtering:
- `document_id`: UUID
- `filename`: Source file
- `doc_type`: `regulation`, `regulatory_guide`, `industry_guidance`, `ufsar`, `licensing_basis`, `other`
- `plant_name`: E.g., `Turkey Point`
- `unit`: Optional unit identifier

## Ingestion
The ingestion pipeline splits text with overlap and preserves structural hints (page markers, section headers). Metadata is passed to `ChunkMetadata`. Emdeddings are natively stored in Firestore as vectors using the Python SDK.

**Note on Chunking Limitations:** The current `OverlappingChunker` uses naive word-splitting and simple regex heuristics. For production-grade regulatory grounding (UFSARs, SERs), it is strongly recommended to upgrade the ingestion stack to a layout-aware parser (e.g., Docling, LlamaParse, or Google Document AI layout parser) to correctly preserve complex tables, semantic headers, and cross-references.

## Storage and Retrieval
Firestore `collection_group` query is used on `chunks` subcollections. It uses native vector `find_nearest` with `Cosine` distance, filtering first by `doc_type` and `plant_name` to constrain searches to specific corpora.

**Vector Index Creation:** After initial seeding, you MUST create a composite index in Firestore to support `find_nearest` combined with metadata filters (`doc_type`, etc.). Running a search query via `verify_retrieval.py` before the index exists will fail, but the error message will provide the exact `gcloud alpha firestore indexes composite create ...` command needed. Run that command to build the index.

## Screening Grounding
The 50.59 screening agent runs dual-stage search if needed, explicitly targeting `ufsar` for plant basis and `industry_guidance` for interpretation, effectively eliminating zero-shot hallucination.
