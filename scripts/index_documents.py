"""Index all documents with multiple chunking strategies."""
import sys
from pathlib import Path
import time
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chunking.structure_chunker import StructureChunker
from src.chunking.hierarchical_chunker import HierarchicalChunker
from src.chunking.sliding_window_chunker import SlidingWindowChunker
from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.embedding_cache import EmbeddingCache

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Index all documents."""
    print("=" * 60)
    print("INDEXING DOCUMENTS")
    print("=" * 60)

    # Paths
    data_dir = Path("data/raw")
    cache_dir = Path("data/cache/embeddings")
    store_dir = Path("data/vector_stores")

    documents = [
        data_dir / "OOP.md",
        data_dir / "Python.md",
        data_dir / "Database Optimization.md",
        data_dir / "Machine Learning.md",
    ]

    # Initialize components
    print("\nInitializing components...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    cache = EmbeddingCache(cache_dir)
    manager = MultiStoreManager(store_dir)

    # Get embedding dimension
    print("Getting embedding dimension...")
    dimension = embedder.get_embedding_dimension()
    print(f"Embedding dimension: {dimension}")

    # Define strategies
    strategies = {
        "structure": StructureChunker(),
        "hierarchical": HierarchicalChunker(),
        "sliding_window": SlidingWindowChunker(chunk_size=512, overlap=50),
    }

    # Create stores
    print("\nCreating vector stores...")
    for strategy_name in strategies:
        manager.create_store(strategy_name, dimension)

    # Process each document
    total_start = time.time()

    for doc_path in documents:
        if not doc_path.exists():
            logger.warning(f"Document not found: {doc_path}")
            continue

        print(f"\n{'=' * 60}")
        print(f"Processing: {doc_path.name}")
        print(f"{'=' * 60}")

        # Read document
        with open(doc_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Process with each strategy
        for strategy_name, chunker in strategies.items():
            print(f"\n[{strategy_name}] Chunking...")
            chunk_start = time.time()

            # Chunk document
            chunks = chunker.chunk(text)
            print(f"  Chunks: {len(chunks)}")

            # Extract texts
            texts = [chunk.text for chunk in chunks]

            # Check cache
            print(f"[{strategy_name}] Checking cache...")
            cached_embeddings, miss_indices = cache.get_batch(
                texts, embedder.model_name
            )

            # Embed missing texts
            if miss_indices:
                print(f"[{strategy_name}] Embedding {len(miss_indices)} new chunks...")
                embed_start = time.time()

                missing_texts = [texts[i] for i in miss_indices]
                new_embeddings = embedder.embed_texts(missing_texts)

                embed_time = time.time() - embed_start
                print(f"  Time: {embed_time:.2f}s ({embed_time/len(miss_indices):.2f}s per chunk)")

                # Cache new embeddings
                cache.set_batch(missing_texts, embedder.model_name, new_embeddings)

                # Fill in cached embeddings
                for i, idx in enumerate(miss_indices):
                    cached_embeddings[idx] = new_embeddings[i]

            # Convert to numpy array
            import numpy as np
            embeddings = np.array(cached_embeddings)

            # Add to vector store
            print(f"[{strategy_name}] Adding to vector store...")
            manager.add_chunks(strategy_name, chunks, embeddings)

            chunk_time = time.time() - chunk_start
            print(f"[{strategy_name}] Total time: {chunk_time:.2f}s")

    # Save all stores
    print(f"\n{'=' * 60}")
    print("Saving vector stores...")
    manager.save_all()

    # Print statistics
    print(f"\n{'=' * 60}")
    print("INDEXING COMPLETE")
    print(f"{'=' * 60}")

    total_time = time.time() - total_start
    print(f"\nTotal time: {total_time:.2f}s ({total_time/60:.2f} minutes)")

    print("\nVector Store Statistics:")
    stats = manager.get_stats()
    for strategy_name, strategy_stats in stats.items():
        print(f"  {strategy_name}: {strategy_stats['size']} vectors")

    print("\nCache Statistics:")
    cache_stats = cache.get_stats()
    print(f"  Cached embeddings: {cache_stats['num_cached']}")
    print(f"  Cache size: {cache_stats['total_size_mb']:.2f} MB")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    main()
