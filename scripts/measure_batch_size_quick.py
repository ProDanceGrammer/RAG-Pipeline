#!/usr/bin/env python3
"""
Quick batch size performance test with fewer samples.
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

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def measure_batch_performance(batch_size: int, texts: list) -> dict:
    """Measure performance for a specific batch size."""
    embedder = OllamaEmbedder(batch_size=batch_size)

    start_time = time.time()
    embeddings = embedder.embed_texts(texts)
    elapsed = time.time() - start_time

    num_texts = len(texts)
    num_batches = (num_texts + batch_size - 1) // batch_size

    return {
        'batch_size': batch_size,
        'num_texts': num_texts,
        'num_batches': num_batches,
        'time': elapsed,
        'time_per_text': elapsed / num_texts,
        'time_per_batch': elapsed / num_batches,
    }


def main():
    print("=" * 80)
    print("BATCH SIZE PERFORMANCE TEST (Quick)")
    print("=" * 80)

    # Smaller test set
    test_texts = [
        "What is encapsulation in object-oriented programming?",
        "How does inheritance work in Python?",
        "What are the SOLID principles?",
        "Explain polymorphism with examples",
        "What is the difference between composition and inheritance?",
        "How do you implement a singleton pattern?",
        "What is dependency injection?",
        "Explain the factory pattern?",
        "What is the observer pattern?",
        "How does the strategy pattern work?",
    ]

    # Test fewer batch sizes
    batch_sizes = [3, 4, 5, 6, 7]

    print(f"\nNumber of texts: {len(test_texts)}")
    print(f"Batch sizes to test: {batch_sizes}")
    print(f"Total embeddings: {len(test_texts) * len(batch_sizes)}")
    print()

    results = []

    for batch_size in batch_sizes:
        print(f"Testing batch_size={batch_size}...", end=" ", flush=True)

        result = measure_batch_performance(batch_size, test_texts)
        results.append(result)

        print(f"{result['time']:.2f}s (batches: {result['num_batches']})")

    # Results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"{'Batch':<6} {'Batches':<8} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}")
    print(f"{'Size':<6} {'Count':<8} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}")
    print("-" * 80)

    for r in results:
        print(f"{r['batch_size']:<6} {r['num_batches']:<8} "
              f"{r['time']:<12.2f} {r['time_per_text']:<12.3f} "
              f"{r['time_per_batch']:<12.3f}")

    # Analysis
    fastest = min(results, key=lambda x: x['time'])
    slowest = max(results, key=lambda x: x['time'])
    current = next((r for r in results if r['batch_size'] == 5), None)

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print(f"Fastest: batch_size={fastest['batch_size']} ({fastest['time']:.2f}s)")
    print(f"Slowest: batch_size={slowest['batch_size']} ({slowest['time']:.2f}s)")
    print(f"Difference: {slowest['time'] - fastest['time']:.2f}s ({((slowest['time'] - fastest['time']) / slowest['time'] * 100):.1f}%)")

    if current:
        print(f"\nCurrent default (batch_size=5): {current['time']:.2f}s")
        if fastest['batch_size'] != 5:
            diff = current['time'] - fastest['time']
            pct = (diff / current['time']) * 100
            print(f"Potential improvement with batch_size={fastest['batch_size']}: {diff:.2f}s ({pct:.1f}% faster)")
        else:
            print("Current default is already optimal!")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_ANALYSIS.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BATCH SIZE PERFORMANCE ANALYSIS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {len(test_texts)}\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n\n")

        f.write("RESULTS:\n\n")
        f.write(f"{'Batch':<6} {'Batches':<8} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}\n")
        f.write(f"{'Size':<6} {'Count':<8} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}\n")
        f.write("-" * 80 + "\n")

        for r in results:
            f.write(f"{r['batch_size']:<6} {r['num_batches']:<8} "
                   f"{r['time']:<12.2f} {r['time_per_text']:<12.3f} "
                   f"{r['time_per_batch']:<12.3f}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Fastest: batch_size={fastest['batch_size']} ({fastest['time']:.2f}s)\n")
        f.write(f"Slowest: batch_size={slowest['batch_size']} ({slowest['time']:.2f}s)\n")
        f.write(f"Range: {slowest['time'] - fastest['time']:.2f}s\n\n")

        if current:
            f.write(f"Current default (batch_size=5): {current['time']:.2f}s\n")
            if fastest['batch_size'] != 5:
                diff = current['time'] - fastest['time']
                pct = (diff / current['time']) * 100
                f.write(f"Potential improvement: {pct:.1f}% faster with batch_size={fastest['batch_size']}\n")
            else:
                f.write("Current default is optimal!\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("INTERPRETATION:\n")
        f.write("=" * 80 + "\n\n")

        f.write("The current implementation processes texts sequentially within batches\n")
        f.write("with a 0.1s delay between each text. This means:\n\n")

        f.write("1. Batch size does NOT affect parallelism (no parallel processing)\n")
        f.write("2. Total time = (num_texts * embedding_time) + (num_texts * 0.1s delay)\n")
        f.write("3. Batch size only affects code organization and memory usage\n\n")

        f.write("Expected time for 10 texts: ~10 * (2.8s embedding + 0.1s delay) = ~29s\n")
        f.write(f"Actual time range: {fastest['time']:.1f}s - {slowest['time']:.1f}s\n\n")

        time_diff = slowest['time'] - fastest['time']
        if time_diff < 2.0:
            f.write("CONCLUSION: Batch size has minimal impact on performance (< 2s difference).\n")
            f.write("The current batch_size=5 is reasonable. No change needed.\n")
        else:
            f.write(f"CONCLUSION: Batch size has measurable impact ({time_diff:.1f}s difference).\n")
            f.write(f"Consider switching to batch_size={fastest['batch_size']} for optimal performance.\n")

    print(f"\nReport written to: {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
