"""Ollama embedder implementation."""
import requests
import numpy as np
from typing import List
import logging
import time

logger = logging.getLogger(__name__)


class OllamaEmbedder:
    """Generate embeddings using Ollama."""

    def __init__(
        self,
        model_name: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
        batch_size: int = 12,
        timeout: int = 60,
        max_retries: int = 3
    ):
        """
        Initialize Ollama embedder.

        Args:
            model_name: Embedding model name
            base_url: Ollama API base URL
            batch_size: Number of texts to embed at once
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        self.model_name = model_name
        self.base_url = base_url
        self.batch_size = batch_size
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            Array of embeddings
        """
        all_embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            self.logger.debug(f"Embedding batch {i // self.batch_size + 1}")

            for text in batch:
                embedding = self.embed_single(text)
                all_embeddings.append(embedding)
                # Small delay to avoid overloading Ollama
                time.sleep(0.1)

        return np.array(all_embeddings)

    def embed_single(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        url = f"{self.base_url}/api/embeddings"

        payload = {
            "model": self.model_name,
            "prompt": text
        }

        # Retry logic
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()

                data = response.json()
                embedding = data.get("embedding", [])

                if not embedding:
                    raise ValueError("Empty embedding returned")

                return np.array(embedding)

            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(5 * (2 ** attempt))  # Longer exponential backoff
                else:
                    raise

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5 * (2 ** attempt))  # Longer exponential backoff
                else:
                    raise

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings from this model.

        Returns:
            Embedding dimension
        """
        # Test with a simple text
        test_embedding = self.embed_single("test")
        return len(test_embedding)

    def is_available(self) -> bool:
        """
        Check if embedding model is available.

        Returns:
            True if available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                return self.model_name in model_names
            return False
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
