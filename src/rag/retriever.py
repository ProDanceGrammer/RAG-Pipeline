from typing import List, Dict, Any
import numpy as np
from .vector_store import VectorStore
from .embedder import Embedder


class Retriever:
    """Document retrieval using vector similarity."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: Embedder,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ):
        self.vector_store = vector_store
        self.embedder = embedder
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query."""
        query_embedding = self.embedder.embed_single(query)

        results = self.vector_store.search(query_embedding, self.top_k)

        filtered_results = []
        for idx, distance, metadata in results:
            similarity = 1 / (1 + distance)

            if similarity >= self.similarity_threshold:
                filtered_results.append({
                    "index": idx,
                    "similarity": similarity,
                    "distance": distance,
                    "metadata": metadata
                })

        return filtered_results

    def retrieve_with_context(self, query: str) -> str:
        """Retrieve documents and format as context string."""
        results = self.retrieve(query)

        if not results:
            return "No relevant context found."

        context_parts = []
        for i, result in enumerate(results, 1):
            text = result["metadata"].get("text", "")
            source = result["metadata"].get("source", "Unknown")
            context_parts.append(f"[{i}] (Source: {source})\n{text}")

        return "\n\n".join(context_parts)
