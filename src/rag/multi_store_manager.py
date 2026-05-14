"""Multi-vector store manager for different chunking strategies."""
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

from .vector_store import FAISSVectorStore
from .bm25_retriever import BM25Retriever
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
        self.bm25_indices: Dict[str, BM25Retriever] = {}
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

        # Also create BM25 index
        bm25 = BM25Retriever()
        self.bm25_indices[strategy_name] = bm25

        self.logger.info(f"Created vector store and BM25 index for strategy: {strategy_name}")
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

        # Add to FAISS store
        store.add(embeddings, metadatas)

        # Build BM25 index from chunk texts
        bm25 = self.bm25_indices.get(strategy_name)
        if bm25 is None:
            bm25 = BM25Retriever()
            self.bm25_indices[strategy_name] = bm25

        # Extract texts for BM25 indexing
        texts = [chunk.text for chunk in chunks]
        bm25.index(texts)

        self.logger.info(
            f"Added {len(chunks)} chunks to {strategy_name} store "
            f"(FAISS: {store.get_size()}, BM25: {bm25.get_size()})"
        )

    def search(
        self,
        strategy_name: str,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Search for similar chunks in a strategy's store using semantic search.

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
            f"Semantic search in {strategy_name} returned {len(results)} results"
        )
        return results

    def search_bm25(
        self,
        strategy_name: str,
        query_text: str,
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Search for similar chunks using BM25 keyword search.

        Args:
            strategy_name: Name of the chunking strategy
            query_text: Query text
            top_k: Number of results to return

        Returns:
            List of (metadata, bm25_score) tuples
        """
        bm25 = self.bm25_indices.get(strategy_name)
        if bm25 is None:
            raise ValueError(f"BM25 index not found for strategy: {strategy_name}")

        store = self.stores.get(strategy_name)
        if store is None:
            raise ValueError(f"Store not found for strategy: {strategy_name}")

        # Get BM25 results (doc_idx, score)
        bm25_results = bm25.search(query_text, top_k=top_k)

        # Convert to (metadata, score) format
        results = []
        for doc_idx, score in bm25_results:
            if doc_idx < len(store.metadata):
                results.append((store.metadata[doc_idx], score))

        self.logger.debug(
            f"BM25 search in {strategy_name} returned {len(results)} results"
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

        # Save FAISS store
        store_path = self.base_dir / f"{strategy_name}_store.faiss"
        store.save(str(store_path))

        # Save BM25 index
        bm25 = self.bm25_indices.get(strategy_name)
        if bm25 is not None:
            bm25_path = self.base_dir / f"{strategy_name}_bm25.pkl"
            try:
                bm25.save(str(bm25_path))
                self.logger.info(f"Saved {strategy_name} store and BM25 index")
            except Exception as e:
                self.logger.error(f"Failed to save BM25 index: {e}")
                # Don't fail the whole operation if BM25 save fails
        else:
            self.logger.info(f"Saved {strategy_name} store (no BM25 index)")

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

        # Load FAISS store
        store = FAISSVectorStore(dimension=dimension)
        store.load(str(store_path))
        self.stores[strategy_name] = store

        # Load BM25 index if it exists
        bm25_path = self.base_dir / f"{strategy_name}_bm25.pkl"
        if bm25_path.exists():
            try:
                bm25 = BM25Retriever()
                bm25.load(str(bm25_path))
                self.bm25_indices[strategy_name] = bm25
                self.logger.info(
                    f"Loaded {strategy_name} store from {store_path} "
                    f"({store.get_size()} vectors, {bm25.get_size()} BM25 docs)"
                )
            except Exception as e:
                self.logger.warning(f"Failed to load BM25 index: {e}")
                self.logger.info(
                    f"Loaded {strategy_name} store from {store_path} "
                    f"({store.get_size()} vectors, no BM25 index)"
                )
        else:
            self.logger.info(
                f"Loaded {strategy_name} store from {store_path} "
                f"({store.get_size()} vectors, no BM25 index)"
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
            bm25 = self.bm25_indices.get(strategy_name)
            stats[strategy_name] = {
                "size": store.get_size(),
                "dimension": store.dimension,
                "bm25_size": bm25.get_size() if bm25 else 0,
            }
        return stats
