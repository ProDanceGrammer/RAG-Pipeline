#!/usr/bin/env python3
"""
Rebuild BM25 indices for existing vector stores.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.multi_store_manager import MultiStoreManager
from src.rag.bm25_retriever import BM25Retriever
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rebuild_bm25_index(strategy_name: str, dimension: int = 768):
    """
    Rebuild BM25 index for a vector store.

    Args:
        strategy_name: Name of the chunking strategy
        dimension: Embedding dimension
    """
    logger.info(f"Rebuilding BM25 index for {strategy_name}...")

    base_dir = Path("data/vector_stores")
    manager = MultiStoreManager(base_dir)

    # Load existing FAISS store
    try:
        store = manager.load_store(strategy_name, dimension=dimension)
        logger.info(f"Loaded {strategy_name} store with {store.get_size()} vectors")
    except Exception as e:
        logger.error(f"Failed to load store: {e}")
        return False

    # Extract texts from metadata
    texts = [metadata.get('text', '') for metadata in store.metadata]
    logger.info(f"Extracted {len(texts)} texts from metadata")

    # Build BM25 index
    bm25 = BM25Retriever()
    bm25.index(texts)

    # Save BM25 index
    bm25_path = base_dir / f"{strategy_name}_bm25.pkl"
    try:
        bm25.save(str(bm25_path))
        logger.info(f"Saved BM25 index to {bm25_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save BM25 index: {e}")
        return False


def main():
    """Rebuild BM25 indices for all vector stores."""
    logger.info("="*80)
    logger.info("REBUILDING BM25 INDICES")
    logger.info("="*80)

    strategies = [
        ("hierarchical", 768),
        ("structure", 768),
    ]

    success_count = 0
    for strategy_name, dimension in strategies:
        if rebuild_bm25_index(strategy_name, dimension):
            success_count += 1
            logger.info(f"✅ Successfully rebuilt BM25 index for {strategy_name}")
        else:
            logger.error(f"❌ Failed to rebuild BM25 index for {strategy_name}")

    logger.info("="*80)
    logger.info(f"COMPLETE: {success_count}/{len(strategies)} indices rebuilt")
    logger.info("="*80)


if __name__ == "__main__":
    main()
