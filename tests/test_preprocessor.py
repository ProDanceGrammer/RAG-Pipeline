"""Tests for text preprocessing."""
import pytest
from src.processing.preprocessor import TextPreprocessor


@pytest.mark.unit
def test_clean_text():
    """Test basic text cleaning."""
    text = "  Multiple   spaces   here  "

    result = TextPreprocessor.clean_text(text)

    assert result == "Multiple spaces here"


@pytest.mark.unit
def test_remove_urls():
    """Test URL removal."""
    text = "Check out https://example.com for more info"

    result = TextPreprocessor.remove_urls(text)

    assert "https://example.com" not in result
    assert "Check out" in result


@pytest.mark.unit
def test_remove_emails():
    """Test email removal."""
    text = "Contact us at test@example.com for help"

    result = TextPreprocessor.remove_emails(text)

    assert "test@example.com" not in result
    assert "Contact us at" in result


@pytest.mark.unit
def test_normalize_whitespace():
    """Test whitespace normalization."""
    text = "Text\n\n\nwith\t\tmultiple\r\nwhitespace"

    result = TextPreprocessor.normalize_whitespace(text)

    assert result == "Text with multiple whitespace"


@pytest.mark.unit
def test_preprocess_combined():
    """Test combined preprocessing."""
    text = "Visit  https://example.com  or email test@example.com  "

    result = TextPreprocessor.preprocess(
        text,
        remove_urls=True,
        remove_emails=True
    )

    assert "https://example.com" not in result
    assert "test@example.com" not in result
    assert result == "Visit or email"
