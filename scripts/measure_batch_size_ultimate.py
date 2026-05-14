#!/usr/bin/env python3
"""
Ultimate fair batch size comparison using LCM of all batch sizes.
Uses 2520 texts = LCM(1,2,4,5,6,7,8,9,10,20) for perfectly even division.
"""
import sys
from pathlib import Path
import time

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
    num_batches = num_texts // batch_size

    return {
        'batch_size': batch_size,
        'num_texts': num_texts,
        'num_batches': num_batches,
        'time': elapsed,
        'time_per_text': elapsed / num_texts,
        'time_per_batch': elapsed / num_batches,
    }


def generate_texts(count: int) -> list:
    """Generate test texts by repeating base samples."""
    base_texts = [
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
    ]

    # Repeat base texts to reach desired count
    texts = []
    while len(texts) < count:
        texts.extend(base_texts)

    return texts[:count]


def main():
    print("=" * 80)
    print("ULTIMATE FAIR BATCH SIZE COMPARISON")
    print("=" * 80)
    print()
    print("Using 2520 texts = LCM(1,2,4,5,6,7,8,9,10,20)")
    print("This ensures ALL batch sizes divide evenly with NO partial batches.")
    print()

    # Generate 2520 texts
    num_texts = 2520
    print(f"Generating {num_texts} test texts...")
    test_texts = generate_texts(num_texts)
    print(f"Generated {len(test_texts)} texts")
    print()

    # Batch sizes to test
    batch_sizes = [1, 2, 4, 5, 6, 7, 8, 9, 10, 20]

    print("Batch configurations:")
    for bs in batch_sizes:
        num_batches = num_texts // bs
        print(f"  batch_size={bs:2}: {num_batches:4} batches × {bs:2} texts = {num_batches * bs} texts")
    print()

    # Estimate time
    estimated_time_per_text = 2.3  # seconds
    total_embeddings = num_texts * len(batch_sizes)
    estimated_total_time = total_embeddings * estimated_time_per_text
    print(f"Estimated total time: {estimated_total_time / 60:.1f} minutes")
    print(f"({total_embeddings} embeddings × {estimated_time_per_text}s each)")
    print()

    response = input("This will take a long time. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        return

    results = []

    for batch_size in batch_sizes:
        print(f"\nTesting batch_size={batch_size:2}...", flush=True)
        print(f"  Configuration: {num_texts // batch_size} batches × {batch_size} texts")
        print(f"  Starting...", end=" ", flush=True)

        result = measure_batch_performance(batch_size, test_texts)
        results.append(result)

        print(f"Done! {result['time']:.1f}s")
        print(f"  Time per text: {result['time_per_text']:.3f}s")
        print(f"  Time per batch: {result['time_per_batch']:.3f}s")

    # Results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"{'Batch':<6} {'Configuration':<15} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}")
    print(f"{'Size':<6} {'(batches×size)':<15} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}")
    print("-" * 80)

    for r in results:
        config = f"{r['num_batches']}×{r['batch_size']}"
        print(f"{r['batch_size']:<6} {config:<15} "
              f"{r['time']:<12.1f} {r['time_per_text']:<12.4f} "
              f"{r['time_per_batch']:<12.3f}")

    # Analysis
    fastest = min(results, key=lambda x: x['time'])
    slowest = max(results, key=lambda x: x['time'])

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print(f"Fastest: batch_size={fastest['batch_size']} ({fastest['num_batches']}×{fastest['batch_size']}) = {fastest['time']:.1f}s")
    print(f"Slowest: batch_size={slowest['batch_size']} ({slowest['num_batches']}×{slowest['batch_size']}) = {slowest['time']:.1f}s")
    print(f"Difference: {slowest['time'] - fastest['time']:.1f}s ({((slowest['time'] - fastest['time']) / slowest['time'] * 100):.1f}%)")

    # Rankings
    print("\nRankings:")
    sorted_results = sorted(results, key=lambda x: x['time'])
    for i, r in enumerate(sorted_results, 1):
        diff = r['time'] - fastest['time']
        pct = (diff / fastest['time'] * 100) if fastest['time'] > 0 else 0
        print(f"  {i}. batch_size={r['batch_size']:2}: {r['time']:7.1f}s (+{diff:5.1f}s, +{pct:4.1f}%)")

    # Current default
    bs5 = next((r for r in results if r['batch_size'] == 5), None)
    if bs5:
        rank = sorted_results.index(bs5) + 1
        print(f"\nCurrent default (batch_size=5):")
        print(f"  Time: {bs5['time']:.1f}s")
        print(f"  Rank: {rank}/{len(results)}")
        if fastest['batch_size'] != 5:
            diff = bs5['time'] - fastest['time']
            pct = (diff / bs5['time']) * 100
            print(f"  Potential improvement with batch_size={fastest['batch_size']}: {diff:.1f}s ({pct:.1f}% faster)")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_ULTIMATE_COMPARISON.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ULTIMATE FAIR BATCH SIZE COMPARISON\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {num_texts} (LCM of all batch sizes)\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n\n")

        f.write("BATCH CONFIGURATIONS:\n")
        for bs in batch_sizes:
            num_batches = num_texts // bs
            f.write(f"  batch_size={bs:2}: {num_batches:4} batches × {bs:2} texts = {num_batches * bs} texts\n")
        f.write("\n")

        f.write("RESULTS:\n\n")
        f.write(f"{'Batch':<6} {'Configuration':<15} {'Total Time':<12} {'Per Text':<12} {'Per Batch':<12}\n")
        f.write(f"{'Size':<6} {'(batches×size)':<15} {'(seconds)':<12} {'(seconds)':<12} {'(seconds)':<12}\n")
        f.write("-" * 80 + "\n")

        for r in results:
            config = f"{r['num_batches']}×{r['batch_size']}"
            f.write(f"{r['batch_size']:<6} {config:<15} "
                   f"{r['time']:<12.1f} {r['time_per_text']:<12.4f} "
                   f"{r['time_per_batch']:<12.3f}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Fastest: batch_size={fastest['batch_size']} ({fastest['num_batches']}×{fastest['batch_size']}) = {fastest['time']:.1f}s\n")
        f.write(f"Slowest: batch_size={slowest['batch_size']} ({slowest['num_batches']}×{slowest['batch_size']}) = {slowest['time']:.1f}s\n")
        f.write(f"Range: {slowest['time'] - fastest['time']:.1f}s ({((slowest['time'] - fastest['time']) / slowest['time'] * 100):.1f}%)\n\n")

        f.write("RANKINGS:\n")
        for i, r in enumerate(sorted_results, 1):
            diff = r['time'] - fastest['time']
            pct = (diff / fastest['time'] * 100) if fastest['time'] > 0 else 0
            f.write(f"  {i}. batch_size={r['batch_size']:2}: {r['time']:7.1f}s (+{diff:5.1f}s, +{pct:4.1f}%)\n")
        f.write("\n")

        if bs5:
            rank = sorted_results.index(bs5) + 1
            f.write(f"CURRENT DEFAULT (batch_size=5):\n")
            f.write(f"  Time: {bs5['time']:.1f}s\n")
            f.write(f"  Rank: {rank}/{len(results)}\n")
            if fastest['batch_size'] != 5:
                diff = bs5['time'] - fastest['time']
                pct = (diff / bs5['time']) * 100
                f.write(f"  Potential improvement: {pct:.1f}% faster with batch_size={fastest['batch_size']}\n")
            f.write("\n")

        f.write("INTERPRETATION:\n\n")
        f.write(f"This test uses {num_texts} texts, which is the LCM (Least Common Multiple)\n")
        f.write("of all tested batch sizes. This ensures perfectly even division with\n")
        f.write("NO partial batches for any configuration.\n\n")

        f.write("All configurations process exactly {num_texts} texts:\n")
        for bs in batch_sizes:
            num_batches = num_texts // bs
            f.write(f"  - batch_size={bs:2}: {num_batches:4} batches × {bs:2} texts\n")
        f.write("\n")

        f.write("This is the fairest possible comparison, eliminating any bias from\n")
        f.write("partial batches or uneven configurations.\n\n")

        time_range = slowest['time'] - fastest['time']
        pct_range = (time_range / slowest['time']) * 100

        f.write(f"CONCLUSION:\n")
        f.write(f"Batch size has {pct_range:.1f}% performance impact across all tested sizes.\n")
        f.write(f"The optimal batch_size is {fastest['batch_size']} for this workload.\n")

    print(f"\nReport written to: {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
