from google.cloud import storage
from src.config import settings

class GCSStorage:
    def __init__(self):
        self.client = storage.Client(project=settings.gcp_project_id)
        self.bucket = self.client.bucket(settings.gcs_bucket_documents)

    async def upload_document(self, document_id: str, file_path: str) -> str:
        """Uploads a document to Cloud Storage."""
        blob = self.bucket.blob(f"documents/{document_id}")
        blob.upload_from_filename(file_path)
        return blob.public_url

    async def list_documents(self) -> list:
        """Lists all uploaded documents."""
        blobs = self.bucket.list_blobs(prefix="documents/")
        return [blob.name for blob in blobs]

    async def delete_document(self, document_id: str):
        """Deletes a document from Cloud Storage."""
        blob = self.bucket.blob(f"documents/{document_id}")
        if blob.exists():
            blob.delete()
