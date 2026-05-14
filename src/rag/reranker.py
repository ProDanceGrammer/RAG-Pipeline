"""Cross-encoder re-ranking for RAG retrieval."""
from sentence_transformers import CrossEncoder
import numpy as np
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """Re-rank search results using cross-encoder model."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize cross-encoder reranker.

        Args:
            model_name: Name of the cross-encoder model to use
        """
        self.model_name = model_name
        self.model = CrossEncoder(model_name)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Loaded cross-encoder model: {model_name}")

    def rerank(
        self,
        query: str,
        results: List[Tuple[Dict, float]],
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Re-rank results using cross-encoder.

        Args:
            query: Query text
            results: List of (metadata, l2_distance) tuples from initial retrieval
            top_k: Number of results to return after re-ranking

        Returns:
            Re-ranked list of (metadata, cross_encoder_score) tuples
            Note: Scores are now cross-encoder scores (higher is better)
        """
        if not results:
            return []

        self.logger.debug(f"Re-ranking {len(results)} results for query: {query[:50]}...")

        # Prepare pairs for cross-encoder
        pairs = [(query, metadata['text']) for metadata, _ in results]

        # Get cross-encoder scores
        scores = self.model.predict(pairs)

        # Combine metadata with new scores
        reranked = [
            (metadata, float(score))
            for (metadata, _), score in zip(results, scores)
        ]

        # Sort by cross-encoder score (higher is better)
        reranked.sort(key=lambda x: x[1], reverse=True)

        self.logger.debug(
            f"Re-ranked results - top score: {reranked[0][1]:.4f}, "
            f"bottom score: {reranked[-1][1]:.4f}"
        )

        return reranked[:top_k]
