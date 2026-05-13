import re
from typing import Dict, Any


class TextPreprocessor:
    """Text cleaning and normalization utilities."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Basic text cleaning."""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    @staticmethod
    def remove_special_chars(text: str, keep_punctuation: bool = True) -> str:
        """Remove special characters."""
        if keep_punctuation:
            pattern = r'[^\w\s.,!?;:\-\']'
        else:
            pattern = r'[^\w\s]'
        return re.sub(pattern, '', text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace to single spaces."""
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses from text."""
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    @staticmethod
    def preprocess(text: str, **options) -> str:
        """Apply multiple preprocessing steps."""
        if options.get('remove_urls', False):
            text = TextPreprocessor.remove_urls(text)

        if options.get('remove_emails', False):
            text = TextPreprocessor.remove_emails(text)

        if options.get('remove_special_chars', False):
            text = TextPreprocessor.remove_special_chars(
                text,
                keep_punctuation=options.get('keep_punctuation', True)
            )

        text = TextPreprocessor.normalize_whitespace(text)

        return text
