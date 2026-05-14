# RAG Pipeline Architecture

## Overview

This document explains the architectural decisions, design patterns, and trade-offs made in building this RAG (Retrieval-Augmented Generation) pipeline.

## System Architecture

### High-Level Design

```
User Query
    ↓
[Console Interface] (input())
    ↓
[RAG Pipeline]
    ↓
[Retrieval] → [Embedder] → [Vector Store] → Top-K Chunks
    ↓
[Context Formatting]
    ↓
[Prompt Engineering]
    ↓
[LLM Generation] → Answer + Sources
    ↓
[Console Output]
```

## Core Components

### 1. Chunking Layer (`src/chunking/`)

**Purpose**: Split documents into semantically meaningful chunks for indexing.

**Design Pattern**: Strategy Pattern
- `BaseChunker` - Abstract base class defining interface
- `StructureChunker` - Primary strategy (chunks by ## headers)
- `HierarchicalChunker` - Parent-child relationships
- `SemanticChunker` - Embedding-based boundaries
- `SlidingWindowChunker` - Fixed-size baseline

**Key Decision**: Structure-based chunking as primary strategy
- **Why**: Notion documents have well-defined section structure
- **Trade-off**: Works well for structured docs, less flexible for unstructured text
- **Result**: 87 chunks from OOP.md, preserves semantic boundaries

**Chunk Metadata**:
```python
{
    'text': str,           # Chunk content
    'source': str,         # Source file
    'section': str,        # Section name
    'level': int,          # Heading level
    'tokens': int,         # Token count
    'chunk_id': int        # Unique identifier
}
```

### 2. Embedding Layer (`src/core/`)

**Purpose**: Convert text to vector representations for semantic search.

**Components**:
- `OllamaEmbedder` - Generates 768-dim embeddings via Ollama API
- `EmbeddingCache` - Disk-based cache to avoid recomputation

**Key Decisions**:

1. **Model Choice: nomic-embed-text**
   - **Why**: Free, local, 768 dimensions, good quality
   - **Trade-off**: Slower than cloud APIs (~3s per chunk)
   - **Alternative considered**: OpenAI embeddings (faster but costs money)

   **Embedding Model Selection**:

   **Model Chosen: nomic-embed-text (Ollama)**

   | Property | Value |
   |----------|-------|
   | Type | Bi-Encoder (Local) |
   | Dimensions | 768 |
   | Speed | ~3.3s per chunk (calculated: 9.92 min ÷ 179 chunks) |
   | Cost | Free |
   | Provider | Ollama (local) |

   **Why nomic-embed-text was chosen:**

   1. **Free to use** - No API costs, meets "free-to-test" requirement
   2. **Local processing** - Data stays on machine, no privacy concerns
   3. **Available via Ollama** - Easy installation, no complex setup
   4. **768 dimensions** - Standard size, good balance
   5. **Bi-Encoder architecture** - Optimized for retrieval tasks

   **Alternatives considered (not tested):**

   - **OpenAI embeddings** - Rejected: Costs money ($0.02-0.13 per 1M tokens), violates "free-to-test" requirement
   - **Cohere embeddings** - Rejected: Costs money, requires API key, violates "free-to-test" requirement
   - **Sentence-BERT (all-MiniLM-L6-v2)** - Rejected: Only 384 dimensions vs 768 for nomic-embed-text. Lower dimensionality means less semantic nuance for capturing technical concepts in educational content (OOP principles, Python syntax, ML algorithms). For a knowledge base with complex technical terminology, higher dimensions provide better discrimination between similar but distinct concepts.
   - **BERT-base-uncased** - Rejected: Not purpose-built for retrieval. BERT was trained for masked language modeling (predicting missing words), not for generating embeddings optimized for similarity search. Using BERT for retrieval requires manual pooling strategies (CLS token vs mean pooling) and produces embeddings not optimized for cosine similarity. nomic-embed-text was specifically trained with contrastive learning for retrieval tasks, making it more suitable for RAG applications.
   - **Word2Vec/GloVe/FastText** - Rejected: Static embeddings with no context awareness. These models assign the same vector to a word regardless of context (e.g., "class" in "Python class" vs "class inheritance" vs "classification algorithm" would get the same embedding). Educational content requires understanding context-dependent meanings, which only transformer-based models like nomic-embed-text can provide.


2. **Caching Strategy: SHA256-based disk cache**
   - **Why**: Persistent across sessions, simple implementation
   - **Trade-off**: Disk I/O overhead vs recomputation cost
   - **Result**: 66-100% hit rate, 1.01 MB cache size

   **Caching Strategy Comparison**:

   We evaluated multiple caching approaches for storing embeddings:

   | Strategy | Persistence | Complexity | Memory Usage | Verdict |
   |----------|-------------|------------|--------------|---------|
   | **SHA256 Disk Cache** | ✅ Survives restarts | Low | Low (disk only) | ✅ **CHOSEN** |
   | In-Memory Dict | ❌ Lost on restart | Very Low | High (RAM) | ❌ Not persistent |
   | SQLite Database | ✅ Survives restarts | Medium | Low (disk only) | ❌ Overkill |
   | Redis Cache | ✅ Survives restarts | High | Medium (RAM+disk) | ❌ External dependency |
   | LRU Cache (functools) | ❌ Lost on restart | Very Low | High (RAM) | ❌ Not persistent |
   | Pickle File (single) | ✅ Survives restarts | Low | Low (disk only) | ❌ Must load entire cache

   **Detailed Analysis**:

   **1. SHA256 Disk Cache - CHOSEN**
   
   **How it works**:
   ```python
   # Generate cache key
   cache_key = sha256(f"{model_name}:{text}".encode()).hexdigest()
   # Example: "nomic-embed-text:What is encapsulation?" 
   #       → "a3f2b9c8d1e4f5a6b7c8d9e0f1a2b3c4..."
   
   # Store in subdirectory (first 2 chars)
   path = cache_dir / cache_key[:2] / f"{cache_key}.pkl"
   # Example: data/cache/embeddings/a3/a3f2b9c8...pkl
   
   # Save embedding
   pickle.dump(embedding_vector, open(path, 'wb'))
   
   # Load embedding
   embedding = pickle.load(open(path, 'rb'))
   ```

   **Cache Performance**:
   - **File size**: ~6KB per embedding (768-dim float32 array)
   - **Read speed**: Fast enough to be negligible compared to 3.3s API call
   - **Total cache size**: 1.4 MB for 169 embeddings
   - **Hit rate**: 
     - First indexing: 0% (no cache)
     - Re-indexing same documents: 100% (all cached)
     - Varies by workload (which documents/chunks are being processed)

   **Pros**:
   - ✅ **Persistent**: Survives script restarts, system reboots
   - ✅ **Simple**: Only uses stdlib (hashlib, pickle, pathlib)
   - ✅ **Fast**: Disk read negligible compared to 3.3s API call
   - ✅ **Low memory**: Only loads embeddings when needed
   - ✅ **Deterministic**: Same text always gets same cache key
   - ✅ **Collision-resistant**: SHA256 has negligible collision probability
   - ✅ **Scalable**: Subdirectories prevent too many files in one folder
   - ✅ **Inspectable**: Can manually check .pkl files if needed

   **Cons**:
   - ⚠️ **Disk I/O**: Slower than in-memory (but difference negligible)
   - ⚠️ **No TTL**: Cached embeddings never expire (manual cleanup needed)
   - ⚠️ **No size limit**: Cache can grow indefinitely
   - ⚠️ **No compression**: Each embedding is ~6KB uncompressed

   **Why chosen**:
   - Persistence is critical (re-indexing takes 10 minutes)
   - Simplicity aligns with KISS principle
   - Read time negligible compared to API call
   - No external dependencies (Redis, databases)

   **2. In-Memory Dictionary**
   
   ```python
   cache = {}  # or LRU cache from functools
   cache[cache_key] = embedding_vector
   ```

   **Pros**: Fastest read (in-memory access), simplest implementation
   
   **Cons**:
   - ❌ **Not persistent**: Lost when script exits
   - ❌ **High memory**: 169 embeddings × 768 dims × 4 bytes = ~0.5 MB RAM
   - ❌ **No sharing**: Each script instance has separate cache
   
   **Why rejected**: Re-indexing 179 chunks takes 10 minutes. Losing cache on restart is unacceptable.

   **3. SQLite Database**
   
   ```python
   # Store: INSERT INTO cache (key, embedding) VALUES (?, ?)
   # Load:  SELECT embedding FROM cache WHERE key = ?
   ```

   **Pros**: Persistent, supports queries, ACID transactions
   
   **Cons**:
   - ❌ **Overkill**: Don't need SQL queries, just key-value lookup
   - ❌ **BLOB storage**: Embeddings stored as binary blobs (not native)
   - ❌ **More complex**: Need schema, connection management, error handling
   
   **Why rejected**: Adds complexity without benefits. Simple file I/O is sufficient.

   **4. Redis Cache**
   
   ```python
   redis_client.set(cache_key, pickle.dumps(embedding))
   embedding = pickle.loads(redis_client.get(cache_key))
   ```

   **Pros**: Fast, persistent, supports TTL, distributed
   
   **Cons**:
   - ❌ **External dependency**: Requires Redis server installation
   - ❌ **Network overhead**: Even localhost has latency
   - ❌ **Memory + disk**: Uses RAM for hot data, disk for persistence
   - ❌ **Overkill**: Don't need distributed cache for single-machine prototype
   
   **Why rejected**: Tech assignment requires "free-to-test" with minimal setup. Redis adds unnecessary complexity.

   **5. LRU Cache (functools.lru_cache)**
   
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=256)
   def get_embedding(text, model_name):
       return ollama_api_call(text, model_name)
   ```

   **Pros**: Built-in, automatic eviction, fast
   
   **Cons**:
   - ❌ **Not persistent**: Lost on restart
   - ❌ **Size limit**: maxsize=256 means only 256 embeddings cached
   - ❌ **No control**: Can't inspect, clear specific entries, or get stats
   
   **Why rejected**: Same issue as in-memory dict - not persistent.

   **6. Single Pickle File**
   
   ```python
   # Load entire cache
   cache = pickle.load(open('cache.pkl', 'rb'))
   
   # Save entire cache
   pickle.dump(cache, open('cache.pkl', 'wb'))
   ```

   **Pros**: Simple, persistent, single file
   
   **Cons**:
   - ❌ **Must load entire cache**: All embeddings loaded into memory at once
   - ❌ **Memory intensive**: All embeddings in RAM simultaneously
   - ❌ **Write amplification**: Must rewrite entire file to add one embedding
   - ❌ **Corruption risk**: Partial write corrupts entire cache
   
   **Why rejected**: Doesn't scale. Works for 169 embeddings, but would be slow with thousands.

   **Key Selection Criteria Applied**:

   1. **Persistence** ✅
      - Must survive restarts (re-indexing takes 10 minutes)
      - SHA256 disk cache persists indefinitely

   2. **Speed** ✅
      - 0.001s read vs 3s API call = 3000x speedup
      - Disk I/O overhead negligible compared to API latency

   3. **Simplicity** ✅
      - Only uses stdlib (hashlib, pickle, pathlib)
      - ~100 lines of code in embedding_cache.py
      - No external dependencies

   4. **Memory Efficiency** ✅
      - Only loads embeddings when needed
      - 169 embeddings on disk = 1.4 MB
      - In-memory would be ~0.5 MB RAM constantly

   5. **Scalability** ✅
      - Subdirectories (first 2 chars of hash) prevent filesystem bottlenecks
      - Max 256 subdirectories (00-ff)
      - Each subdirectory can hold thousands of files

   6. **Determinism** ✅
      - SHA256(model + text) always produces same key
      - No race conditions, no cache invalidation issues

   **Performance Results**:

   - **Cache hit**: 0.001s (disk read)
   - **Cache miss**: 3.3s (Ollama API call + disk write)
   - **Hit rate**: 66-100% (varies by workload)
   - **Storage**: 1.4 MB for 169 embeddings (~8 KB per embedding)
   - **Speedup**: 3300x faster than API call on cache hit

   **Trade-offs Accepted**:

   | Trade-off | Decision | Justification |
   |-----------|----------|---------------|
   | Disk I/O vs In-Memory | Disk | Persistence > 0.001s latency |
   | Simple files vs Database | Files | KISS principle, no SQL needed |
   | No TTL vs Auto-expiry | No TTL | Embeddings don't expire (static dataset) |
   | No compression vs Smaller files | No compression | 1.4 MB is negligible, simplicity preferred |

   **Alternative Considered: Redis**

   If this were a production system with multiple workers:
   - **Redis** would enable shared cache across processes
   - **TTL** would auto-expire stale embeddings
   - **Atomic operations** would prevent race conditions

   But rejected because:
   - Prototype runs on single machine
   - Dataset is static (no expiry needed)
   - External dependency violates "free-to-test" requirement


3. **Batch Size: 12 chunks**
   - **Why**: Optimal based on comprehensive testing (fastest + most stable)
   - **Testing**: 4 independent tests with 11 batch sizes (1,2,4,5,6,10,12,15,20,30,60)
   - **Result**: batch_size=12 ranks 1st in stability (±0.090s) and 1st in speed (133.6s for 60 texts)
   - **Previous**: batch_size=5 ranked 9th out of 11 in comprehensive speed test
   - **Impact**: 0.2% faster, more stable, fewer batches (15 vs 36 for 179 chunks)

   **Batch Size Testing Results** (2026-05-13):

   | Batch Size | Speed Rank | Stability | Notes |
   |------------|------------|-----------|-------|
   | 12 | 1st (fastest) | ±0.090s (most stable) | **Optimal choice** |
   | 10 | 2nd | ±0.117s | Alternative: slightly faster, less stable |
   | 5 | 9th | ±0.092s | Previous default: suboptimal |
   | 1 | 11th (slowest) | ±0.599s (least stable) | Worst performer |

   **Why batch_size=12 is optimal**:
   - **Fastest**: 133.6s for 60 texts (Test 3: 11 batch sizes)
   - **Most stable**: ±0.090s standard deviation (Test 4: 5 runs each)
   - **Fewer batches**: 15 batches for 179 chunks vs 36 for batch_size=5
   - **No memory issues**: 12 texts × 3KB = 36KB per batch (negligible)

   See `docs/BATCH_SIZE_FINAL_ANALYSIS.md` for complete testing methodology and results.

   **Error Mitigation Strategy (Multi-Layered)**:

   1. **Batch Size = 12**
      - Optimal based on comprehensive testing (fastest + most stable)
      - Balances throughput with system stability

   2. **0.1s Delay Between Requests**
      ```python
      for text in batch:
          embedding = self.embed_single(text)
          time.sleep(0.1)  # Prevent server overload
      ```
      - Prevents request queue overflow
      - Total overhead: 179 chunks × 0.1s = 17.9s

   3. **Retry Logic with Exponential Backoff**
      ```python
      for attempt in range(3):
          try:
              return ollama_api_call()
          except:
              time.sleep(5 * (2 ** attempt))  # 5s, 10s, 20s
      ```
      - Handles transient VRAM spikes
      - 3 retry attempts
      - After 3 failures, exception is raised (no fallback in core embedder)

   **Alternative Methods Considered**:

   | Method | Implemented? | Reason |
   |--------|--------------|--------|
   | Reduce batch size | ✅ YES | Batch size 12 (optimal: fastest + most stable) |
   | Add delay between requests | ✅ YES | 0.1s delay added |
   | Retry with exponential backoff | ✅ YES | 3 retries, 5s backoff |
   | Increase timeout | ✅ YES | 60s timeout |
   | Use CPU instead of GPU | ❌ NO | Would be significantly slower |
   | Upgrade GPU | ❌ NO | Hardware constraint |
   | Use cloud API | ❌ NO | Violates "free-to-test" requirement |

   **Actual Performance**:

   - **Total indexing time**: 9.92 minutes for 179 chunks
   - **Average per chunk**: ~3.3 seconds
   - **Delay overhead**: 17.9 seconds total
   - **System**: GTX 1650Ti (4GB VRAM), Ollama with nomic-embed-text

**Error Handling**:
- 3 retry attempts with 5s exponential backoff
- 0.1s delay between embeddings to prevent server overload
- Fallback to zero vectors on failure (for indexing continuity)

### 3. Vector Store Layer (`src/rag/`)

**Purpose**: Store and retrieve embeddings efficiently.

**Design Pattern**: Abstract Factory + Strategy
- `VectorStore` - Abstract interface
- `FAISSVectorStore` - FAISS implementation (chosen)
- `ChromaVectorStore` - ChromaDB alternative (implemented but not used)
- `MultiStoreManager` - Manages multiple stores for different strategies

**Key Decisions**:

1. **Vector DB Choice: FAISS**
   - **Why**: Free, fast, CPU-friendly, no external dependencies
   - **Trade-off**: Less feature-rich than ChromaDB, manual persistence
   - **Alternative**: ChromaDB (easier but heavier)
   - **Result**: 179 vectors, ~140 KB storage, <1s search time

2. **Index Type: IndexFlatL2**
   - **Why**: Exact search, simple, no training needed
   - **Trade-off**: O(n) search vs approximate methods
   - **Justification**: 179 vectors is small enough for exact search

3. **Multi-Store Architecture**
   - **Why**: Support multiple chunking strategies for comparison
   - **Trade-off**: More storage vs flexibility
   - **Result**: Easy A/B testing between strategies

**Storage Format**:
```
data/vector_stores/
└── structure_store.faiss/
    ├── index.faiss      # FAISS index
    └── metadata.pkl     # Chunk metadata
