"""RAG Pipeline with answer generation."""
import logging
from typing import List, Dict, Tuple
import time

from ..core.ollama_client import OllamaClient
from ..core.ollama_embedder import OllamaEmbedder
from ..rag.multi_store_manager import MultiStoreManager

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG pipeline with retrieval and generation."""

    def __init__(
        self,
        embedder: OllamaEmbedder,
        generator: OllamaClient,
        manager: MultiStoreManager,
        strategy_name: str = "structure",
        top_k: int = 3,
        max_context_length: int = 2000
    ):
        """
        Initialize RAG pipeline.

        Args:
            embedder: Embedder for queries
            generator: LLM for answer generation
            manager: Vector store manager
            strategy_name: Chunking strategy to use
            top_k: Number of chunks to retrieve
            max_context_length: Maximum context length in characters
        """
        self.embedder = embedder
        self.generator = generator
        self.manager = manager
        self.strategy_name = strategy_name
        self.top_k = top_k
        self.max_context_length = max_context_length
        self.logger = logging.getLogger(__name__)

    def retrieve(self, query: str) -> List[Tuple[Dict, float]]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: User query

        Returns:
            List of (metadata, score) tuples
        """
        self.logger.info(f"Retrieving for query: {query}")

        # Embed query
        start_time = time.time()
        query_emb = self.embedder.embed_single(query)
        embed_time = time.time() - start_time
        self.logger.debug(f"Query embedding took {embed_time:.2f}s")

        # Search
        start_time = time.time()
        results = self.manager.search(self.strategy_name, query_emb, top_k=self.top_k)
        search_time = time.time() - start_time
        self.logger.debug(f"Search took {search_time:.2f}s")

        self.logger.info(f"Retrieved {len(results)} chunks")
        return results

    def format_context(self, results: List[Tuple[Dict, float]]) -> str:
        """
        Format retrieved chunks into context string.

        Args:
            results: List of (metadata, score) tuples

        Returns:
            Formatted context string
        """
        context_parts = []
        total_length = 0

        for i, (metadata, score) in enumerate(results, 1):
            section = metadata.get('section', 'Unknown')
            text = metadata.get('text', '')

            # Truncate if needed
            if total_length + len(text) > self.max_context_length:
                remaining = self.max_context_length - total_length
                text = text[:remaining] + "..."
                context_parts.append(f"[{i}] Section: {section}\n{text}")
                break

            context_parts.append(f"[{i}] Section: {section}\n{text}")
            total_length += len(text)

        context = "\n\n".join(context_parts)
        self.logger.debug(f"Context length: {len(context)} characters")
        return context

    def generate_prompt(self, query: str, context: str) -> str:
        """
        Generate prompt for LLM.

        Args:
            query: User query
            context: Retrieved context

        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful assistant answering questions about Python, OOP, Machine Learning, and Database Optimization.

Use the following context from educational notes to answer the question. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {query}

Answer: Provide a clear, concise answer based on the context above. Include specific details and examples when available."""

        return prompt

    def generate_answer(self, query: str, context: str) -> str:
        """
        Generate answer using LLM.

        Args:
            query: User query
            context: Retrieved context

        Returns:
            Generated answer
        """
        self.logger.info("Generating answer...")

        # Create prompt
        prompt = self.generate_prompt(query, context)

        # Generate
        start_time = time.time()
        try:
            answer = self.generator.generate(
                prompt,
                max_tokens=500,
                temperature=0.7
            )
            gen_time = time.time() - start_time
            self.logger.info(f"Generation took {gen_time:.2f}s")
            return answer.strip()

        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return f"Error generating answer: {e}"

    def query(self, query: str) -> Dict:
        """
        Complete RAG query: retrieve + generate.

        Args:
            query: User query

        Returns:
            Dictionary with answer, sources, and metadata
        """
        self.logger.info(f"Processing query: {query}")
        start_time = time.time()

        # Retrieve
        results = self.retrieve(query)

        if not results:
            return {
                'query': query,
                'answer': "I couldn't find relevant information to answer your question.",
                'sources': [],
                'latency': time.time() - start_time
            }

        # Format context
        context = self.format_context(results)

        # Generate answer
        answer = self.generate_answer(query, context)

        # Extract sources
        sources = []
        for metadata, score in results:
            sources.append({
                'section': metadata.get('section', 'Unknown'),
                'score': float(score),
                'text_preview': metadata.get('text', '')[:100]
            })

        total_time = time.time() - start_time

        result = {
            'query': query,
            'answer': answer,
            'sources': sources,
            'latency': total_time
        }

        self.logger.info(f"Query completed in {total_time:.2f}s")
        return result

    def query_stream(self, query: str):
        """
        Complete RAG query with streaming generation.

        Args:
            query: User query

        Yields:
            Answer chunks as they are generated
        """
        self.logger.info(f"Processing query (streaming): {query}")

        # Retrieve
        results = self.retrieve(query)

        if not results:
            yield "I couldn't find relevant information to answer your question."
            return

        # Format context
        context = self.format_context(results)

        # Create prompt
        prompt = self.generate_prompt(query, context)

        # Stream generation
        try:
            for chunk in self.generator.generate_stream(prompt, max_tokens=500, temperature=0.7):
                yield chunk
        except Exception as e:
            self.logger.error(f"Streaming generation failed: {e}")
            yield f"\n\nError: {e}"
