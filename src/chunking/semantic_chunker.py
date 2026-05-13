"""Semantic chunking strategy using embeddings."""
from typing import List
import numpy as np
from .base_chunker import BaseChunker, Chunk
import logging

logger = logging.getLogger(__name__)


class SemanticChunker(BaseChunker):
    """
    Semantic chunking based on embedding similarity.

    Splits text when semantic similarity drops below threshold.
    This is an experimental strategy to validate structure-based approach.
    """

    def __init__(
        self,
        embedder=None,
        similarity_threshold: float = 0.7,
        min_chunk_size: int = 50,
        max_chunk_size: int = 1000,
        **kwargs
    ):
        """
        Initialize semantic chunker.

        Args:
            embedder: Embedder instance for generating embeddings
            similarity_threshold: Minimum similarity to keep sentences together
            min_chunk_size: Minimum chunk size in tokens
            max_chunk_size: Maximum chunk size in tokens
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.embedder = embedder
        self.similarity_threshold = similarity_threshold
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Chunk text based on semantic similarity.

        Args:
            text: Text to chunk
            source: Source identifier

        Returns:
            List of semantically coherent chunks
        """
        if self.embedder is None:
            self.logger.warning(
                "No embedder provided, falling back to sentence-based chunking"
            )
            return self._fallback_sentence_chunking(text, source)

        # Split into sentences
        sentences = self._split_sentences(text)

        if len(sentences) <= 1:
            return [Chunk(
                text=text,
                metadata={
                    'source': source,
                    'chunking_strategy': 'semantic',
                    'chunk_index': 0
                }
            )]

        # Generate embeddings for sentences
        try:
            embeddings = self.embedder.embed_texts(sentences)
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return self._fallback_sentence_chunking(text, source)

        # Calculate similarity between consecutive sentences
        similarities = self._calculate_similarities(embeddings)

        # Find split points where similarity drops
        split_indices = self._find_split_points(similarities)

        # Create chunks
        chunks = self._create_chunks_from_splits(
            sentences, split_indices, source
        )

        self.logger.info(
            f"Created {len(chunks)} semantic chunks from {source} "
            f"(threshold={self.similarity_threshold})"
        )

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        import re

        # Simple sentence splitting (can be improved with nltk/spacy)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_similarities(self, embeddings: np.ndarray) -> List[float]:
        """
        Calculate cosine similarity between consecutive embeddings.

        Args:
            embeddings: Array of embeddings

        Returns:
            List of similarity scores
        """
        similarities = []

        for i in range(len(embeddings) - 1):
            vec1 = embeddings[i]
            vec2 = embeddings[i + 1]

            # Cosine similarity
            similarity = np.dot(vec1, vec2) / (
                np.linalg.norm(vec1) * np.linalg.norm(vec2)
            )
            similarities.append(float(similarity))

        return similarities

    def _find_split_points(self, similarities: List[float]) -> List[int]:
        """
        Find indices where similarity drops below threshold.

        Args:
            similarities: List of similarity scores

        Returns:
            List of split indices
        """
        split_indices = [0]  # Start with first sentence

        for i, sim in enumerate(similarities):
            if sim < self.similarity_threshold:
                split_indices.append(i + 1)

        return split_indices

    def _create_chunks_from_splits(
        self, sentences: List[str], split_indices: List[int], source: str
    ) -> List[Chunk]:
        """
        Create chunks from split points.

        Args:
            sentences: List of sentences
            split_indices: Indices where to split
            source: Source identifier

        Returns:
            List of chunks
        """
        chunks = []
        split_indices.append(len(sentences))  # Add end index

        for i in range(len(split_indices) - 1):
            start = split_indices[i]
            end = split_indices[i + 1]

            chunk_sentences = sentences[start:end]
            chunk_text = ' '.join(chunk_sentences)

            # Enforce size constraints
            word_count = len(chunk_text.split())
            if word_count < self.min_chunk_size and i < len(split_indices) - 2:
                # Merge with next chunk if too small
                continue

            chunk = Chunk(
                text=chunk_text,
                metadata={
                    'source': source,
                    'chunk_index': len(chunks),
                    'start_sentence': start,
                    'end_sentence': end,
                    'sentence_count': end - start,
                    'chunking_strategy': 'semantic'
                }
            )

            chunks.append(chunk)

        return chunks

    def _fallback_sentence_chunking(self, text: str, source: str) -> List[Chunk]:
        """
        Fallback to simple sentence-based chunking.

        Args:
            text: Text to chunk
            source: Source identifier

        Returns:
            List of chunks
        """
        sentences = self._split_sentences(text)
        chunks = []

        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence.split())

            if current_size + sentence_size > self.max_chunk_size and current_chunk:
                # Create chunk
                chunk_text = ' '.join(current_chunk)
                chunk = Chunk(
                    text=chunk_text,
                    metadata={
                        'source': source,
                        'chunk_index': len(chunks),
                        'chunking_strategy': 'semantic_fallback'
                    }
                )
                chunks.append(chunk)

                current_chunk = []
                current_size = 0

            current_chunk.append(sentence)
            current_size += sentence_size

        # Add last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk = Chunk(
                text=chunk_text,
                metadata={
                    'source': source,
                    'chunk_index': len(chunks),
                    'chunking_strategy': 'semantic_fallback'
                }
            )
            chunks.append(chunk)

        return chunks