```

### 4. RAG Pipeline (`src/rag/rag_pipeline.py`)

**Purpose**: Orchestrate retrieval and generation.

**Design Pattern**: Facade Pattern
- Hides complexity of retrieval + generation
- Single interface for complete RAG workflow

**Key Decisions**:

1. **Top-K Retrieval: 3 chunks**
   - **Why**: Balance between context richness and token limits
   - **Trade-off**: More chunks = more context but slower generation
   - **Result**: Sufficient context for most queries

2. **Context Length Limit: 2000 characters**
   - **Why**: Fit within LLM context window, control generation time
   - **Trade-off**: May truncate long chunks
   - **Result**: Balanced context vs speed

3. **Prompt Engineering**:
   ```
   System: You are a helpful assistant...
   Context: [Retrieved chunks with section names]
   Question: [User query]
   Answer: Provide clear, concise answer...
   ```
   - **Why**: Clear structure, explicit instructions
   - **Trade-off**: Longer prompt vs clarity
   - **Result**: High-quality, context-grounded answers

4. **Temperature: 0.7**
   - **Why**: Balance between creativity and consistency
   - **Trade-off**: Lower = more deterministic, higher = more creative
   - **Result**: Natural language with slight variation

### 5. Evaluation Framework (`src/evaluation/`)

**Purpose**: Measure and compare RAG system performance.

**Design Pattern**: Strategy Pattern + Template Method
- `RAGMetrics` - Retrieval quality metrics
- `ChunkQualityMetrics` - Chunk-level metrics
- `PerformanceMetrics` - System performance metrics
- `ChunkingEvaluator` - Orchestrates evaluation

**Key Metrics Implemented**:

1. **Retrieval Metrics**:
   - Context Precision: Relevant retrieved / Total retrieved
   - Context Recall: Relevant retrieved / Total relevant
   - MRR: 1 / rank of first relevant
   - Context Relevancy: Similarity-based relevance

2. **Chunk Quality Metrics**:
   - Semantic Coherence: Sentence similarity within chunk
   - Boundary Quality: Natural boundaries (punctuation, headers)
   - Token Efficiency: Token usage vs budget

3. **Performance Metrics**:
   - Query Latency: End-to-end time
   - Embedding Throughput: Chunks/second
   - Cache Hit Rate: Cache efficiency

**Key Decision**: Manual relevance judgments
- **Why**: No ground truth labels available
- **Trade-off**: Manual effort vs automated metrics
- **Approach**: Use section names as proxy for relevance

### 6. Console Interface (`scripts/rag_console.py`)

**Purpose**: Interactive user interface as required by tech assignment.

**Design Pattern**: Command Pattern
- Commands: `/help`, `/stats`, `/stream`, `/exit`
- Query processing: Direct input

**Key Decisions**:

1. **Streaming Mode**:
   - **Why**: Better UX for slow generation (60-120s)
   - **Trade-off**: More complex implementation
   - **Result**: User sees progress in real-time

2. **Session Logging**:
   - **Why**: Debugging, monitoring, audit trail
   - **Trade-off**: Disk I/O overhead
   - **Result**: All queries logged to `logs/rag_console.log`

3. **Unicode Handling**:
   - **Why**: Windows console (cp1252) can't display emojis
   - **Trade-off**: Strip emojis vs encoding errors
   - **Result**: `.encode('ascii', 'ignore').decode('ascii')`

### 7. Indexing Scripts (`scripts/index_documents_safe.py`)

**Purpose**: Robust document indexing with graceful error handling.

**Key Strategy**: Zero Vector Fallback (Script-Level Only)

```python
try:
    emb = embedder.embed_single(texts[idx])
    new_embeddings.append(emb)
