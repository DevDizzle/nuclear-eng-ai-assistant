from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api import documents, query, screening, summarize, compare, audit

app = FastAPI(
    title="Nuclear Engineering AI Assistant",
    description="RAG-powered AI Assistant for nuclear power plant engineering teams.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(query.router, prefix="/api/query", tags=["Query"])
app.include_router(screening.router, prefix="/api/screening", tags=["50.59 Screening"])
app.include_router(summarize.router, prefix="/api/summarize", tags=["Summarize"])
app.include_router(compare.router, prefix="/api/compare", tags=["Compare"])
app.include_router(audit.router, prefix="/api/audit", tags=["Audit Log"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
