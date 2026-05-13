"""Test retrieval from indexed documents."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_embedder import OllamaEmbedder
from src.rag.multi_store_manager import MultiStoreManager


def main():
    """Test retrieval."""
    print("=" * 60)
    print("TESTING RETRIEVAL")
    print("=" * 60)

    # Initialize
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))

    # Load store
    print("\nLoading vector store...")
    manager.load_store("structure", dimension=768)

    stats = manager.get_stats()
    print(f"Loaded: {stats['structure']['size']} vectors")

    # Test queries
    queries = [
        "What is encapsulation in OOP?",
        "How does inheritance work?",
        "What are Python decorators?",
        "Explain database indexing",
        "What is machine learning?",
    ]

    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"{'=' * 60}")

        # Embed query
        query_emb = embedder.embed_single(query)

        # Search
        results = manager.search("structure", query_emb, top_k=3)

        # Display results
        for i, (metadata, score) in enumerate(results):
            print(f"\n[{i+1}] Score: {score:.2f}")
            print(f"Source: {metadata.get('source', 'N/A')}")
            print(f"Section: {metadata.get('section', 'N/A')}")
            text = metadata['text'][:150].encode('ascii', 'ignore').decode('ascii')
            print(f"Text: {text}...")

    print(f"\n{'=' * 60}")
    print("RETRIEVAL TEST COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
