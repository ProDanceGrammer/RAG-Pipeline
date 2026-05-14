#!/usr/bin/env python3
"""
Measure stability (standard deviation) for top-performing batch sizes.
Runs each batch size multiple times to calculate consistency.
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


def measure_batch_performance(batch_size: int, texts: list) -> float:
    """Measure performance for a specific batch size (single run)."""
    embedder = OllamaEmbedder(batch_size=batch_size)

    start_time = time.time()
    embeddings = embedder.embed_texts(texts)
    elapsed = time.time() - start_time

    return elapsed


def measure_stability(batch_size: int, texts: list, runs: int = 5) -> dict:
    """Measure stability across multiple runs."""
    print(f"Testing batch_size={batch_size:2} ({runs} runs)...", flush=True)

    times = []
    for run in range(runs):
        print(f"  Run {run+1}/{runs}...", end=" ", flush=True)
        elapsed = measure_batch_performance(batch_size, texts)
        times.append(elapsed)
        print(f"{elapsed:.1f}s")

        # Small delay between runs
        if run < runs - 1:
            time.sleep(2)

    avg_time = statistics.mean(times)
    stdev_time = statistics.stdev(times) if len(times) > 1 else 0
    min_time = min(times)
    max_time = max(times)
    range_time = max_time - min_time
    cv = (stdev_time / avg_time * 100) if avg_time > 0 else 0

    return {
        'batch_size': batch_size,
        'runs': runs,
        'times': times,
        'avg': avg_time,
        'stdev': stdev_time,
        'min': min_time,
        'max': max_time,
        'range': range_time,
        'cv': cv,
    }


def main():
    print("=" * 80)
    print("BATCH SIZE STABILITY MEASUREMENT")
    print("=" * 80)
    print()

    # Use 20 texts for faster testing
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

    # Test top performers from previous test + current default
    batch_sizes = [1, 5, 6, 10, 12, 20]
    runs = 5

    print(f"Number of texts: {len(test_texts)}")
    print(f"Batch sizes to test: {batch_sizes}")
    print(f"Runs per batch size: {runs}")
    print(f"Total embeddings: {len(test_texts) * len(batch_sizes) * runs}")
    print()

    estimated_time = len(test_texts) * len(batch_sizes) * runs * 2.3 / 60
    print(f"Estimated time: ~{estimated_time:.1f} minutes")
    print()

    results = []

    for batch_size in batch_sizes:
        result = measure_stability(batch_size, test_texts, runs=runs)
        results.append(result)
        print(f"  Avg: {result['avg']:.2f}s ± {result['stdev']:.3f}s (CV: {result['cv']:.2f}%)")
        print()

    # Results
    print("=" * 80)
    print("STABILITY RESULTS")
    print("=" * 80)
    print()
    print(f"{'Batch':<6} {'Avg Time':<10} {'StdDev':<10} {'Min':<8} {'Max':<8} {'Range':<8} {'CV':<8}")
    print(f"{'Size':<6} {'(seconds)':<10} {'(±seconds)':<10} {'(s)':<8} {'(s)':<8} {'(s)':<8} {'(%)':<8}")
    print("-" * 80)

    for r in results:
        print(f"{r['batch_size']:<6} {r['avg']:<10.2f} {r['stdev']:<10.3f} "
              f"{r['min']:<8.2f} {r['max']:<8.2f} {r['range']:<8.2f} {r['cv']:<8.2f}")

    # Analysis
    most_stable = min(results, key=lambda x: x['stdev'])
    least_stable = max(results, key=lambda x: x['stdev'])
    fastest_avg = min(results, key=lambda x: x['avg'])

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print(f"Most stable: batch_size={most_stable['batch_size']} (±{most_stable['stdev']:.3f}s, CV={most_stable['cv']:.2f}%)")
    print(f"Least stable: batch_size={least_stable['batch_size']} (±{least_stable['stdev']:.3f}s, CV={least_stable['cv']:.2f}%)")
    print(f"Fastest average: batch_size={fastest_avg['batch_size']} ({fastest_avg['avg']:.2f}s)")

    # Current default
    bs5 = next((r for r in results if r['batch_size'] == 5), None)
    if bs5:
        print(f"\nCurrent default (batch_size=5):")
        print(f"  Avg: {bs5['avg']:.2f}s")
        print(f"  Stability: ±{bs5['stdev']:.3f}s (CV={bs5['cv']:.2f}%)")

        sorted_by_stability = sorted(results, key=lambda x: x['stdev'])
        stability_rank = sorted_by_stability.index(bs5) + 1
        print(f"  Stability rank: {stability_rank}/{len(results)}")

        sorted_by_speed = sorted(results, key=lambda x: x['avg'])
        speed_rank = sorted_by_speed.index(bs5) + 1
        print(f"  Speed rank: {speed_rank}/{len(results)}")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_STABILITY.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BATCH SIZE STABILITY MEASUREMENT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {len(test_texts)}\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n")
        f.write(f"Runs per batch size: {runs}\n\n")

        f.write("RESULTS:\n\n")
        f.write(f"{'Batch':<6} {'Avg Time':<10} {'StdDev':<10} {'Min':<8} {'Max':<8} {'Range':<8} {'CV':<8}\n")
        f.write(f"{'Size':<6} {'(seconds)':<10} {'(±seconds)':<10} {'(s)':<8} {'(s)':<8} {'(s)':<8} {'(%)':<8}\n")
        f.write("-" * 80 + "\n")

        for r in results:
            f.write(f"{r['batch_size']:<6} {r['avg']:<10.2f} {r['stdev']:<10.3f} "
                   f"{r['min']:<8.2f} {r['max']:<8.2f} {r['range']:<8.2f} {r['cv']:<8.2f}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Most stable: batch_size={most_stable['batch_size']} (±{most_stable['stdev']:.3f}s)\n")
        f.write(f"Least stable: batch_size={least_stable['batch_size']} (±{least_stable['stdev']:.3f}s)\n")
        f.write(f"Fastest average: batch_size={fastest_avg['batch_size']} ({fastest_avg['avg']:.2f}s)\n\n")

        if bs5:
            f.write(f"CURRENT DEFAULT (batch_size=5):\n")
            f.write(f"  Avg: {bs5['avg']:.2f}s\n")
            f.write(f"  Stability: ±{bs5['stdev']:.3f}s (CV={bs5['cv']:.2f}%)\n")
            f.write(f"  Stability rank: {stability_rank}/{len(results)}\n")
            f.write(f"  Speed rank: {speed_rank}/{len(results)}\n\n")

        f.write("INTERPRETATION:\n\n")
        f.write("Standard Deviation (StdDev):\n")
        f.write("  - Measures consistency across runs\n")
        f.write("  - Lower is better (more predictable)\n")
        f.write("  - ±0.01s = very stable\n")
        f.write("  - ±0.10s = moderate stability\n")
        f.write("  - ±0.50s = unstable\n\n")

        f.write("Coefficient of Variation (CV):\n")
        f.write("  - StdDev normalized by average (as percentage)\n")
        f.write("  - Allows comparison across different time scales\n")
        f.write("  - <1% = very stable\n")
        f.write("  - 1-5% = moderate stability\n")
        f.write("  - >5% = unstable\n\n")

        f.write("RECOMMENDATION:\n")
        if most_stable['batch_size'] == fastest_avg['batch_size']:
            f.write(f"batch_size={most_stable['batch_size']} is both fastest AND most stable.\n")
            f.write("Clear winner for optimal performance.\n")
        else:
            f.write(f"Trade-off between speed and stability:\n")
            f.write(f"  - Fastest: batch_size={fastest_avg['batch_size']} ({fastest_avg['avg']:.2f}s, ±{fastest_avg['stdev']:.3f}s)\n")
            f.write(f"  - Most stable: batch_size={most_stable['batch_size']} ({most_stable['avg']:.2f}s, ±{most_stable['stdev']:.3f}s)\n")
            f.write(f"\nChoose based on priority: speed vs predictability.\n")

    print(f"\nReport written to: {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
