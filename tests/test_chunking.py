"""Tests for text chunking."""
import pytest
from src.processing.chunking import TextChunker


@pytest.fixture
def chunker():
    return TextChunker(chunk_size=10, chunk_overlap=2)


@pytest.mark.unit
def test_chunk_basic(chunker):
    """Test basic text chunking."""
    text = " ".join([f"word{i}" for i in range(25)])

    chunks = chunker.chunk(text)

    assert len(chunks) > 1
    assert all(isinstance(chunk, str) for chunk in chunks)


@pytest.mark.unit
def test_chunk_short_text(chunker):
    """Test chunking text shorter than chunk size."""
    text = "short text"

    chunks = chunker.chunk(text)

    assert len(chunks) == 1
    assert chunks[0] == text


@pytest.mark.unit
def test_chunk_by_sentences():
    """Test sentence-based chunking."""
    chunker = TextChunker()
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."

    chunks = chunker.chunk_by_sentences(text, max_sentences=2)

    assert len(chunks) == 2
    assert "First sentence." in chunks[0]


@pytest.mark.unit
def test_chunk_by_paragraphs():
    """Test paragraph-based chunking."""
    chunker = TextChunker()
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    chunks = chunker.chunk_by_paragraphs(text)

    assert len(chunks) == 3
    assert chunks[0] == "First paragraph."
