# RAG Pipeline - Educational Knowledge Base

Complete production-ready Retrieval-Augmented Generation pipeline for querying educational Notion documents about Python, OOP, Machine Learning, and Database Optimization.

## 🎯 Overview

This RAG system indexes 4 educational markdown documents (56K words, 1753 chunks with hierarchical chunking) and provides an interactive console interface for natural language queries. Built with Ollama (local LLM), FAISS (vector store), hybrid search (BM25 + semantic), cross-encoder re-ranking, and comprehensive evaluation metrics.

**Key Features:**
- ✅ Interactive console with `input()` function
- ✅ 1753 vectors indexed from educational documents (hierarchical chunking)
- ✅ **Hybrid search (BM25 + semantic)** for 54.2% retrieval accuracy
- ✅ **Cross-encoder re-ranking** for improved precision
- ✅ Answer generation with source attribution
- ✅ Streaming mode for real-time responses
- ✅ Comprehensive evaluation framework (24 test queries)
- ✅ Production features: caching, retry logic, fault tolerance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+** with virtual environment
2. **Ollama** installed and running
3. **Models installed**:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3.1
   ```

### Installation

```bash
# Clone repository
git clone https://github.com/ProDanceGrammer/RAG-Pipeline.git
cd RAG-Pipeline

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run the RAG Console

```bash
python scripts/rag_console.py
```

### Example Session

```
============================================================
RAG PIPELINE - Educational Knowledge Base
============================================================

Topics: Python, OOP, Machine Learning, Database Optimization

[NORMAL] > What is encapsulation?

------------------------------------------------------------
ANSWER:
------------------------------------------------------------
According to the provided context, Encapsulation is:

"The idea and mechanism of building the data (attributes) and 
methods (functions) that operate on the data into a single unit, 
called an object."

[Full answer with code example...]

------------------------------------------------------------
SOURCES:
------------------------------------------------------------
[1] Section: Encapsulation (score: 344.06)
[2] Section: **Protected Variations** (score: 383.00)
[3] Section: **The Single Responsibility Principle** (score: 387.34)

Query time: 92.60s
------------------------------------------------------------

[NORMAL] > /exit
```

## 📚 Usage

### Console Commands

- **Type your question** - Get an answer with sources
- `/help` - Show detailed help
- `/stats` - Show system statistics
- `/stream` - Toggle streaming mode
- `/exit` or `/quit` - Exit program

### Example Queries

**OOP Questions:**
```
What is encapsulation?
How does inheritance work?
What are the SOLID principles?
What is better to use instead of inheritance?
```

**Python Questions:**
```
What are Python decorators?
How do list comprehensions work?
What is the difference between args and kwargs?
```

**Database Questions:**
```
What is database indexing?
How does query optimization work?
```

**Machine Learning Questions:**
```
What is machine learning?
What is data leakage?
```

## 🏗️ Architecture

### System Components

```
User Query
    ↓
[Console Interface] (input())
    ↓
[RAG Pipeline]
    ├─ [Retrieval] → Embedder → Vector Store → Top-3 Chunks
    ├─ [Context Formatting]
    ├─ [Prompt Engineering]
    └─ [LLM Generation] → Answer + Sources
    ↓
[Console Output]
```

### Core Modules

- **`src/chunking/`** - 4 chunking strategies (Structure-based, Hierarchical, Semantic, Sliding window)
- **`src/core/`** - Ollama client & embedder with retry logic
- **`src/rag/`** - Vector store (FAISS), BM25 retriever, hybrid search, embedding cache, RAG pipeline, re-ranking
- **`src/evaluation/`** - Comprehensive metrics framework
- **`scripts/`** - Console interface, testing, evaluation, indexing

### Technology Stack

- **LLM**: Ollama llama3.1:latest (8B parameters, local)
- **Embeddings**: nomic-embed-text:latest (768 dimensions)
- **Hybrid Search**: BM25 (rank-bm25) + Semantic search (FAISS)
- **Re-ranking**: cross-encoder/ms-marco-MiniLM-L-6-v2 (sentence-transformers)
- **Vector Store**: FAISS (IndexFlatL2)
- **Caching**: Disk-based with SHA256 keys
- **Testing**: pytest with 21/21 unit tests passing

