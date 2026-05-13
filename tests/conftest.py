"""Pytest configuration and fixtures."""
import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def sample_documents():
    """Return sample documents for testing."""
    return [
        {
            "text": "Machine learning is a subset of artificial intelligence.",
            "source": "doc1.txt"
        },
        {
            "text": "Deep learning uses neural networks with multiple layers.",
            "source": "doc2.txt"
        }
    ]


@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API keys for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-456")


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "requires_api: Tests requiring API keys")
