"""Tests for vector store implementations."""
import pytest
import numpy as np
from src.rag.vector_store import FAISSVectorStore


@pytest.fixture
def sample_vectors():
    """Generate sample vectors for testing."""
    return np.random.rand(10, 128).astype('float32')


@pytest.fixture
def sample_metadata():
    """Generate sample metadata."""
    return [{"text": f"Document {i}", "source": f"doc{i}.txt"} for i in range(10)]


@pytest.mark.unit
def test_faiss_add_vectors(sample_vectors, sample_metadata):
    """Test adding vectors to FAISS store."""
    store = FAISSVectorStore(dimension=128)

    store.add(sample_vectors, sample_metadata)

    assert store.index.ntotal == 10
    assert len(store.metadata) == 10


@pytest.mark.unit
def test_faiss_search(sample_vectors, sample_metadata):
    """Test searching in FAISS store."""
    store = FAISSVectorStore(dimension=128)
    store.add(sample_vectors, sample_metadata)

    query_vector = sample_vectors[0]
    results = store.search(query_vector, top_k=3)

    assert len(results) == 3
    assert results[0][0] == 0  # First result should be the query itself
    assert results[0][1] < 0.01  # Distance should be very small


@pytest.mark.unit
def test_faiss_save_load(sample_vectors, sample_metadata, tmp_path):
    """Test saving and loading FAISS store."""
    store = FAISSVectorStore(dimension=128)
    store.add(sample_vectors, sample_metadata)

    save_path = tmp_path / "test_store"
    store.save(str(save_path))

    new_store = FAISSVectorStore(dimension=128)
    new_store.load(str(save_path))

    assert new_store.index.ntotal == 10
    assert len(new_store.metadata) == 10
    assert new_store.metadata[0]["text"] == "Document 0"
