import numpy as np
from typing import List, Union
from ..core.base_llm import BaseLLM


class Embedder:
    """Document embedding generation."""

    def __init__(self, llm: BaseLLM, batch_size: int = 100):
        self.llm = llm
        self.batch_size = batch_size

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = self.llm.embed(batch)
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    def embed_single(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embedding = self.llm.embed([text])[0]
        return np.array(embedding)

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
