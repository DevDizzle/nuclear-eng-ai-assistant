import pytest
from unittest.mock import AsyncMock, MagicMock
from src.storage.firestore import FirestoreStorage
from src.models.document import ChunkMetadata

@pytest.mark.asyncio
async def test_vector_search_filters():
    # Mock firestore client and its chained calls
    mock_db = MagicMock()
    mock_collection_group = MagicMock()
    mock_query = MagicMock()
    mock_vector_query = MagicMock()
    
    mock_db.collection_group.return_value = mock_collection_group
    mock_collection_group.where.return_value = mock_query
    mock_query.where.return_value = mock_query
    mock_query.find_nearest.return_value = mock_vector_query
    mock_vector_query.stream.return_value = []
    
    storage = FirestoreStorage()
    storage.db = mock_db
    
    results = await storage.vector_search(
        query_embedding=[0.1, 0.2], 
        top_k=5, 
        doc_types=["ufsar"], 
        plant_name="TestPlant"
    )
    
    assert results == []
    # Assert collection_group called
    mock_db.collection_group.assert_called_with("chunks")
    # Assert where called for doc_types and plant_name
    assert mock_query.where.call_count >= 1
