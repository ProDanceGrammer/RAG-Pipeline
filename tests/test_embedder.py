"""Tests for embedder module."""
import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
from src.rag.embedder import Embedder


@pytest.fixture
def mock_llm():
    llm = Mock()
    llm.embed = Mock(return_value=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    return llm


@pytest.fixture
def embedder(mock_llm):
    return Embedder(mock_llm, batch_size=2)


@pytest.mark.unit
def test_embed_single(embedder, mock_llm):
    """Test single text embedding."""
    mock_llm.embed.return_value = [[0.1, 0.2, 0.3]]

    result = embedder.embed_single("test text")

    assert isinstance(result, np.ndarray)
    assert result.shape == (3,)
    mock_llm.embed.assert_called_once_with(["test text"])


@pytest.mark.unit
def test_embed_texts(embedder, mock_llm):
    """Test batch text embedding."""
    texts = ["text1", "text2"]

    result = embedder.embed_texts(texts)

    assert isinstance(result, np.ndarray)
    assert result.shape == (2, 3)
    mock_llm.embed.assert_called_once()


@pytest.mark.unit
def test_cosine_similarity():
    """Test cosine similarity calculation."""
    vec1 = np.array([1.0, 0.0, 0.0])
    vec2 = np.array([1.0, 0.0, 0.0])

    similarity = Embedder.cosine_similarity(vec1, vec2)

    assert abs(similarity - 1.0) < 1e-6


@pytest.mark.unit
def test_embed_texts_batching(embedder, mock_llm):
    """Test that batching works correctly."""
    texts = ["text1", "text2", "text3", "text4", "text5"]
    mock_llm.embed.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]

    result = embedder.embed_texts(texts)

    assert mock_llm.embed.call_count == 3
