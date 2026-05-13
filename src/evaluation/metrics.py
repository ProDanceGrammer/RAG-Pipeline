"""Evaluation metrics for RAG pipeline."""
import numpy as np
from typing import List, Dict, Tuple, Set
import logging

logger = logging.getLogger(__name__)


class RAGMetrics:
    """Metrics for evaluating RAG retrieval quality."""

    @staticmethod
    def context_precision(
        retrieved_chunks: List[Dict],
        relevant_chunk_ids: Set[int],
        top_k: int = None
    ) -> float:
        """
        Calculate context precision.

        Measures how many of the retrieved chunks are actually relevant.

        Args:
            retrieved_chunks: List of retrieved chunk metadata
            relevant_chunk_ids: Set of IDs of chunks that are relevant
            top_k: Consider only top K results (default: all)

        Returns:
            Precision score (0-1)
        """
        if not retrieved_chunks:
            return 0.0

        chunks_to_check = retrieved_chunks[:top_k] if top_k else retrieved_chunks

        relevant_retrieved = sum(
            1 for chunk in chunks_to_check
            if chunk.get('chunk_id') in relevant_chunk_ids
        )

        precision = relevant_retrieved / len(chunks_to_check)
        logger.debug(f"Context precision: {precision:.4f} ({relevant_retrieved}/{len(chunks_to_check)})")
        return precision

    @staticmethod
    def context_recall(
        retrieved_chunks: List[Dict],
        relevant_chunk_ids: Set[int]
    ) -> float:
        """
        Calculate context recall.

        Measures how many relevant chunks from the knowledge base were retrieved.

        Args:
            retrieved_chunks: List of retrieved chunk metadata
            relevant_chunk_ids: Set of IDs of all relevant chunks in corpus

        Returns:
            Recall score (0-1)
        """
        if not relevant_chunk_ids:
            return 0.0

        retrieved_ids = {chunk.get('chunk_id') for chunk in retrieved_chunks}
        relevant_retrieved = len(retrieved_ids & relevant_chunk_ids)

        recall = relevant_retrieved / len(relevant_chunk_ids)
        logger.debug(f"Context recall: {recall:.4f} ({relevant_retrieved}/{len(relevant_chunk_ids)})")
        return recall

    @staticmethod
    def context_relevancy(
        retrieved_chunks: List[Dict],
        relevance_scores: List[float]
    ) -> float:
        """
        Calculate context relevancy.

        Measures how well retrieved chunks align with user's intent.
        Uses similarity scores or manual relevance judgments.

        Args:
            retrieved_chunks: List of retrieved chunk metadata
            relevance_scores: Relevance score for each chunk (0-1)

        Returns:
            Average relevancy score (0-1)
        """
        if not retrieved_chunks or not relevance_scores:
            return 0.0

        avg_relevancy = np.mean(relevance_scores)
        logger.debug(f"Context relevancy: {avg_relevancy:.4f}")
        return float(avg_relevancy)

    @staticmethod
    def mean_reciprocal_rank(
        retrieved_chunks: List[Dict],
        relevant_chunk_ids: Set[int]
    ) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).

        Measures the rank of the first relevant result.

        Args:
            retrieved_chunks: List of retrieved chunk metadata (ordered by rank)
            relevant_chunk_ids: Set of IDs of relevant chunks

        Returns:
            MRR score (0-1)
        """
        for rank, chunk in enumerate(retrieved_chunks, start=1):
            if chunk.get('chunk_id') in relevant_chunk_ids:
                mrr = 1.0 / rank
                logger.debug(f"MRR: {mrr:.4f} (first relevant at rank {rank})")
                return mrr

        logger.debug("MRR: 0.0 (no relevant chunks found)")
        return 0.0

    @staticmethod
    def chunk_utilization(
        chunk_text: str,
        generated_answer: str,
        threshold: float = 0.3
    ) -> float:
        """
        Calculate chunk utilization.

        Measures how much of a chunk's content was used in the answer.
        Simple word overlap metric.

        Args:
            chunk_text: Text of the retrieved chunk
            generated_answer: Generated answer text
            threshold: Minimum word length to consider

        Returns:
            Utilization score (0-1)
        """
        # Tokenize and normalize
        chunk_words = set(
            word.lower()
            for word in chunk_text.split()
            if len(word) > threshold
        )
        answer_words = set(
            word.lower()
            for word in generated_answer.split()
            if len(word) > threshold
        )

        if not chunk_words:
            return 0.0

        overlap = len(chunk_words & answer_words)
        utilization = overlap / len(chunk_words)

        logger.debug(f"Chunk utilization: {utilization:.4f} ({overlap}/{len(chunk_words)} words)")
        return utilization

    @staticmethod
    def chunk_attribution(
        chunks: List[Dict],
        generated_answer: str,
        min_overlap: int = 3
    ) -> Dict[int, float]:
        """
        Calculate chunk attribution.

        Identifies which chunks contributed to the answer.

        Args:
            chunks: List of retrieved chunks with metadata
            generated_answer: Generated answer text
            min_overlap: Minimum word overlap to consider attribution

        Returns:
            Dictionary mapping chunk_id to attribution score
        """
        answer_words = set(
            word.lower()
            for word in generated_answer.split()
            if len(word) > 3
        )

        attributions = {}

        for chunk in chunks:
            chunk_id = chunk.get('chunk_id')
            chunk_text = chunk.get('text', '')

            chunk_words = set(
                word.lower()
                for word in chunk_text.split()
                if len(word) > 3
            )

            overlap = len(chunk_words & answer_words)

            if overlap >= min_overlap:
                attribution = overlap / len(answer_words) if answer_words else 0.0
                attributions[chunk_id] = attribution

        logger.debug(f"Chunk attribution: {len(attributions)} chunks contributed")
        return attributions


class ChunkQualityMetrics:
    """Metrics for evaluating chunk quality."""

    @staticmethod
    def semantic_coherence(chunk_text: str, embedder) -> float:
        """
        Calculate semantic coherence within a chunk.

        Measures how semantically similar sentences within a chunk are.

        Args:
            chunk_text: Text of the chunk
            embedder: Embedder instance to generate sentence embeddings

        Returns:
            Coherence score (0-1)
        """
        # Split into sentences
        sentences = [s.strip() for s in chunk_text.split('.') if s.strip()]

        if len(sentences) < 2:
            return 1.0  # Single sentence is perfectly coherent

        # Embed sentences
        embeddings = embedder.embed_texts(sentences)

        # Calculate pairwise similarities
        similarities = []
        for i in range(len(embeddings) - 1):
            sim = embedder.cosine_similarity(embeddings[i], embeddings[i + 1])
            similarities.append(sim)

        coherence = np.mean(similarities)
        logger.debug(f"Semantic coherence: {coherence:.4f}")
        return float(coherence)

    @staticmethod
    def boundary_quality(
        chunk_text: str,
        ends_with_punctuation: bool = True
    ) -> float:
        """
        Calculate boundary quality.

        Measures if chunk ends at natural boundaries (sentence/section).

        Args:
            chunk_text: Text of the chunk
            ends_with_punctuation: Whether to check for punctuation

        Returns:
            Quality score (0-1)
        """
        score = 0.0

        # Check if ends with sentence punctuation
        if chunk_text.rstrip().endswith(('.', '!', '?', '\n')):
            score += 0.5

        # Check if starts with capital letter or markdown header
        if chunk_text.lstrip().startswith(('#', '##', '###')) or chunk_text[0].isupper():
            score += 0.5

        logger.debug(f"Boundary quality: {score:.4f}")
        return score

    @staticmethod
    def token_efficiency(
        chunk_text: str,
        tokenizer,
        max_tokens: int = 512
    ) -> float:
        """
        Calculate token efficiency.

        Measures how well chunk uses available token budget.

        Args:
            chunk_text: Text of the chunk
            tokenizer: Tokenizer instance
            max_tokens: Maximum token budget

        Returns:
            Efficiency score (0-1)
        """
        tokens = tokenizer.count_tokens(chunk_text)
        efficiency = min(tokens / max_tokens, 1.0)

        logger.debug(f"Token efficiency: {efficiency:.4f} ({tokens}/{max_tokens} tokens)")
        return efficiency


class PerformanceMetrics:
    """Metrics for evaluating system performance."""

    @staticmethod
    def query_latency(start_time: float, end_time: float) -> float:
        """
        Calculate query latency.

        Args:
            start_time: Query start timestamp
            end_time: Query end timestamp

        Returns:
            Latency in seconds
        """
        latency = end_time - start_time
        logger.debug(f"Query latency: {latency:.4f}s")
        return latency

    @staticmethod
    def embedding_throughput(
        num_chunks: int,
        total_time: float
    ) -> float:
        """
        Calculate embedding throughput.

        Args:
            num_chunks: Number of chunks embedded
            total_time: Total time in seconds

        Returns:
            Chunks per second
        """
        throughput = num_chunks / total_time if total_time > 0 else 0.0
        logger.debug(f"Embedding throughput: {throughput:.2f} chunks/s")
        return throughput

    @staticmethod
    def cache_hit_rate(hits: int, total: int) -> float:
        """
        Calculate cache hit rate.

        Args:
            hits: Number of cache hits
            total: Total number of requests

        Returns:
            Hit rate (0-1)
        """
        rate = hits / total if total > 0 else 0.0
        logger.debug(f"Cache hit rate: {rate:.4f} ({hits}/{total})")
        return rate
