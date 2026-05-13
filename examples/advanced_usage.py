"""Advanced RAG examples."""
from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import ChromaVectorStore
from src.rag.retriever import Retriever
from src.rag.indexer import DocumentIndexer
from src.processing.chunking import TextChunker
from src.processing.preprocessor import TextPreprocessor
from src.prompts.chain import PromptChain
from src.inference.inference_engine import InferenceEngine


def example_chroma_vector_store():
    """Example: Using ChromaDB instead of FAISS."""
    print("=== ChromaDB Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    embedder = Embedder(llm)
    vector_store = ChromaVectorStore(
        collection_name="my_documents",
        persist_directory="data/vectordb/chroma"
    )

    chunker = TextChunker()
    indexer = DocumentIndexer(vector_store, embedder, chunker)

    documents = [
        {"text": "Python is a high-level programming language.", "source": "python.txt"},
        {"text": "JavaScript is used for web development.", "source": "js.txt"}
    ]

    indexer.index_documents(documents)
    print("Documents indexed in ChromaDB\n")


def example_text_preprocessing():
    """Example: Text preprocessing before indexing."""
    print("=== Text Preprocessing Example ===\n")

    raw_text = """
    Check out https://example.com for more info!
    Contact us at support@example.com

    This    has    extra    whitespace...
    """

    cleaned = TextPreprocessor.preprocess(
        raw_text,
        remove_urls=True,
        remove_emails=True,
        remove_special_chars=False
    )

    print(f"Original:\n{raw_text}\n")
    print(f"Cleaned:\n{cleaned}\n")


def example_prompt_chaining():
    """Example: Multi-step prompt chain."""
    print("=== Prompt Chaining Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    chain = PromptChain(llm)
    chain.add_step(
        "extract",
        "Extract the main topics from this text: {input}"
    )
    chain.add_step(
        "summarize",
        "Create a one-sentence summary of these topics: {input}"
    )

    document = """
    Artificial intelligence and machine learning are transforming healthcare.
    Deep learning models can now detect diseases from medical images with high accuracy.
    Natural language processing helps analyze patient records efficiently.
    """

    result = chain.execute(document)
    print(f"Final result: {result}\n")

    print("Intermediate steps:")
    for i, step_result in enumerate(chain.get_intermediate_results(), 1):
        print(f"Step {i}: {step_result}\n")


def example_streaming_response():
    """Example: Streaming LLM responses."""
    print("=== Streaming Response Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    engine = InferenceEngine(llm)

    print("Streaming response: ", end="", flush=True)
    for chunk in engine.query("Explain quantum computing in one sentence.", stream=True):
        print(chunk, end="", flush=True)
    print("\n")


def example_custom_chunking():
    """Example: Different chunking strategies."""
    print("=== Custom Chunking Example ===\n")

    text = """
    First paragraph about AI.
    It has multiple sentences.

    Second paragraph about ML.
    Also with multiple sentences.

    Third paragraph about DL.
    """

    chunker = TextChunker()

    # Chunk by paragraphs
    para_chunks = chunker.chunk_by_paragraphs(text)
    print(f"Paragraph chunks: {len(para_chunks)}")
    for i, chunk in enumerate(para_chunks, 1):
        print(f"  {i}. {chunk[:50]}...")

    # Chunk by sentences
    sent_chunks = chunker.chunk_by_sentences(text, max_sentences=2)
    print(f"\nSentence chunks: {len(sent_chunks)}")
    for i, chunk in enumerate(sent_chunks, 1):
        print(f"  {i}. {chunk[:50]}...")


def example_retrieval_with_threshold():
    """Example: Retrieval with similarity threshold."""
    print("=== Retrieval with Threshold Example ===\n")

    factory = ModelFactory()
    llm = factory.create_model("openai", "gpt35")

    embedder = Embedder(llm)
    vector_store = ChromaVectorStore()
    chunker = TextChunker()

    documents = [
        {"text": "Python is great for data science.", "source": "python.txt"},
        {"text": "Java is used for enterprise applications.", "source": "java.txt"},
        {"text": "JavaScript runs in web browsers.", "source": "js.txt"}
    ]

    indexer = DocumentIndexer(vector_store, embedder, chunker)
    indexer.index_documents(documents)

    # High threshold - only very similar results
    retriever = Retriever(vector_store, embedder, top_k=5, similarity_threshold=0.9)
    results = retriever.retrieve("Tell me about Python")

    print(f"Found {len(results)} results above threshold 0.9")
    for result in results:
        print(f"  Similarity: {result['similarity']:.3f} - {result['metadata']['source']}")


if __name__ == "__main__":
    # Run examples (uncomment as needed)
    # example_chroma_vector_store()
    # example_text_preprocessing()
    # example_prompt_chaining()
    # example_streaming_response()
    # example_custom_chunking()
    # example_retrieval_with_threshold()

    print("Advanced examples ready. Uncomment function calls to run.")
