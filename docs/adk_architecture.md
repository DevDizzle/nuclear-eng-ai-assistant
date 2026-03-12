# ADK Architecture

The system has been modernized to use the Google Cloud Agent Development Kit (ADK).

## Components

- **Tools (`src/adk/tools/`)**: `search_documents` wraps the native Firestore vector search. It receives typed inputs (`RetrievalRequest`) and returns a formatted context block.
- **Agents (`src/adk/agents/`)**:
  - `retrieval_agent`: A SequentialAgent (Researcher -> Formatter) for grounded QA. Uses tools and returns `QueryResponse`.
  - `screening_agent`: A SequentialAgent (Researcher -> Formatter) for 50.59 screening. Retrieves from UFSAR and guidance programmatically via callbacks before synthesizing, eliminating zero-shot hallucination. It then formats to `ScreeningResponse`.
  - `router_agent`: A top-level orchestration agent designed for a future unified chat UI. Currently, the FastAPI application (`/api/query` and `/api/screening`) invokes the specialized pipelines directly to preserve API contracts, while the router remains available for conversational routing.
- **Runners (`src/api/`)**: API endpoints execute agents using ADK `Runner` and `InMemorySessionService`, injecting requests and retrieving structured states.

This ensures execution is grounded, observable, and modularly separated between reasoning (tools) and formatting (schema).
