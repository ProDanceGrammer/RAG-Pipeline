#!/usr/bin/env python3
"""
Evaluate hybrid search performance with different configurations.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.rag_pipeline import RAGPipeline
from src.core.ollama_client import OllamaClient
from tests.test_queries import TEST_QUERIES
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def evaluate_configuration(
    config_name: str,
    use_hybrid: bool,
    use_reranking: bool,
    alpha: float = 0.7
):
    """
    Evaluate a specific configuration.

    Args:
        config_name: Name of the configuration
        use_hybrid: Enable hybrid search
        use_reranking: Enable re-ranking
        alpha: Hybrid search alpha parameter

    Returns:
        Dictionary with results
    """
    print(f"\n{'='*80}")
    print(f"Testing: {config_name}")
    print(f"{'='*80}")

    # Initialize components
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest", batch_size=12)
    generator = OllamaClient(model_name="llama3.1:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))

    # Load vector store
    try:
        manager.load_store("hierarchical", dimension=768)
        logger.info(f"Loaded hierarchical store")
    except Exception as e:
        logger.error(f"Failed to load store: {e}")
        return None

    # Create pipeline with configuration
    pipeline = RAGPipeline(
        embedder=embedder,
        generator=generator,
        manager=manager,
        strategy_name="hierarchical",
        top_k=5,
        use_reranking=use_reranking,
        use_topic_filtering=False,
        use_hybrid_search=use_hybrid,
        hybrid_alpha=alpha
    )

    # Evaluate on test queries
    results = []
    total_time = 0

    # Use first 10 queries for quick evaluation
    test_queries = TEST_QUERIES[:10]

    for i, query_data in enumerate(test_queries, 1):
        query = query_data["query"]
        expected = query_data["expected_sections"]
        topic = query_data["topic"]
        difficulty = query_data["difficulty"]

        print(f"\n[{i}/{len(test_queries)}] Query: {query}")
        print(f"  Topic: {topic}, Difficulty: {difficulty}")
        print(f"  Expected: {expected}")

        try:
            start_time = time.time()
            retrieved = pipeline.retrieve(query)
            retrieval_time = time.time() - start_time
            total_time += retrieval_time

            if retrieved:
                top_section = retrieved[0][0].get('section', 'N/A')
                top_score = retrieved[0][1]

                # Get top 3 sections
                top_3_sections = [
                    metadata.get('section', 'N/A')
                    for metadata, score in retrieved[:3]
                ]

                print(f"  Retrieved: {top_3_sections}")
                print(f"  Top: {top_section} (score: {top_score:.4f})")
                print(f"  Time: {retrieval_time:.2f}s")

                # Check if top section matches expected
                is_correct = any(
                    exp.lower() in top_section.lower()
                    for exp in expected
                )

                # Check if any expected section in top 3
                is_acceptable = any(
                    any(exp.lower() in sec.lower() for exp in expected)
                    for sec in top_3_sections
                )

                results.append({
                    'query': query,
                    'topic': topic,
                    'difficulty': difficulty,
                    'expected': expected,
                    'top_section': top_section,
                    'top_3_sections': top_3_sections,
                    'top_score': top_score,
                    'retrieval_time': retrieval_time,
                    'is_correct': is_correct,
                    'is_acceptable': is_acceptable
                })

                status = "CORRECT" if is_correct else ("ACCEPTABLE" if is_acceptable else "WRONG")
                print(f"  Status: {status}")
            else:
                print(f"  → No results")
                results.append({
                    'query': query,
                    'topic': topic,
                    'difficulty': difficulty,
                    'expected': expected,
                    'top_section': None,
                    'top_3_sections': [],
                    'top_score': None,
                    'retrieval_time': retrieval_time,
                    'is_correct': False,
                    'is_acceptable': False
                })

        except Exception as e:
            print(f"  ERROR: {e}")
            logger.error(f"Error evaluating query: {e}", exc_info=True)
            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'expected': expected,
                'top_section': None,
                'top_3_sections': [],
                'top_score': None,
                'retrieval_time': 0,
                'is_correct': False,
                'is_acceptable': False,
                'error': str(e)
            })

    # Calculate metrics
    correct_count = sum(1 for r in results if r['is_correct'])
    acceptable_count = sum(1 for r in results if r['is_acceptable'])
    avg_time = total_time / len(results) if results else 0

    print(f"\n{'='*80}")
    print(f"RESULTS: {config_name}")
    print(f"{'='*80}")
    print(f"Exact match: {correct_count}/{len(results)} ({correct_count/len(results)*100:.1f}%)")
    print(f"Acceptable: {acceptable_count}/{len(results)} ({acceptable_count/len(results)*100:.1f}%)")
    print(f"Avg retrieval time: {avg_time:.2f}s")

    return {
        'config_name': config_name,
        'results': results,
        'correct_count': correct_count,
        'acceptable_count': acceptable_count,
        'total_queries': len(results),
        'avg_time': avg_time
    }


def main():
    """Run evaluation on multiple configurations."""
    print("="*80)
    print("HYBRID SEARCH EVALUATION - PHASE 4")
    print("="*80)

    configurations = [
        ("Baseline (semantic only, no reranking)", False, False, 0.7),
        ("Semantic + reranking (Phase 3)", False, True, 0.7),
        ("Hybrid (alpha=0.7, no reranking)", True, False, 0.7),
        ("Hybrid (alpha=0.7) + reranking", True, True, 0.7),
        ("Hybrid (alpha=0.6) + reranking", True, True, 0.6),
        ("Hybrid (alpha=0.8) + reranking", True, True, 0.8),
    ]

    all_results = []

    for config_name, use_hybrid, use_reranking, alpha in configurations:
        result = evaluate_configuration(config_name, use_hybrid, use_reranking, alpha)
        if result:
            all_results.append(result)

        # Small delay between configurations
        time.sleep(2)

    # Summary comparison
    print(f"\n{'='*80}")
    print("SUMMARY COMPARISON")
    print(f"{'='*80}\n")

    print(f"{'Configuration':<45} {'Exact':<12} {'Acceptable':<12} {'Avg Time':<10}")
    print("-" * 80)

    for result in all_results:
        config = result['config_name']
        exact = f"{result['correct_count']}/{result['total_queries']}"
        exact_pct = f"({result['correct_count']/result['total_queries']*100:.0f}%)"
        acceptable = f"{result['acceptable_count']}/{result['total_queries']}"
        acc_pct = f"({result['acceptable_count']/result['total_queries']*100:.0f}%)"
        avg_time = f"{result['avg_time']:.2f}s"

        print(f"{config:<45} {exact:<6} {exact_pct:<6} {acceptable:<6} {acc_pct:<6} {avg_time:<10}")

    # Save detailed results
    output_path = Path("docs/EVALUATION_RESULTS_PHASE4.md")
    save_detailed_results(all_results, output_path)

    print(f"\n{'='*80}")
    print("EVALUATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nDetailed results saved to: {output_path}")


def save_detailed_results(all_results, output_path):
    """Save detailed results to markdown file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# RAG Pipeline Hybrid Search Evaluation - Phase 4\n\n")
        f.write(f"**Date**: 2026-05-14\n")
        f.write(f"**Configurations tested**: {len(all_results)}\n")
        f.write(f"**Queries per configuration**: 10\n\n")

        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write("| Configuration | Exact Match | Acceptable | Avg Time |\n")
        f.write("|---------------|-------------|------------|----------|\n")

        for result in all_results:
            config = result['config_name']
            exact = f"{result['correct_count']}/{result['total_queries']}"
            exact_pct = f"{result['correct_count']/result['total_queries']*100:.0f}%"
            acceptable = f"{result['acceptable_count']}/{result['total_queries']}"
            acc_pct = f"{result['acceptable_count']/result['total_queries']*100:.0f}%"
            avg_time = f"{result['avg_time']:.2f}s"

            f.write(f"| {config} | {exact} ({exact_pct}) | {acceptable} ({acc_pct}) | {avg_time} |\n")

        f.write("\n---\n\n")
        f.write("## Query-by-Query Results\n\n")

        # Get baseline for comparison
        if all_results:
            baseline = all_results[0]['results']

            for i, query_result in enumerate(baseline, 1):
                query = query_result['query']
                expected = query_result['expected']

                f.write(f"### Query {i}: \"{query}\"\n\n")
                f.write(f"**Expected**: {expected}\n\n")
                f.write("| Configuration | Top Section | Score | Status |\n")
                f.write("|---------------|-------------|-------|--------|\n")

                for result in all_results:
                    if i <= len(result['results']):
                        qr = result['results'][i-1]
                        config = result['config_name']
                        section = qr['top_section'] or 'N/A'
                        score = f"{qr['top_score']:.4f}" if qr['top_score'] else 'N/A'
                        status = "✅" if qr['is_correct'] else ("⚠️" if qr['is_acceptable'] else "❌")

                        f.write(f"| {config} | {section} | {score} | {status} |\n")

                f.write("\n")

    logger.info(f"Detailed results saved to {output_path}")


if __name__ == "__main__":
    main()
