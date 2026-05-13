"""Multi-vector store manager for different chunking strategies."""
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

from .vector_store import FAISSVectorStore
from ..chunking.base_chunker import Chunk

logger = logging.getLogger(__name__)


class MultiStoreManager:
    """Manages multiple vector stores for different chunking strategies."""

    def __init__(self, base_dir: Path):
        """
        Initialize multi-store manager.

        Args:
            base_dir: Base directory for storing vector stores
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.stores: Dict[str, FAISSVectorStore] = {}
        self.logger = logging.getLogger(__name__)

    def create_store(self, strategy_name: str, dimension: int) -> FAISSVectorStore:
        """
        Create a new vector store for a chunking strategy.

        Args:
            strategy_name: Name of the chunking strategy
            dimension: Embedding dimension

        Returns:
            Vector store instance
        """
        store_path = self.base_dir / f"{strategy_name}_store.faiss"
        store = FAISSVectorStore(dimension=dimension)
        self.stores[strategy_name] = store
        self.logger.info(f"Created vector store for strategy: {strategy_name}")
        return store

    def get_store(self, strategy_name: str) -> Optional[FAISSVectorStore]:
        """
        Get vector store for a strategy.

        Args:
            strategy_name: Name of the chunking strategy

        Returns:
            Vector store or None if not found
        """
        return self.stores.get(strategy_name)

    def add_chunks(
        self,
        strategy_name: str,
        chunks: List[Chunk],
        embeddings: np.ndarray
    ) -> None:
        """
        Add chunks and embeddings to a strategy's store.

        Args:
            strategy_name: Name of the chunking strategy
            chunks: List of chunks
            embeddings: Embedding vectors
        """
        store = self.stores.get(strategy_name)
        if store is None:
            raise ValueError(f"Store not found for strategy: {strategy_name}")

        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Chunks ({len(chunks)}) and embeddings ({len(embeddings)}) "
                "length mismatch"
            )

        # Convert chunks to metadata dicts
        metadatas = [
            {
                "text": chunk.text,
                "source": chunk.metadata.get("source", ""),
                "section": chunk.metadata.get("section", ""),
                "level": chunk.metadata.get("level", 0),
                "tokens": chunk.metadata.get("tokens", 0),
            }
            for chunk in chunks
        ]

        # Add to store
        store.add(embeddings, metadatas)
        self.logger.info(
            f"Added {len(chunks)} chunks to {strategy_name} store "
            f"(total: {store.get_size()})"
        )

    def search(
        self,
        strategy_name: str,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Search for similar chunks in a strategy's store.

        Args:
            strategy_name: Name of the chunking strategy
            query_embedding: Query embedding vector
            top_k: Number of results to return

        Returns:
            List of (metadata, score) tuples
        """
        store = self.stores.get(strategy_name)
        if store is None:
            raise ValueError(f"Store not found for strategy: {strategy_name}")

        raw_results = store.search(query_embedding, top_k=top_k)
        # Convert from (idx, distance, metadata) to (metadata, distance)
        results = [(metadata, distance) for idx, distance, metadata in raw_results]
        self.logger.debug(
            f"Search in {strategy_name} returned {len(results)} results"
        )
        return results

    def save_store(self, strategy_name: str) -> None:
        """
        Save a strategy's store to disk.

        Args:
            strategy_name: Name of the chunking strategy
        """
        store = self.stores.get(strategy_name)
        if store is None:
            raise ValueError(f"Store not found for strategy: {strategy_name}")

        store_path = self.base_dir / f"{strategy_name}_store.faiss"
        store.save(str(store_path))
        self.logger.info(f"Saved {strategy_name} store to {store_path}")

    def load_store(self, strategy_name: str, dimension: int) -> FAISSVectorStore:
        """
        Load a strategy's store from disk.

        Args:
            strategy_name: Name of the chunking strategy
            dimension: Embedding dimension

        Returns:
            Loaded vector store
        """
        store_path = self.base_dir / f"{strategy_name}_store.faiss"
        if not store_path.exists():
            raise FileNotFoundError(f"Store not found: {store_path}")

        store = FAISSVectorStore(dimension=dimension)
        store.load(str(store_path))
        self.stores[strategy_name] = store
        self.logger.info(
            f"Loaded {strategy_name} store from {store_path} "
            f"({store.get_size()} vectors)"
        )
        return store

    def save_all(self) -> None:
        """Save all stores to disk."""
        for strategy_name in self.stores:
            self.save_store(strategy_name)
        self.logger.info(f"Saved all {len(self.stores)} stores")

    def get_stats(self) -> Dict[str, Dict]:
        """
        Get statistics for all stores.

        Returns:
            Dictionary of strategy -> stats
        """
        stats = {}
        for strategy_name, store in self.stores.items():
            stats[strategy_name] = {
                "size": store.get_size(),
                "dimension": store.dimension,
            }
        return stats
