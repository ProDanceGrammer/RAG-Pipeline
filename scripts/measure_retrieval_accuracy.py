#!/usr/bin/env python3
"""
Measure retrieval accuracy by comparing retrieved chunks against ground truth.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.test_queries import TEST_QUERIES
from src.rag.multi_store_manager import MultiStoreManager
from src.core.ollama_embedder import OllamaEmbedder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_precision_at_k(retrieved_sections: list, expected_sections: list, k: int = 3) -> float:
    """Calculate precision@k: fraction of retrieved items that are relevant."""
    retrieved_k = retrieved_sections[:k]
    relevant_count = 0

    for retrieved in retrieved_k:
        for expected in expected_sections:
            if expected.lower() in retrieved.lower():
                relevant_count += 1
                break

    return relevant_count / k if k > 0 else 0.0


def calculate_recall_at_k(retrieved_sections: list, expected_sections: list, k: int = 3) -> float:
    """Calculate recall@k: fraction of relevant items that were retrieved."""
    retrieved_k = retrieved_sections[:k]
    found_count = 0

    for expected in expected_sections:
        for retrieved in retrieved_k:
            if expected.lower() in retrieved.lower():
                found_count += 1
                break

    return found_count / len(expected_sections) if expected_sections else 0.0


def calculate_mrr(retrieved_sections: list, expected_sections: list) -> float:
    """Calculate Mean Reciprocal Rank: 1/rank of first relevant item."""
    for rank, retrieved in enumerate(retrieved_sections, 1):
        for expected in expected_sections:
            if expected.lower() in retrieved.lower():
                return 1.0 / rank
    return 0.0


def main():
    # Initialize components
    logger.info("Initializing RAG components...")
    embedder = OllamaEmbedder()
    base_dir = project_root / "data" / "vector_stores"
    store_manager = MultiStoreManager(base_dir=base_dir)

    # Load vector store
    store_path = project_root / "data" / "vector_stores" / "structure_store.faiss"
    if not store_path.exists():
        logger.error(f"Vector store not found: {store_path}")
        return

    store_manager.load_store("structure", str(store_path))
    logger.info(f"Loaded vector store with {store_manager.get_store('structure').count()} vectors")

    # Evaluate all queries
    results = []
    precision_scores = []
    recall_scores = []
    mrr_scores = []

    logger.info(f"\nEvaluating {len(TEST_QUERIES)} test queries...")
    logger.info("=" * 80)

    for i, test_query in enumerate(TEST_QUERIES, 1):
        query = test_query["query"]
        expected = test_query["expected_sections"]
        topic = test_query["topic"]
        difficulty = test_query["difficulty"]

        logger.info(f"\n[{i}/{len(TEST_QUERIES)}] Query: {query}")
        logger.info(f"  Topic: {topic}, Difficulty: {difficulty}")
        logger.info(f"  Expected sections: {expected}")

        # Retrieve chunks
        try:
            chunks = store_manager.search("structure", query, top_k=3)
            retrieved_sections = [chunk.metadata.get("section", "Unknown") for chunk in chunks]

            logger.info(f"  Retrieved sections: {retrieved_sections}")

            # Calculate metrics
            precision = calculate_precision_at_k(retrieved_sections, expected, k=3)
            recall = calculate_recall_at_k(retrieved_sections, expected, k=3)
            mrr = calculate_mrr(retrieved_sections, expected)

            logger.info(f"  Precision@3: {precision:.2%}")
            logger.info(f"  Recall@3: {recall:.2%}")
            logger.info(f"  MRR: {mrr:.3f}")

            precision_scores.append(precision)
            recall_scores.append(recall)
            mrr_scores.append(mrr)

            results.append({
                "query": query,
                "topic": topic,
                "difficulty": difficulty,
                "expected": expected,
                "retrieved": retrieved_sections,
                "precision": precision,
                "recall": recall,
                "mrr": mrr,
            })

        except Exception as e:
            logger.error(f"  ERROR: {e}")
            continue

    # Calculate overall metrics
    logger.info("\n" + "=" * 80)
    logger.info("OVERALL RESULTS:")
    logger.info("=" * 80)

    avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0
    avg_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0
    avg_mrr = sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0

    logger.info(f"\nAverage Precision@3: {avg_precision:.2%}")
    logger.info(f"Average Recall@3: {avg_recall:.2%}")
    logger.info(f"Average MRR: {avg_mrr:.3f}")
    logger.info(f"Queries evaluated: {len(results)}/{len(TEST_QUERIES)}")

    # Breakdown by topic
    logger.info("\nBREAKDOWN BY TOPIC:")
    for topic in ["OOP", "Python", "Database", "ML"]:
        topic_results = [r for r in results if r["topic"] == topic]
        if topic_results:
            topic_precision = sum(r["precision"] for r in topic_results) / len(topic_results)
            topic_recall = sum(r["recall"] for r in topic_results) / len(topic_results)
            logger.info(f"  {topic}: Precision={topic_precision:.2%}, Recall={topic_recall:.2%} ({len(topic_results)} queries)")

    # Breakdown by difficulty
    logger.info("\nBREAKDOWN BY DIFFICULTY:")
    for difficulty in ["easy", "medium", "hard"]:
        diff_results = [r for r in results if r["difficulty"] == difficulty]
        if diff_results:
            diff_precision = sum(r["precision"] for r in diff_results) / len(diff_results)
            diff_recall = sum(r["recall"] for r in diff_results) / len(diff_results)
            logger.info(f"  {difficulty}: Precision={diff_precision:.2%}, Recall={diff_recall:.2%} ({len(diff_results)} queries)")

    # Write detailed report
    output_path = project_root / "docs" / "RETRIEVAL_ACCURACY.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RETRIEVAL ACCURACY MEASUREMENT REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test queries: {len(TEST_QUERIES)}\n")
        f.write(f"Queries evaluated: {len(results)}\n\n")

        f.write("OVERALL METRICS:\n")
        f.write(f"  Average Precision@3: {avg_precision:.2%}\n")
        f.write(f"  Average Recall@3: {avg_recall:.2%}\n")
        f.write(f"  Average MRR: {avg_mrr:.3f}\n\n")

        f.write("BREAKDOWN BY TOPIC:\n")
        for topic in ["OOP", "Python", "Database", "ML"]:
            topic_results = [r for r in results if r["topic"] == topic]
            if topic_results:
                topic_precision = sum(r["precision"] for r in topic_results) / len(topic_results)
                topic_recall = sum(r["recall"] for r in topic_results) / len(topic_results)
                f.write(f"  {topic}: Precision={topic_precision:.2%}, Recall={topic_recall:.2%} ({len(topic_results)} queries)\n")

        f.write("\nBREAKDOWN BY DIFFICULTY:\n")
        for difficulty in ["easy", "medium", "hard"]:
            diff_results = [r for r in results if r["difficulty"] == difficulty]
            if diff_results:
                diff_precision = sum(r["precision"] for r in diff_results) / len(diff_results)
                diff_recall = sum(r["recall"] for r in diff_results) / len(diff_results)
                f.write(f"  {difficulty}: Precision={diff_precision:.2%}, Recall={diff_recall:.2%} ({len(diff_results)} queries)\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("DETAILED RESULTS:\n")
        f.write("=" * 80 + "\n\n")

        for i, result in enumerate(results, 1):
            f.write(f"[{i}] {result['query']}\n")
            f.write(f"    Topic: {result['topic']}, Difficulty: {result['difficulty']}\n")
            f.write(f"    Expected: {result['expected']}\n")
            f.write(f"    Retrieved: {result['retrieved']}\n")
            f.write(f"    Precision@3: {result['precision']:.2%}\n")
            f.write(f"    Recall@3: {result['recall']:.2%}\n")
            f.write(f"    MRR: {result['mrr']:.3f}\n\n")

    logger.info(f"\nDetailed report written to: {output_path}")


if __name__ == '__main__':
    main()
