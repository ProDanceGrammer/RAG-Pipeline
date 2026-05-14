# Cross-Encoder Re-ranking Guide

This guide explains how to use the cross-encoder re-ranking feature to improve RAG retrieval accuracy.

---

## Overview

**Cross-encoder re-ranking** improves retrieval accuracy by re-scoring initial search results using a more sophisticated model that understands the semantic relationship between queries and documents.

**Performance Impact:**
- Exact match rate: 30% → 50% (+20% improvement)
- Acceptable rate: 60% → 70% (+10% improvement)
- Retrieval time: 2.2s → 4.1s (+87% slower, but acceptable)

---

## Quick Start

Re-ranking is **enabled by default** as of Phase 3. No configuration needed.

```python
from src.core.ollama_embedder import OllamaEmbedder
from src.core.ollama_client import OllamaClient
from src.rag.multi_store_manager import MultiStoreManager
from src.rag.rag_pipeline import RAGPipeline

# Initialize components
embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
generator = OllamaClient(model_name="llama3.1:latest")
manager = MultiStoreManager(Path("data/vector_stores"))
manager.load_store("hierarchical", dimension=768)

# Create pipeline (re-ranking enabled by default)
pipeline = RAGPipeline(
    embedder=embedder,
    generator=generator,
    manager=manager,
    strategy_name="hierarchical",
    top_k=5
)

# Query as usual
result = pipeline.query("What are the SOLID principles?")
print(result['answer'])
```

---

## Configuration Options

### Enable/Disable Re-ranking

```python
# Re-ranking enabled (default, recommended)
pipeline = RAGPipeline(
    embedder=embedder,
    generator=generator,
    manager=manager,
    strategy_name="hierarchical",
    top_k=5,
    use_reranking=True  # Default
)

# Re-ranking disabled (faster but less accurate)
pipeline = RAGPipeline(
    embedder=embedder,
    generator=generator,
    manager=manager,
    strategy_name="hierarchical",
    top_k=5,
    use_reranking=False
)
```

### Topic Filtering (Not Recommended)

Topic filtering was tested but provides **no improvement** over re-ranking alone.

```python
# Not recommended - adds complexity without benefit
pipeline = RAGPipeline(
    embedder=embedder,
    generator=generator,
    manager=manager,
    strategy_name="hierarchical",
    top_k=5,
    use_reranking=True,
    use_topic_filtering=False  # Keep disabled
)
```

---

## How It Works

### 1. Initial Retrieval (Embedding Search)

The pipeline first retrieves `top_k * 4` candidates using embedding similarity:

```python
# With re-ranking: get 20 candidates (top_k=5 * 4)
# Without re-ranking: get 5 candidates (top_k=5)
search_k = self.top_k * 4 if self.use_reranking else self.top_k
results = self.manager.search(self.strategy_name, query_emb, top_k=search_k)
```

### 2. Re-ranking (Cross-Encoder)

The cross-encoder model scores each query-document pair:

```python
# Cross-encoder sees full text, not just embeddings
pairs = [(query, chunk_text) for chunk_text in candidates]
scores = cross_encoder.predict(pairs)

# Higher score = more relevant
# Scores typically range from -15 to +15
```

### 3. Final Selection

Return top-k results after re-ranking:

```python
# Sort by cross-encoder score (higher is better)
reranked.sort(key=lambda x: x[1], reverse=True)
return reranked[:top_k]
```

---

## Understanding Scores

### L2 Distance (Embedding Search)

- **Lower is better** (distance metric)
- Typical range: 150-400
- Example: 159.46 (close), 362.54 (far)
- Problem: Similar scores for different concepts

### Cross-Encoder Score (Re-ranking)

- **Higher is better** (relevance score)
- Typical range: -15 to +15
- Example: 4.95 (relevant), -11.13 (not relevant)
- Better at distinguishing semantic relevance

---

## Performance Characteristics

### Memory Usage

- **Model size**: ~90MB (ms-marco-MiniLM-L-6-v2)
- **Runtime memory**: ~200MB additional
- **First load**: Downloads model from HuggingFace (~2-3 seconds)
- **Subsequent loads**: Cached locally (instant)

### Latency Breakdown