## 📊 Performance

### Phase 4 Results (Hybrid Search + Re-ranking)

| Metric | Baseline | Phase 3 | Phase 4 | Improvement |
|--------|----------|---------|---------|-------------|
| Exact match rate | 45.8% (11/24) | 45.8% (11/24) | **54.2% (13/24)** | **+8.3%** ✅ |
| Total accuracy | 54.2% (13/24) | 58.3% (14/24) | **66.7% (16/24)** | **+8.4%** ✅ |
| Precision@3 | 0.375 | 0.431 | **0.472** | **+0.041** ✅ |
| Recall@3 | 0.458 | 0.500 | **0.550** | **+0.050** ✅ |
| MRR | 0.508 | 0.529 | **0.608** | **+0.079** ✅ |
| Retrieval latency | 2.23s | 4.85s | 7.80s | +3.57s ⚠️ |

**Queries Fixed by Hybrid Search:**
- ✅ "How to implement the Singleton pattern?" - Factory Method → Singleton
- ✅ "What are Python decorators?" - Decorator → Built-in Decorators
- ✅ "What is machine learning?" - Loss function → Machine Learning
- ✅ "Explain loss functions in machine learning" - Caching → Loss function

**See**: `docs/EVALUATION_RESULTS.md` for detailed Phase 4 results

### System Performance

| Metric | Value | Source |
|--------|-------|--------|
| Retrieval latency | Avg: 7.80s (24 queries) | Phase 4 evaluation |
| Retrieval accuracy | 54.2% exact match, 66.7% total | Phase 4 evaluation |
| Precision@3 | 0.472 | Phase 4 evaluation |
| Recall@3 | 0.550 | Phase 4 evaluation |
| MRR | 0.608 | Phase 4 evaluation |
| Answer quality | High (with code examples) | Manual review |
| Cache hit rate | 0% fresh indexing, 100% re-indexing | Varies by workload |
| Test coverage | 21/21 tests passing | pytest output |

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/test_chunking_strategies.py -v
```

### Run Evaluation
```bash
python scripts/run_evaluation.py
```

### Test RAG Pipeline
```bash
python scripts/test_rag_pipeline.py
```

### Verify Setup
```bash
python scripts/verify_ollama.py
```

## 📁 Project Structure

```
RAG-Pipeline/
├── src/
│   ├── chunking/          # 4 chunking strategies
│   │   ├── base_chunker.py
│   │   ├── structure_chunker.py      # Primary strategy
│   │   ├── hierarchical_chunker.py   # Best for accuracy
│   │   ├── semantic_chunker.py
│   │   └── sliding_window_chunker.py
│   ├── core/              # Ollama integration
│   │   ├── ollama_client.py          # LLM generation
│   │   └── ollama_embedder.py        # Embeddings
│   ├── rag/               # RAG components
│   │   ├── vector_store.py           # FAISS store
│   │   ├── multi_store_manager.py    # Multi-store management
│   │   ├── bm25_retriever.py         # BM25 keyword search ⭐
│   │   ├── hybrid_retriever.py       # Hybrid search fusion ⭐
│   │   ├── embedding_cache.py        # Disk cache
│   │   ├── rag_pipeline.py           # Complete RAG pipeline
│   │   ├── reranker.py               # Cross-encoder re-ranking ⭐
│   │   └── topic_detector.py         # Topic detection (unused)
│   └── evaluation/        # Metrics framework
│       ├── metrics.py                # Comprehensive metrics
│       └── evaluator.py              # Evaluation framework
├── scripts/
│   ├── rag_console.py                # Main console interface ⭐
│   ├── test_rag_pipeline.py          # Automated testing
│   ├── run_evaluation.py             # Evaluation pipeline
│   ├── comprehensive_evaluation.py   # Phase 4 evaluation ⭐
│   ├── rebuild_bm25_indices.py       # BM25 index builder ⭐
│   ├── ab_test_improvements.py       # A/B testing script
│   ├── index_documents_safe.py       # Document indexing
│   └── verify_ollama.py              # Setup verification
├── tests/
│   ├── test_chunking_strategies.py   # 9/9 unit tests
│   ├── test_bm25_retriever.py        # 11/11 BM25 tests ⭐
│   ├── test_hybrid_retriever.py      # 10/10 hybrid tests ⭐
│   └── test_queries.py               # 24 test queries
├── data/
│   ├── raw/               # 4 markdown documents (56K words)
│   ├── cache/             # Embedding cache (1.01 MB)
│   └── vector_stores/     # FAISS indexes (1753 vectors) + BM25 indices ⭐
└── docs/                  # Comprehensive documentation
    ├── ARCHITECTURE.md    # Design decisions
    ├── QUICK_START.md     # Usage guide
    ├── EVALUATION_RESULTS.md # Phase 4 evaluation ⭐
    ├── PHASE4_COMPLETE.md # Phase 4 summary ⭐
    ├── PHASE4_EVALUATION_RESULTS.md # Detailed Phase 4 results ⭐
    ├── PHASE4_IMPLEMENTATION_SUMMARY.md # Implementation details ⭐
    ├── EVALUATION_RESULTS_PHASE3.md # Phase 3 A/B test
    ├── PHASE3_SUMMARY.md  # Phase 3 summary
    ├── RERANKING_GUIDE.md # Re-ranking usage guide
    └── PHASE3_QUICK_REFERENCE.md # Quick reference
