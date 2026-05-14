# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-05-13

### Phase 3: Cross-Encoder Re-ranking

#### Added
- **Cross-encoder re-ranking** using sentence-transformers library
  - Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
  - Improves exact match rate from 30% to 50% (+20%)
  - Enabled by default in `RAGPipeline`
- **Topic-based filtering** (tested but not enabled by default)
  - Keyword-based topic detection for ML, OOP, Python, Database
  - Provides no improvement over re-ranking alone
- **A/B testing framework** for comparing configurations
  - Script: `scripts/ab_test_improvements.py`
  - Tests 4 configurations: baseline, re-ranking only, topic filtering only, both
- **Comprehensive Phase 3 documentation**
  - `docs/EVALUATION_RESULTS_PHASE3.md` - Detailed A/B test results
  - `docs/PHASE3_SUMMARY.md` - Summary and recommendations
  - `docs/RERANKING_GUIDE.md` - Usage guide for re-ranking
  - `docs/PHASE3_QUICK_REFERENCE.md` - Quick reference card

#### Changed
- `src/rag/rag_pipeline.py`
  - Added `use_reranking` parameter (default: True)
  - Added `use_topic_filtering` parameter (default: False)
  - Lazy loading of reranker and topic detector modules
  - Retrieves `top_k * 4` candidates when re-ranking enabled
- `requirements.txt`
  - Added `sentence-transformers>=2.2.0` dependency
- `README.md`
  - Updated with Phase 3 results and documentation links
  - Updated performance metrics
  - Updated project structure with new files

#### Fixed
- Unicode encoding error in A/B test script (Windows console compatibility)
  - Changed arrow character (→) to ASCII arrow (->)

#### Performance
- Retrieval time: 2.18s → 4.07s (+87% slower)
- Exact match rate: 30% → 50% (+20% improvement)
- Acceptable rate: 60% → 70% (+10% improvement)

#### Queries Fixed
1. "Explain loss functions in machine learning"
   - Before: Caching/Memoization in Data Science ❌
   - After: Loss function ✅

2. "What are Python decorators?"
   - Before: Decorator combination ⚠️
   - After: Decorator ✅

3. "What are the SOLID principles?"
   - Before: Creator (GRASP) ❌
   - After: SOLID ✅

#### Known Issues
- One regression: "What are the advantages of polymorphism?"
  - Before: Polymorphism ✅
  - After: Composite ❌
  - Net gain: +3 correct, -1 regression = +2 improvement

- Still failing (5/10 queries):
  - Single Responsibility Principle
  - Encapsulation
  - List comprehensions
  - Inheritance alternatives
  - Polymorphism (regression)

#### Next Steps
- Try different embedding model (expected +10-20% improvement)
- Implement hybrid search (BM25 + semantic, expected +15-25%)
- Fine-tune cross-encoder on domain data (expected +10-15%)
- Target: 70% exact match rate (currently 50%)

---

## [1.0.0] - 2026-05-12

### Phase 1-2: Hierarchical Chunking and Evaluation

#### Added
- **Hierarchical chunking strategy**
  - Creates 1753 chunks vs 179 with structure-based chunking
  - Preserves document hierarchy and context
  - Includes topic metadata for filtering
- **Multi-store manager** for managing multiple vector stores
- **Comprehensive evaluation framework**
  - 24 test queries across 4 topics (Python, OOP, ML, Database)
  - Metrics: precision, recall, MRR, relevancy scores
  - Cross-validation support
- **Interactive RAG console** with streaming mode
- **Embedding cache** for faster re-indexing
- **Production features**
  - Retry mechanisms with exponential backoff
  - Fault tolerance and error recovery
  - Session logging and monitoring

#### Changed
- Switched from structure-based to hierarchical chunking as default
- Increased `top_k` from 3 to 5 for better recall

#### Performance
- Vector store: 179 vectors → 1753 vectors
- Retrieval accuracy: Not measured → 30% exact match (baseline)
- Cache hit rate: 66-100% depending on workload

#### Documentation
- `docs/ARCHITECTURE.md` - Design decisions
- `docs/QUICK_START.md` - Usage guide
- `docs/PROJECT_COMPLETE.md` - Project summary
- `docs/EVALUATION_RESULTS.md` - Phase 1-2 evaluation
- `CLAUDE.md` - Development guide

---

## [0.1.0] - Initial Release

### Added
- Basic RAG pipeline with Ollama integration
- FAISS vector store
- Structure-based chunking
- 4 educational markdown documents (56K words)
- Basic console interface
- Unit tests for chunking strategies

#### Components
- `src/core/ollama_client.py` - LLM generation
- `src/core/ollama_embedder.py` - Embeddings
- `src/chunking/structure_chunker.py` - Structure-based chunking
- `src/rag/vector_store.py` - FAISS integration
- `src/rag/rag_pipeline.py` - Complete RAG pipeline
- `scripts/rag_console.py` - Interactive console

#### Technology Stack
- Ollama llama3.1:latest (8B parameters)
- nomic-embed-text:latest (768 dimensions)
- FAISS IndexFlatL2
- Python 3.10+

---

## Version History

- **1.1.0** (2026-05-13) - Phase 3: Cross-encoder re-ranking (+20% accuracy)
- **1.0.0** (2026-05-12) - Phase 1-2: Hierarchical chunking and evaluation
- **0.1.0** (Initial) - Basic RAG pipeline with structure-based chunking
