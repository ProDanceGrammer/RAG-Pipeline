from typing import Dict, Any


class PromptTemplate:
    """Reusable prompt templates for various tasks."""

    RAG_QUERY = """You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""

    SUMMARIZATION = """Summarize the following text concisely:

{text}

Summary:"""

    EXTRACTION = """Extract {entity_type} from the following text:

{text}

Extracted {entity_type}:"""

    CLASSIFICATION = """Classify the following text into one of these categories: {categories}

Text: {text}

Category:"""

    @staticmethod
    def format(template: str, **kwargs) -> str:
        """Format a template with provided variables."""
        return template.format(**kwargs)

    @staticmethod
    def rag_query(context: str, question: str) -> str:
        return PromptTemplate.format(
            PromptTemplate.RAG_QUERY,
            context=context,
            question=question
        )

    @staticmethod
    def summarize(text: str) -> str:
        return PromptTemplate.format(
            PromptTemplate.SUMMARIZATION,
            text=text
        )

    @staticmethod
    def extract(text: str, entity_type: str) -> str:
        return PromptTemplate.format(
            PromptTemplate.EXTRACTION,
            text=text,
            entity_type=entity_type
        )

    @staticmethod
    def classify(text: str, categories: list) -> str:
        return PromptTemplate.format(
            PromptTemplate.CLASSIFICATION,
            text=text,
            categories=", ".join(categories)
        )
