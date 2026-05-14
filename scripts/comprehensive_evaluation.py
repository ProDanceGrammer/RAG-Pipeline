#!/usr/bin/env python3
"""
Comprehensive evaluation with scoring for Phase 4.
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

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def calculate_scores(retrieved_sections, expected_sections):
    """Calculate precision, recall, and MRR scores."""
    # Precision@3: fraction of top-3 that are relevant
    relevant_in_top3 = 0
    for retrieved in retrieved_sections[:3]:
        for expected in expected_sections:
            if expected.lower() in retrieved.lower():
                relevant_in_top3 += 1
                break
    precision = relevant_in_top3 / 3 if len(retrieved_sections) >= 3 else 0

    # Recall@3: fraction of expected that were retrieved in top-3
    found_count = 0
    for expected in expected_sections:
        for retrieved in retrieved_sections[:3]:
            if expected.lower() in retrieved.lower():
                found_count += 1
                break
    recall = found_count / len(expected_sections) if expected_sections else 0

    # MRR: 1/rank of first relevant item
    mrr = 0.0
    for rank, retrieved in enumerate(retrieved_sections, 1):
        for expected in expected_sections:
            if expected.lower() in retrieved.lower():
                mrr = 1.0 / rank
                break
        if mrr > 0:
            break

    return precision, recall, mrr


def evaluate_full(config_name, use_hybrid, use_reranking, alpha=0.7):
    """Full evaluation with detailed scoring."""
    print(f"\n{'='*80}")
    print(f"EVALUATING: {config_name}")
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

    # Use all 26 test queries
    results = []
    total_time = 0

    correct = 0
    acceptable = 0

    all_precision = []
    all_recall = []
    all_mrr = []

    for i, query_data in enumerate(TEST_QUERIES, 1):
        query = query_data["query"]
        expected = query_data["expected_sections"]
        topic = query_data["topic"]
        difficulty = query_data["difficulty"]

        print(f"[{i}/{len(TEST_QUERIES)}] {query[:60]}...")

        start = time.time()
        retrieved = pipeline.retrieve(query)
        elapsed = time.time() - start
        total_time += elapsed

        if retrieved:
            retrieved_sections = [m.get('section', 'N/A') for m, _ in retrieved]
            top_section = retrieved_sections[0]

            # Check correctness
            is_correct = any(exp.lower() in top_section.lower() for exp in expected)
            is_acceptable = any(
                any(exp.lower() in sec.lower() for exp in expected)
                for sec in retrieved_sections[:3]
            )

            if is_correct:
                correct += 1
                status = "CORRECT"
            elif is_acceptable:
                acceptable += 1
                status = "ACCEPTABLE"
            else:
                status = "WRONG"

            # Calculate scores
            precision, recall, mrr = calculate_scores(retrieved_sections, expected)
            all_precision.append(precision)
            all_recall.append(recall)
            all_mrr.append(mrr)

            print(f"  Top: {top_section[:50]}")
            print(f"  Status: {status} | P@3: {precision:.2f} | R@3: {recall:.2f} | MRR: {mrr:.2f}")

            results.append({
                'query': query,
                'topic': topic,
                'difficulty': difficulty,
                'expected': expected,
                'retrieved': retrieved_sections[:3],
                'top_section': top_section,
                'is_correct': is_correct,
                'is_acceptable': is_acceptable,
                'precision': precision,
                'recall': recall,
                'mrr': mrr,
                'time': elapsed
            })
        else:
            print(f"  Status: NO RESULTS")
            all_precision.append(0)
            all_recall.append(0)
            all_mrr.append(0)

    # Calculate overall metrics
    avg_precision = sum(all_precision) / len(all_precision) if all_precision else 0
    avg_recall = sum(all_recall) / len(all_recall) if all_recall else 0
    avg_mrr = sum(all_mrr) / len(all_mrr) if all_mrr else 0
    avg_time = total_time / len(TEST_QUERIES)

    print(f"\n{'='*80}")
    print(f"RESULTS: {config_name}")
    print(f"{'='*80}")
    print(f"Exact match:     {correct}/{len(TEST_QUERIES)} ({correct/len(TEST_QUERIES)*100:.1f}%)")
    print(f"Acceptable:      {acceptable}/{len(TEST_QUERIES)} ({acceptable/len(TEST_QUERIES)*100:.1f}%)")
    print(f"Total correct:   {correct+acceptable}/{len(TEST_QUERIES)} ({(correct+acceptable)/len(TEST_QUERIES)*100:.1f}%)")
    print(f"Avg Precision@3: {avg_precision:.3f}")
    print(f"Avg Recall@3:    {avg_recall:.3f}")
    print(f"Avg MRR:         {avg_mrr:.3f}")
    print(f"Avg latency:     {avg_time:.2f}s")

    # Breakdown by topic
    print(f"\nBREAKDOWN BY TOPIC:")
    for topic in ["OOP", "Python", "Database", "ML"]:
        topic_results = [r for r in results if r['topic'] == topic]
        if topic_results:
            topic_correct = sum(1 for r in topic_results if r['is_correct'])
            topic_precision = sum(r['precision'] for r in topic_results) / len(topic_results)
            topic_recall = sum(r['recall'] for r in topic_results) / len(topic_results)
            print(f"  {topic:8} - Exact: {topic_correct}/{len(topic_results)} | P@3: {topic_precision:.2f} | R@3: {topic_recall:.2f}")

    # Breakdown by difficulty
    print(f"\nBREAKDOWN BY DIFFICULTY:")
    for difficulty in ["easy", "medium", "hard"]:
        diff_results = [r for r in results if r['difficulty'] == difficulty]
        if diff_results:
            diff_correct = sum(1 for r in diff_results if r['is_correct'])
            diff_precision = sum(r['precision'] for r in diff_results) / len(diff_results)
            diff_recall = sum(r['recall'] for r in diff_results) / len(diff_results)
            print(f"  {difficulty:6} - Exact: {diff_correct}/{len(diff_results)} | P@3: {diff_precision:.2f} | R@3: {diff_recall:.2f}")

    return {
        'config': config_name,
        'correct': correct,
        'acceptable': acceptable,
        'total': len(TEST_QUERIES),
        'precision': avg_precision,
        'recall': avg_recall,
        'mrr': avg_mrr,
        'time': avg_time,
        'results': results
    }


def main():
    print("="*80)
    print("COMPREHENSIVE EVALUATION WITH SCORING")
    print("="*80)

    all_results = []

    # Baseline: Semantic only (no reranking, no hybrid)
    print("\n\n### BASELINE: Semantic Only ###")
    all_results.append(evaluate_full(
        "Baseline: Semantic only",
        use_hybrid=False,
        use_reranking=False
    ))
    time.sleep(2)

    # Phase 3: Semantic + reranking
    print("\n\n### PHASE 3: Semantic + Re-ranking ###")
    all_results.append(evaluate_full(
        "Phase 3: Semantic + reranking",
        use_hybrid=False,
        use_reranking=True
    ))
    time.sleep(2)

    # Phase 4: Hybrid + reranking (alpha=0.6)
    print("\n\n### PHASE 4: Hybrid + Re-ranking ###")
    all_results.append(evaluate_full(
        "Phase 4: Hybrid (0.6) + reranking",
        use_hybrid=True,
        use_reranking=True,
        alpha=0.6
    ))

    # Final comparison
    print(f"\n\n{'='*80}")
    print("FINAL COMPARISON - ALL CONFIGURATIONS")
    print(f"{'='*80}\n")

    print(f"{'Configuration':<35} {'Exact':<12} {'Total':<12} {'P@3':<8} {'R@3':<8} {'MRR':<8} {'Time':<8}")
    print("-"*80)

    for r in all_results:
        exact_pct = f"{r['correct']}/{r['total']} ({r['correct']/r['total']*100:.0f}%)"
        total_pct = f"{r['correct']+r['acceptable']}/{r['total']} ({(r['correct']+r['acceptable'])/r['total']*100:.0f}%)"
        print(f"{r['config']:<35} {exact_pct:<12} {total_pct:<12} {r['precision']:.3f}  {r['recall']:.3f}  {r['mrr']:.3f}  {r['time']:.2f}s")

    # Calculate improvements
    if len(all_results) >= 3:
        baseline = all_results[0]
        phase3 = all_results[1]
        phase4 = all_results[2]

        print(f"\n{'='*80}")
        print("IMPROVEMENTS")
        print(f"{'='*80}")
        print(f"Phase 3 vs Baseline:")
        print(f"  Exact match: {(phase3['correct'] - baseline['correct'])/baseline['total']*100:+.1f}%")
        print(f"  Precision@3: {(phase3['precision'] - baseline['precision']):+.3f}")
        print(f"  Recall@3:    {(phase3['recall'] - baseline['recall']):+.3f}")
        print(f"  MRR:         {(phase3['mrr'] - baseline['mrr']):+.3f}")

        print(f"\nPhase 4 vs Phase 3:")
        print(f"  Exact match: {(phase4['correct'] - phase3['correct'])/phase3['total']*100:+.1f}%")
        print(f"  Precision@3: {(phase4['precision'] - phase3['precision']):+.3f}")
        print(f"  Recall@3:    {(phase4['recall'] - phase3['recall']):+.3f}")
        print(f"  MRR:         {(phase4['mrr'] - phase3['mrr']):+.3f}")

        print(f"\nPhase 4 vs Baseline:")
        print(f"  Exact match: {(phase4['correct'] - baseline['correct'])/baseline['total']*100:+.1f}%")
        print(f"  Precision@3: {(phase4['precision'] - baseline['precision']):+.3f}")
        print(f"  Recall@3:    {(phase4['recall'] - baseline['recall']):+.3f}")
        print(f"  MRR:         {(phase4['mrr'] - baseline['mrr']):+.3f}")

    print(f"\n{'='*80}")
    print("EVALUATION COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
