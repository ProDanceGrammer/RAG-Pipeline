from typing import List
import re


class TextChunker:
    """Text splitting and chunking utilities."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)

            if i + self.chunk_size >= len(words):
                break

        return chunks if chunks else [text]

    def chunk_by_sentences(self, text: str, max_sentences: int = 5) -> List[str]:
        """Split text by sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []

        for i in range(0, len(sentences), max_sentences):
            chunk = " ".join(sentences[i:i + max_sentences])
            chunks.append(chunk)

        return chunks if chunks else [text]

    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """Split text by paragraphs."""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
