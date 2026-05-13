from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class BaseLLM(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """Generate text from a prompt."""
        pass

    @abstractmethod
    def generate_stream(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ):
        """Generate text with streaming response."""
        pass

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        pass

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return len(text.split()) * 1.3