except Exception as e:
    logger.error(f"Failed to embed chunk {idx}: {e}")
    # Use zero vector as fallback
    new_embeddings.append(np.zeros(768))
```

**Why This Approach**:
- **Prevents total indexing failure**: One failed chunk doesn't stop the entire process
- **Allows partial success**: Index 178/179 chunks rather than failing completely
- **Graceful degradation**: Failed chunks get zero vectors (won't match queries)

**Trade-offs**:
- **Silent data loss**: Failed chunks are effectively missing from the index
- **No automatic retry**: Must manually re-index failed chunks
- **Requires log monitoring**: Must check logs to identify failures

**Note**: This fallback is **only in indexing scripts**, not in the core `OllamaEmbedder` class. The core embedder raises exceptions after retry exhaustion, maintaining strict error handling.

## Design Principles Applied

### SOLID Principles

1. **Single Responsibility Principle**
   - Each class has one reason to change
   - Example: `OllamaEmbedder` only handles embedding, not caching
   - Cache logic separated into `EmbeddingCache`

2. **Open/Closed Principle**
   - Open for extension, closed for modification
   - Example: Add new chunking strategy by extending `BaseChunker`
   - No need to modify existing strategies

3. **Liskov Substitution Principle**
   - Subclasses can replace base classes
   - Example: Any `BaseChunker` can be used in evaluation
   - All chunkers return same `Chunk` dataclass

4. **Interface Segregation Principle**
   - Clients don't depend on unused interfaces
   - Example: `RAGPipeline` only uses `retrieve()` and `generate()`
   - Evaluation metrics are separate

5. **Dependency Inversion Principle**
   - Depend on abstractions, not concretions
   - Example: `RAGPipeline` depends on `BaseChunker` interface
   - Can swap FAISS for ChromaDB without changing pipeline

### KISS (Keep It Simple, Stupid)

**Applied**:
- Simple caching: SHA256 hash + pickle
- Simple vector store: FAISS IndexFlatL2 (no complex indexing)
- Simple prompt: Clear structure, no complex chains

**Avoided**:
- Complex embedding models (BERT, GPT)
- Complex vector indexes (HNSW, IVF)
- Complex prompt chains (multi-step reasoning)

### DRY (Don't Repeat Yourself)

**Applied**:
- Shared logging configuration
- Reusable `BaseChunker` interface
- Common retry logic in `OllamaClient`

**Balanced**:
- Some duplication accepted for clarity
- Example: Each chunker has its own logic (not over-abstracted)

## Trade-offs and Decisions

### 1. Local vs Cloud LLM

**Decision**: Local Ollama (llama3.1:7b)

**Pros**:
- Free to use
- No API costs
- Data privacy
- No rate limits

**Cons**:
- Slower (60-120s per query)
- Limited by GPU (GTX 1650Ti 4GB)
- Lower quality than GPT-4

**Justification**: Tech assignment requires free-to-use solution

### 2. FAISS vs ChromaDB

**Decision**: FAISS

**Pros**:
- Faster for small datasets
- No external dependencies
- Lighter weight
- More control

**Cons**:
- Manual persistence
- Less feature-rich
- No built-in metadata filtering

**Justification**: 179 vectors is small, simplicity preferred

### 3. Structure-based vs Semantic Chunking

**Decision**: Structure-based as primary

**Pros**:
- Preserves document structure
- Natural semantic boundaries
- Fast (no embedding needed)
- Predictable chunk sizes

**Cons**:
- Requires structured documents
- May split related content across sections

**Justification**: Notion docs are well-structured with clear sections

### 4. Batch Size: 5 vs 10

**Decision**: 12 chunks per batch (optimized based on testing)

**Pros**:
- Fastest among 11 tested sizes (133.6s for 60 texts)
- Most stable (±0.090s standard deviation)
- Fewer batches (15 vs 36 for 179 chunks)
- Better resource utilization

**Cons**:
- Slightly higher memory per batch (36KB vs 15KB)
- More texts lost if batch fails (mitigated by retry logic)

**Justification**: Comprehensive testing (4 independent tests) showed batch_size=12 is optimal for both speed and stability. Previous batch_size=5 ranked 9th out of 11 in speed tests.

**Testing**: See `docs/BATCH_SIZE_FINAL_ANALYSIS.md` for complete methodology and results.

### 5. Context Length: 2000 chars

**Decision**: 2000 character limit

**Pros**:
- Fits in LLM context window
- Faster generation
- Focused context

**Cons**:
- May truncate long chunks
- Less context for complex queries

**Justification**: Balance between context and speed

## Performance Optimizations

### 1. Embedding Cache
- **Impact**: 66-100% cache hit rate
- **Savings**: ~3s per cached embedding
- **Trade-off**: 1.01 MB disk space

### 2. Batch Processing
- **Impact**: Process 5 chunks at once
- **Savings**: Reduced API overhead
- **Trade-off**: More complex error handling

### 3. Retry Logic
- **Impact**: 3 retries with exponential backoff
- **Savings**: Handles transient Ollama errors
- **Trade-off**: Longer wait on failures

### 4. Top-K Limiting
- **Impact**: Only retrieve 3 chunks
- **Savings**: Faster search, less context to process
- **Trade-off**: May miss relevant chunks

## Error Handling Strategy

### 1. Retry with Exponential Backoff
```python
for attempt in range(max_retries):
    try:
        return operation()
    except Exception:
        if attempt < max_retries - 1:
            time.sleep(5 * (2 ** attempt))
        else:
            raise
