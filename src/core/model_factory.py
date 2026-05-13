import yaml
from pathlib import Path
from typing import Dict, Any
from .base_llm import BaseLLM
from .gpt_client import GPTClient
from .claude_client import ClaudeClient
from .local_llm import LocalLLM


class ModelFactory:
    """Factory for creating LLM clients based on configuration."""

    _providers = {
        "openai": GPTClient,
        "anthropic": ClaudeClient,
        "local": LocalLLM,
    }

    def __init__(self, config_path: str = "config/model_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_model(self, provider: str, model_key: str) -> BaseLLM:
        if provider not in self._providers:
            raise ValueError(f"Unknown provider: {provider}")

        provider_config = self.config["providers"][provider]
        model_config = provider_config["models"][model_key]

        client_class = self._providers[provider]
        return client_class(
            model_name=model_config["name"],
            **{k: v for k, v in model_config.items() if k != "name"}
        )

    def create_default_model(self) -> BaseLLM:
        return self.create_model("openai", "gpt4")
