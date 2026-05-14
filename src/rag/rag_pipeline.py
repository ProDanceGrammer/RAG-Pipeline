"""RAG Pipeline with answer generation."""
import logging
from typing import List, Dict, Tuple, Optional
import time

from ..core.ollama_client import OllamaClient
from ..core.ollama_embedder import OllamaEmbedder
from ..rag.multi_store_manager import MultiStoreManager
from ..rag.hybrid_retriever import HybridRetriever

logger = logging.getLogger(__name__)

# Generic sections to filter out from retrieval results
GENERIC_SECTIONS = {'Terms', 'Introduction', 'Overview', 'Summary'}


class RAGPipeline:
    """Complete RAG pipeline with retrieval and generation."""

    def __init__(
        self,
        embedder: OllamaEmbedder,
        generator: OllamaClient,
        manager: MultiStoreManager,
        strategy_name: str = "structure",
        top_k: int = 3,
        max_context_length: int = 2000,
        use_reranking: bool = True,
        use_topic_filtering: bool = False,
        use_hybrid_search: bool = True,
        hybrid_alpha: float = 0.7
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
            use_reranking: Enable cross-encoder re-ranking
            use_topic_filtering: Enable topic-based filtering
            use_hybrid_search: Enable hybrid search (BM25 + semantic)
            hybrid_alpha: Weight for semantic search (0.0=pure BM25, 1.0=pure semantic)
        """
        self.embedder = embedder
        self.generator = generator
        self.manager = manager
        self.strategy_name = strategy_name
        self.top_k = top_k
        self.max_context_length = max_context_length
        self.use_reranking = use_reranking
        self.use_topic_filtering = use_topic_filtering
        self.use_hybrid_search = use_hybrid_search
        self.hybrid_alpha = hybrid_alpha
        self.logger = logging.getLogger(__name__)

        # Lazy load reranker and topic detector
        self.reranker = None
        self.topic_detector = None
        self.hybrid_retriever = None

        if use_reranking:
            from ..rag.reranker import CrossEncoderReranker
            self.reranker = CrossEncoderReranker()
            self.logger.info("Cross-encoder re-ranking enabled")

        if use_topic_filtering:
            from ..rag import topic_detector
            self.topic_detector = topic_detector
            self.logger.info("Topic filtering enabled")

        if use_hybrid_search:
            self.hybrid_retriever = HybridRetriever()
            self.logger.info(f"Hybrid search enabled (alpha={hybrid_alpha})")

    def retrieve(self, query: str) -> List[Tuple[Dict, float]]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: User query

        Returns:
            List of (metadata, score) tuples
        """
        self.logger.info(f"Retrieving for query: {query}")

        # Detect topic if filtering enabled
        topic = None
        if self.use_topic_filtering and self.topic_detector:
            topic = self.topic_detector.detect_topic(query)
            if topic:
                self.logger.debug(f"Detected topic: {topic}")

        # Embed query
        start_time = time.time()
        query_emb = self.embedder.embed_single(query)
        embed_time = time.time() - start_time
        self.logger.debug(f"Query embedding took {embed_time:.2f}s")

        # Search (get more results if re-ranking or using hybrid search)
        search_k = self.top_k * 4 if (self.use_reranking or self.use_hybrid_search) else self.top_k

        # Perform search based on configuration
        if self.use_hybrid_search and self.hybrid_retriever:
            # Hybrid search: combine BM25 and semantic
            start_time = time.time()

            # Get BM25 results
            bm25_start = time.time()
            bm25_results = self.manager.search_bm25(self.strategy_name, query, top_k=search_k)
            bm25_time = time.time() - bm25_start
            self.logger.debug(f"BM25 search took {bm25_time:.2f}s")

            # Get semantic results
            semantic_start = time.time()
            semantic_results = self.manager.search(self.strategy_name, query_emb, top_k=search_k)
            semantic_time = time.time() - semantic_start
            self.logger.debug(f"Semantic search took {semantic_time:.2f}s")

            # Fuse results
            fusion_start = time.time()
            results = self.hybrid_retriever.fuse(bm25_results, semantic_results, alpha=self.hybrid_alpha)
            fusion_time = time.time() - fusion_start
            self.logger.debug(f"Fusion took {fusion_time:.2f}s")

            search_time = time.time() - start_time
            self.logger.debug(f"Hybrid search took {search_time:.2f}s total")
        else:
            # Semantic-only search (original behavior)
            start_time = time.time()
            results = self.manager.search(self.strategy_name, query_emb, top_k=search_k)
            search_time = time.time() - start_time
            self.logger.debug(f"Semantic search took {search_time:.2f}s")

        # Filter by topic if detected
        if topic and self.use_topic_filtering:
            filtered_by_topic = [
                (metadata, score)
                for metadata, score in results
                if metadata.get('topic') == topic
            ]
            if filtered_by_topic:  # Only use filtered if we got results
                self.logger.debug(f"Filtered to {len(filtered_by_topic)} results by topic '{topic}'")
                results = filtered_by_topic
            else:
                self.logger.debug(f"No results for topic '{topic}', using all results")

        # Filter out generic sections
        filtered_results = [
            (metadata, score)
            for metadata, score in results
            if metadata.get('section', '') not in GENERIC_SECTIONS
        ]

        if len(filtered_results) < len(results):
            self.logger.debug(f"Filtered out {len(results) - len(filtered_results)} generic sections")

        # Re-rank if enabled
        if self.use_reranking and self.reranker and filtered_results:
            start_time = time.time()
            filtered_results = self.reranker.rerank(query, filtered_results, top_k=self.top_k)
            rerank_time = time.time() - start_time
            self.logger.debug(f"Re-ranking took {rerank_time:.2f}s")
        else:
            # Just take top_k if not re-ranking
            filtered_results = filtered_results[:self.top_k]

        self.logger.info(f"Retrieved {len(filtered_results)} chunks (after filtering)")
        return filtered_results

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
