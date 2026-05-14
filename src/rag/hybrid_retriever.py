"""Hybrid retriever combining BM25 and semantic search using Reciprocal Rank Fusion."""
import logging
from typing import List, Tuple, Dict

logger = logging.getLogger(__name__)


class HybridRetriever:
    """Combines BM25 and semantic search results using Reciprocal Rank Fusion."""

    def __init__(self, k: int = 60):
        """
        Initialize hybrid retriever.

        Args:
            k: RRF constant (default: 60, standard value from literature)
        """
        self.k = k
        self.logger = logging.getLogger(__name__)

    def fuse(
        self,
        bm25_results: List[Tuple[Dict, float]],
        semantic_results: List[Tuple[Dict, float]],
        alpha: float = 0.7
    ) -> List[Tuple[Dict, float]]:
        """
        Fuse BM25 and semantic search results using Reciprocal Rank Fusion.

        Args:
            bm25_results: List of (metadata, bm25_score) tuples
            semantic_results: List of (metadata, distance) tuples
            alpha: Weight for semantic results (0.0=pure BM25, 1.0=pure semantic)

        Returns:
            Fused list of (metadata, fused_score) tuples, sorted by score descending
        """
        self.logger.debug(
            f"Fusing {len(bm25_results)} BM25 results with "
            f"{len(semantic_results)} semantic results (alpha={alpha})"
        )

        # Build rank maps for both result sets
        bm25_ranks = self._build_rank_map(bm25_results)
        semantic_ranks = self._build_rank_map(semantic_results)

        # Get all unique documents
        all_docs = set()
        for metadata, _ in bm25_results:
            doc_id = self._get_doc_id(metadata)
            all_docs.add(doc_id)
        for metadata, _ in semantic_results:
            doc_id = self._get_doc_id(metadata)
            all_docs.add(doc_id)

        # Calculate RRF scores
        fused_scores = {}
        doc_metadata = {}

        for doc_id in all_docs:
            # RRF formula: score = sum(1 / (k + rank)) for each result list
            bm25_score = 0.0
            semantic_score = 0.0

            if doc_id in bm25_ranks:
                rank, metadata = bm25_ranks[doc_id]
                bm25_score = 1.0 / (self.k + rank)
                doc_metadata[doc_id] = metadata

            if doc_id in semantic_ranks:
                rank, metadata = semantic_ranks[doc_id]
                semantic_score = 1.0 / (self.k + rank)
                doc_metadata[doc_id] = metadata

            # Weighted combination
            fused_score = (1 - alpha) * bm25_score + alpha * semantic_score
            fused_scores[doc_id] = fused_score

        # Sort by fused score descending
        sorted_docs = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Convert back to (metadata, score) format
        results = [
            (doc_metadata[doc_id], score)
            for doc_id, score in sorted_docs
        ]

        if results:
            self.logger.debug(
                f"Fusion complete: {len(results)} results, "
                f"top score: {results[0][1]:.4f}"
            )
        else:
            self.logger.debug("Fusion complete: no results")

        return results

    def _build_rank_map(
        self,
        results: List[Tuple[Dict, float]]
    ) -> Dict[str, Tuple[int, Dict]]:
        """
        Build a map from document ID to (rank, metadata).

        Args:
            results: List of (metadata, score) tuples

        Returns:
            Dictionary mapping doc_id -> (rank, metadata)
        """
        rank_map = {}
        for rank, (metadata, score) in enumerate(results, start=1):
            doc_id = self._get_doc_id(metadata)
            rank_map[doc_id] = (rank, metadata)
        return rank_map

    def _get_doc_id(self, metadata: Dict) -> str:
        """
        Get a unique document ID from metadata.

        Args:
            metadata: Document metadata

        Returns:
            Unique document ID
        """
        # Use section + text prefix as unique ID
        section = metadata.get('section', 'unknown')
        text = metadata.get('text', '')
        text_prefix = text[:50] if text else ''
        return f"{section}:{text_prefix}"
