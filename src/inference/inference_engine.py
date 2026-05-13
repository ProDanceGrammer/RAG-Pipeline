from typing import Optional, Dict, Any
from ..core.base_llm import BaseLLM
from ..rag.retriever import Retriever
from ..prompts.templates import PromptTemplate


class InferenceEngine:
    """Orchestrates RAG inference pipeline."""

    def __init__(
        self,
        llm: BaseLLM,
        retriever: Optional[Retriever] = None
    ):
        self.llm = llm
        self.retriever = retriever

    def query(
        self,
        question: str,
        use_rag: bool = True,
        stream: bool = False,
        **kwargs
    ) -> str:
        """Execute a query with optional RAG."""
        if use_rag and self.retriever:
            context = self.retriever.retrieve_with_context(question)
            prompt = PromptTemplate.rag_query(context, question)
        else:
            prompt = question

        if stream:
            return self.llm.generate_stream(prompt, **kwargs)
        else:
            return self.llm.generate(prompt, **kwargs)

    def query_with_metadata(
        self,
        question: str,
        use_rag: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute query and return response with metadata."""
        retrieved_docs = []

        if use_rag and self.retriever:
            retrieved_docs = self.retriever.retrieve(question)
            context = self.retriever.retrieve_with_context(question)
            prompt = PromptTemplate.rag_query(context, question)
        else:
            prompt = question

        response = self.llm.generate(prompt, **kwargs)

        return {
            "answer": response,
            "question": question,
            "retrieved_documents": retrieved_docs,
            "used_rag": use_rag
        }

    def summarize(self, text: str, **kwargs) -> str:
        """Summarize text."""
        prompt = PromptTemplate.summarize(text)
        return self.llm.generate(prompt, **kwargs)

    def extract(self, text: str, entity_type: str, **kwargs) -> str:
        """Extract entities from text."""
        prompt = PromptTemplate.extract(text, entity_type)
        return self.llm.generate(prompt, **kwargs)

    def classify(self, text: str, categories: list, **kwargs) -> str:
        """Classify text into categories."""
        prompt = PromptTemplate.classify(text, categories)
        return self.llm.generate(prompt, **kwargs)
