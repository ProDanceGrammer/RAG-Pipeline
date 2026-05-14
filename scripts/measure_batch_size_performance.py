#!/usr/bin/env python3
"""
Measure embedding performance across different batch sizes.

Tests batch sizes 1, 3, 4, 5, 6, 7, 10 to determine optimal configuration.
"""
import sys
from pathlib import Path
import time
import statistics

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.ollama_embedder import OllamaEmbedder
import logging

logging.basicConfig(level=logging.WARNING)  # Reduce noise
logger = logging.getLogger(__name__)


def measure_batch_performance(batch_size: int, texts: list, runs: int = 3) -> dict:
    """
    Measure performance for a specific batch size.

    Args:
        batch_size: Number of texts per batch
        texts: List of texts to embed
        runs: Number of test runs for averaging

    Returns:
        Performance metrics dict
    """
    embedder = OllamaEmbedder(batch_size=batch_size)

    times = []

    for run in range(runs):
        start_time = time.time()
        embeddings = embedder.embed_texts(texts)
        elapsed = time.time() - start_time
        times.append(elapsed)

        # Small delay between runs
        if run < runs - 1:
            time.sleep(1)

    num_texts = len(texts)
    num_batches = (num_texts + batch_size - 1) // batch_size

    return {
        'batch_size': batch_size,
        'num_texts': num_texts,
        'num_batches': num_batches,
        'runs': runs,
        'times': times,
        'min_time': min(times),
        'max_time': max(times),
        'avg_time': statistics.mean(times),
        'median_time': statistics.median(times),
        'stdev_time': statistics.stdev(times) if len(times) > 1 else 0,
        'time_per_text': statistics.mean(times) / num_texts,
        'time_per_batch': statistics.mean(times) / num_batches,
    }


