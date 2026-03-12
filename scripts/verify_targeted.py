import asyncio
from src.retrieval.search import VectorSearch
from src.models.retrieval import RetrievalRequest

async def verify_targeted():
    searcher = VectorSearch()
    
    queries = [
        {"q": "main steam line radiation monitors Turkey Point Unit 3", "types": ["ufsar", "licensing_basis"]},
        {"q": "steam generator tube rupture radiation monitor UFSAR Turkey Point", "types": ["ufsar", "licensing_basis"]},
        {"q": "digital transmitter replacement radiation monitoring 50.59", "types": ["regulation", "regulatory_guide", "industry_guidance"]}
    ]
    
    for query in queries:
        print(f"\n--- Testing Query: {query['q']} ---")
        req = RetrievalRequest(
            query=query["q"],
            top_k=3,
            doc_types=query.get("types"),
            plant_name="Turkey Point" if "ufsar" in query.get("types", []) else None
        )
        
        try:
            res = await searcher.search(req)
            print(f"Found {len(res.hits)} results.")
            for i, hit in enumerate(res.hits):
                print(f"  Result {i+1}: {hit.title or hit.filename} (Type: {hit.doc_type}) - Distance: {hit.distance}")
                print(f"  Preview: {hit.text[:200]}...\n")
        except Exception as e:
            print(f"Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(verify_targeted())