| Operation | Time | Percentage |
|-----------|------|------------|
| Query embedding | 0.1s | 2% |
| Vector search | 0.1s | 2% |
| Cross-encoder re-ranking | 2.0s | 49% |
| Context formatting | 0.1s | 2% |
| LLM generation | 1.8s | 45% |
| **Total** | **4.1s** | **100%** |

### Optimization Tips

1. **Batch queries** if processing multiple at once
2. **Reduce top_k** if speed is critical (try top_k=3)
3. **Use GPU** if available (set device='cuda' in reranker)
4. **Cache results** for repeated queries

---

## Examples

### Example 1: Query Fixed by Re-ranking

**Query**: "What are the SOLID principles?"

**Without re-ranking:**
```
Top result: Creator (GRASP principle)
Score: 159.46 (L2 distance)
Status: ❌ Wrong - retrieved different design principles
```

**With re-ranking:**
```
Top result: SOLID
Score: 4.95 (cross-encoder)
Status: ✅ Correct - found exact match
```

### Example 2: Query with Regression

**Query**: "What are the advantages of polymorphism?"

**Without re-ranking:**
```
Top result: Polymorphism
Score: 221.22 (L2 distance)
Status: ✅ Correct
```

**With re-ranking:**
```
Top result: Composite
Score: 1.80 (cross-encoder)
Status: ❌ Wrong - regression from re-ranking
```

**Note**: This is the only regression out of 10 queries. The net gain is still positive (+3 correct, -1 regression).

---

## Troubleshooting

### Model Download Issues

If the model fails to download:

```python
# Set HuggingFace token for faster downloads
import os
os.environ['HF_TOKEN'] = 'your_token_here'

# Or download manually
from sentence_transformers import CrossEncoder
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
```

### Slow Performance

If re-ranking is too slow:

```python
# Option 1: Reduce candidates
pipeline = RAGPipeline(
    ...,
    top_k=3,  # Fewer results to re-rank
    use_reranking=True
)

# Option 2: Use GPU (if available)
from src.rag.reranker import CrossEncoderReranker
reranker = CrossEncoderReranker(device='cuda')
```

### Memory Issues

If running out of memory:

```python
# Option 1: Disable re-ranking
pipeline = RAGPipeline(
    ...,
    use_reranking=False
)

# Option 2: Use smaller model (not recommended - less accurate)
from src.rag.reranker import CrossEncoderReranker
reranker = CrossEncoderReranker(
    model_name='cross-encoder/ms-marco-TinyBERT-L-2-v2'
)
```

---

## Evaluation Results

Full evaluation results available in:
- `docs/EVALUATION_RESULTS_PHASE3.md` - Detailed query-by-query results
- `docs/PHASE3_SUMMARY.md` - Summary and recommendations

### Key Metrics

| Metric | Baseline | With Re-ranking | Improvement |
|--------|----------|-----------------|-------------|
| Exact match rate | 30% | 50% | +20% |
| Acceptable rate | 60% | 70% | +10% |
| Avg retrieval time | 2.18s | 4.07s | +87% |

### Queries Fixed

1. **Loss functions**: Caching → Loss function ✅
2. **Decorators**: Decorator combination → Decorator ✅
3. **SOLID principles**: Creator → SOLID ✅

### Queries Still Failing

1. **Single Responsibility**: Still retrieves Database Partitioning ❌
2. **Encapsulation**: Retrieves Composition ⚠️
3. **List comprehensions**: Retrieves Generator ⚠️
4. **Inheritance alternative**: Retrieves Inheritance ⚠️
5. **Polymorphism**: Regression from re-ranking ❌

---

## Next Steps

To further improve accuracy beyond 50%:

1. **Try different embedding model** (recommended first step)
   - Replace nomic-embed-text with all-MiniLM-L6-v2 or bge-large-en-v1.5
   - Expected improvement: +10-20%

2. **Implement hybrid search** (BM25 + semantic)
   - Combine keyword matching with semantic search
   - Expected improvement: +15-25%

3. **Fine-tune cross-encoder** (last resort)
   - Train on domain-specific data
   - Expected improvement: +10-15%

See `docs/PHASE3_SUMMARY.md` for detailed next steps.

---

## References

- **Model**: [cross-encoder/ms-marco-MiniLM-L-6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)
- **Library**: [sentence-transformers](https://www.sbert.net/)
- **Paper**: [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)