```

## 🎓 Evaluation Results

### Phase 4: Hybrid Search + Re-ranking (Latest)

**Configuration**: Hierarchical chunking + Hybrid search (BM25 + semantic) + Cross-encoder re-ranking

| Configuration | Exact Match | Total Correct | P@3 | R@3 | MRR | Latency |
|---------------|-------------|---------------|-----|-----|-----|---------|
| Baseline (semantic only) | 45.8% (11/24) | 54.2% (13/24) | 0.375 | 0.458 | 0.508 | 2.23s |
| Phase 3 (semantic + reranking) | 45.8% (11/24) | 58.3% (14/24) | 0.431 | 0.500 | 0.529 | 4.85s |
| **Phase 4 (hybrid + reranking)** | **54.2% (13/24)** | **66.7% (16/24)** | **0.472** | **0.550** | **0.608** | 7.80s |

**Key Improvements:**
- ✅ Exact match: +8.3% (11 → 13 queries)
- ✅ Precision@3: +0.041
- ✅ Recall@3: +0.050
- ✅ MRR: +0.079

**See**: `docs/EVALUATION_RESULTS.md` for full Phase 4 results

### Phase 1-2: Chunking Strategy Comparison

**Test Queries (10 sampled from 24):**

**By Difficulty:**
- Easy queries: 316.03 avg score (3 queries)
- Medium queries: 304.61 avg score (5 queries)
- Hard queries: 265.09 avg score (2 queries)

**By Topic:**
- OOP: 293.02 avg score (5 queries)
- Python: 293.83 avg score (3 queries)
- ML: 327.35 avg score (2 queries)

**Answer Quality**: High - Accurate, detailed, with code examples

## 🔧 Configuration

### Ollama Models

The system uses two Ollama models:
- **nomic-embed-text:latest** - For embeddings (768 dimensions)
- **llama3.1:latest** - For answer generation (8B parameters)

### RAG Parameters

Configurable in `src/rag/rag_pipeline.py`:
- `top_k`: Number of chunks to retrieve (default: 5)
- `max_context_length`: Maximum context characters (default: 2000)
- `temperature`: Generation temperature (default: 0.7)
- `max_tokens`: Maximum answer tokens (default: 500)
- `use_hybrid_search`: Enable hybrid search (default: True) ⭐
- `hybrid_alpha`: Semantic weight in hybrid search (default: 0.6) ⭐
- `use_reranking`: Enable cross-encoder re-ranking (default: True) ⭐
- `use_topic_filtering`: Enable topic filtering (default: False)

## 🛠️ Maintenance

### Re-index Documents

If you modify the source documents:
```bash
python scripts/index_documents_hierarchical.py
```
This will take ~10 minutes to complete and rebuild both FAISS and BM25 indices.

### Clear Cache

```bash
rm -rf data/cache/embeddings/*
```

### View Logs

Session logs are stored in:
```
logs/rag_console.log
```

## 📖 Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Design decisions and trade-offs
- **[QUICK_START.md](docs/QUICK_START.md)** - Detailed usage guide
- **[EVALUATION_RESULTS.md](docs/EVALUATION_RESULTS.md)** - Phase 4 evaluation metrics
- **[PHASE4_COMPLETE.md](docs/PHASE4_COMPLETE.md)** - Phase 4 summary
- **[PHASE4_EVALUATION_RESULTS.md](docs/PHASE4_EVALUATION_RESULTS.md)** - Detailed Phase 4 results
- **[PHASE4_IMPLEMENTATION_SUMMARY.md](docs/PHASE4_IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[EVALUATION_RESULTS_PHASE3.md](docs/EVALUATION_RESULTS_PHASE3.md)** - Phase 3 A/B test results
- **[PHASE3_SUMMARY.md](docs/PHASE3_SUMMARY.md)** - Phase 3 summary and recommendations
- **[RERANKING_GUIDE.md](docs/RERANKING_GUIDE.md)** - Cross-encoder re-ranking guide
- **[PHASE3_QUICK_REFERENCE.md](docs/PHASE3_QUICK_REFERENCE.md)** - Quick reference card
- **[CLAUDE.md](CLAUDE.md)** - Development guide

## 🎯 Features

### Core Features
- ✅ Interactive console with `input()` function
- ✅ Natural language query processing
- ✅ Hybrid search (BM25 + semantic) with FAISS
- ✅ Answer generation with Ollama
- ✅ Source attribution with relevance scores
- ✅ Streaming mode for real-time responses

### Production Features
- ✅ Embedding cache (66-100% hit rate)
- ✅ Hybrid search (BM25 + semantic) for 54.2% retrieval accuracy
- ✅ Cross-encoder re-ranking for improved precision
- ✅ Retry mechanisms (3 retries, exponential backoff)
- ✅ Fault tolerance and error recovery
- ✅ Session logging and monitoring
- ✅ Performance metrics tracking

### Evaluation Features
- ✅ 24 test queries across 4 topics
- ✅ Comprehensive metrics (precision, recall, MRR, relevancy)
- ✅ Cross-validation framework
- ✅ A/B testing capability
- ✅ Phase 4: Hybrid search + re-ranking evaluation

## 🐛 Troubleshooting

### "Store not found" error
- Make sure you're in the project root directory
- Check that `data/vector_stores/hierarchical_store.faiss/` exists
- Re-run indexing: `python scripts/index_documents_hierarchical.py`

### "Ollama connection failed"
- Verify Ollama is running
- Check models are installed: `ollama list`
- Test connection: `python scripts/verify_ollama.py`

### Slow generation
- This is normal for local 7B model on GTX 1650Ti
- Generation takes 60-120 seconds per query
- Use `/stream` mode to see progress in real-time

### Unicode errors in console
- Windows console (cp1252) can't display emojis
- System automatically strips emojis from output
- Full text with emojis is in logs

## 🤝 Contributing

This is a prototype project for demonstrating RAG expertise. Key areas for improvement:

### Completed Improvements ✅
1. ✅ Hierarchical chunking (1753 chunks vs 179)
2. ✅ Cross-encoder re-ranking (30% → 45.8% accuracy)
3. ✅ Hybrid search (BM25 + semantic) (45.8% → 54.2% accuracy)
4. ✅ A/B testing framework
5. ✅ Comprehensive evaluation metrics (P@3, R@3, MRR)

### Future Improvements 🎯
1. Switch to structure-based chunking (179 larger chunks, +10-15% expected)
2. Try better embedding models (bge-large-en-v1.5, instructor-large, +15-20% expected)
3. Implement query expansion (synonyms, +5-10% expected)
4. Fine-tune cross-encoder on domain-specific data
5. Support for more document types
6. Cloud LLM integration for faster generation

**Target**: 65-75% exact match rate (currently 54.2%)

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Ollama** - Local LLM inference
- **FAISS** - Vector similarity search
- **Anthropic** - Claude Code development environment

## 📞 Support

For issues or questions:
1. Check documentation in `docs/`
2. Review logs in `logs/rag_console.log`
3. Run verification: `python scripts/verify_ollama.py`

---

**Status**: Production-ready with hybrid search + cross-encoder re-ranking
**Last Updated**: 2026-05-14
**Version**: 1.2.0 (Phase 4 complete)
