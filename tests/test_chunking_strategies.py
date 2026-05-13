"""Test chunking strategies."""
import pytest
from pathlib import Path
from src.chunking import (
    StructureChunker,
    HierarchicalChunker,
    SemanticChunker,
    SlidingWindowChunker,
    Chunk
)


@pytest.fixture
def sample_markdown():
    """Sample markdown text for testing."""
    return """# Main Title

## Section 1: Introduction

This is the introduction section.

🔽 What?

This is a definition.

🤔 How does it work?

This explains how it works.

## Section 2: Details

More detailed information here.

🔽 What?

Another definition.

👍 Advantages

- Advantage 1
- Advantage 2

## Section 3: Code Example

Here is some code:

```python
def hello():
    print("Hello")
```

This is after the code block.
"""


@pytest.mark.unit
def test_structure_chunker(sample_markdown):
    """Test structure-based chunking."""
    chunker = StructureChunker()
    chunks = chunker.chunk(sample_markdown, source="test.md")

    assert len(chunks) > 0
    assert all(isinstance(c, Chunk) for c in chunks)
    assert all(c.metadata['chunking_strategy'] == 'structure' for c in chunks)

    # Check that sections are preserved
    section_names = [c.metadata.get('section', '') for c in chunks]
    assert any('Introduction' in s for s in section_names)
    assert any('Details' in s for s in section_names)


@pytest.mark.unit
def test_hierarchical_chunker(sample_markdown):
    """Test hierarchical chunking."""
    chunker = HierarchicalChunker()
    chunks = chunker.chunk(sample_markdown, source="test.md")

    assert len(chunks) > 0

    # Check for parent and child chunks
    parent_chunks = [c for c in chunks if c.metadata.get('chunk_type') == 'parent']
    child_chunks = [c for c in chunks if c.metadata.get('chunk_type') == 'child']

    assert len(parent_chunks) > 0
    assert len(child_chunks) > 0

    # Check emoji subsections
    subsections = [c.metadata.get('subsection', '') for c in child_chunks]
    assert any('🔽 What?' in s for s in subsections)


@pytest.mark.unit
def test_sliding_window_chunker(sample_markdown):
    """Test sliding window chunking."""
    chunker = SlidingWindowChunker(chunk_size=50, overlap=10)
    chunks = chunker.chunk(sample_markdown, source="test.md")

    assert len(chunks) > 0
    assert all(c.metadata['chunking_strategy'] == 'sliding_window' for c in chunks)

    # Check overlap
    if len(chunks) > 1:
        # Chunks should have some overlapping content
        assert chunks[0].metadata['chunk_size'] == 50
        assert chunks[0].metadata['overlap'] == 10


@pytest.mark.unit
def test_semantic_chunker_fallback(sample_markdown):
    """Test semantic chunker without embedder (fallback mode)."""
    chunker = SemanticChunker(embedder=None)
    chunks = chunker.chunk(sample_markdown, source="test.md")

    assert len(chunks) > 0
    assert all('semantic' in c.metadata['chunking_strategy'] for c in chunks)


@pytest.mark.unit
def test_chunk_stats():
    """Test chunk statistics calculation."""
    chunker = StructureChunker()
    chunks = [
        Chunk(text="Short text", metadata={'source': 'test'}),
        Chunk(text="This is a longer text with more words", metadata={'source': 'test'}),
        Chunk(text="Medium length text here", metadata={'source': 'test'})
    ]

    stats = chunker.get_stats(chunks)

    assert stats['total_chunks'] == 3
    assert stats['total_tokens'] > 0
    assert stats['avg_tokens'] > 0
    assert stats['min_tokens'] > 0
    assert stats['max_tokens'] > 0


@pytest.mark.unit
def test_chunk_token_estimation():
    """Test token estimation in chunks."""
    chunk = Chunk(text="This is a test sentence with ten words in it.")

    # Should estimate roughly 10 * 1.3 = 13 tokens
    assert 10 <= len(chunk) <= 15


@pytest.mark.unit
def test_empty_text_handling():
    """Test handling of empty text."""
    chunker = StructureChunker()
    chunks = chunker.chunk("", source="empty.md")

    assert len(chunks) == 0


@pytest.mark.unit
def test_code_block_preservation():
    """Test that code blocks are preserved in chunks."""
    text = """## Code Section

Here is code:

```python
def test():
    return True
```

End of section.
"""

    chunker = StructureChunker()
    chunks = chunker.chunk(text, source="code.md")

    assert len(chunks) > 0
    # Code block should be in the chunk
    assert '```python' in chunks[0].text
    assert 'def test():' in chunks[0].text


@pytest.mark.unit
def test_multiple_documents():
    """Test chunking multiple documents."""
    documents = [
        {'text': '## Section A\nContent A', 'source': 'doc1.md'},
        {'text': '## Section B\nContent B', 'source': 'doc2.md'}
    ]

    chunker = StructureChunker()
    chunks = chunker.chunk_documents(documents)

    assert len(chunks) == 2
    sources = [c.metadata['source'] for c in chunks]
    assert 'doc1.md' in sources
    assert 'doc2.md' in sources
