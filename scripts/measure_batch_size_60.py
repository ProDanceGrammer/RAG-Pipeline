#!/usr/bin/env python3
"""
Practical fair batch size comparison using 60 texts.
60 = LCM(1,2,4,5,6,10) - divides evenly for most common batch sizes.
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


def main():
    print("=" * 80)
    print("PRACTICAL FAIR BATCH SIZE COMPARISON")
    print("=" * 80)
    print()
    print("Using 60 texts = LCM(1,2,4,5,6,10)")
    print("All tested batch sizes divide evenly with NO partial batches.")
    print()

    # 60 texts - practical size that divides evenly
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
        "What is the proxy pattern?",
        "How does the bridge pattern work?",
        "What is the composite pattern?",
        "Explain the flyweight pattern",
        "What is the facade pattern?",
        "How does the chain of responsibility work?",
        "What is the iterator pattern?",
        "Explain the mediator pattern",
        "What is the memento pattern?",
        "How does the visitor pattern work?",
        "What is the interpreter pattern?",
        "Explain the prototype pattern?",
        "What is the builder pattern?",
        "How does dependency inversion work?",
        "What is the open-closed principle?",
        "Explain the Liskov substitution principle",
        "What is the interface segregation principle?",
        "How does the single responsibility principle work?",
        "What is tight coupling?",
        "Explain loose coupling",
        "What is cohesion in software design?",
        "How does encapsulation improve maintainability?",
        "What is information hiding?",
        "Explain the law of Demeter",
        "What is a design pattern?",
        "How do creational patterns work?",
        "What are structural patterns?",
        "Explain behavioral patterns",
        "What is refactoring?",
        "How does code smell detection work?",
        "What is technical debt?",
        "Explain clean code principles",
        "What is YAGNI?",
        "How does KISS principle work?",
        "What is DRY principle?",
        "Explain separation of concerns",
        "What is modularity?",
        "How does abstraction reduce complexity?",
        "What is polymorphic behavior?",
        "Explain dynamic dispatch",
    ]

    # Batch sizes that divide 60 evenly
    batch_sizes = [1, 2, 4, 5, 6, 10, 12, 15, 20, 30, 60]

    print(f"Number of texts: {len(test_texts)}")
    print(f"Batch sizes to test: {batch_sizes}")
    print()
    print("Batch configurations:")
    for bs in batch_sizes:
        num_batches = len(test_texts) // bs
        print(f"  batch_size={bs:2}: {num_batches:2} batches × {bs:2} texts = {num_batches * bs} texts")
    print()

    # Estimate time
    estimated_time = len(test_texts) * len(batch_sizes) * 2.3 / 60
    print(f"Estimated time: ~{estimated_time:.1f} minutes")
    print()

    results = []

    for batch_size in batch_sizes:
        print(f"Testing batch_size={batch_size:2}...", end=" ", flush=True)

        result = measure_batch_performance(batch_size, test_texts)
        results.append(result)

        print(f"{result['time']:.1f}s ({result['num_batches']} batches)")

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
        print(f"  {i:2}. batch_size={r['batch_size']:2}: {r['time']:6.1f}s (+{diff:4.1f}s, +{pct:4.1f}%)")

    # Current default
    bs5 = next((r for r in results if r['batch_size'] == 5), None)
    if bs5:
        rank = sorted_results.index(bs5) + 1
        print(f"\nCurrent default (batch_size=5):")
        print(f"  Configuration: {bs5['num_batches']}×{bs5['batch_size']}")
        print(f"  Time: {bs5['time']:.1f}s")
        print(f"  Rank: {rank}/{len(results)}")
        if fastest['batch_size'] != 5:
            diff = bs5['time'] - fastest['time']
            pct = (diff / bs5['time']) * 100
            print(f"  Potential improvement with batch_size={fastest['batch_size']}: {diff:.1f}s ({pct:.1f}% faster)")

    # Write report
    output_path = project_root / "docs" / "BATCH_SIZE_FINAL_TEST.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PRACTICAL FAIR BATCH SIZE COMPARISON\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Test texts: {len(test_texts)} (LCM of 1,2,4,5,6,10)\n")
        f.write(f"Batch sizes tested: {batch_sizes}\n\n")

        f.write("BATCH CONFIGURATIONS (all divide evenly):\n")
        for bs in batch_sizes:
            num_batches = len(test_texts) // bs
            f.write(f"  batch_size={bs:2}: {num_batches:2} batches × {bs:2} texts = {num_batches * bs} texts\n")
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

        f.write(f"Fastest: batch_size={fastest['batch_size']} = {fastest['time']:.1f}s\n")
        f.write(f"Slowest: batch_size={slowest['batch_size']} = {slowest['time']:.1f}s\n")
        f.write(f"Range: {slowest['time'] - fastest['time']:.1f}s ({((slowest['time'] - fastest['time']) / slowest['time'] * 100):.1f}%)\n\n")

        f.write("RANKINGS:\n")
        for i, r in enumerate(sorted_results, 1):
            diff = r['time'] - fastest['time']
            pct = (diff / fastest['time'] * 100) if fastest['time'] > 0 else 0
            f.write(f"  {i:2}. batch_size={r['batch_size']:2}: {r['time']:6.1f}s (+{diff:4.1f}s, +{pct:4.1f}%)\n")
        f.write("\n")

        if bs5:
            rank = sorted_results.index(bs5) + 1
            f.write(f"CURRENT DEFAULT (batch_size=5):\n")
            f.write(f"  Configuration: {bs5['num_batches']}×{bs5['batch_size']}\n")
            f.write(f"  Time: {bs5['time']:.1f}s\n")
            f.write(f"  Rank: {rank}/{len(results)}\n")
            if fastest['batch_size'] != 5:
                diff = bs5['time'] - fastest['time']
                pct = (diff / bs5['time']) * 100
                f.write(f"  Potential improvement: {pct:.1f}% faster with batch_size={fastest['batch_size']}\n")
            f.write("\n")

        f.write("RECOMMENDATION:\n")
        f.write(f"Use batch_size={fastest['batch_size']} for optimal performance.\n")

    print(f"\nReport written to: {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
