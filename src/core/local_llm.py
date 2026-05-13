from typing import List, Optional
from .base_llm import BaseLLM


class LocalLLM(BaseLLM):
    """Local/self-hosted LLM client (e.g., llama.cpp, vLLM, Ollama)."""

    def __init__(self, model_name: str, model_path: str = None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the local model. Implement based on your framework."""
        raise NotImplementedError("Implement model loading for your local LLM framework")

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        raise NotImplementedError("Implement generation for your local LLM framework")

    def generate_stream(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ):
        raise NotImplementedError("Implement streaming for your local LLM framework")

    def embed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError("Implement embeddings for your local LLM framework")
