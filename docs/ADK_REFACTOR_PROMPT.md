# ADK Refactoring & Model Upgrade Prompt

**Purpose:** This document contains a detailed prompt designed to be passed to a Gemini CLI agent in a future session. It instructs the agent to systematically refactor the Nuclear Engineering AI Assistant to use Google's Agent Development Kit (ADK) and upgrade the underlying foundation model.

---

## Copy and Paste the text below to the Gemini CLI:

```text
Hello Gemini! We need to execute a major architectural refactor on the `nuclear-eng-ai-assistant` project located at `/home/user/nuclear-eng-ai-assistant`. 

Currently, the application uses custom Python wrapper classes (`RetrievalAgentWrapper`, `ScreeningAgentWrapper`, and `GeminiClient`) to interface directly with the `google.genai` SDK and perform sequential RAG operations. 

We need to modernize this architecture to use Google's Agent Development Kit (ADK) for better state management, tool calling, and alignment with Vertex AI Agent Engine best practices. Concurrently, we are upgrading our foundation model.

Please execute the following tasks systematically:

### 1. Upgrade the Foundation Model
- Locate where the model is defined (likely in `src/config.py`, `.env`, or hardcoded in `src/generation/gemini.py`).
- Update the default model string to use `gemini-3.1-flash-lite`.

### 2. Refactor to ADK Paradigm
- **Shift from Sequential to Tool-Calling:** The current approach manually orchestrates vector search, string concatenation, and LLM calls. We need to refactor this so that the vector search (`src/retrieval/search.py`'s `VectorSearch`) is exposed as a strongly-typed Python function with a detailed docstring, making it a "tool" that an ADK Agent can invoke.
- **Implement `google.adk.agents.Agent`:** Replace the custom logic in `src/agents/retrieval.py` and `src/agents/screening.py` by defining native ADK `Agent` instances. 
    - The agents should be instantiated with the new `gemini-3.1-flash-lite` model.
    - The system prompts (currently in `src/generation/templates.py`) should be passed to the `instruction` parameter of the `Agent`.
    - The retrieval agent must be given the newly created search tool via the `tools=[...]` parameter.
- **Implement `vertexai.agent_engines.AdkApp`:** Wrap the new `Agent` definitions inside an `AdkApp`. Update the FastAPI endpoints (likely in `src/api/` or `src/main.py`) to interact with the agent using `AdkApp.async_stream_query` or similar async methods provided by ADK.

### 3. Handle Async and State
- ADK is inherently asynchronous. Ensure that the event loop and async/await keywords are correctly utilized throughout the new execution path, especially where the FastAPI routes call the ADK App.
- (Optional but recommended) Implement basic session management using `AdkApp.async_create_session` so that multi-turn interactions can be supported in the future.

### 4. Cleanup and Verification
- Remove or deprecate the old custom wrapper classes (`GeminiClient`, old agent wrappers) if they are no longer needed.
- Ensure `google-adk` and `vertexai` dependencies in `pyproject.toml` are correctly aligned.
- Provide a summary of the files changed and explain how the new ADK tool-calling flow works compared to the old sequential flow.

### 5. Testing, QA, and SWE Best Practices
- **Strict Typing:** Ensure all new functions, tools, and agent wrappers use strict Python type hinting.
- **Error Handling:** Implement try/except blocks around network calls and ADK agent invocations to ensure graceful degradation.
- **Unit Testing:** Update or write new unit tests (using `pytest`) in the `tests/` directory to verify the new tool functions and API endpoint responses. Ensure tests pass before concluding the refactor.
- **Linting:** Run standard SWE checks (e.g., `ruff`, `black`, `mypy` as defined in `pyproject.toml`) to ensure the codebase remains clean and idiomatic.

### 6. Deployment to Cloud Run
- **Dockerization Review:** Check the existing `Dockerfile` and `cloudbuild.yaml` to ensure they are compatible with the new dependencies and asynchronous execution environment.
- **Deploy:** Execute a deployment of the refactored FastAPI application to Google Cloud Run (project: `profitscout-lx6bb`, region: `us-central1` or as specified in environment/context).
- **Validation:** Test the deployed Cloud Run endpoint to confirm that the ADK integration functions successfully in the production environment.

Please start by mapping out the codebase to understand the exact entry points (FastAPI routes) and how they currently trace down to `src/agents/retrieval.py` and `src/generation/gemini.py`. Let me know your step-by-step plan before making file modifications.
```