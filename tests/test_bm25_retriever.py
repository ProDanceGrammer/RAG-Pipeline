"""Unit tests for BM25 retriever."""
import pytest
from src.rag.bm25_retriever import BM25Retriever
from pathlib import Path
import tempfile


class TestBM25Retriever:
    """Test BM25 retriever functionality."""

    def test_initialization(self):
        """Test BM25 retriever initialization."""
        retriever = BM25Retriever(k1=1.5, b=0.75)
        assert retriever.k1 == 1.5
        assert retriever.b == 0.75
        assert retriever.num_docs == 0

    def test_tokenization(self):
        """Test text tokenization."""
        retriever = BM25Retriever()

        # Basic tokenization
        tokens = retriever.tokenize("Hello World")
        assert tokens == ["hello", "world"]

        # With punctuation
        tokens = retriever.tokenize("Hello, World!")
        assert tokens == ["hello", "world"]

        # With numbers
        tokens = retriever.tokenize("Python 3.9")
        assert tokens == ["python", "3", "9"]

    def test_indexing(self):
        """Test document indexing."""
        retriever = BM25Retriever()
        documents = [
            "Python is a programming language",
            "Machine learning uses Python",
            "SOLID principles in OOP"
        ]

        retriever.index(documents)

        assert retriever.num_docs == 3
        assert len(retriever.corpus) == 3
        assert len(retriever.tokenized_corpus) == 3
        assert len(retriever.doc_lengths) == 3
        assert retriever.avgdl > 0

    def test_exact_term_matching(self):
        """Test that BM25 scores exact term matches higher."""
        retriever = BM25Retriever()
        documents = [
            "SOLID principles are important in OOP",
            "Creator is a GRASP principle",
            "Database partitioning improves performance"
        ]

        retriever.index(documents)

        # Search for "SOLID"
        results = retriever.search("SOLID principles", top_k=3)

        assert len(results) > 0
        # First result should be the document with "SOLID"
        assert results[0][0] == 0  # Index of first document
        assert results[0][1] > 0  # Score should be positive

    def test_search_empty_index(self):
        """Test search on empty index."""
        retriever = BM25Retriever()
        results = retriever.search("test query", top_k=5)
        assert results == []

    def test_search_empty_query(self):
        """Test search with empty query."""
        retriever = BM25Retriever()
        documents = ["Python programming", "Machine learning"]
        retriever.index(documents)

        results = retriever.search("", top_k=5)
        assert results == []

    def test_search_top_k(self):
        """Test that search returns correct number of results."""
        retriever = BM25Retriever()
        documents = [
            "Python programming language",
            "Python for data science",
            "Java programming language",
            "JavaScript web development",
            "C++ systems programming"
        ]

        retriever.index(documents)

        # Search for "Python"
        results = retriever.search("Python", top_k=2)
        assert len(results) == 2

        # Both results should have "Python" in them
        assert results[0][0] in [0, 1]  # First two documents
        assert results[1][0] in [0, 1]

    def test_save_and_load(self):
        """Test saving and loading BM25 index."""
        retriever = BM25Retriever()
        documents = [
            "Python programming",
            "Machine learning",
            "Data science"
        ]

        retriever.index(documents)

        # Save to temporary file
        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "test_bm25.pkl"
            retriever.save(str(save_path))

            # Load into new retriever
            new_retriever = BM25Retriever()
            new_retriever.load(str(save_path))

            # Verify loaded data
            assert new_retriever.num_docs == 3
            assert len(new_retriever.corpus) == 3
            assert new_retriever.k1 == retriever.k1
            assert new_retriever.b == retriever.b

            # Verify search works the same
            results1 = retriever.search("Python", top_k=2)
            results2 = new_retriever.search("Python", top_k=2)
            assert results1 == results2

    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file."""
        retriever = BM25Retriever()

        with pytest.raises(FileNotFoundError):
            retriever.load("/nonexistent/path/bm25.pkl")

    def test_get_size(self):
        """Test getting index size."""
        retriever = BM25Retriever()
        assert retriever.get_size() == 0

        documents = ["doc1", "doc2", "doc3"]
        retriever.index(documents)
        assert retriever.get_size() == 3

    def test_score_ordering(self):
        """Test that scores are ordered correctly."""
        retriever = BM25Retriever()
        documents = [
            "Python Python Python",  # High frequency
            "Python programming",    # Medium frequency
            "Java programming"       # No match
        ]

        retriever.index(documents)
        results = retriever.search("Python", top_k=3)

        # Scores should be in descending order
        assert len(results) >= 2
        assert results[0][1] >= results[1][1]

        # Document with highest Python frequency should rank first
        assert results[0][0] == 0
