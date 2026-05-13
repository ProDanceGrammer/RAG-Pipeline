"""Integration test for RAG pipeline."""
import pytest
from unittest.mock import Mock
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore
from src.rag.retriever import Retriever
from src.rag.indexer import DocumentIndexer
from src.processing.chunking import TextChunker
from src.inference.inference_engine import InferenceEngine


@pytest.fixture
def mock_llm():
    llm = Mock()
    llm.embed = Mock(return_value=[[0.1] * 128 for _ in range(10)])
    llm.generate = Mock(return_value="This is a test response.")
    return llm


@pytest.mark.integration
def test_rag_pipeline_end_to_end(mock_llm, sample_documents):
    """Test complete RAG pipeline."""
    # Setup components
    embedder = Embedder(mock_llm, batch_size=10)
    vector_store = FAISSVectorStore(dimension=128)
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)

    # Index documents
    indexer = DocumentIndexer(vector_store, embedder, chunker)
    indexer.index_documents(sample_documents)

    # Query
    retriever = Retriever(vector_store, embedder, top_k=2)
    engine = InferenceEngine(mock_llm, retriever)

    response = engine.query("What is machine learning?", use_rag=True)

    assert response == "This is a test response."
    assert mock_llm.generate.called


@pytest.mark.integration
def test_query_without_rag(mock_llm):
    """Test query without RAG retrieval."""
    engine = InferenceEngine(mock_llm)

    response = engine.query("What is AI?", use_rag=False)

    assert response == "This is a test response."
    assert mock_llm.generate.called


@pytest.mark.integration
def test_query_with_metadata(mock_llm, sample_documents):
    """Test query returning metadata."""
    embedder = Embedder(mock_llm, batch_size=10)
    vector_store = FAISSVectorStore(dimension=128)
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)

    indexer = DocumentIndexer(vector_store, embedder, chunker)
    indexer.index_documents(sample_documents)

    retriever = Retriever(vector_store, embedder, top_k=2)
    engine = InferenceEngine(mock_llm, retriever)

    result = engine.query_with_metadata("What is machine learning?", use_rag=True)

    assert "answer" in result
    assert "question" in result
    assert "retrieved_documents" in result
    assert result["used_rag"] is True
