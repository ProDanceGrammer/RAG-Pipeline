"""Index documents one at a time with better error handling."""
import sys
from pathlib import Path
import time
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chunking.structure_chunker import StructureChunker
from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.embedding_cache import EmbeddingCache
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def index_document(doc_path, strategy_name, chunker, embedder, cache, manager):
    """Index a single document with a single strategy."""
    print(f"\n[{strategy_name}] Processing {doc_path.name}...")

    # Read document
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk
    chunks = chunker.chunk(text)
    print(f"  Chunks: {len(chunks)}")

    # Extract texts
    texts = [chunk.text for chunk in chunks]

    # Check cache
    cached_embeddings, miss_indices = cache.get_batch(texts, embedder.model_name)
    print(f"  Cache: {len(texts) - len(miss_indices)}/{len(texts)} hits")

    # Embed missing texts one by one
    if miss_indices:
        print(f"  Embedding {len(miss_indices)} new chunks...")
        new_embeddings = []

        for i, idx in enumerate(miss_indices):
            if i % 10 == 0:
                print(f"    Progress: {i}/{len(miss_indices)}")

            try:
                emb = embedder.embed_single(texts[idx])
                new_embeddings.append(emb)
                # Cache immediately
                cache.set(texts[idx], embedder.model_name, emb)
            except Exception as e:
                logger.error(f"Failed to embed chunk {idx}: {e}")
                # Use zero vector as fallback
                new_embeddings.append(np.zeros(768))

        new_embeddings = np.array(new_embeddings)

        # Fill in cached embeddings
        for i, idx in enumerate(miss_indices):
            cached_embeddings[idx] = new_embeddings[i]

    # Convert to array
    embeddings = np.array(cached_embeddings)

    # Add to store
    print(f"  Adding to vector store...")
    manager.add_chunks(strategy_name, chunks, embeddings)

    # Save after each document
    manager.save_store(strategy_name)
    print(f"  Saved {strategy_name} store")


def main():
    """Index all documents with structure chunking only."""
    print("=" * 60)
    print("INDEXING DOCUMENTS - Structure Strategy Only")
    print("=" * 60)

    # Paths
    data_dir = Path("data/raw")
    cache_dir = Path("data/cache/embeddings")
    store_dir = Path("data/vector_stores")

    # Start with smaller documents first
    documents = [
        data_dir / "Machine Learning.md",
        data_dir / "Python.md",
        data_dir / "Database Optimization.md",
        data_dir / "OOP.md",  # Largest last
    ]

    # Initialize
    print("\nInitializing...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    cache = EmbeddingCache(cache_dir)
    manager = MultiStoreManager(store_dir)

    # Get dimension
    dimension = embedder.get_embedding_dimension()
    print(f"Embedding dimension: {dimension}")

    # Create store for structure strategy only
    strategy_name = "structure"
    print(f"\nCreating vector store for {strategy_name}...")
    manager.create_store(strategy_name, dimension)

    # Initialize chunker
    chunker = StructureChunker()

    # Process each document
    total_start = time.time()

    for doc_path in documents:
        if not doc_path.exists():
            logger.warning(f"Document not found: {doc_path}")
            continue

        print(f"\n{'=' * 60}")
        print(f"Document: {doc_path.name}")
        print(f"{'=' * 60}")

        doc_start = time.time()

        try:
            index_document(doc_path, strategy_name, chunker, embedder, cache, manager)
            doc_time = time.time() - doc_start
            print(f"\nDocument indexed in {doc_time:.2f}s ({doc_time/60:.2f} min)")
        except Exception as e:
            logger.error(f"Failed to index {doc_path.name}: {e}")
            continue

    # Final save
    print(f"\n{'=' * 60}")
    print("INDEXING COMPLETE")
    print(f"{'=' * 60}")

    total_time = time.time() - total_start
    print(f"\nTotal time: {total_time:.2f}s ({total_time/60:.2f} minutes)")

    # Statistics
    stats = manager.get_stats()
    print(f"\nVector Store: {stats[strategy_name]['size']} vectors")

    cache_stats = cache.get_stats()
    print(f"Cache: {cache_stats['num_cached']} embeddings ({cache_stats['total_size_mb']:.2f} MB)")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    main()
