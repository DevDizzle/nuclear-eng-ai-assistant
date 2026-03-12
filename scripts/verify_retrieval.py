import asyncio
from src.retrieval.search import VectorSearch
from src.models.retrieval import RetrievalRequest

async def verify_retrieval():
    searcher = VectorSearch()
    
    queries = [
        {"q": "What is the definition of a minimal increase in probability?", "types": ["industry_guidance", "regulation"]},
        {"q": "What are the affected design functions for the fire protection system at Turkey Point?", "types": ["licensing_basis", "ufsar"], "plant": "Turkey Point"}
    ]
    
    for query in queries:
        print(f"\n--- Testing Query: {query['q']} ---")
        req = RetrievalRequest(
            query=query["q"],
            top_k=3,
            doc_types=query.get("types"),
            plant_name=query.get("plant")
        )
        
        try:
            res = await searcher.search(req)
            print(f"Found {len(res.hits)} results.")
            for i, hit in enumerate(res.hits):
                print(f"  Result {i+1}: {hit.title or hit.filename} (Type: {hit.doc_type}) - Distance: {hit.distance}")
                print(f"  Preview: {hit.text[:100]}...\n")
        except Exception as e:
            print(f"Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(verify_retrieval())
