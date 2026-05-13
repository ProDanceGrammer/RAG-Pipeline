"""Embedding cache system to avoid re-computing embeddings."""
import pickle
import hashlib
import logging
from pathlib import Path
from typing import List, Optional
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingCache:
    """Cache embeddings to disk to avoid recomputation."""

    def __init__(self, cache_dir: Path):
        """
        Initialize embedding cache.

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def _get_cache_key(self, text: str, model_name: str) -> str:
        """
        Generate cache key from text and model name.

        Args:
            text: Text to embed
            model_name: Name of embedding model

        Returns:
            Cache key (hash)
        """
        content = f"{model_name}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get cache file path for a key.

        Args:
            cache_key: Cache key

        Returns:
            Path to cache file
        """
        # Use first 2 chars as subdirectory for better file distribution
        subdir = self.cache_dir / cache_key[:2]
        subdir.mkdir(exist_ok=True)
        return subdir / f"{cache_key}.pkl"

    def get(self, text: str, model_name: str) -> Optional[np.ndarray]:
        """
        Get cached embedding if available.

        Args:
            text: Text to embed
            model_name: Name of embedding model

        Returns:
            Cached embedding or None
        """
        cache_key = self._get_cache_key(text, model_name)
        cache_path = self._get_cache_path(cache_key)

        if cache_path.exists():
            try:
                with open(cache_path, "rb") as f:
                    embedding = pickle.load(f)
                self.logger.debug(f"Cache hit for key: {cache_key[:8]}...")
                return embedding
            except Exception as e:
                self.logger.warning(f"Failed to load cache: {e}")
                return None

        self.logger.debug(f"Cache miss for key: {cache_key[:8]}...")
        return None

    def set(self, text: str, model_name: str, embedding: np.ndarray) -> None:
        """
        Cache an embedding.

        Args:
            text: Text that was embedded
            model_name: Name of embedding model
            embedding: Embedding vector
        """
        cache_key = self._get_cache_key(text, model_name)
        cache_path = self._get_cache_path(cache_key)

        try:
            with open(cache_path, "wb") as f:
                pickle.dump(embedding, f)
            self.logger.debug(f"Cached embedding for key: {cache_key[:8]}...")
        except Exception as e:
            self.logger.warning(f"Failed to cache embedding: {e}")

    def get_batch(
        self,
        texts: List[str],
        model_name: str
    ) -> tuple[List[Optional[np.ndarray]], List[int]]:
        """
        Get cached embeddings for multiple texts.

        Args:
            texts: List of texts
            model_name: Name of embedding model

        Returns:
            Tuple of (embeddings list with None for misses, indices of misses)
        """
        embeddings = []
        miss_indices = []

        for i, text in enumerate(texts):
            embedding = self.get(text, model_name)
            embeddings.append(embedding)
            if embedding is None:
                miss_indices.append(i)

        hit_count = len(texts) - len(miss_indices)
        self.logger.info(
            f"Batch cache: {hit_count}/{len(texts)} hits "
            f"({100 * hit_count / len(texts):.1f}%)"
        )

        return embeddings, miss_indices

    def set_batch(
        self,
        texts: List[str],
        model_name: str,
        embeddings: np.ndarray
    ) -> None:
        """
        Cache multiple embeddings.

        Args:
            texts: List of texts
            model_name: Name of embedding model
            embeddings: Array of embedding vectors
        """
        if len(texts) != len(embeddings):
            raise ValueError("Texts and embeddings length mismatch")

        for text, embedding in zip(texts, embeddings):
            self.set(text, model_name, embedding)

        self.logger.info(f"Cached {len(texts)} embeddings")

    def clear(self) -> None:
        """Clear all cached embeddings."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info("Cleared embedding cache")

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        cache_files = list(self.cache_dir.rglob("*.pkl"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "num_cached": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(self.cache_dir),
        }
