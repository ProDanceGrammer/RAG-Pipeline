"""Base classes for chunking strategies."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""

    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate token count after initialization."""
        if 'tokens' not in self.metadata:
            self.metadata['tokens'] = self._estimate_tokens()

    def _estimate_tokens(self) -> int:
        """Estimate token count (rough approximation: words * 1.3)."""
        return int(len(self.text.split()) * 1.3)

    def __len__(self) -> int:
        """Return token count."""
        return self.metadata.get('tokens', 0)

    def __repr__(self) -> str:
        """String representation."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Chunk(tokens={len(self)}, text='{preview}')"


class BaseChunker(ABC):
    """Abstract base class for chunking strategies."""

    def __init__(self, **kwargs):
        """Initialize chunker with configuration."""
        self.config = kwargs
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def chunk(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Chunk text into smaller pieces.

        Args:
            text: Text to chunk
            source: Source identifier (filename, URL, etc.)

        Returns:
            List of Chunk objects
        """
        pass

    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Chunk]:
        """
        Chunk multiple documents.

        Args:
            documents: List of dicts with 'text' and 'source' keys

        Returns:
            List of all chunks from all documents
        """
        all_chunks = []

        for doc in documents:
            text = doc.get('text', '')
            source = doc.get('source', 'unknown')

            try:
                chunks = self.chunk(text, source)
                all_chunks.extend(chunks)
                self.logger.info(f"Chunked {source}: {len(chunks)} chunks")
            except Exception as e:
                self.logger.error(f"Error chunking {source}: {e}")

        return all_chunks

    def get_stats(self, chunks: List[Chunk]) -> Dict[str, Any]:
        """
        Calculate statistics for chunks.

        Args:
            chunks: List of chunks

        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'total_tokens': 0,
                'avg_tokens': 0,
                'min_tokens': 0,
                'max_tokens': 0
            }

        token_counts = [len(chunk) for chunk in chunks]

        return {
            'total_chunks': len(chunks),
            'total_tokens': sum(token_counts),
            'avg_tokens': sum(token_counts) / len(token_counts),
            'min_tokens': min(token_counts),
            'max_tokens': max(token_counts),
            'strategy': self.__class__.__name__
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}({self.config})"
