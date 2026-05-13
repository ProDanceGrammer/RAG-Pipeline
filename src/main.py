"""Main entry point for RAG Pipeline."""
import argparse
import yaml
from pathlib import Path
from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore, ChromaVectorStore
from src.rag.retriever import Retriever
from src.inference.inference_engine import InferenceEngine


def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline")
    parser.add_argument("--query", type=str, help="Query to process")
    parser.add_argument("--config", default="config/model_config.yaml", help="Config file")
    parser.add_argument("--vector-store", default="data/vectordb", help="Vector store path")
    parser.add_argument("--no-rag", action="store_true", help="Disable RAG retrieval")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    print("Initializing RAG Pipeline...")
    factory = ModelFactory(args.config)
    llm = factory.create_default_model()

    embedder = Embedder(llm, batch_size=config["embeddings"]["batch_size"])

    vector_store_path = Path(args.vector_store)
    if vector_store_path.exists():
        print(f"Loading vector store from {args.vector_store}...")
        vector_store = FAISSVectorStore(dimension=config["embeddings"]["dimension"])
        vector_store.load(args.vector_store)
        retriever = Retriever(
            vector_store,
            embedder,
            top_k=config["rag"]["top_k"],
            similarity_threshold=config["rag"]["similarity_threshold"]
        )
    else:
        print("No vector store found. RAG disabled.")
        retriever = None

    engine = InferenceEngine(llm, retriever)

    if args.query:
        print(f"\nQuery: {args.query}")
        print("\nProcessing...")
        response = engine.query(args.query, use_rag=not args.no_rag and retriever is not None)
        print(f"\nResponse:\n{response}")
    else:
        print("\nInteractive mode. Type 'exit' to quit.")
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if not query:
                continue

            response = engine.query(query, use_rag=not args.no_rag and retriever is not None)
            print(f"\nResponse:\n{response}")


if __name__ == "__main__":
    main()