def main():
    logger.info("=" * 80)
    logger.info("BATCH SIZE PERFORMANCE MEASUREMENT")
    logger.info("=" * 80)

    # Test texts - representative samples from the knowledge base
    test_texts = [
        "What is encapsulation in object-oriented programming?",
        "How does inheritance work in Python?",
        "What are the SOLID principles?",
        "Explain polymorphism with examples",
        "What is the difference between composition and inheritance?",
        "How do you implement a singleton pattern?",
        "What is dependency injection?",
        "Explain the factory pattern",
        "What is the observer pattern?",
        "How does the strategy pattern work?",
        "What is abstraction in OOP?",
        "Explain method overloading and overriding",
        "What are abstract classes?",
        "How do interfaces work?",
        "What is multiple inheritance?",
    ]

    # Batch sizes to test
    batch_sizes = [1, 3, 4, 5, 6, 7, 10]

    print("\n" + "=" * 80)
    print("TESTING CONFIGURATION")
    print("=" * 80)
    print(f"Number of texts: {len(test_texts)}")
    print(f"Batch sizes to test: {batch_sizes}")
    print(f"Runs per batch size: 3")
    print(f"Total tests: {len(batch_sizes) * 3} = {len(batch_sizes) * 3 * len(test_texts)} embeddings")
    print()

    results = []

    for batch_size in batch_sizes:
        print(f"\nTesting batch_size={batch_size}...")
        print(f"  Expected batches: {(len(test_texts) + batch_size - 1) // batch_size}")

        result = measure_batch_performance(batch_size, test_texts, runs=3)
        results.append(result)

        print(f"  Avg time: {result['avg_time']:.2f}s")
        print(f"  Time per text: {result['time_per_text']:.3f}s")
        print(f"  Time per batch: {result['time_per_batch']:.3f}s")

    # Analysis
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    # Table header
    print(f"{'Batch':<6} {'Batches':<8} {'Avg Time':<10} {'Per Text':<10} {'Per Batch':<10} {'StdDev':<8}")
    print(f"{'Size':<6} {'Count':<8} {'(seconds)':<10} {'(seconds)':<10} {'(seconds)':<10} {'(s)':<8}")
    print("-" * 80)

    for r in results:
        print(f"{r['batch_size']:<6} {r['num_batches']:<8} "
              f"{r['avg_time']:<10.2f} {r['time_per_text']:<10.3f} "
              f"{r['time_per_batch']:<10.3f} {r['stdev_time']:<8.3f}")

    # Find optimal
    fastest = min(results, key=lambda x: x['avg_time'])
    most_stable = min(results, key=lambda x: x['stdev_time'])

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)

    print(f"\nFastest batch size: {fastest['batch_size']}")
    print(f"  Total time: {fastest['avg_time']:.2f}s")
    print(f"  Time per text: {fastest['time_per_text']:.3f}s")

    print(f"\nMost stable batch size: {most_stable['batch_size']}")
    print(f"  Standard deviation: {most_stable['stdev_time']:.3f}s")

    # Compare to current default (5)
    current_default = next((r for r in results if r['batch_size'] == 5), None)
    if current_default:
        print(f"\nCurrent default (batch_size=5):")
        print(f"  Total time: {current_default['avg_time']:.2f}s")
        print(f"  Time per text: {current_default['time_per_text']:.3f}s")
        print(f"  Rank by speed: {sorted(results, key=lambda x: x['avg_time']).index(current_default) + 1}/{len(results)}")

        if fastest['batch_size'] != 5:
            speedup = ((current_default['avg_time'] - fastest['avg_time']) / current_default['avg_time']) * 100
            print(f"\nPotential improvement with batch_size={fastest['batch_size']}:")
            print(f"  Time saved: {current_default['avg_time'] - fastest['avg_time']:.2f}s ({speedup:.1f}% faster)")

    # Detailed comparison
    print("\n" + "=" * 80)
    print("DETAILED COMPARISON")
    print("=" * 80)

    baseline = results[0]  # batch_size=1
    print(f"\nBaseline (batch_size=1): {baseline['avg_time']:.2f}s")
    print()

    for r in results[1:]:
        speedup = ((baseline['avg_time'] - r['avg_time']) / baseline['avg_time']) * 100
        time_saved = baseline['avg_time'] - r['avg_time']
        print(f"batch_size={r['batch_size']:2}: {r['avg_time']:6.2f}s "
              f"(saves {time_saved:5.2f}s, {speedup:+5.1f}% vs baseline)")

    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()

    # Check if there's a clear winner
    sorted_by_time = sorted(results, key=lambda x: x['avg_time'])
    top3 = sorted_by_time[:3]

    time_diff_top2 = top3[1]['avg_time'] - top3[0]['avg_time']

    if time_diff_top2 < 1.0:  # Less than 1 second difference
        print("WARNING: Top performers are very close (< 1s difference)")
        print(f"   Consider other factors: stability, memory, API limits")
        print()
        print(f"   Top 3 batch sizes:")
        for i, r in enumerate(top3, 1):
            print(f"   {i}. batch_size={r['batch_size']}: {r['avg_time']:.2f}s (+/-{r['stdev_time']:.3f}s)")
    else:
        print(f"Clear winner: batch_size={fastest['batch_size']}")
        print(f"  Significantly faster than alternatives")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_ANALYSIS.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BATCH SIZE PERFORMANCE ANALYSIS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {len(test_texts)}\n")
        f.write(f"Runs per batch size: 3\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n\n")

        f.write("RESULTS:\n\n")
        f.write(f"{'Batch':<6} {'Batches':<8} {'Avg Time':<10} {'Per Text':<10} {'Per Batch':<10} {'StdDev':<8}\n")
        f.write(f"{'Size':<6} {'Count':<8} {'(seconds)':<10} {'(seconds)':<10} {'(seconds)':<10} {'(s)':<8}\n")
        f.write("-" * 80 + "\n")

        for r in results:
            f.write(f"{r['batch_size']:<6} {r['num_batches']:<8} "
                   f"{r['avg_time']:<10.2f} {r['time_per_text']:<10.3f} "
                   f"{r['time_per_batch']:<10.3f} {r['stdev_time']:<8.3f}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Fastest: batch_size={fastest['batch_size']} ({fastest['avg_time']:.2f}s)\n")
        f.write(f"Most stable: batch_size={most_stable['batch_size']} (±{most_stable['stdev_time']:.3f}s)\n")

        if current_default:
            f.write(f"\nCurrent default (batch_size=5): {current_default['avg_time']:.2f}s\n")
            if fastest['batch_size'] != 5:
                speedup = ((current_default['avg_time'] - fastest['avg_time']) / current_default['avg_time']) * 100
                f.write(f"Potential improvement: {speedup:.1f}% faster with batch_size={fastest['batch_size']}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("INTERPRETATION:\n")
        f.write("=" * 80 + "\n\n")

        f.write("Batch size affects:\n")
        f.write("1. Total processing time (lower is better)\n")
        f.write("2. Memory usage (larger batches = more memory)\n")
        f.write("3. API rate limits (larger batches = fewer requests)\n")
        f.write("4. Stability (lower standard deviation = more predictable)\n\n")

        f.write("The current implementation processes texts sequentially within batches,\n")
        f.write("so batch_size primarily affects memory and code organization, not parallelism.\n")
        f.write("The 0.1s delay between texts is the dominant factor in total time.\n\n")

        f.write("RECOMMENDATION:\n")
        if time_diff_top2 < 1.0:
            f.write(f"Top performers are within 1s of each other. Current batch_size=5 is reasonable.\n")
            f.write(f"Consider keeping it unless memory or API limits are concerns.\n")
        else:
            f.write(f"Switch to batch_size={fastest['batch_size']} for {((current_default['avg_time'] - fastest['avg_time']) / current_default['avg_time']) * 100:.1f}% speedup.\n")

    print(f"\nReport written to: {output_path}")
    print("\nDone!")


if __name__ == '__main__':
    main()
