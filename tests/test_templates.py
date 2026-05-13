"""Tests for prompt templates."""
import pytest
from src.prompts.templates import PromptTemplate


@pytest.mark.unit
def test_rag_query_template():
    """Test RAG query template formatting."""
    context = "Machine learning is a subset of AI."
    question = "What is machine learning?"

    result = PromptTemplate.rag_query(context, question)

    assert "Machine learning is a subset of AI." in result
    assert "What is machine learning?" in result
    assert "Context:" in result
    assert "Question:" in result


@pytest.mark.unit
def test_summarization_template():
    """Test summarization template."""
    text = "Long text to summarize..."

    result = PromptTemplate.summarize(text)

    assert text in result
    assert "Summarize" in result


@pytest.mark.unit
def test_extraction_template():
    """Test extraction template."""
    text = "John works at Google in California."
    entity_type = "companies"

    result = PromptTemplate.extract(text, entity_type)

    assert text in result
    assert entity_type in result


@pytest.mark.unit
def test_classification_template():
    """Test classification template."""
    text = "This product is amazing!"
    categories = ["positive", "negative", "neutral"]

    result = PromptTemplate.classify(text, categories)

    assert text in result
    assert "positive" in result
    assert "negative" in result


@pytest.mark.unit
def test_format_generic():
    """Test generic template formatting."""
    template = "Hello {name}, you are {age} years old."

    result = PromptTemplate.format(template, name="Alice", age=30)

    assert result == "Hello Alice, you are 30 years old."
