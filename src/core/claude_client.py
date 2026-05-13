import os
from typing import List, Optional
from anthropic import Anthropic
from .base_llm import BaseLLM


class ClaudeClient(BaseLLM):
    """Anthropic Claude client implementation."""

    def __init__(self, model_name: str = "claude-sonnet-4-6", **kwargs):
        super().__init__(model_name, **kwargs)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens or self.config.get("max_tokens", 4096),
            temperature=temperature or self.config.get("temperature", 0.7),
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return message.content[0].text

    def generate_stream(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ):
        with self.client.messages.stream(
            model=self.model_name,
            max_tokens=max_tokens or self.config.get("max_tokens", 4096),
            temperature=temperature or self.config.get("temperature", 0.7),
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        ) as stream:
            for text in stream.text_stream:
                yield text

    def embed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError("Claude does not provide embedding API. Use OpenAI or local embeddings.")
