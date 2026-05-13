"""Example usage of RAG Pipeline."""
from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore
from src.rag.retriever import Retriever
from src.rag.indexer import DocumentIndexer
from src.processing.chunking import TextChunker
from src.inference.inference_engine import InferenceEngine


def example_basic_query():
    """Example: Basic query without RAG."""
    print("=== Basic Query Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    engine = InferenceEngine(llm)

    response = engine.query("What is machine learning?", use_rag=False)
    print(f"Response: {response}\n")


def example_rag_pipeline():
    """Example: Full RAG pipeline."""
    print("=== RAG Pipeline Example ===\n")

    # Initialize components
    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    embedder = Embedder(llm, batch_size=100)
    vector_store = FAISSVectorStore(dimension=1536)
    chunker = TextChunker(chunk_size=512, chunk_overlap=50)

    # Index documents
    documents = [
        {
            "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
            "source": "ml_intro.txt"
        },
        {
            "text": "Deep learning uses neural networks with multiple layers to process complex patterns.",
            "source": "dl_intro.txt"
        }
    ]

    indexer = DocumentIndexer(vector_store, embedder, chunker)
    indexer.index_documents(documents)

    # Query with RAG
    retriever = Retriever(vector_store, embedder, top_k=3)
    engine = InferenceEngine(llm, retriever)

    response = engine.query("What is machine learning?", use_rag=True)
    print(f"Response: {response}\n")


def example_summarization():
    """Example: Text summarization."""
    print("=== Summarization Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")
    engine = InferenceEngine(llm)

    text = """
    Artificial intelligence has transformed many industries. Machine learning algorithms
    can now process vast amounts of data and identify patterns that humans might miss.
    Deep learning, a subset of machine learning, has been particularly successful in
    image recognition, natural language processing, and game playing.
    """

    summary = engine.summarize(text)
    print(f"Summary: {summary}\n")


def example_extraction():
    """Example: Entity extraction."""
    print("=== Extraction Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")
    engine = InferenceEngine(llm)

    text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."

    entities = engine.extract(text, "companies and people")
    print(f"Extracted entities: {entities}\n")


if __name__ == "__main__":
    # Run examples (comment out those requiring API keys if not available)
    # example_basic_query()
    # example_rag_pipeline()
    # example_summarization()
    # example_extraction()

    print("Examples ready to run. Uncomment the function calls above.")
