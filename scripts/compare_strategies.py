"""Compare structure vs hierarchical chunking strategies."""
import sys
from pathlib import Path
import logging
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from tests.test_queries import get_all_queries

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def evaluate_strategy(strategy_name, embedder, manager, sample_queries):
    """Evaluate a single strategy on sample queries.

    Args:
        strategy_name: Name of the strategy ("structure" or "hierarchical")
        embedder: OllamaEmbedder instance
        manager: MultiStoreManager instance
        sample_queries: List of query dictionaries

    Returns:
        List of result dictionaries
    """
    print(f"\n{'=' * 60}")
    print(f"EVALUATING: {strategy_name.upper()}")
    print(f"{'=' * 60}")

    results = []

    for i, query_data in enumerate(sample_queries, 1):
        query = query_data["query"]
        topic = query_data["topic"]
        difficulty = query_data["difficulty"]

        print(f"\n[{i}/{len(sample_queries)}] Query: {query}")
        print(f"  Topic: {topic}, Difficulty: {difficulty}")

        try:
            # Embed query
            query_emb = embedder.embed_single(query)

            # Search
            search_results = manager.search(strategy_name, query_emb, top_k=5)

            # Display top 3 results
            print(f"  Results:")
            for j, (metadata, score) in enumerate(search_results[:3], 1):
                section = metadata.get('section', 'N/A')
                print(f"    [{j}] Score: {score:.2f}, Section: {section}")

            # Store for analysis
            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'top_section': search_results[0][0].get('section', 'N/A') if search_results else None,
                'top_score': float(search_results[0][1]) if search_results else None,
                'top_3_sections': [
                    metadata.get('section', 'N/A')
                    for metadata, score in search_results[:3]
                ]
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'top_section': None,
                'top_score': None,
                'top_3_sections': []
            })

    return results


def analyze_results(strategy_name, results):
    """Analyze and print results for a strategy.

    Args:
        strategy_name: Name of the strategy
        results: List of result dictionaries
    """
    print(f"\n{'=' * 60}")
    print(f"ANALYSIS: {strategy_name.upper()}")
    print(f"{'=' * 60}")

    # Overall metrics
    valid_results = [r for r in results if r['top_score'] is not None]
    avg_score = sum(r['top_score'] for r in valid_results) / len(valid_results) if valid_results else 0

    print(f"\nOverall:")
    print(f"  Total queries: {len(results)}")
    print(f"  Valid results: {len(valid_results)}")
    print(f"  Average top score: {avg_score:.2f}")

    # By topic
    print(f"\nBy Topic:")
    topics = set(r['topic'] for r in results)
    for topic in sorted(topics):
        topic_results = [r for r in valid_results if r['topic'] == topic]
        if topic_results:
            topic_avg = sum(r['top_score'] for r in topic_results) / len(topic_results)
            print(f"  {topic}: {len(topic_results)} queries, avg score: {topic_avg:.2f}")

    # By difficulty
    print(f"\nBy Difficulty:")
    difficulties = set(r['difficulty'] for r in results)
    for difficulty in sorted(difficulties):
        diff_results = [r for r in valid_results if r['difficulty'] == difficulty]
        if diff_results:
            diff_avg = sum(r['top_score'] for r in diff_results) / len(diff_results)
            print(f"  {difficulty}: {len(diff_results)} queries, avg score: {diff_avg:.2f}")


