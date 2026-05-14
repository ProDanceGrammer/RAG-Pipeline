#!/usr/bin/env python3
"""
Quick evaluation of hybrid search vs semantic-only.
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def quick_eval(use_hybrid: bool, alpha: float = 0.7):
    """Quick evaluation of a configuration."""
    config_name = f"Hybrid (alpha={alpha})" if use_hybrid else "Semantic only"
    print(f"\n{'='*80}")
    print(f"Testing: {config_name}")
    print(f"{'='*80}")

    # Initialize
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest", batch_size=12)
    generator = OllamaClient(model_name="llama3.1:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))
    manager.load_store("hierarchical", dimension=768)

    # Create pipeline
    pipeline = RAGPipeline(
        embedder=embedder,
        generator=generator,
        manager=manager,
        strategy_name="hierarchical",
        top_k=5,
        use_reranking=False,  # Disable for now
        use_topic_filtering=False,
        use_hybrid_search=use_hybrid,
        hybrid_alpha=alpha
    )

    # Test on first 10 queries
    test_queries = TEST_QUERIES[:10]
    correct = 0
    acceptable = 0
    total_time = 0

    for i, query_data in enumerate(test_queries, 1):
        query = query_data["query"]
        expected = query_data["expected_sections"]

        print(f"\n[{i}/10] {query}")
        print(f"  Expected: {expected[0] if expected else 'N/A'}")

        start = time.time()
        retrieved = pipeline.retrieve(query)
        elapsed = time.time() - start
        total_time += elapsed

        if retrieved:
            top_section = retrieved[0][0].get('section', 'N/A')
            print(f"  Retrieved: {top_section}")

            # Check correctness
            is_correct = any(exp.lower() in top_section.lower() for exp in expected)
            is_acceptable = any(
                any(exp.lower() in metadata.get('section', '').lower() for exp in expected)
                for metadata, _ in retrieved[:3]
            )

            if is_correct:
                correct += 1
                print(f"  Status: CORRECT")
            elif is_acceptable:
                acceptable += 1
                print(f"  Status: ACCEPTABLE (in top-3)")
            else:
                print(f"  Status: WRONG")

    print(f"\n{'='*80}")
    print(f"RESULTS: {config_name}")
    print(f"{'='*80}")
    print(f"Exact match: {correct}/10 ({correct*10}%)")
    print(f"Acceptable (top-3): {acceptable}/10 ({acceptable*10}%)")
    print(f"Total correct+acceptable: {correct+acceptable}/10 ({(correct+acceptable)*10}%)")
    print(f"Avg time: {total_time/10:.2f}s")

    return {
        'config': config_name,
        'correct': correct,
        'acceptable': acceptable,
        'avg_time': total_time/10
    }


def main():
    """Run quick evaluation."""
    print("="*80)
    print("QUICK HYBRID SEARCH EVALUATION")
    print("="*80)

    results = []

    # Test semantic only
    results.append(quick_eval(use_hybrid=False))
    time.sleep(2)

    # Test hybrid with different alphas
    for alpha in [0.5, 0.7, 0.8]:
        results.append(quick_eval(use_hybrid=True, alpha=alpha))
        time.sleep(2)

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    print(f"{'Configuration':<30} {'Exact':<10} {'Top-3':<10} {'Total':<10} {'Time':<10}")
    print("-"*80)

    for r in results:
        print(f"{r['config']:<30} {r['correct']}/10    {r['acceptable']}/10    {r['correct']+r['acceptable']}/10    {r['avg_time']:.2f}s")

    print(f"\n{'='*80}")
    print("EVALUATION COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
