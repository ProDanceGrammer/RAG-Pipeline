"""Evaluation framework for comparing chunking strategies."""
import time
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

from .metrics import RAGMetrics, ChunkQualityMetrics, PerformanceMetrics
from ..chunking.base_chunker import BaseChunker
from ..core.ollama_embedder import OllamaEmbedder
from ..rag.multi_store_manager import MultiStoreManager

logger = logging.getLogger(__name__)


class ChunkingEvaluator:
    """Evaluates and compares chunking strategies."""

    def __init__(
        self,
        embedder: OllamaEmbedder,
        manager: MultiStoreManager
    ):
        """
        Initialize evaluator.

        Args:
            embedder: Embedder instance
            manager: Multi-store manager
        """
        self.embedder = embedder
        self.manager = manager
        self.rag_metrics = RAGMetrics()
        self.chunk_metrics = ChunkQualityMetrics()
        self.perf_metrics = PerformanceMetrics()
        self.logger = logging.getLogger(__name__)

    def evaluate_retrieval(
        self,
        strategy_name: str,
        query: str,
        relevant_chunk_ids: set,
        top_k: int = 5
    ) -> Dict[str, float]:
        """
        Evaluate retrieval quality for a query.

        Args:
            strategy_name: Name of chunking strategy
            query: Query text
            relevant_chunk_ids: Set of relevant chunk IDs
            top_k: Number of results to retrieve

        Returns:
            Dictionary of metric scores
        """
        self.logger.info(f"Evaluating retrieval for strategy: {strategy_name}")

        # Measure query latency
        start_time = time.time()

        # Embed query
        query_emb = self.embedder.embed_single(query)

        # Search
        results = self.manager.search(strategy_name, query_emb, top_k=top_k)

        end_time = time.time()

        # Extract metadata
        retrieved_chunks = [metadata for metadata, score in results]

        # Calculate metrics
        metrics = {
            'precision': self.rag_metrics.context_precision(
                retrieved_chunks, relevant_chunk_ids, top_k
            ),
            'recall': self.rag_metrics.context_recall(
                retrieved_chunks, relevant_chunk_ids
            ),
            'mrr': self.rag_metrics.mean_reciprocal_rank(
                retrieved_chunks, relevant_chunk_ids
            ),
            'latency': self.perf_metrics.query_latency(start_time, end_time),
        }

        # Calculate relevancy from similarity scores
        similarity_scores = [1.0 / (1.0 + score) for metadata, score in results]
        metrics['relevancy'] = self.rag_metrics.context_relevancy(
            retrieved_chunks, similarity_scores
        )

        self.logger.info(f"Retrieval metrics: {metrics}")
        return metrics

    def evaluate_chunk_quality(
        self,
        chunks: List,
        strategy_name: str
    ) -> Dict[str, float]:
        """
        Evaluate quality of chunks from a strategy.

        Args:
            chunks: List of chunks
            strategy_name: Name of chunking strategy

        Returns:
            Dictionary of quality metrics
        """
        self.logger.info(f"Evaluating chunk quality for: {strategy_name}")

        coherence_scores = []
        boundary_scores = []
        token_counts = []

        # Sample chunks to avoid long evaluation
        sample_size = min(20, len(chunks))
        sampled_chunks = np.random.choice(chunks, sample_size, replace=False)

        for chunk in sampled_chunks:
            # Semantic coherence (expensive, so sample)
            try:
                coherence = self.chunk_metrics.semantic_coherence(
                    chunk.text, self.embedder
                )
                coherence_scores.append(coherence)
            except Exception as e:
                self.logger.warning(f"Failed to calculate coherence: {e}")

            # Boundary quality
            boundary = self.chunk_metrics.boundary_quality(chunk.text)
            boundary_scores.append(boundary)

            # Token count
            tokens = chunk.metadata.get('tokens', 0)
            token_counts.append(tokens)

        metrics = {
            'avg_coherence': np.mean(coherence_scores) if coherence_scores else 0.0,
            'avg_boundary_quality': np.mean(boundary_scores),
            'avg_tokens': np.mean(token_counts),
            'std_tokens': np.std(token_counts),
            'min_tokens': np.min(token_counts),
            'max_tokens': np.max(token_counts),
        }

        self.logger.info(f"Chunk quality metrics: {metrics}")
        return metrics

    def compare_strategies(
        self,
        strategies: Dict[str, BaseChunker],
        test_queries: List[Tuple[str, set]],
        document_text: str
    ) -> Dict[str, Dict]:
        """
        Compare multiple chunking strategies.

        Args:
            strategies: Dictionary of strategy_name -> chunker
            test_queries: List of (query, relevant_chunk_ids) tuples
            document_text: Document text to chunk

        Returns:
            Dictionary of strategy_name -> metrics
        """
        self.logger.info(f"Comparing {len(strategies)} strategies on {len(test_queries)} queries")

        results = {}

        for strategy_name, chunker in strategies.items():
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Evaluating strategy: {strategy_name}")
            self.logger.info(f"{'='*60}")

            # Chunk document
            start_time = time.time()
            chunks = chunker.chunk(document_text)
            chunk_time = time.time() - start_time

            self.logger.info(f"Created {len(chunks)} chunks in {chunk_time:.2f}s")

            # Evaluate chunk quality
            quality_metrics = self.evaluate_chunk_quality(chunks, strategy_name)

            # Evaluate retrieval on test queries
            retrieval_metrics = []

            for query, relevant_ids in test_queries:
                try:
                    metrics = self.evaluate_retrieval(
                        strategy_name, query, relevant_ids, top_k=5
                    )
                    retrieval_metrics.append(metrics)
                except Exception as e:
                    self.logger.error(f"Failed to evaluate query '{query}': {e}")

            # Aggregate retrieval metrics
            avg_retrieval = {}
            if retrieval_metrics:
                for key in retrieval_metrics[0].keys():
                    values = [m[key] for m in retrieval_metrics]
                    avg_retrieval[f'avg_{key}'] = np.mean(values)
                    avg_retrieval[f'std_{key}'] = np.std(values)

            # Combine results
            results[strategy_name] = {
                'num_chunks': len(chunks),
                'chunk_time': chunk_time,
                'quality': quality_metrics,
                'retrieval': avg_retrieval,
            }

        self.logger.info(f"\n{'='*60}")
        self.logger.info("Comparison complete")
        self.logger.info(f"{'='*60}")

        return results

    def cross_validate(
        self,
        strategy_name: str,
        chunker: BaseChunker,
        documents: List[str],
        test_queries_per_doc: List[List[Tuple[str, set]]],
        k_folds: int = 5
    ) -> Dict[str, List[float]]:
        """
        Perform cross-validation on a chunking strategy.

        Args:
            strategy_name: Name of strategy
            chunker: Chunker instance
            documents: List of document texts
            test_queries_per_doc: List of query sets per document
            k_folds: Number of folds

        Returns:
            Dictionary of metric_name -> list of scores per fold
        """
        self.logger.info(f"Cross-validating {strategy_name} with {k_folds} folds")

        fold_size = len(documents) // k_folds
        all_metrics = {
            'precision': [],
            'recall': [],
            'mrr': [],
            'relevancy': [],
            'latency': [],
        }

        for fold in range(k_folds):
            self.logger.info(f"\nFold {fold + 1}/{k_folds}")

            # Split data
            start_idx = fold * fold_size
            end_idx = start_idx + fold_size if fold < k_folds - 1 else len(documents)

            test_docs = documents[start_idx:end_idx]
            test_queries = test_queries_per_doc[start_idx:end_idx]

            # Evaluate on test set
            for doc, queries in zip(test_docs, test_queries):
                for query, relevant_ids in queries:
                    try:
                        metrics = self.evaluate_retrieval(
                            strategy_name, query, relevant_ids
                        )
                        for key, value in metrics.items():
                            if key in all_metrics:
                                all_metrics[key].append(value)
                    except Exception as e:
                        self.logger.error(f"Failed on fold {fold}: {e}")

        # Calculate statistics
        stats = {}
        for metric, values in all_metrics.items():
            if values:
                stats[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                }

        self.logger.info(f"Cross-validation complete: {stats}")
        return stats

    def generate_report(
        self,
        comparison_results: Dict[str, Dict],
        output_path: Path
    ) -> None:
        """
        Generate evaluation report.

        Args:
            comparison_results: Results from compare_strategies
            output_path: Path to save report
        """
        self.logger.info(f"Generating report: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Chunking Strategy Evaluation Report\n\n")

            # Summary table
            f.write("## Summary\n\n")
            f.write("| Strategy | Chunks | Avg Precision | Avg Recall | Avg MRR | Avg Latency (s) |\n")
            f.write("|----------|--------|---------------|------------|---------|------------------|\n")

            for strategy, results in comparison_results.items():
                retrieval = results.get('retrieval', {})
                f.write(
                    f"| {strategy} | {results['num_chunks']} | "
                    f"{retrieval.get('avg_precision', 0):.4f} | "
                    f"{retrieval.get('avg_recall', 0):.4f} | "
                    f"{retrieval.get('avg_mrr', 0):.4f} | "
                    f"{retrieval.get('avg_latency', 0):.4f} |\n"
                )

            # Detailed results
            f.write("\n## Detailed Results\n\n")

            for strategy, results in comparison_results.items():
                f.write(f"### {strategy}\n\n")

                f.write(f"**Chunks**: {results['num_chunks']}\n")
                f.write(f"**Chunking time**: {results['chunk_time']:.2f}s\n\n")

                f.write("**Quality Metrics**:\n")
                quality = results.get('quality', {})
                for key, value in quality.items():
                    f.write(f"- {key}: {value:.4f}\n")

                f.write("\n**Retrieval Metrics**:\n")
                retrieval = results.get('retrieval', {})
                for key, value in retrieval.items():
                    f.write(f"- {key}: {value:.4f}\n")

                f.write("\n")

        self.logger.info(f"Report saved to {output_path}")
