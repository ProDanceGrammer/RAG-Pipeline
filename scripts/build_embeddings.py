"""Build embeddings for documents."""
import argparse
import yaml
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore, ChromaVectorStore
from src.rag.indexer import DocumentIndexer
from src.processing.chunking import TextChunker


def main():
    parser = argparse.ArgumentParser(description="Build embeddings for documents")
    parser.add_argument("--input-dir", required=True, help="Directory containing documents")
    parser.add_argument("--output-dir", default="data/vectordb", help="Output directory for vector store")
    parser.add_argument("--vector-store", choices=["faiss", "chroma"], default="faiss", help="Vector store type")
    parser.add_argument("--config", default="config/model_config.yaml", help="Config file path")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    print("Initializing models...")
    factory = ModelFactory(args.config)
    llm = factory.create_model("openai", "gpt35")

    embedder = Embedder(llm, batch_size=config["embeddings"]["batch_size"])

    chunker = TextChunker(
        chunk_size=config["rag"]["chunk_size"],
        chunk_overlap=config["rag"]["chunk_overlap"]
    )

    if args.vector_store == "faiss":
        vector_store = FAISSVectorStore(dimension=config["embeddings"]["dimension"])
    else:
        vector_store = ChromaVectorStore(persist_directory=args.output_dir)

    indexer = DocumentIndexer(vector_store, embedder, chunker)

    print(f"Indexing documents from {args.input_dir}...")
    input_path = Path(args.input_dir)
    file_paths = list(input_path.glob("**/*.txt")) + list(input_path.glob("**/*.json"))

    if not file_paths:
        print("No documents found!")
        return

    indexer.index_from_files([str(p) for p in file_paths])

    print(f"Saving vector store to {args.output_dir}...")
    vector_store.save(args.output_dir)

    print(f"Successfully indexed {len(file_paths)} documents!")


if __name__ == "__main__":
    main()
