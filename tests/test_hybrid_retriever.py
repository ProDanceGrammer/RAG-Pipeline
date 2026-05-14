"""Unit tests for hybrid retriever."""
import pytest
from src.rag.hybrid_retriever import HybridRetriever


class TestHybridRetriever:
    """Test hybrid retriever functionality."""

    def test_initialization(self):
        """Test hybrid retriever initialization."""
        retriever = HybridRetriever(k=60)
        assert retriever.k == 60

    def test_fuse_empty_results(self):
        """Test fusion with empty results."""
        retriever = HybridRetriever()

        # Both empty
        result = retriever.fuse([], [], alpha=0.7)
        assert result == []

        # One empty
        bm25_results = [({'text': 'doc1', 'section': 'A'}, 10.0)]
        result = retriever.fuse(bm25_results, [], alpha=0.7)
        assert len(result) == 1

        result = retriever.fuse([], bm25_results, alpha=0.7)
        assert len(result) == 1

    def test_fuse_basic(self):
        """Test basic fusion of BM25 and semantic results."""
        retriever = HybridRetriever()

        bm25_results = [
            ({'text': 'SOLID principles in OOP', 'section': 'SOLID'}, 15.0),
            ({'text': 'Creator pattern', 'section': 'Creator'}, 5.0),
        ]

        semantic_results = [
            ({'text': 'Creator pattern', 'section': 'Creator'}, 200.0),
            ({'text': 'SOLID principles in OOP', 'section': 'SOLID'}, 250.0),
        ]

        # Fuse with alpha=0.7 (70% semantic, 30% BM25)
        result = retriever.fuse(bm25_results, semantic_results, alpha=0.7)

        assert len(result) == 2
        # All results should have metadata and score
        for metadata, score in result:
            assert 'text' in metadata
            assert 'section' in metadata
            assert score > 0

    def test_fuse_alpha_pure_bm25(self):
        """Test fusion with alpha=0 (pure BM25)."""
        retriever = HybridRetriever()

        bm25_results = [
            ({'text': 'doc1', 'section': 'A'}, 10.0),
            ({'text': 'doc2', 'section': 'B'}, 5.0),
        ]

        semantic_results = [
            ({'text': 'doc2', 'section': 'B'}, 200.0),
            ({'text': 'doc1', 'section': 'A'}, 100.0),
        ]

        # With alpha=0, should prioritize BM25 ranking
        result = retriever.fuse(bm25_results, semantic_results, alpha=0.0)

        assert len(result) == 2
        # BM25 had doc1 first, so it should rank higher
        assert result[0][0]['section'] == 'A'

    def test_fuse_alpha_pure_semantic(self):
        """Test fusion with alpha=1 (pure semantic)."""
        retriever = HybridRetriever()

        bm25_results = [
            ({'text': 'doc1', 'section': 'A'}, 10.0),
            ({'text': 'doc2', 'section': 'B'}, 5.0),
        ]

        semantic_results = [
            ({'text': 'doc2', 'section': 'B'}, 200.0),
            ({'text': 'doc1', 'section': 'A'}, 100.0),
        ]

        # With alpha=1, should prioritize semantic ranking
        result = retriever.fuse(bm25_results, semantic_results, alpha=1.0)

        assert len(result) == 2
        # Semantic had doc2 first, so it should rank higher
        assert result[0][0]['section'] == 'B'

    def test_fuse_no_overlap(self):
        """Test fusion when results don't overlap."""
        retriever = HybridRetriever()

        bm25_results = [
            ({'text': 'doc1', 'section': 'A'}, 10.0),
        ]

        semantic_results = [
            ({'text': 'doc2', 'section': 'B'}, 200.0),
        ]

        result = retriever.fuse(bm25_results, semantic_results, alpha=0.7)

        # Should have both documents
        assert len(result) == 2

    def test_fuse_complete_overlap(self):
        """Test fusion when results completely overlap."""
        retriever = HybridRetriever()

        bm25_results = [
            ({'text': 'doc1', 'section': 'A'}, 10.0),
            ({'text': 'doc2', 'section': 'B'}, 5.0),
        ]

        semantic_results = [
            ({'text': 'doc1', 'section': 'A'}, 200.0),
            ({'text': 'doc2', 'section': 'B'}, 100.0),
        ]

        result = retriever.fuse(bm25_results, semantic_results, alpha=0.7)

        # Should have both documents (no duplicates)
        assert len(result) == 2

    def test_get_doc_id_consistency(self):
        """Test that document ID generation is consistent."""
        retriever = HybridRetriever()

        metadata1 = {'text': 'Python programming', 'section': 'Python'}
        metadata2 = {'text': 'Python programming', 'section': 'Python'}

        doc_id1 = retriever._get_doc_id(metadata1)
        doc_id2 = retriever._get_doc_id(metadata2)

        assert doc_id1 == doc_id2

    def test_get_doc_id_different(self):
        """Test that different documents get different IDs."""
        retriever = HybridRetriever()

        metadata1 = {'text': 'Python programming', 'section': 'Python'}
        metadata2 = {'text': 'Java programming', 'section': 'Java'}

        doc_id1 = retriever._get_doc_id(metadata1)
        doc_id2 = retriever._get_doc_id(metadata2)

        assert doc_id1 != doc_id2

    def test_rrf_score_calculation(self):
        """Test that RRF scores are calculated correctly."""
        retriever = HybridRetriever(k=60)

        # Single result in both lists at rank 1
        bm25_results = [
            ({'text': 'doc1', 'section': 'A'}, 10.0),
        ]

        semantic_results = [
            ({'text': 'doc1', 'section': 'A'}, 200.0),
        ]

        result = retriever.fuse(bm25_results, semantic_results, alpha=0.5)

        # RRF score = 0.5 * (1/(60+1)) + 0.5 * (1/(60+1))
        # = 0.5 * (1/61) + 0.5 * (1/61) = 1/61
        expected_score = 1.0 / 61.0

        assert len(result) == 1
        assert abs(result[0][1] - expected_score) < 0.0001
