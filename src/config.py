from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the Nuclear Engineering AI Assistant."""
    gcp_project_id: str = "profitscout-lx6bb"
    gcp_region: str = "us-central1"
    
    # Storage settings
    gcs_bucket_documents: str = "nuclear-ai-documents"
    
    # Firestore / Vector Search
    firestore_database: str = "(default)"
    
    # BigQuery
    bq_dataset: str = "nuclear_ai_audit"
    bq_table_audit: str = "audit_log"
    
    # Document AI
    docai_processor_id: str = ""
    
    # Model settings
    embedding_model: str = "text-embedding-005"
    llm_model: str = "gemini-2.5-pro"
    
    class Config:
        env_file = ".env"
        env_prefix = "NUKE_AI_"

settings = Settings()