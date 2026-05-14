# RAG Pipeline - Quick Start Guide

## Running the RAG Console

### Prerequisites
1. Ollama installed and running
2. Models installed: `nomic-embed-text:latest` and `llama3.1:latest`
3. Documents indexed (179 vectors in vector store)

### Starting the Console

**From the project root directory:**
```bash
cd C:\Users\YVV\PycharmProjects\Practice\RAG-Pipeline
python scripts/rag_console.py
```

**Or using the virtual environment:**
```bash
.venv\Scripts\python.exe scripts\rag_console.py
```

### Using the Console

Once started, you'll see:
```
============================================================
RAG PIPELINE - Educational Knowledge Base
============================================================

Topics: Python, OOP, Machine Learning, Database Optimization

Commands:
  - Type your question and press Enter
  - '/help' - Show help
  - '/stats' - Show statistics
  - '/stream' - Toggle streaming mode
  - '/exit' or '/quit' - Exit

============================================================

[NORMAL] > 
```

### Example Queries

**OOP Questions:**
```
> What is encapsulation?
> How does inheritance work?
> What are the SOLID principles?
> What is better to use instead of inheritance?
```

**Python Questions:**
```
> What are Python decorators?
> How do list comprehensions work?
> What is the difference between args and kwargs?
> How to use context managers?
```

**Database Questions:**
```
> What is database indexing?
> How does query optimization work?
> What are best practices for normalization?
```

**Machine Learning Questions:**
```
> What is machine learning?
> What is data leakage?
> Explain loss functions
```

### Commands

- **`/help`** - Show detailed help
- **`/stats`** - Show system statistics (vector count, models, etc.)
- **`/stream`** - Toggle streaming mode (see answer as it's generated)
- **`/exit`** or **`/quit`** - Exit the program

### Expected Performance

- **Retrieval**: Min: 4.19s, Max: 6.00s (2 queries measured)
- **Generation**: Min: 30.84s, Max: 68.48s (2 queries measured)
- **Total**: Min: 35.03s, Max: 74.48s per query (2 queries measured)
- **Note**: Performance varies by query complexity and answer length

### Troubleshooting

**Error: "Store not found"**
- Make sure you're in the project root directory
- Check that `data/vector_stores/structure_store.faiss/` exists
- Re-run indexing if needed: `python scripts/index_documents_safe.py`

**Error: "Ollama connection failed"**
- Make sure Ollama is running
- Verify models are installed: `ollama list`
- Test connection: `python scripts/verify_ollama.py`

**Slow generation**
- This is normal for local 8B model on GTX 1650Ti
- Generation takes 30-70 seconds per query (measured)
- Use `/stream` mode to see progress

### Session Logs

All queries are logged to: `logs/rag_console.log`

### Example Session

```
[NORMAL] > What is encapsulation?

------------------------------------------------------------
ANSWER:
------------------------------------------------------------
According to the provided context, Encapsulation is:

"The idea and mechanism of building the data (attributes) and 
methods (functions) that operate on the data into a single unit, 
called an object."

In other words, encapsulation is a design principle that bundles 
data and methods that manipulate that data within a single object...

[Full answer with code example]

------------------------------------------------------------
SOURCES:
------------------------------------------------------------

[1] Section: Encapsulation
    Relevance score: 344.06

[2] Section: **Protected Variations**
    Relevance score: 383.00

[3] Section: **The Single Responsibility Principle**
    Relevance score: 387.34

------------------------------------------------------------
Query time: 92.60s
------------------------------------------------------------

[NORMAL] > /stats

============================================================
SYSTEM STATISTICS
============================================================

Vector Store: structure
  Total vectors: 179
  Dimension: 768
  Top-K retrieval: 3
  Max context length: 2000 chars

Models:
  Embedder: nomic-embed-text:latest
  Generator: llama3.1:latest

============================================================

[NORMAL] > /exit

Goodbye!
Total queries processed: 1
```

## Alternative: Non-Interactive Testing

If you want to test without the console:
```bash
python scripts/test_rag_pipeline.py
```

This will run 3 predefined queries and show the results.

## Re-indexing Documents

If you need to re-index the documents:
```bash
python scripts/index_documents_safe.py
```

This will take about 10 minutes to complete.
