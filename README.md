# RAG Pipeline - Educational Knowledge Base

Complete production-ready Retrieval-Augmented Generation pipeline for querying educational Notion documents about Python, OOP, Machine Learning, and Database Optimization.

## 🎯 Overview

This RAG system indexes 4 educational markdown documents (56K words, 1753 chunks with hierarchical chunking) and provides an interactive console interface for natural language queries. Built with Ollama (local LLM), FAISS (vector store), cross-encoder re-ranking, and comprehensive evaluation metrics.

**Key Features:**
- ✅ Interactive console with `input()` function
- ✅ 1753 vectors indexed from educational documents (hierarchical chunking)
- ✅ **Cross-encoder re-ranking** for 50% retrieval accuracy (+20% improvement)
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
cd C:\Users\YVV\PycharmProjects\Practice\RAG-Pipeline

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies (if needed)
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
- **`src/rag/`** - Vector store (FAISS), embedding cache, RAG pipeline
- **`src/evaluation/`** - Comprehensive metrics framework
- **`scripts/`** - Console interface, testing, evaluation, indexing

### Technology Stack

- **LLM**: Ollama llama3.1:latest (8B parameters, local)
- **Embeddings**: nomic-embed-text:latest (768 dimensions)
- **Re-ranking**: cross-encoder/ms-marco-MiniLM-L-6-v2 (sentence-transformers)
- **Vector Store**: FAISS (IndexFlatL2)
- **Caching**: Disk-based with SHA256 keys
- **Testing**: pytest with 9/9 unit tests passing

## 📊 Performance

### Phase 3 Results (Cross-Encoder Re-ranking)

| Metric | Baseline | With Re-ranking | Improvement |
|--------|----------|-----------------|-------------|
| Exact match rate | 30% (3/10) | **50% (5/10)** | **+20%** ✅ |
| Acceptable rate | 60% (6/10) | **70% (7/10)** | **+10%** ✅ |
| Retrieval latency | 2.18s | 4.07s | +87% ⚠️ |
| Vector store size | 1753 vectors | 1753 vectors | - |
| Embedding dimensions | 768 | 768 | - |

**Queries Fixed by Re-ranking:**
- ✅ "Explain loss functions in machine learning" - Caching → Loss function
- ✅ "What are Python decorators?" - Decorator combination → Decorator
- ✅ "What are the SOLID principles?" - Creator (GRASP) → SOLID

**See**: `docs/EVALUATION_RESULTS_PHASE3.md` for detailed results

### System Performance

| Metric | Value | Source |
|--------|-------|--------|
| Retrieval latency | Min: 4.19s, Max: 6.00s, Avg: 5.10s (2 queries) | logs/rag_console.log |
| Generation latency | Min: 30.84s, Max: 68.48s, Avg: 49.66s (2 queries) | logs/rag_console.log |
| Total query latency | Min: 35.03s, Max: 74.48s, Avg: 54.76s (2 queries) | logs/rag_console.log |
| Retrieval accuracy | 50% exact match, 70% acceptable | Phase 3 evaluation |
| Answer quality | High (with code examples) | Manual review |
| Cache hit rate | 0% fresh indexing, 100% re-indexing | Varies by workload |
| Test coverage | 16% overall, 9/9 chunking tests passing | pytest --cov output |

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
│   ├── ab_test_improvements.py       # A/B testing script ⭐
│   ├── index_documents_safe.py       # Document indexing
│   └── verify_ollama.py              # Setup verification
├── tests/
│   ├── test_chunking_strategies.py   # 9/9 unit tests
│   └── test_queries.py               # 24 test queries
├── data/
│   ├── raw/               # 4 markdown documents (56K words)
│   ├── cache/             # Embedding cache (1.01 MB)
│   └── vector_stores/     # FAISS indexes (1753 vectors)
└── docs/                  # Comprehensive documentation
    ├── ARCHITECTURE.md    # Design decisions
    ├── QUICK_START.md     # Usage guide
    ├── PROJECT_COMPLETE.md # Project summary
    ├── EVALUATION_RESULTS.md # Phase 1-2 evaluation
    ├── EVALUATION_RESULTS_PHASE3.md # Phase 3 A/B test ⭐
    ├── PHASE3_SUMMARY.md  # Phase 3 summary ⭐
    ├── RERANKING_GUIDE.md # Re-ranking usage guide ⭐
    └── PHASE3_QUICK_REFERENCE.md # Quick reference ⭐
