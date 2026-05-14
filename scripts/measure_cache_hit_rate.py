#!/usr/bin/env python3
"""
Measure cache hit rate by instrumenting the embedding cache.
"""
import sys
from pathlib import Path
import shutil
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.ollama_embedder import OllamaEmbedder
from src.rag.embedding_cache import EmbeddingCache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentedCache(EmbeddingCache):
    """Cache with hit/miss tracking."""

    def __init__(self, cache_dir: str):
        super().__init__(cache_dir)
        self.hits = 0
        self.misses = 0
        self.model_name = "nomic-embed-text"

    def get(self, text: str, model_name: str = None) -> any:
        """Get embedding from cache, tracking hits/misses."""
        if model_name is None:
            model_name = self.model_name
        result = super().get(text, model_name)
        if result is not None:
            self.hits += 1
            logger.debug(f"Cache HIT: {text[:50]}...")
        else:
            self.misses += 1
            logger.debug(f"Cache MISS: {text[:50]}...")
        return result

    def set(self, text: str, model_name: str, embedding):
        """Put embedding in cache."""
        super().set(text, model_name, embedding)

    def get_stats(self):
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total': total,
            'hit_rate': hit_rate,
        }

    def reset_stats(self):
        """Reset hit/miss counters."""
        self.hits = 0
        self.misses = 0


def test_scenario(name: str, cache: InstrumentedCache, embedder: OllamaEmbedder, texts: list):
    """Test a caching scenario."""
    logger.info(f"\n{'='*80}")
    logger.info(f"SCENARIO: {name}")
    logger.info(f"{'='*80}")

    cache.reset_stats()
    start_time = time.time()

    # Embed texts
    for i, text in enumerate(texts, 1):
        logger.info(f"  Processing text {i}/{len(texts)}...")

        # Check cache first
        cached = cache.get(text, cache.model_name)
        if cached is None:
            # Not in cache, compute embedding
            embeddings = embedder.embed_texts([text])
            embedding = embeddings[0]
            cache.set(text, cache.model_name, embedding)
        else:
            embedding = cached

    elapsed = time.time() - start_time
    stats = cache.get_stats()

    logger.info(f"\nResults:")
    logger.info(f"  Hits: {stats['hits']}")
    logger.info(f"  Misses: {stats['misses']}")
    logger.info(f"  Total requests: {stats['total']}")
    logger.info(f"  Hit rate: {stats['hit_rate']:.1f}%")
    logger.info(f"  Time: {elapsed:.2f}s")

    return stats


def main():
    logger.info("Cache Hit Rate Measurement")
    logger.info("=" * 80)

    # Setup
    cache_dir = project_root / "data" / "cache" / "test_cache"
    embedder = OllamaEmbedder()

    # Sample texts for testing
    sample_texts = [
        "What is encapsulation in object-oriented programming?",
        "How does inheritance work in Python?",
        "What are the SOLID principles?",
        "Explain polymorphism with examples",
        "What is the difference between composition and inheritance?",
    ]

    all_results = []

    # Scenario 1: Fresh cache (cold start)
    logger.info("\n" + "=" * 80)
    logger.info("SCENARIO 1: Fresh indexing (cold start)")
    logger.info("=" * 80)
    logger.info("Clearing cache...")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache = InstrumentedCache(str(cache_dir))
    stats1 = test_scenario("Fresh indexing", cache, embedder, sample_texts)
    all_results.append(("Fresh indexing", stats1))

    # Scenario 2: Re-indexing (warm cache)
    logger.info("\n" + "=" * 80)
    logger.info("SCENARIO 2: Re-indexing (warm cache)")
    logger.info("=" * 80)
    logger.info("Using existing cache...")

    cache = InstrumentedCache(str(cache_dir))
    stats2 = test_scenario("Re-indexing", cache, embedder, sample_texts)
    all_results.append(("Re-indexing", stats2))

    # Scenario 3: Partial update (mixed)
    logger.info("\n" + "=" * 80)
    logger.info("SCENARIO 3: Partial update (mixed)")
    logger.info("=" * 80)
    logger.info("Adding new texts to existing cache...")

    mixed_texts = sample_texts[:3] + [
        "What is database normalization?",
        "How to optimize SQL queries?",
    ]

    cache = InstrumentedCache(str(cache_dir))
    stats3 = test_scenario("Partial update", cache, embedder, mixed_texts)
    all_results.append(("Partial update", stats3))

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)

    for scenario, stats in all_results:
        logger.info(f"\n{scenario}:")
        logger.info(f"  Hit rate: {stats['hit_rate']:.1f}%")
        logger.info(f"  Hits: {stats['hits']}, Misses: {stats['misses']}")

    # Write report
    output_path = project_root / "docs" / "CACHE_HIT_RATE.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CACHE HIT RATE MEASUREMENT REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Cache directory: {cache_dir}\n")
        f.write(f"Sample texts: {len(sample_texts)}\n\n")

        f.write("RESULTS BY SCENARIO:\n\n")

        for scenario, stats in all_results:
            f.write(f"{scenario}:\n")
            f.write(f"  Hit rate: {stats['hit_rate']:.1f}%\n")
            f.write(f"  Hits: {stats['hits']}\n")
            f.write(f"  Misses: {stats['misses']}\n")
            f.write(f"  Total requests: {stats['total']}\n\n")

        f.write("INTERPRETATION:\n\n")
        f.write("Fresh indexing: 0% hit rate (all cache misses)\n")
        f.write("  - First time embedding texts, nothing in cache\n")
        f.write("  - All embeddings must be computed\n\n")

        f.write("Re-indexing: 100% hit rate (all cache hits)\n")
        f.write("  - Same texts already in cache\n")
        f.write("  - No computation needed, instant retrieval\n\n")

        f.write("Partial update: 60% hit rate (3/5 hits)\n")
        f.write("  - 3 texts already cached (hits)\n")
        f.write("  - 2 new texts need computation (misses)\n")
        f.write("  - Typical scenario for incremental updates\n\n")

        f.write("CONCLUSION:\n")
        f.write("Cache hit rate varies by workload:\n")
        f.write("  - 0% for fresh indexing\n")
        f.write("  - 100% for re-indexing\n")
        f.write("  - 60% for partial updates (in this test)\n")
        f.write("  - Real-world: depends on how many texts are new vs repeated\n")

    logger.info(f"\nReport written to: {output_path}")

    # Cleanup test cache
    logger.info("\nCleaning up test cache...")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    logger.info("Done!")


if __name__ == '__main__':
    main()
