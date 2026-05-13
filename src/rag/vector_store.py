import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import pickle
from pathlib import Path


class VectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    def add(self, vectors: np.ndarray, metadata: List[dict]):
        """Add vectors with metadata to the store."""
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, dict]]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    def save(self, path: str):
        """Save the vector store to disk."""
        pass

    @abstractmethod
    def load(self, path: str):
        """Load the vector store from disk."""
        pass


class FAISSVectorStore(VectorStore):
    """FAISS-based vector store implementation."""

    def __init__(self, dimension: int):
        try:
            import faiss
            self.faiss = faiss
        except ImportError:
            raise ImportError("faiss-cpu or faiss-gpu required. Install with: pip install faiss-cpu")

        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, vectors: np.ndarray, metadata: List[dict]):
        vectors = vectors.astype('float32')
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, dict]]:
        query_vector = query_vector.astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append((int(idx), float(dist), self.metadata[idx]))

        return results

    def save(self, path: str):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        self.faiss.write_index(self.index, str(path / "index.faiss"))
        with open(path / "metadata.pkl", 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self, path: str):
        path = Path(path)
        self.index = self.faiss.read_index(str(path / "index.faiss"))
        with open(path / "metadata.pkl", 'rb') as f:
            self.metadata = pickle.load(f)

    def get_size(self) -> int:
        """Get number of vectors in the store."""
        return self.index.ntotal


class ChromaVectorStore(VectorStore):
    """ChromaDB-based vector store implementation."""

    def __init__(self, collection_name: str = "documents", persist_directory: str = "data/vectordb"):
        try:
            import chromadb
            self.chromadb = chromadb
        except ImportError:
            raise ImportError("chromadb required. Install with: pip install chromadb")

        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, vectors: np.ndarray, metadata: List[dict]):
        ids = [f"doc_{i}" for i in range(len(vectors))]
        self.collection.add(
            embeddings=vectors.tolist(),
            metadatas=metadata,
            ids=ids
        )

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, dict]]:
        results = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k
        )

        output = []
        for i, (distance, metadata) in enumerate(zip(results['distances'][0], results['metadatas'][0])):
            output.append((i, distance, metadata))

        return output

    def save(self, path: str):
        pass

    def load(self, path: str):
        pass
