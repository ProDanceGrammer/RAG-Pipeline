"""BM25 retriever for keyword-based search."""
import logging
import pickle
from pathlib import Path
from typing import List, Tuple, Optional
import re

logger = logging.getLogger(__name__)


class BM25Retriever:
    """BM25-based keyword search retriever."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 retriever.

        Args:
            k1: Term frequency saturation parameter (default: 1.5)
            b: Length normalization parameter (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.tokenized_corpus = []
        self.doc_lengths = []
        self.avgdl = 0.0
        self.doc_freqs = {}
        self.idf = {}
        self.num_docs = 0
        self.logger = logging.getLogger(__name__)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into terms.

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        # Simple tokenization: lowercase, split on whitespace and punctuation
        text = text.lower()
        # Keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def index(self, documents: List[str]) -> None:
        """
        Build BM25 index from documents.

        Args:
            documents: List of document texts
        """
        self.logger.info(f"Building BM25 index for {len(documents)} documents...")

        self.corpus = documents
        self.tokenized_corpus = [self.tokenize(doc) for doc in documents]
        self.doc_lengths = [len(doc) for doc in self.tokenized_corpus]
        self.num_docs = len(documents)
        self.avgdl = sum(self.doc_lengths) / self.num_docs if self.num_docs > 0 else 0

        # Calculate document frequencies
        self.doc_freqs = {}
        for tokenized_doc in self.tokenized_corpus:
            unique_tokens = set(tokenized_doc)
            for token in unique_tokens:
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1

        # Calculate IDF scores
        self.idf = {}
        for token, freq in self.doc_freqs.items():
            self.idf[token] = self._calc_idf(freq)

        self.logger.info(
            f"BM25 index built: {self.num_docs} docs, "
            f"{len(self.idf)} unique terms, "
            f"avg doc length: {self.avgdl:.1f}"
        )

    def _calc_idf(self, doc_freq: int) -> float:
        """
        Calculate IDF score for a term.

        Args:
            doc_freq: Number of documents containing the term

        Returns:
            IDF score
        """
        # IDF formula: log((N - df + 0.5) / (df + 0.5) + 1)
        import math
        return math.log(
            (self.num_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0
        )

    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Search for documents matching the query.

        Args:
            query: Query text
            top_k: Number of results to return

        Returns:
            List of (doc_idx, bm25_score) tuples, sorted by score descending
        """
        if self.num_docs == 0:
            self.logger.warning("BM25 index is empty")
            return []

        query_tokens = self.tokenize(query)
        if not query_tokens:
            self.logger.warning("Query tokenized to empty list")
            return []

        self.logger.debug(f"BM25 search for query: {query[:50]}... ({len(query_tokens)} tokens)")

        # Calculate BM25 scores for all documents
        scores = []
        for doc_idx in range(self.num_docs):
            score = self._score_document(query_tokens, doc_idx)
            scores.append((doc_idx, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return top-k
        results = scores[:top_k]

        if results:
            self.logger.debug(
                f"BM25 search returned {len(results)} results, "
                f"top score: {results[0][1]:.4f}"
            )
        else:
            self.logger.debug("BM25 search returned no results")

        return results

    def _score_document(self, query_tokens: List[str], doc_idx: int) -> float:
        """
        Calculate BM25 score for a document given query tokens.

        Args:
            query_tokens: Tokenized query
            doc_idx: Document index

        Returns:
            BM25 score
        """
        score = 0.0
        doc_tokens = self.tokenized_corpus[doc_idx]
        doc_len = self.doc_lengths[doc_idx]

        # Count term frequencies in document
        term_freqs = {}
        for token in doc_tokens:
            term_freqs[token] = term_freqs.get(token, 0) + 1

        # Calculate BM25 score
        for token in query_tokens:
            if token not in term_freqs:
                continue

            tf = term_freqs[token]
            idf = self.idf.get(token, 0)

            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            score += idf * (numerator / denominator)

        return score

    def save(self, path: str) -> None:
        """
        Save BM25 index to disk.

        Args:
            path: Path to save index
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        index_data = {
            'k1': self.k1,
            'b': self.b,
            'corpus': self.corpus,
            'tokenized_corpus': self.tokenized_corpus,
            'doc_lengths': self.doc_lengths,
            'avgdl': self.avgdl,
            'doc_freqs': self.doc_freqs,
            'idf': self.idf,
            'num_docs': self.num_docs
        }

        try:
            with open(path, 'wb') as f:
                pickle.dump(index_data, f)
            self.logger.info(f"BM25 index saved to {path}")
        except Exception as e:
            self.logger.error(f"Failed to save BM25 index: {e}")
            raise

    def load(self, path: str) -> None:
        """
        Load BM25 index from disk.

        Args:
            path: Path to load index from
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"BM25 index not found: {path}")

        try:
            with open(path, 'rb') as f:
                index_data = pickle.load(f)

            self.k1 = index_data['k1']
            self.b = index_data['b']
            self.corpus = index_data['corpus']
            self.tokenized_corpus = index_data['tokenized_corpus']
            self.doc_lengths = index_data['doc_lengths']
            self.avgdl = index_data['avgdl']
            self.doc_freqs = index_data['doc_freqs']
            self.idf = index_data['idf']
            self.num_docs = index_data['num_docs']

            self.logger.info(
                f"BM25 index loaded from {path}: "
                f"{self.num_docs} docs, {len(self.idf)} terms"
            )
        except Exception as e:
            self.logger.error(f"Failed to load BM25 index: {e}")
            raise

    def get_size(self) -> int:
        """
        Get number of documents in the index.

        Returns:
            Number of documents
        """
        return self.num_docs
