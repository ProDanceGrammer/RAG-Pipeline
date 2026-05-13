"""Structure-based chunking strategy."""
import re
from typing import List
from .base_chunker import BaseChunker, Chunk
from .table_handler import TableHandler
import logging

logger = logging.getLogger(__name__)


class StructureChunker(BaseChunker):
    """
    Chunk documents by markdown structure (## headers).

    This is the primary recommended strategy for well-structured
    educational content like Notion documents.
    """

    def __init__(self, preserve_tables: bool = True, **kwargs):
        """
        Initialize structure-based chunker.

        Args:
            preserve_tables: Keep tables within their sections
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.preserve_tables = preserve_tables
        self.table_handler = TableHandler()

    def chunk(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Chunk text by ## markdown headers.

        Args:
            text: Markdown text to chunk
            source: Source identifier

        Returns:
            List of chunks, one per ## section
        """
        chunks = []

        # Split by ## headers (but not # or ###)
        sections = self._split_by_headers(text)

        for i, section in enumerate(sections):
            if not section['text'].strip():
                continue

            # Extract section header
            header = section['header']
            section_text = section['text']
            level = section['level']

            # Create chunk
            chunk = Chunk(
                text=section_text,
                metadata={
                    'source': source,
                    'section': header,
                    'section_index': i,
                    'level': level,
                    'chunking_strategy': 'structure'
                }
            )

            chunks.append(chunk)

        self.logger.info(f"Created {len(chunks)} structure-based chunks from {source}")
        return chunks

    def _split_by_headers(self, text: str) -> List[dict]:
        """
        Split text by ## headers.

        Args:
            text: Markdown text

        Returns:
            List of dicts with 'header', 'text', 'level'
        """
        sections = []
        lines = text.split('\n')

        current_section = None
        current_lines = []

        for line in lines:
            # Check for ## header (not # or ###)
            header_match = re.match(r'^(#{1,3})\s+(.+)$', line)

            if header_match:
                level = len(header_match.group(1))
                header_text = header_match.group(2).strip()

                # Save previous section
                if current_section is not None:
                    sections.append({
                        'header': current_section['header'],
                        'level': current_section['level'],
                        'text': '\n'.join(current_lines)
                    })

                # Start new section
                current_section = {
                    'header': header_text,
                    'level': level
                }
                current_lines = [line]  # Include header in text
            else:
                if current_section is not None:
                    current_lines.append(line)

        # Add last section
        if current_section is not None:
            sections.append({
                'header': current_section['header'],
                'level': current_section['level'],
                'text': '\n'.join(current_lines)
            })

        return sections

    def _extract_header(self, text: str) -> str:
        """
        Extract the first header from text.

        Args:
            text: Text to search

        Returns:
            Header text or "Unknown Section"
        """
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith('##'):
                return line.strip().lstrip('#').strip()

        return "Unknown Section"
