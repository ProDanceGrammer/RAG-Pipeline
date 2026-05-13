"""Run evaluation on chunking strategies."""
import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chunking.structure_chunker import StructureChunker
from src.chunking.hierarchical_chunker import HierarchicalChunker
from src.chunking.sliding_window_chunker import SlidingWindowChunker
from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from src.evaluation.evaluator import ChunkingEvaluator
from tests.test_queries import get_all_queries, get_queries_by_topic

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run evaluation."""
    print("=" * 60)
    print("CHUNKING STRATEGY EVALUATION")
    print("=" * 60)

    # Initialize
    print("\nInitializing components...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))
    evaluator = ChunkingEvaluator(embedder, manager)

    # Load existing stores
    print("Loading vector stores...")
    try:
        manager.load_store("structure", dimension=768)
        print("  Loaded structure store")
    except Exception as e:
        print(f"  Error loading structure store: {e}")
        return

    # Get test queries
    all_queries = get_all_queries()
    print(f"\nTest queries: {len(all_queries)}")

    # Evaluate retrieval on sample queries
    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION")
    print("=" * 60)

    # Sample 10 queries for evaluation
    import random
    random.seed(42)
    sample_queries = random.sample(all_queries, min(10, len(all_queries)))

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
            search_results = manager.search("structure", query_emb, top_k=5)

            # Display results
            print(f"  Results:")
            for j, (metadata, score) in enumerate(search_results[:3], 1):
                section = metadata.get('section', 'N/A')
                text_preview = metadata['text'][:80].encode('ascii', 'ignore').decode('ascii')
                print(f"    [{j}] Score: {score:.2f}, Section: {section}")
                print(f"        Text: {text_preview}...")

            # Store for analysis
            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'top_section': search_results[0][0].get('section', 'N/A') if search_results else None,
                'top_score': search_results[0][1] if search_results else None,
            })

        except Exception as e:
            print(f"  ERROR: {e}")

    # Summary by topic
    print("\n" + "=" * 60)
    print("SUMMARY BY TOPIC")
    print("=" * 60)

    topics = set(r['topic'] for r in results)
    for topic in topics:
        topic_results = [r for r in results if r['topic'] == topic]
        avg_score = sum(r['top_score'] for r in topic_results if r['top_score']) / len(topic_results)
        print(f"\n{topic}:")
        print(f"  Queries: {len(topic_results)}")
        print(f"  Avg top score: {avg_score:.2f}")

    # Summary by difficulty
    print("\n" + "=" * 60)
    print("SUMMARY BY DIFFICULTY")
    print("=" * 60)

    difficulties = set(r['difficulty'] for r in results)
    for difficulty in difficulties:
        diff_results = [r for r in results if r['difficulty'] == difficulty]
        avg_score = sum(r['top_score'] for r in diff_results if r['top_score']) / len(diff_results)
        print(f"\n{difficulty}:")
        print(f"  Queries: {len(diff_results)}")
        print(f"  Avg top score: {avg_score:.2f}")

    # Performance metrics
    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)

    stats = manager.get_stats()
    print(f"\nVector Store (structure):")
    print(f"  Total vectors: {stats['structure']['size']}")
    print(f"  Dimension: {stats['structure']['dimension']}")

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)

    # Save results
    output_path = Path("docs/EVALUATION_RESULTS.md")
    print(f"\nSaving results to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# RAG Pipeline Evaluation Results\n\n")
        f.write(f"**Date**: 2026-05-12\n")
        f.write(f"**Strategy**: Structure-based chunking\n")
        f.write(f"**Total queries tested**: {len(sample_queries)}\n\n")

        f.write("## Query Results\n\n")
        f.write("| Query | Topic | Difficulty | Top Section | Score |\n")
        f.write("|-------|-------|------------|-------------|-------|\n")

        for r in results:
            query_short = r['query'][:40] + "..." if len(r['query']) > 40 else r['query']
            section_short = r['top_section'][:30] if r['top_section'] else "N/A"
            score = f"{r['top_score']:.2f}" if r['top_score'] else "N/A"
            f.write(f"| {query_short} | {r['topic']} | {r['difficulty']} | {section_short} | {score} |\n")

        f.write("\n## Summary by Topic\n\n")
        for topic in topics:
            topic_results = [r for r in results if r['topic'] == topic]
            avg_score = sum(r['top_score'] for r in topic_results if r['top_score']) / len(topic_results)
            f.write(f"- **{topic}**: {len(topic_results)} queries, avg score: {avg_score:.2f}\n")

        f.write("\n## Summary by Difficulty\n\n")
        for difficulty in difficulties:
            diff_results = [r for r in results if r['difficulty'] == difficulty]
            avg_score = sum(r['top_score'] for r in diff_results if r['top_score']) / len(diff_results)
            f.write(f"- **{difficulty}**: {len(diff_results)} queries, avg score: {avg_score:.2f}\n")

        f.write("\n## Vector Store Stats\n\n")
        f.write(f"- Total vectors: {stats['structure']['size']}\n")
        f.write(f"- Dimension: {stats['structure']['dimension']}\n")

    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
