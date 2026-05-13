"""Test indexing with a single small document."""
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


def main():
    """Test indexing with smallest document."""
    print("=" * 60)
    print("TEST INDEXING - Machine Learning.md only")
    print("=" * 60)

    # Paths
    doc_path = Path("data/raw/Machine Learning.md")
    cache_dir = Path("data/cache/embeddings")
    store_dir = Path("data/vector_stores")

    if not doc_path.exists():
        print(f"ERROR: Document not found: {doc_path}")
        return

    # Initialize components
    print("\nInitializing...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    cache = EmbeddingCache(cache_dir)
    manager = MultiStoreManager(store_dir)

    # Get dimension
    print("Getting embedding dimension...")
    dimension = embedder.get_embedding_dimension()
    print(f"Dimension: {dimension}")

    # Create store
    print("\nCreating vector store...")
    manager.create_store("test_structure", dimension)

    # Read document
    print(f"\nReading {doc_path.name}...")
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk
    print("Chunking...")
    chunker = StructureChunker()
    chunks = chunker.chunk(text)
    print(f"Created {len(chunks)} chunks")

    # Limit to first 10 chunks for testing
    chunks = chunks[:10]
    texts = [chunk.text for chunk in chunks]
    print(f"Testing with first {len(chunks)} chunks")

    # Check cache
    print("\nChecking cache...")
    cached_embeddings, miss_indices = cache.get_batch(texts, embedder.model_name)
    print(f"Cache hits: {len(texts) - len(miss_indices)}/{len(texts)}")

    # Embed missing
    if miss_indices:
        print(f"\nEmbedding {len(miss_indices)} chunks...")
        start_time = time.time()

        missing_texts = [texts[i] for i in miss_indices]

        # Embed one by one with progress
        new_embeddings = []
        for i, text in enumerate(missing_texts):
            print(f"  [{i+1}/{len(missing_texts)}] Embedding chunk {miss_indices[i]+1}...")
            try:
                emb = embedder.embed_single(text)
                new_embeddings.append(emb)
                print(f"    OK (dim: {len(emb)})")
            except Exception as e:
                print(f"    ERROR: {e}")
                raise

        new_embeddings = np.array(new_embeddings)
        elapsed = time.time() - start_time
        print(f"\nEmbedding complete: {elapsed:.2f}s ({elapsed/len(miss_indices):.2f}s per chunk)")

        # Cache
        cache.set_batch(missing_texts, embedder.model_name, new_embeddings)

        # Fill in
        for i, idx in enumerate(miss_indices):
            cached_embeddings[idx] = new_embeddings[i]

    # Convert to array
    embeddings = np.array(cached_embeddings)
    print(f"\nEmbeddings shape: {embeddings.shape}")

    # Add to store
    print("Adding to vector store...")
    manager.add_chunks("test_structure", chunks, embeddings)

    # Save
    print("Saving...")
    manager.save_store("test_structure")

    # Test search
    print("\nTesting search...")
    query = "What is machine learning?"
    query_emb = embedder.embed_single(query)
    results = manager.search("test_structure", query_emb, top_k=3)

    print(f"\nQuery: {query}")
    print(f"Results: {len(results)}")
    for i, (metadata, score) in enumerate(results):
        print(f"\n[{i+1}] Score: {score:.4f}")
        print(f"Section: {metadata.get('section', 'N/A')}")
        text_preview = metadata['text'][:100].encode('ascii', 'ignore').decode('ascii')
        print(f"Text preview: {text_preview}...")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
