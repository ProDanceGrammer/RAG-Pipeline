#!/usr/bin/env python3
"""
Fair batch size comparison with equal batch configurations.
Uses 20 texts so all batch sizes divide evenly.
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
    print("FAIR BATCH SIZE COMPARISON")
    print("=" * 80)

    # 20 texts - divisible by 1, 2, 4, 5, 10, 20
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
        "Explain the decorator pattern",
        "What is the adapter pattern?",
        "How does the command pattern work?",
        "What is the template method pattern?",
        "Explain the state pattern",
    ]

    # Batch sizes that divide 20 evenly
    batch_sizes = [1, 2, 4, 5, 10, 20]

    print(f"\nNumber of texts: {len(test_texts)}")
    print(f"Batch sizes to test: {batch_sizes}")
    print("\nBatch configurations:")
    for bs in batch_sizes:
        num_batches = len(test_texts) // bs
        print(f"  batch_size={bs:2}: {num_batches:2} batches × {bs:2} texts = {num_batches * bs} texts")
    print()

    results = []

    for batch_size in batch_sizes:
        print(f"Testing batch_size={batch_size:2}...", end=" ", flush=True)

        result = measure_batch_performance(batch_size, test_texts)
        results.append(result)

        print(f"{result['time']:.2f}s ({result['num_batches']} batches)")

    # Results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"{'Batch':<6} {'Config':<15} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}")
    print(f"{'Size':<6} {'(batches×size)':<15} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}")
    print("-" * 80)

    for r in results:
        config = f"{r['num_batches']}×{r['batch_size']}"
        print(f"{r['batch_size']:<6} {config:<15} "
              f"{r['time']:<12.2f} {r['time_per_text']:<12.3f} "
              f"{r['time_per_batch']:<12.3f}")

    # Analysis
    fastest = min(results, key=lambda x: x['time'])
    slowest = max(results, key=lambda x: x['time'])

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print(f"Fastest: batch_size={fastest['batch_size']} ({fastest['num_batches']}×{fastest['batch_size']}) = {fastest['time']:.2f}s")
    print(f"Slowest: batch_size={slowest['batch_size']} ({slowest['num_batches']}×{slowest['batch_size']}) = {slowest['time']:.2f}s")
    print(f"Difference: {slowest['time'] - fastest['time']:.2f}s ({((slowest['time'] - fastest['time']) / slowest['time'] * 100):.1f}%)")

    # Compare extremes
    bs1 = next((r for r in results if r['batch_size'] == 1), None)
    bs20 = next((r for r in results if r['batch_size'] == 20), None)
    bs5 = next((r for r in results if r['batch_size'] == 5), None)

    if bs1 and bs20:
        print(f"\nExtreme comparison:")
        print(f"  1×20 (batch_size=1):  {bs1['time']:.2f}s")
        print(f"  20×1 (batch_size=20): {bs20['time']:.2f}s")
        print(f"  Difference: {abs(bs1['time'] - bs20['time']):.2f}s")

    if bs5:
        print(f"\nCurrent default (batch_size=5):")
        print(f"  4×5: {bs5['time']:.2f}s")
        print(f"  Rank: {sorted(results, key=lambda x: x['time']).index(bs5) + 1}/{len(results)}")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_FAIR_COMPARISON.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("FAIR BATCH SIZE COMPARISON\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {len(test_texts)} (divisible by all batch sizes)\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n\n")

        f.write("BATCH CONFIGURATIONS:\n")
        for bs in batch_sizes:
            num_batches = len(test_texts) // bs
            f.write(f"  batch_size={bs:2}: {num_batches:2} batches × {bs:2} texts = {num_batches * bs} texts\n")
        f.write("\n")

        f.write("RESULTS:\n\n")
        f.write(f"{'Batch':<6} {'Config':<15} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}\n")
        f.write(f"{'Size':<6} {'(batches×size)':<15} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}\n")
        f.write("-" * 80 + "\n")

        for r in results:
            config = f"{r['num_batches']}×{r['batch_size']}"
            f.write(f"{r['batch_size']:<6} {config:<15} "
                   f"{r['time']:<12.2f} {r['time_per_text']:<12.3f} "
                   f"{r['time_per_batch']:<12.3f}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Fastest: batch_size={fastest['batch_size']} ({fastest['num_batches']}×{fastest['batch_size']}) = {fastest['time']:.2f}s\n")
        f.write(f"Slowest: batch_size={slowest['batch_size']} ({slowest['num_batches']}×{slowest['batch_size']}) = {slowest['time']:.2f}s\n")
        f.write(f"Range: {slowest['time'] - fastest['time']:.2f}s\n\n")

        if bs1 and bs20:
            f.write("EXTREME COMPARISON (1×20 vs 20×1):\n")
            f.write(f"  batch_size=1  (20 batches × 1 text):  {bs1['time']:.2f}s\n")
            f.write(f"  batch_size=20 (1 batch × 20 texts):   {bs20['time']:.2f}s\n")
            f.write(f"  Difference: {abs(bs1['time'] - bs20['time']):.2f}s\n\n")

        if bs5:
            f.write(f"CURRENT DEFAULT (batch_size=5):\n")
            f.write(f"  Configuration: 4 batches × 5 texts\n")
            f.write(f"  Time: {bs5['time']:.2f}s\n")
            f.write(f"  Rank: {sorted(results, key=lambda x: x['time']).index(bs5) + 1}/{len(results)}\n\n")

        f.write("INTERPRETATION:\n\n")
        f.write("This test uses 20 texts so all batch sizes divide evenly:\n")
        f.write("  - batch_size=1:  20 batches × 1 text\n")
        f.write("  - batch_size=2:  10 batches × 2 texts\n")
        f.write("  - batch_size=4:  5 batches × 4 texts\n")
        f.write("  - batch_size=5:  4 batches × 5 texts\n")
        f.write("  - batch_size=10: 2 batches × 10 texts\n")
        f.write("  - batch_size=20: 1 batch × 20 texts\n\n")

        f.write("This eliminates the unfair comparison from the previous test where\n")
        f.write("batch_size=10 had partial batches (1×10 + 1×5) while batch_size=1\n")
        f.write("had all equal batches (15×1).\n\n")

        time_range = slowest['time'] - fastest['time']
        if time_range < 1.0:
            f.write("CONCLUSION: Batch size has minimal impact (< 1s difference).\n")
            f.write("All configurations process texts sequentially, so total time is\n")
            f.write("dominated by (num_texts × embedding_time), not batch organization.\n")
        else:
            f.write(f"CONCLUSION: Batch size has measurable impact ({time_range:.1f}s difference).\n")
            f.write(f"Consider using batch_size={fastest['batch_size']} for optimal performance.\n")

    print(f"\nReport written to: {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
