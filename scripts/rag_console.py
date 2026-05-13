"""Console interface for RAG pipeline."""
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/rag_console.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("RAG PIPELINE - Educational Knowledge Base")
    print("=" * 60)
    print("\nTopics: Python, OOP, Machine Learning, Database Optimization")
    print("\nCommands:")
    print("  - Type your question and press Enter")
    print("  - '/help' - Show help")
    print("  - '/stats' - Show statistics")
    print("  - '/stream' - Toggle streaming mode")
    print("  - '/exit' or '/quit' - Exit")
    print("\n" + "=" * 60 + "\n")


def print_help():
    """Print help information."""
    print("\n" + "=" * 60)
    print("HELP")
    print("=" * 60)
    print("\nHow to use:")
    print("  1. Type your question in natural language")
    print("  2. Press Enter to get an answer")
    print("  3. The system will retrieve relevant information and generate an answer")
    print("\nExample questions:")
    print("  - What is encapsulation?")
    print("  - How does inheritance work?")
    print("  - What are Python decorators?")
    print("  - Explain database indexing")
    print("  - What is machine learning?")
    print("\nCommands:")
    print("  /help   - Show this help")
    print("  /stats  - Show system statistics")
    print("  /stream - Toggle streaming mode (on/off)")
    print("  /exit   - Exit the program")
    print("=" * 60 + "\n")


def print_stats(pipeline: RAGPipeline):
    """Print system statistics."""
    print("\n" + "=" * 60)
    print("SYSTEM STATISTICS")
    print("=" * 60)

    stats = pipeline.manager.get_stats()
    strategy = pipeline.strategy_name

    print(f"\nVector Store: {strategy}")
    print(f"  Total vectors: {stats[strategy]['size']}")
    print(f"  Dimension: {stats[strategy]['dimension']}")
    print(f"  Top-K retrieval: {pipeline.top_k}")
    print(f"  Max context length: {pipeline.max_context_length} chars")

    print("\nModels:")
    print(f"  Embedder: {pipeline.embedder.model_name}")
    print(f"  Generator: {pipeline.generator.model_name}")

    print("=" * 60 + "\n")


def print_answer(result: dict, show_sources: bool = True):
    """Print answer with sources."""
    print("\n" + "-" * 60)
    print("ANSWER:")
    print("-" * 60)

    # Clean answer for console output
    answer = result['answer'].encode('ascii', 'ignore').decode('ascii')
    print(answer)

    if show_sources and result.get('sources'):
        print("\n" + "-" * 60)
        print("SOURCES:")
        print("-" * 60)

        for i, source in enumerate(result['sources'], 1):
            section = source['section'].encode('ascii', 'ignore').decode('ascii')
            score = source['score']
            print(f"\n[{i}] Section: {section}")
            print(f"    Relevance score: {score:.2f}")

    print("\n" + "-" * 60)
    print(f"Query time: {result['latency']:.2f}s")
    print("-" * 60 + "\n")


def main():
    """Main console interface."""
    print_banner()

    # Initialize components
    print("Initializing RAG pipeline...")
    try:
        embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
        generator = OllamaClient(model_name="llama3.1:latest")
        manager = MultiStoreManager(Path("data/vector_stores"))

        # Load vector store
        print("Loading knowledge base...")
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

        print("Ready!\n")

    except Exception as e:
        print(f"ERROR: Failed to initialize: {e}")
        logger.error(f"Initialization failed: {e}")
        return

    # Interactive loop
    streaming_mode = False
    query_count = 0

    while True:
        try:
            # Get user input
            mode_indicator = "[STREAM]" if streaming_mode else "[NORMAL]"
            user_input = input(f"{mode_indicator} > ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['/exit', '/quit']:
                print("\nGoodbye!")
                break

            elif user_input.lower() == '/help':
                print_help()
                continue

            elif user_input.lower() == '/stats':
                print_stats(pipeline)
                continue

            elif user_input.lower() == '/stream':
                streaming_mode = not streaming_mode
                status = "enabled" if streaming_mode else "disabled"
                print(f"\nStreaming mode {status}\n")
                continue

            # Process query
            query_count += 1
            logger.info(f"Query #{query_count}: {user_input}")

            if streaming_mode:
                # Streaming mode
                print("\n" + "-" * 60)
                print("ANSWER:")
                print("-" * 60)

                for chunk in pipeline.query_stream(user_input):
                    # Clean for console
                    clean_chunk = chunk.encode('ascii', 'ignore').decode('ascii')
                    print(clean_chunk, end='', flush=True)

                print("\n" + "-" * 60 + "\n")

            else:
                # Normal mode
                result = pipeline.query(user_input)
                print_answer(result, show_sources=True)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type /exit to quit.\n")
            continue

        except Exception as e:
            print(f"\nERROR: {e}\n")
            logger.error(f"Query error: {e}")
            continue

    # Cleanup
    print(f"\nTotal queries processed: {query_count}")
    logger.info(f"Session ended. Total queries: {query_count}")


if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    main()