```

## 🎓 Evaluation Results

### Phase 3: Cross-Encoder Re-ranking (Latest)

**Configuration**: Hierarchical chunking + Cross-encoder re-ranking

| Configuration | Exact Match | Acceptable | Avg Time |
|---------------|-------------|------------|----------|
| Baseline (no re-ranking) | 30% (3/10) | 60% (6/10) | 2.18s |
| **With re-ranking** | **50% (5/10)** | **70% (7/10)** | 4.07s |

**Key Improvements:**
- ✅ Query 1 (Loss functions): Fixed
- ✅ Query 5 (Decorators): Fixed
- ✅ Query 8 (SOLID principles): Fixed
- ⚠️ Query 9 (Polymorphism): Regression

**See**: `docs/EVALUATION_RESULTS_PHASE3.md` for full A/B test results

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
- `use_reranking`: Enable cross-encoder re-ranking (default: True) ⭐
- `use_topic_filtering`: Enable topic filtering (default: False)

## 🛠️ Maintenance

### Re-index Documents

If you modify the source documents:
```bash
python scripts/index_documents_safe.py
```
This will take ~10 minutes to complete.

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
- **[PROJECT_COMPLETE.md](docs/PROJECT_COMPLETE.md)** - Complete project summary
- **[EVALUATION_RESULTS.md](docs/EVALUATION_RESULTS.md)** - Phase 1-2 evaluation metrics
- **[EVALUATION_RESULTS_PHASE3.md](docs/EVALUATION_RESULTS_PHASE3.md)** - Phase 3 A/B test results ⭐
- **[PHASE3_SUMMARY.md](docs/PHASE3_SUMMARY.md)** - Phase 3 summary and recommendations ⭐
- **[RERANKING_GUIDE.md](docs/RERANKING_GUIDE.md)** - Cross-encoder re-ranking guide ⭐
- **[PHASE3_QUICK_REFERENCE.md](docs/PHASE3_QUICK_REFERENCE.md)** - Quick reference card ⭐
- **[CLAUDE.md](CLAUDE.md)** - Development guide

## 🎯 Features

### Core Features
- ✅ Interactive console with `input()` function
- ✅ Natural language query processing
- ✅ Semantic search with FAISS
- ✅ Answer generation with Ollama
- ✅ Source attribution with relevance scores
- ✅ Streaming mode for real-time responses

### Production Features
- ✅ Embedding cache (66-100% hit rate)
- ✅ Cross-encoder re-ranking (50% retrieval accuracy)
- ✅ Retry mechanisms (3 retries, exponential backoff)
- ✅ Fault tolerance and error recovery
- ✅ Session logging and monitoring
- ✅ Performance metrics tracking

### Evaluation Features
- ✅ 24 test queries across 4 topics
- ✅ Comprehensive metrics (precision, recall, MRR, relevancy)
- ✅ Cross-validation framework
- ✅ A/B testing capability
- ✅ Phase 3: Re-ranking vs baseline comparison

## 🐛 Troubleshooting

### "Store not found" error
- Make sure you're in the project root directory
- Check that `data/vector_stores/structure_store.faiss/` exists
- Re-run indexing: `python scripts/index_documents_safe.py`

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
2. ✅ Cross-encoder re-ranking (30% → 50% accuracy)
3. ✅ A/B testing framework
4. ✅ Comprehensive evaluation metrics

### Future Improvements 🎯
1. Try different embedding models (all-MiniLM-L6-v2, bge-large-en-v1.5)
2. Implement hybrid search (BM25 + semantic)
3. Fine-tune cross-encoder on domain-specific data
4. Support for more document types
5. Cloud LLM integration for faster generation

**Target**: 70% exact match rate (currently 50%)

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

**Status**: Production-ready prototype with cross-encoder re-ranking, 85% complete
**Last Updated**: 2026-05-13
**Version**: 1.1.0 (Phase 3 complete)
