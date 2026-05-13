from typing import List, Dict, Any, Callable
from ..core.base_llm import BaseLLM


class PromptChain:
    """Multi-step prompt chaining for complex tasks."""

    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.steps: List[Dict[str, Any]] = []
        self.results: List[str] = []

    def add_step(
        self,
        name: str,
        prompt_template: str,
        transform: Callable[[str], str] = None
    ):
        """Add a step to the chain."""
        self.steps.append({
            "name": name,
            "prompt_template": prompt_template,
            "transform": transform
        })
        return self

    def execute(self, initial_input: str, **kwargs) -> str:
        """Execute the prompt chain."""
        current_input = initial_input
        self.results = []

        for step in self.steps:
            prompt = step["prompt_template"].format(
                input=current_input,
                **kwargs
            )

            result = self.llm.generate(prompt)
            self.results.append(result)

            if step["transform"]:
                current_input = step["transform"](result)
            else:
                current_input = result

        return current_input

    def get_intermediate_results(self) -> List[str]:
        """Get all intermediate results from the chain."""
        return self.results