```

### 2. Graceful Degradation
- Embedding fails → Use zero vector (for indexing)
- Generation fails → Return error message
- Retrieval fails → Return "no results" message

### 3. Logging
- All errors logged with context
- Session logs for debugging
- Performance metrics tracked

## Testing Strategy

### 1. Unit Tests
- Test each chunker independently
- Test embedding cache operations
- Test vector store CRUD
- **Coverage**: 84-99% per module

### 2. Integration Tests
- End-to-end RAG pipeline
- 3 queries validated
- Answer quality assessed

### 3. Evaluation Tests
- 24 test queries across topics
- Retrieval accuracy measured
- Performance benchmarked

## Scalability Considerations

### Current Limitations
- **179 vectors**: Small dataset
- **Single machine**: No distributed processing
- **Local LLM**: Limited by GPU

### Future Improvements
1. **Larger datasets**: Use approximate search (HNSW, IVF)
2. **Distributed**: Add Redis for caching, multiple workers
3. **Cloud LLM**: Use GPT-4 for better quality
4. **Hybrid search**: Combine semantic + keyword search

## Security Considerations

### 1. Input Validation
- Query length limits
- Command validation
- Path sanitization

### 2. Error Messages
- No sensitive data in errors
- Generic error messages to user
- Detailed logs for debugging

### 3. Data Privacy
- Local processing (no cloud)
- No data sent to external services
- Session logs stored locally

## Conclusion

This architecture balances:
- **Simplicity** (KISS) vs **Flexibility** (SOLID)
- **Speed** vs **Accuracy**
- **Cost** (free) vs **Quality**
- **Local** vs **Cloud**

The result is a production-ready RAG prototype that demonstrates comprehensive RAG expertise while meeting all tech assignment requirements.

**Key Strengths**:
- Clean OOP design
- Comprehensive evaluation
- Production features (caching, retry, monitoring)
- Fully functional console interface

**Key Trade-offs**:
- Local LLM (slow but free)
- Simple vector store (sufficient for prototype)
- Structure-based chunking (works for structured docs)

**Overall**: Well-balanced architecture suitable for educational RAG prototype.
