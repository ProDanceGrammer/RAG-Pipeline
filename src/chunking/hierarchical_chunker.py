"""Hierarchical chunking strategy."""
import re
from typing import List, Dict, Any
from .base_chunker import BaseChunker, Chunk
import logging

logger = logging.getLogger(__name__)


class HierarchicalChunker(BaseChunker):
    """
    Create hierarchical chunks with parent-child relationships.

    Parent chunks: Full ## sections
    Child chunks: Individual emoji subsections (🔽 What?, 🤔 How?, etc.)
    """

    # Standard emoji subsections in Notion documents
    EMOJI_MARKERS = [
        "🔽 What?",
        "🔁 What does it do?",
        "🤷‍♂️ Why do we use it?",
        "🤔 How does it work?",
        "✍️ How to use it?",
        "👍 Advantages",
        "👎 Disadvantages",
        "↔️ Alternatives",
        "✅ Best practices",
        "🛠️ Use cases",
        "🛑 Worst practices"
    ]

    def __init__(self, create_parent_chunks: bool = True, create_child_chunks: bool = True, **kwargs):
        """
        Initialize hierarchical chunker.

        Args:
            create_parent_chunks: Create full section chunks
            create_child_chunks: Create emoji subsection chunks
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.create_parent_chunks = create_parent_chunks
        self.create_child_chunks = create_child_chunks

    def chunk(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Create hierarchical chunks.

        Args:
            text: Markdown text to chunk
            source: Source identifier

        Returns:
            List of parent and child chunks
        """
        chunks = []

        # Split by ## headers
        sections = self._split_by_headers(text)

        for section_idx, section in enumerate(sections):
            if not section['text'].strip():
                continue

            header = section['header']
            section_text = section['text']
            level = section['level']

            # Create parent chunk (full section)
            if self.create_parent_chunks:
                parent_chunk = Chunk(
                    text=section_text,
                    metadata={
                        'source': source,
                        'section': header,
                        'section_index': section_idx,
                        'level': level,
                        'chunk_type': 'parent',
                        'chunking_strategy': 'hierarchical'
                    }
                )
                chunks.append(parent_chunk)

            # Create child chunks (emoji subsections)
            if self.create_child_chunks:
                child_chunks = self._extract_emoji_subsections(
                    section_text, header, source, section_idx
                )
                chunks.extend(child_chunks)

        self.logger.info(
            f"Created {len(chunks)} hierarchical chunks from {source} "
            f"({sum(1 for c in chunks if c.metadata.get('chunk_type') == 'parent')} parents, "
            f"{sum(1 for c in chunks if c.metadata.get('chunk_type') == 'child')} children)"
        )

        return chunks

    def _split_by_headers(self, text: str) -> List[Dict[str, Any]]:
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
                current_lines = [line]
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

    def _extract_emoji_subsections(
        self, section_text: str, parent_header: str, source: str, section_idx: int
    ) -> List[Chunk]:
        """
        Extract emoji subsections as child chunks.

        Args:
            section_text: Full section text
            parent_header: Parent section header
            source: Source identifier
            section_idx: Parent section index

        Returns:
            List of child chunks
        """
        child_chunks = []
        lines = section_text.split('\n')

        current_subsection = None
        current_lines = []

        for line in lines:
            # Check if line starts with an emoji marker
            found_marker = None
            for marker in self.EMOJI_MARKERS:
                if marker in line:
                    found_marker = marker
                    break

            if found_marker:
                # Save previous subsection
                if current_subsection is not None:
                    subsection_text = '\n'.join(current_lines).strip()
                    if subsection_text:
                        child_chunk = Chunk(
                            text=subsection_text,
                            metadata={
                                'source': source,
                                'section': parent_header,
                                'subsection': current_subsection,
                                'section_index': section_idx,
                                'chunk_type': 'child',
                                'parent_section': parent_header,
                                'chunking_strategy': 'hierarchical'
                            }
                        )
                        child_chunks.append(child_chunk)

                # Start new subsection
                current_subsection = found_marker
                current_lines = [line]
            else:
                if current_subsection is not None:
                    current_lines.append(line)

        # Add last subsection
        if current_subsection is not None:
            subsection_text = '\n'.join(current_lines).strip()
            if subsection_text:
                child_chunk = Chunk(
                    text=subsection_text,
                    metadata={
                        'source': source,
                        'section': parent_header,
                        'subsection': current_subsection,
                        'section_index': section_idx,
                        'chunk_type': 'child',
                        'parent_section': parent_header,
                        'chunking_strategy': 'hierarchical'
                    }
                )
                child_chunks.append(child_chunk)

        return child_chunks
