"""Ollama LLM client implementation."""
import requests
import time
from typing import List, Optional, Generator
from .base_llm import BaseLLM
import logging

logger = logging.getLogger(__name__)


class OllamaClient(BaseLLM):
    """Ollama local LLM client implementation."""

    def __init__(
        self,
        model_name: str = "llama3.1:7b",
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
        max_retries: int = 3,
        **kwargs
    ):
        """
        Initialize Ollama client.

        Args:
            model_name: Name of the Ollama model
            base_url: Ollama API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            **kwargs: Additional configuration
        """
        super().__init__(model_name, **kwargs)
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {}
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        if temperature is not None:
            payload["options"]["temperature"] = temperature

        # Add any additional options
        payload["options"].update(kwargs)

        # Retry logic
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f"Generating with {self.model_name}, attempt {attempt + 1}")
                response = requests.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()

                data = response.json()
                return data.get("response", "")

            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def generate_stream(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Generate text with streaming response.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Yields:
            Text chunks as they are generated
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {}
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        if temperature is not None:
            payload["options"]["temperature"] = temperature

        payload["options"].update(kwargs)

        try:
            response = requests.post(url, json=payload, stream=True, timeout=self.timeout)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Streaming error: {e}")
            raise

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts.

        Note: This uses a separate embedding model.
        Set embedding_model in config or use OllamaEmbedder.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        raise NotImplementedError(
            "Use OllamaEmbedder for embeddings. "
            "OllamaClient is for text generation only."
        )

    def is_available(self) -> bool:
        """
        Check if Ollama is running and model is available.

        Returns:
            True if available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                return self.model_name in model_names
            return False
        except requests.exceptions.RequestException:
            return False

    def list_models(self) -> List[str]:
        """
        List available Ollama models.

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m.get("name", "") for m in models]
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error listing models: {e}")
            return []
