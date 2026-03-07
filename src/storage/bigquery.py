from google.cloud import bigquery
from src.config import settings
from src.models.audit import AuditEntry

class BigQueryAudit:
    def __init__(self):
        self.client = bigquery.Client(project=settings.gcp_project_id)
        self.table_id = f"{settings.gcp_project_id}.{settings.bq_dataset}.{settings.bq_table_audit}"

    async def log_action(self, entry: AuditEntry):
        """Writes an audit log entry to BigQuery."""
        errors = self.client.insert_rows_json(self.table_id, [entry.model_dump(mode="json")])
        if errors:
            print(f"Encountered errors while inserting rows: {errors}")
