#!/usr/bin/env python3
"""
Evaluate hybrid search WITH re-ranking (the full solution).
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


def eval_config(name: str, use_hybrid: bool, use_reranking: bool, alpha: float = 0.7):
    """Evaluate a configuration."""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"{'='*80}")

    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest", batch_size=12)
    generator = OllamaClient(model_name="llama3.1:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))
    manager.load_store("hierarchical", dimension=768)

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
                print(f"  Status: ACCEPTABLE")
            else:
                print(f"  Status: WRONG")

    print(f"\n{'='*80}")
    print(f"RESULTS: {name}")
    print(f"{'='*80}")
    print(f"Exact match: {correct}/10 ({correct*10}%)")
    print(f"Acceptable: {acceptable}/10 ({acceptable*10}%)")
    print(f"Total: {correct+acceptable}/10 ({(correct+acceptable)*10}%)")
    print(f"Avg time: {total_time/10:.2f}s")

    return {'name': name, 'correct': correct, 'acceptable': acceptable, 'time': total_time/10}


def main():
    print("="*80)
    print("HYBRID SEARCH + RE-RANKING EVALUATION")
    print("="*80)

    results = []

    # Phase 3 baseline: Semantic + reranking
    results.append(eval_config(
        "Phase 3: Semantic + reranking",
        use_hybrid=False,
        use_reranking=True
    ))
    time.sleep(2)

    # Phase 4: Hybrid + reranking (our solution)
    results.append(eval_config(
        "Phase 4: Hybrid (0.7) + reranking",
        use_hybrid=True,
        use_reranking=True,
        alpha=0.7
    ))
    time.sleep(2)

    # Try different alpha
    results.append(eval_config(
        "Phase 4: Hybrid (0.6) + reranking",
        use_hybrid=True,
        use_reranking=True,
        alpha=0.6
    ))

    # Summary
    print(f"\n{'='*80}")
    print("FINAL COMPARISON")
    print(f"{'='*80}\n")
    print(f"{'Configuration':<40} {'Exact':<10} {'Accept':<10} {'Total':<10} {'Time':<10}")
    print("-"*80)

    for r in results:
        total = r['correct'] + r['acceptable']
        print(f"{r['name']:<40} {r['correct']}/10    {r['acceptable']}/10    {total}/10    {r['time']:.2f}s")

    # Calculate improvement
    if len(results) >= 2:
        baseline = results[0]
        hybrid = results[1]
        improvement = (hybrid['correct'] - baseline['correct']) * 10
        print(f"\n{'='*80}")
        print(f"IMPROVEMENT: {improvement:+d}% exact match rate")
        print(f"{'='*80}")


if __name__ == "__main__":
    main()
