"""Sliding window chunking strategy."""
from typing import List
from .base_chunker import BaseChunker, Chunk
import logging

logger = logging.getLogger(__name__)


class SlidingWindowChunker(BaseChunker):
    """
    Sliding window chunking with fixed size and overlap.

    This is a baseline strategy for comparison.
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 50, **kwargs):
        """
        Initialize sliding window chunker.

        Args:
            chunk_size: Target chunk size in tokens
            overlap: Number of overlapping tokens between chunks
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.overlap = overlap

        if overlap >= chunk_size:
            raise ValueError("Overlap must be less than chunk_size")

    def chunk(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Chunk text using sliding window.

        Args:
            text: Text to chunk
            source: Source identifier

        Returns:
            List of chunks with fixed size and overlap
        """
        # Split into words (rough token approximation)
        words = text.split()

        if not words:
            return []

        chunks = []
        stride = self.chunk_size - self.overlap

        for i in range(0, len(words), stride):
            chunk_words = words[i:i + self.chunk_size]

            if not chunk_words:
                break

            chunk_text = ' '.join(chunk_words)

            chunk = Chunk(
                text=chunk_text,
                metadata={
                    'source': source,
                    'chunk_index': len(chunks),
                    'start_word': i,
                    'end_word': i + len(chunk_words),
                    'chunking_strategy': 'sliding_window',
                    'chunk_size': self.chunk_size,
                    'overlap': self.overlap
                }
            )

            chunks.append(chunk)

            # Stop if we've reached the end
            if i + self.chunk_size >= len(words):
                break

        self.logger.info(
            f"Created {len(chunks)} sliding window chunks from {source} "
            f"(size={self.chunk_size}, overlap={self.overlap})"
        )

        return chunks

    def __repr__(self) -> str:
        """String representation."""
        return f"SlidingWindowChunker(chunk_size={self.chunk_size}, overlap={self.overlap})"
