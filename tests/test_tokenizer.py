"""Tests for tokenizer."""
import pytest
from src.processing.tokenizer import Tokenizer


@pytest.mark.unit
def test_simple_tokenize():
    """Test simple whitespace tokenization."""
    text = "This is a test"

    tokens = Tokenizer.simple_tokenize(text)

    assert tokens == ["This", "is", "a", "test"]


@pytest.mark.unit
def test_word_tokenize():
    """Test word tokenization."""
    text = "Hello, world! How are you?"

    tokens = Tokenizer.word_tokenize(text)

    assert "hello" in tokens
    assert "world" in tokens
    assert "," not in tokens


@pytest.mark.unit
def test_count_tokens():
    """Test token counting."""
    text = "This is a simple test sentence"

    count = Tokenizer.count_tokens(text)

    assert count == 6


@pytest.mark.unit
def test_truncate_to_tokens():
    """Test text truncation."""
    text = "word1 word2 word3 word4 word5"

    result = Tokenizer.truncate_to_tokens(text, max_tokens=3)

    assert result == "word1 word2 word3"


@pytest.mark.unit
def test_truncate_short_text():
    """Test truncation of text shorter than limit."""
    text = "short text"

    result = Tokenizer.truncate_to_tokens(text, max_tokens=10)

    assert result == text