def compare_results(structure_results, hierarchical_results):
    """Compare results between two strategies.

    Args:
        structure_results: Results from structure strategy
        hierarchical_results: Results from hierarchical strategy
    """
    print(f"\n{'=' * 60}")
    print("COMPARISON: STRUCTURE vs HIERARCHICAL")
    print(f"{'=' * 60}")

    # Overall comparison
    structure_avg = sum(r['top_score'] for r in structure_results if r['top_score']) / len(structure_results)
    hierarchical_avg = sum(r['top_score'] for r in hierarchical_results if r['top_score']) / len(hierarchical_results)

    print(f"\nAverage Top Score:")
    print(f"  Structure:     {structure_avg:.2f}")
    print(f"  Hierarchical:  {hierarchical_avg:.2f}")
    print(f"  Difference:    {hierarchical_avg - structure_avg:.2f} ({'better' if hierarchical_avg < structure_avg else 'worse'})")

    # Query-by-query comparison
    print(f"\nQuery-by-Query Comparison:")
    better = 0
    worse = 0
    same = 0

    for s_result, h_result in zip(structure_results, hierarchical_results):
        if s_result['top_score'] and h_result['top_score']:
            diff = h_result['top_score'] - s_result['top_score']
            if diff < -1.0:  # Hierarchical is better (lower score)
                better += 1
            elif diff > 1.0:  # Hierarchical is worse
                worse += 1
            else:
                same += 1

    print(f"  Hierarchical better: {better}")
    print(f"  Hierarchical worse:  {worse}")
    print(f"  Similar:             {same}")

    # Topic comparison
    print(f"\nBy Topic:")
    topics = set(r['topic'] for r in structure_results)
    for topic in sorted(topics):
        s_topic = [r for r in structure_results if r['topic'] == topic and r['top_score']]
        h_topic = [r for r in hierarchical_results if r['topic'] == topic and r['top_score']]

        if s_topic and h_topic:
            s_avg = sum(r['top_score'] for r in s_topic) / len(s_topic)
            h_avg = sum(r['top_score'] for r in h_topic) / len(h_topic)
            diff = h_avg - s_avg
            print(f"  {topic}: Structure {s_avg:.2f}, Hierarchical {h_avg:.2f} (diff: {diff:+.2f})")


def save_comparison_report(structure_results, hierarchical_results, structure_stats, hierarchical_stats):
    """Save comparison report to markdown file.

    Args:
        structure_results: Results from structure strategy
        hierarchical_results: Results from hierarchical strategy
        structure_stats: Stats for structure store
        hierarchical_stats: Stats for hierarchical store
    """
    output_path = Path("docs/EVALUATION_COMPARISON.md")
    print(f"\nSaving comparison report to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# RAG Strategy Comparison: Structure vs Hierarchical\n\n")
        f.write(f"**Date**: 2026-05-13\n")
        f.write(f"**Queries tested**: {len(structure_results)}\n\n")

        f.write("---\n\n")
        f.write("## Vector Store Stats\n\n")
        f.write("| Metric | Structure | Hierarchical |\n")
        f.write("|--------|-----------|-------------|\n")
        f.write(f"| Total vectors | {structure_stats['size']} | {hierarchical_stats['size']} |\n")
        f.write(f"| Dimension | {structure_stats['dimension']} | {hierarchical_stats['dimension']} |\n\n")

        f.write("---\n\n")
        f.write("## Overall Performance\n\n")

        structure_avg = sum(r['top_score'] for r in structure_results if r['top_score']) / len(structure_results)
        hierarchical_avg = sum(r['top_score'] for r in hierarchical_results if r['top_score']) / len(hierarchical_results)

        f.write("| Metric | Structure | Hierarchical | Winner |\n")
        f.write("|--------|-----------|--------------|--------|\n")
        f.write(f"| Avg Top Score | {structure_avg:.2f} | {hierarchical_avg:.2f} | ")
        f.write(f"{'Hierarchical' if hierarchical_avg < structure_avg else 'Structure'} |\n\n")

        f.write("---\n\n")
        f.write("## Query Results\n\n")
        f.write("| # | Query | Topic | Structure Score | Hierarchical Score | Winner |\n")
        f.write("|---|-------|-------|-----------------|--------------------|---------|\n")

        for i, (s_result, h_result) in enumerate(zip(structure_results, hierarchical_results), 1):
            query_short = s_result['query'][:50] + "..." if len(s_result['query']) > 50 else s_result['query']
            s_score = f"{s_result['top_score']:.2f}" if s_result['top_score'] else "N/A"
            h_score = f"{h_result['top_score']:.2f}" if h_result['top_score'] else "N/A"

            winner = "Tie"
            if s_result['top_score'] and h_result['top_score']:
                diff = h_result['top_score'] - s_result['top_score']
                if diff < -1.0:
                    winner = "Hierarchical"
                elif diff > 1.0:
                    winner = "Structure"

            f.write(f"| {i} | {query_short} | {s_result['topic']} | {s_score} | {h_score} | {winner} |\n")

        f.write("\n---\n\n")
        f.write("## Performance by Topic\n\n")
        f.write("| Topic | Structure Avg | Hierarchical Avg | Difference |\n")
        f.write("|-------|---------------|------------------|------------|\n")

        topics = set(r['topic'] for r in structure_results)
        for topic in sorted(topics):
            s_topic = [r for r in structure_results if r['topic'] == topic and r['top_score']]
            h_topic = [r for r in hierarchical_results if r['topic'] == topic and r['top_score']]

            if s_topic and h_topic:
                s_avg = sum(r['top_score'] for r in s_topic) / len(s_topic)
                h_avg = sum(r['top_score'] for r in h_topic) / len(h_topic)
                diff = h_avg - s_avg
                f.write(f"| {topic} | {s_avg:.2f} | {h_avg:.2f} | {diff:+.2f} |\n")

        f.write("\n---\n\n")
        f.write("## Conclusion\n\n")

        if hierarchical_avg < structure_avg:
            f.write(f"**Winner: Hierarchical** (avg score {hierarchical_avg:.2f} vs {structure_avg:.2f})\n\n")
            f.write("Hierarchical chunking provides better retrieval accuracy with more context-rich chunks.\n")
        else:
            f.write(f"**Winner: Structure** (avg score {structure_avg:.2f} vs {hierarchical_avg:.2f})\n\n")
            f.write("Structure chunking provides better retrieval accuracy with simpler, more focused chunks.\n")

    print(f"Report saved to {output_path}")


