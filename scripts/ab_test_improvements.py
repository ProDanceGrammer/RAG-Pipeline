"""A/B test different improvement configurations."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.rag_pipeline import RAGPipeline
from src.core.ollama_client import OllamaClient
from tests.test_queries import get_all_queries
import random
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def evaluate_configuration(config_name, use_reranking, use_topic_filtering):
    """
    Evaluate a specific configuration.

    Args:
        config_name: Name of the configuration
        use_reranking: Enable re-ranking
        use_topic_filtering: Enable topic filtering

    Returns:
        List of result dictionaries
    """
    print(f"\n{'='*60}")
    print(f"Testing: {config_name}")
    print(f"{'='*60}")

    # Initialize components
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    generator = OllamaClient(model_name="llama3.1:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))
    manager.load_store("hierarchical", dimension=768)

    # Create pipeline with configuration
    pipeline = RAGPipeline(
        embedder=embedder,
        generator=generator,
        manager=manager,
        strategy_name="hierarchical",
        top_k=5,
        use_reranking=use_reranking,
        use_topic_filtering=use_topic_filtering
    )

    # Get test queries (same 10 as evaluation)
    all_queries = get_all_queries()
    random.seed(42)
    sample_queries = random.sample(all_queries, min(10, len(all_queries)))

    # Evaluate
    results = []
    total_time = 0

    for i, query_data in enumerate(sample_queries, 1):
        query = query_data["query"]
        topic = query_data["topic"]
        difficulty = query_data["difficulty"]

        print(f"\n[{i}/10] Query: {query}")
        print(f"  Topic: {topic}, Difficulty: {difficulty}")

        try:
            start_time = time.time()
            retrieved = pipeline.retrieve(query)
            retrieval_time = time.time() - start_time
            total_time += retrieval_time

            if retrieved:
                top_section = retrieved[0][0].get('section', 'N/A')
                top_score = retrieved[0][1]
                print(f"  -> {top_section} (score: {top_score:.2f})")
                print(f"  Retrieval time: {retrieval_time:.2f}s")

                # Get top 3 sections
                top_3_sections = [
                    metadata.get('section', 'N/A')
                    for metadata, score in retrieved[:3]
                ]

                results.append({
                    'query': query,
                    'topic': topic,
                    'difficulty': difficulty,
                    'top_section': top_section,
                    'top_score': top_score,
                    'top_3_sections': top_3_sections,
                    'retrieval_time': retrieval_time
                })
            else:
                print(f"  → No results")
                results.append({
                    'query': query,
                    'topic': topic,
                    'difficulty': difficulty,
                    'top_section': None,
                    'top_score': None,
                    'top_3_sections': [],
                    'retrieval_time': retrieval_time
                })

        except Exception as e:
            print(f"  ERROR: {e}")
            logger.error(f"Error evaluating query: {e}")
            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'top_section': None,
                'top_score': None,
                'top_3_sections': [],
                'retrieval_time': 0,
                'error': str(e)
            })

    avg_time = total_time / len(results) if results else 0
    print(f"\nAverage retrieval time: {avg_time:.2f}s")

    return results


def compare_results(all_results):
    """
    Compare results across all configurations.

    Args:
        all_results: Dictionary of config_name -> results

    Returns:
        Comparison statistics
    """
    print(f"\n{'='*60}")
    print("A/B TEST COMPARISON")
    print(f"{'='*60}")

    comparison = {}

    for config_name, results in all_results.items():
        valid_results = [r for r in results if r['top_section'] is not None]
        avg_time = sum(r['retrieval_time'] for r in results) / len(results) if results else 0

        comparison[config_name] = {
            'total_queries': len(results),
            'valid_results': len(valid_results),
            'avg_retrieval_time': avg_time
        }

        print(f"\n{config_name}:")
        print(f"  Valid results: {len(valid_results)}/{len(results)}")
        print(f"  Avg retrieval time: {avg_time:.2f}s")

    return comparison


def save_results(all_results, comparison):
    """
    Save A/B test results to markdown file.

    Args:
        all_results: Dictionary of config_name -> results
        comparison: Comparison statistics
    """
    output_path = Path("docs/EVALUATION_RESULTS_PHASE3.md")
    print(f"\nSaving results to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# RAG Pipeline A/B Test Results - Phase 3\n\n")
        f.write(f"**Date**: 2026-05-13\n")
        f.write(f"**Configurations tested**: {len(all_results)}\n")
        f.write(f"**Queries per configuration**: 10\n\n")

        f.write("---\n\n")
        f.write("## Configurations\n\n")
        f.write("1. **Baseline**: No improvements (current hierarchical system)\n")
        f.write("2. **Re-ranking only**: Cross-encoder re-ranking enabled\n")
        f.write("3. **Topic filtering only**: Topic-based filtering enabled\n")
        f.write("4. **Re-ranking + Topic filtering**: Both enabled\n\n")

        f.write("---\n\n")
        f.write("## Overall Comparison\n\n")
        f.write("| Configuration | Valid Results | Avg Retrieval Time |\n")
        f.write("|---------------|---------------|--------------------|\n")

        for config_name, stats in comparison.items():
            f.write(f"| {config_name} | {stats['valid_results']}/{stats['total_queries']} | {stats['avg_retrieval_time']:.2f}s |\n")

        f.write("\n---\n\n")
        f.write("## Query-by-Query Results\n\n")

        # Get baseline results for comparison
        baseline_results = all_results.get("Baseline (no improvements)", [])

        for i, baseline_result in enumerate(baseline_results, 1):
            query = baseline_result['query']
            topic = baseline_result['topic']

            f.write(f"### Query {i}: \"{query}\"\n\n")
            f.write(f"**Topic**: {topic}\n\n")
            f.write("| Configuration | Top Section | Score |\n")
            f.write("|---------------|-------------|-------|\n")

            for config_name, results in all_results.items():
                if i <= len(results):
                    result = results[i-1]
                    section = result['top_section'] or 'N/A'
                    score = f"{result['top_score']:.2f}" if result['top_score'] else 'N/A'
                    f.write(f"| {config_name} | {section} | {score} |\n")

            f.write("\n")

        f.write("---\n\n")
        f.write("## Analysis\n\n")
        f.write("**TODO**: Manual analysis of which configuration performs best\n\n")
        f.write("Compare:\n")
        f.write("- Correctness rate (manual evaluation needed)\n")
        f.write("- Retrieval time\n")
        f.write("- Which queries improved/regressed\n\n")

    print(f"Results saved to {output_path}")


def main():
    """Run A/B test on all configurations."""
    print("="*60)
    print("RAG PIPELINE A/B TEST - PHASE 3")
    print("="*60)

    configurations = [
        ("Baseline (no improvements)", False, False),
        ("Re-ranking only", True, False),
        ("Topic filtering only", False, True),
        ("Re-ranking + Topic filtering", True, True)
    ]

    all_results = {}

    for config_name, use_reranking, use_topic_filtering in configurations:
        results = evaluate_configuration(config_name, use_reranking, use_topic_filtering)
        all_results[config_name] = results

    # Compare results
    comparison = compare_results(all_results)

    # Save results
    save_results(all_results, comparison)

    print(f"\n{'='*60}")
    print("A/B TEST COMPLETE")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("1. Review docs/EVALUATION_RESULTS_PHASE3.md")
    print("2. Manually evaluate correctness for each configuration")
    print("3. Decide which configuration to enable by default")


if __name__ == "__main__":
    main()
