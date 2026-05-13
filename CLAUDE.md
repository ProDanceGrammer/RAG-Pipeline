# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a production-ready RAG (Retrieval-Augmented Generation) pipeline supporting multiple LLM providers (OpenAI GPT, Anthropic Claude, local models) with flexible vector storage backends (FAISS, ChromaDB).

## Architecture

### Core Components

- **LLM Clients** (`src/core/`): Abstract base class with provider-specific implementations
  - `BaseLLM`: Abstract interface defining `generate()`, `generate_stream()`, and `embed()` methods
  - `GPTClient`: OpenAI implementation using the `openai` SDK
  - `ClaudeClient`: Anthropic implementation using the `anthropic` SDK
  - `LocalLLM`: Stub for local/self-hosted models (llama.cpp, vLLM, Ollama)
  - `ModelFactory`: Creates LLM instances from YAML config

- **RAG Pipeline** (`src/rag/`):
  - `Embedder`: Generates vector embeddings with batching support
  - `VectorStore`: Abstract interface with FAISS and ChromaDB implementations
  - `Retriever`: Performs similarity search and formats context
  - `DocumentIndexer`: Chunks and indexes documents into vector stores

- **Processing** (`src/processing/`):
  - `TextChunker`: Splits text by tokens, sentences, or paragraphs with overlap
  - `Tokenizer`: Simple tokenization and token counting
  - `TextPreprocessor`: Cleaning, normalization, URL/email removal

- **Inference** (`src/inference/`):
  - `InferenceEngine`: Orchestrates RAG queries, summarization, extraction, classification
  - `ResponseParser`: Extracts JSON, lists, code blocks from LLM responses

- **Prompts** (`src/prompts/`):
  - `PromptTemplate`: Reusable templates for RAG, summarization, extraction, classification
  - `PromptChain`: Multi-step prompt chaining with intermediate transformations

## Development Commands

### Environment Setup
```bash
# Automated setup
./scripts/setup_env.sh

# Manual setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Testing
```bash
# Run all tests with coverage
./scripts/run_tests.sh

# Run specific test file
pytest tests/test_embedder.py -v

# Run with specific marker
pytest -m unit -v
```

### Building Embeddings
```bash
# Index documents into vector store
python scripts/build_embeddings.py \
    --input-dir /path/to/documents \
    --output-dir data/vectordb \
    --vector-store faiss  # or chroma
```

### Cleanup
```bash
# Clean all temporary files
python scripts/cleanup.py --target all

# Clean specific target
python scripts/cleanup.py --target cache
```

### Docker
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f rag-pipeline
```

## Configuration

- **Model Config** (`config/model_config.yaml`): LLM providers, models, parameters, embedding settings, RAG parameters
- **Logging Config** (`config/logging_config.yaml`): Log levels, formatters, handlers
- **Environment Variables** (`.env`): API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), log level, cache settings

## Key Patterns

### Adding a New LLM Provider

1. Create new client in `src/core/` inheriting from `BaseLLM`
2. Implement `generate()`, `generate_stream()`, and `embed()` methods
3. Register in `ModelFactory._providers` dict
4. Add configuration to `config/model_config.yaml`

### Adding a New Vector Store

1. Create new class in `src/rag/vector_store.py` inheriting from `VectorStore`
2. Implement `add()`, `search()`, `save()`, and `load()` methods
3. Update `DocumentIndexer` to support the new store type

### Creating Custom Prompts

Use `PromptTemplate` for single-step prompts or `PromptChain` for multi-step workflows:

```python
from src.prompts.chain import PromptChain

chain = PromptChain(llm)
chain.add_step("extract", "Extract key points from: {input}")
chain.add_step("summarize", "Summarize these points: {input}")
result = chain.execute(document_text)
```

## Testing Strategy

- Unit tests for individual components (embedder, chunker, preprocessor)
- Integration tests for RAG pipeline end-to-end
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`
- Mock LLM calls in tests to avoid API costs
- Use `@pytest.mark.requires_api` for tests needing real API keys

## Dependencies

- Core: `openai`, `anthropic`, `pyyaml`, `numpy`
- Vector stores: `faiss-cpu` (or `faiss-gpu`), `chromadb`
- Text processing: `tiktoken`
- Testing: `pytest`, `pytest-cov`, `pytest-asyncio`

## Common Issues

- **Import errors**: Ensure virtual environment is activated and you're in project root
- **API key errors**: Check `.env` file exists with valid keys
- **FAISS installation**: Use `faiss-cpu` for CPU-only systems, `faiss-gpu` for CUDA support
- **ChromaDB persistence**: Ensure `data/vectordb` directory exists and has write permissions
