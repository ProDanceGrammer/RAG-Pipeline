"""Utility for handling markdown tables in chunks."""
import re
from typing import List, Tuple


class TableHandler:
    """Handle markdown tables during chunking."""

    @staticmethod
    def detect_tables(text: str) -> List[Tuple[int, int]]:
        """
        Detect markdown table positions in text.

        Args:
            text: Text to search

        Returns:
            List of (start, end) positions for each table
        """
        tables = []
        lines = text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if line looks like a table row
            if '|' in line and line.strip().startswith('|'):
                # Check next line for separator
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if re.match(r'^\s*\|[\s\-:|]+\|\s*$', next_line):
                        # Found table start
                        start = i

                        # Find table end
                        j = i + 2
                        while j < len(lines) and '|' in lines[j]:
                            j += 1

                        end = j
                        tables.append((start, end))
                        i = j
                        continue

            i += 1

        return tables

    @staticmethod
    def extract_table(text: str, start: int, end: int) -> str:
        """
        Extract table from text by line numbers.

        Args:
            text: Full text
            start: Start line number
            end: End line number

        Returns:
            Table text
        """
        lines = text.split('\n')
        return '\n'.join(lines[start:end])

    @staticmethod
    def is_table_in_range(table_pos: Tuple[int, int], chunk_start: int, chunk_end: int) -> bool:
        """
        Check if table overlaps with chunk range.

        Args:
            table_pos: (start, end) of table
            chunk_start: Start line of chunk
            chunk_end: End line of chunk

        Returns:
            True if table overlaps with chunk
        """
        table_start, table_end = table_pos

        # Table completely within chunk
        if chunk_start <= table_start and table_end <= chunk_end:
            return True

        # Table partially overlaps
        if (chunk_start <= table_start < chunk_end) or (chunk_start < table_end <= chunk_end):
            return True

        return False

    @staticmethod
    def should_keep_table_with_chunk(table_size: int, chunk_size: int, max_chunk_size: int) -> bool:
        """
        Decide if table should be kept with chunk or separated.

        Args:
            table_size: Size of table in tokens
            chunk_size: Size of chunk in tokens
            max_chunk_size: Maximum allowed chunk size

        Returns:
            True if table should stay with chunk
        """
        # If combined size is reasonable, keep together
        if chunk_size + table_size <= max_chunk_size * 1.2:
            return True

        # If table is small relative to chunk, keep together
        if table_size < chunk_size * 0.3:
            return True

        return False

    @staticmethod
    def create_table_chunk_with_context(table_text: str, context_header: str, source: str) -> dict:
        """
        Create a dedicated chunk for a large table with context.

        Args:
            table_text: The table markdown
            context_header: Section header for context
            source: Source document

        Returns:
            Dictionary with chunk data
        """
        chunk_text = f"{context_header}\n\n{table_text}"

        return {
            'text': chunk_text,
            'metadata': {
                'source': source,
                'type': 'table',
                'context': context_header
            }
        }
