from typing import List, Dict, Any
from pathlib import Path
import json
from .vector_store import VectorStore
from .embedder import Embedder
from ..processing.chunking import TextChunker


class DocumentIndexer:
    """Index documents into vector store."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: Embedder,
        chunker: TextChunker
    ):
        self.vector_store = vector_store
        self.embedder = embedder
        self.chunker = chunker

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Index a list of documents."""
        all_chunks = []
        all_metadata = []

        for doc in documents:
            text = doc.get("text", "")
            source = doc.get("source", "unknown")

            chunks = self.chunker.chunk(text)

            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    "text": chunk,
                    "source": source,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    **{k: v for k, v in doc.items() if k not in ["text", "source"]}
                })

        embeddings = self.embedder.embed_texts(all_chunks)
        self.vector_store.add(embeddings, all_metadata)

    def index_from_files(self, file_paths: List[str]):
        """Index documents from file paths."""
        documents = []

        for file_path in file_paths:
            path = Path(file_path)

            if path.suffix == ".txt":
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif path.suffix == ".json":
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    text = data.get("text", str(data))
            else:
                continue

            documents.append({
                "text": text,
                "source": str(path),
                "filename": path.name
            })

        self.index_documents(documents)