def main():
    """Compare structure vs hierarchical chunking strategies."""
    print("=" * 60)
    print("STRATEGY COMPARISON: STRUCTURE vs HIERARCHICAL")
    print("=" * 60)

    # Initialize
    print("\nInitializing components...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))

    # Load both stores
    print("Loading vector stores...")
    try:
        manager.load_store("structure", dimension=768)
        print("  [OK] Loaded structure store")
    except Exception as e:
        print(f"  [ERROR] Error loading structure store: {e}")
        return

    try:
        manager.load_store("hierarchical", dimension=768)
        print("  [OK] Loaded hierarchical store")
    except Exception as e:
        print(f"  [ERROR] Error loading hierarchical store: {e}")
        return

    # Get test queries (same 10-query sample as evaluation)
    all_queries = get_all_queries()
    import random
    random.seed(42)
    sample_queries = random.sample(all_queries, min(10, len(all_queries)))

    print(f"\nTest queries: {len(sample_queries)}")

    # Evaluate structure strategy
    structure_results = evaluate_strategy("structure", embedder, manager, sample_queries)

    # Evaluate hierarchical strategy
    hierarchical_results = evaluate_strategy("hierarchical", embedder, manager, sample_queries)

    # Analyze each strategy
    analyze_results("structure", structure_results)
    analyze_results("hierarchical", hierarchical_results)

    # Compare strategies
    compare_results(structure_results, hierarchical_results)

    # Get stats
    stats = manager.get_stats()
    structure_stats = stats['structure']
    hierarchical_stats = stats['hierarchical']

    # Save comparison report
    save_comparison_report(structure_results, hierarchical_results, structure_stats, hierarchical_stats)

    print(f"\n{'=' * 60}")
    print("COMPARISON COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
