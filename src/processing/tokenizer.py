from typing import List
import re


class Tokenizer:
    """Tokenization utilities."""

    @staticmethod
    def simple_tokenize(text: str) -> List[str]:
        """Simple whitespace tokenization."""
        return text.split()

    @staticmethod
    def word_tokenize(text: str) -> List[str]:
        """Word tokenization with punctuation handling."""
        return re.findall(r'\b\w+\b', text.lower())

    @staticmethod
    def count_tokens(text: str) -> int:
        """Estimate token count (rough approximation)."""
        return len(Tokenizer.word_tokenize(text))

    @staticmethod
    def truncate_to_tokens(text: str, max_tokens: int) -> str:
        """Truncate text to maximum token count."""
        tokens = Tokenizer.simple_tokenize(text)
        if len(tokens) <= max_tokens:
            return text
        return " ".join(tokens[:max_tokens])
