import asyncio
import argparse
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from src.config import settings

async def reindex_corpus(dry_run: bool = True):
    """
    Utility script to migrate chunk data to the native Vector type if previously stored as lists.
    """
    print(f"Connecting to Firestore (project={settings.gcp_project_id}, db={settings.firestore_database})...")
    db = firestore.Client(project=settings.gcp_project_id, database=settings.firestore_database)
    
    print(f"Scanning all chunks... (Dry Run: {dry_run})")
    chunks = db.collection_group("chunks").stream()
    
    scanned = 0
    converted = 0
    skipped = 0
    
    batch = db.batch()
    operations_in_batch = 0
    
    for doc in chunks:
        scanned += 1
        data = doc.to_dict()
        embedding = data.get("embedding")
        
        if isinstance(embedding, list):
            # Needs conversion
            if not dry_run:
                batch.update(doc.reference, {"embedding": Vector(embedding)})
                operations_in_batch += 1
                
                # Commit in chunks of 400 (Firestore limit is 500)
                if operations_in_batch >= 400:
                    batch.commit()
                    batch = db.batch()
                    operations_in_batch = 0
            converted += 1
        else:
            # Already a Vector or missing
            skipped += 1
            
        if scanned % 100 == 0:
            print(f"Scanned {scanned} documents...")

    if not dry_run and operations_in_batch > 0:
        batch.commit()
        
    print("\n--- Migration Complete ---")
    print(f"Total Scanned: {scanned}")
    print(f"Needs Conversion / Converted: {converted}")
    print(f"Skipped (Already Vector or Missing): {skipped}")
    
    if dry_run:
        print("\nNOTE: This was a dry run. Rerun with --apply to perform actual conversion.")
    
    print("\nNext steps:")
    print("If you haven't already, you must create a composite index for vector search.")
    print("Run a search query; if the index is missing, the error output will provide the exact `gcloud` command to create it.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate legacy list embeddings to Firestore Vector type.")
    parser.add_argument("--apply", action="store_true", help="Apply changes (disable dry run)")
    args = parser.parse_args()
    
    asyncio.run(reindex_corpus(dry_run=not args.apply))
