from typing import List
from vertexai.language_models import TextEmbeddingModel
from src.config import settings
import vertexai

class VertexEmbedder:
    def __init__(self):
        vertexai.init(project=settings.gcp_project_id, location="us-central1")
        self.model = TextEmbeddingModel.from_pretrained(settings.embedding_model)

    async def embed_chunks(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Vertex AI Embeddings API in batches."""
        embeddings = []
        batch_size = 30
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            emb_responses = self.model.get_embeddings(batch)
            embeddings.extend([emb.values for emb in emb_responses])
        return embeddings
