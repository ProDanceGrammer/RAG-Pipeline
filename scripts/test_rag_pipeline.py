"""Test RAG pipeline without console interaction."""
import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_embedder import OllamaEmbedder
from src.core.ollama_client import OllamaClient
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.rag_pipeline import RAGPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Test RAG pipeline."""
    print("=" * 60)
    print("TESTING RAG PIPELINE")
    print("=" * 60)

    # Initialize
    print("\nInitializing components...")
    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
    generator = OllamaClient(model_name="llama3.1:latest")
    manager = MultiStoreManager(Path("data/vector_stores"))

    # Load vector store
    print("Loading vector store...")
    manager.load_store("structure", dimension=768)

    # Create pipeline
    pipeline = RAGPipeline(
        embedder=embedder,
        generator=generator,
        manager=manager,
        strategy_name="structure",
        top_k=3,
        max_context_length=2000
    )

    print("Pipeline ready!\n")

    # Test queries
    test_queries = [
        "What is encapsulation?",
        "How do Python decorators work?",
        "What is database indexing?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"TEST QUERY {i}: {query}")
        print(f"{'=' * 60}")

        try:
            result = pipeline.query(query)

            print("\nANSWER:")
            print("-" * 60)
            answer = result['answer'].encode('ascii', 'ignore').decode('ascii')
            print(answer)

            print("\n\nSOURCES:")
            print("-" * 60)
            for j, source in enumerate(result['sources'], 1):
                section = source['section'].encode('ascii', 'ignore').decode('ascii')
                print(f"[{j}] {section} (score: {source['score']:.2f})")

            print(f"\nLatency: {result['latency']:.2f}s")

        except Exception as e:
            print(f"ERROR: {e}")
            logger.error(f"Query failed: {e}")

    print(f"\n{'=' * 60}")
    print("TEST COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
