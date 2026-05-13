# RAG Pipeline

A production-ready Retrieval-Augmented Generation (RAG) pipeline supporting multiple LLM providers (OpenAI, Anthropic Claude, local models) with flexible vector storage backends.

## Features

- **Multi-Provider LLM Support**: OpenAI GPT, Anthropic Claude, and local models
- **Flexible Vector Stores**: FAISS and ChromaDB implementations
- **Document Processing**: Chunking, tokenization, and preprocessing utilities
- **RAG Pipeline**: Complete retrieval and generation workflow
- **Prompt Management**: Reusable templates and multi-step chaining
- **Configurable**: YAML-based configuration for models and parameters

## Quick Start

### Installation

```bash
# Run setup script
./scripts/setup_env.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env` and add your API keys:
```bash
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

2. Adjust model settings in `config/model_config.yaml`

### Basic Usage

```python
from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore
from src.rag.retriever import Retriever
from src.inference.inference_engine import InferenceEngine

# Initialize components
factory = ModelFactory()
llm = factory.create_default_model()
embedder = Embedder(llm)
vector_store = FAISSVectorStore(dimension=1536)
retriever = Retriever(vector_store, embedder)

# Create inference engine
engine = InferenceEngine(llm, retriever)

# Query with RAG
response = engine.query("What is machine learning?", use_rag=True)
print(response)
```

## Project Structure

- `src/core/`: LLM client implementations and factory
- `src/rag/`: RAG components (embedder, retriever, vector store, indexer)
- `src/prompts/`: Prompt templates and chaining
- `src/processing/`: Text processing utilities
- `src/inference/`: Inference engine and response parsing
- `config/`: Configuration files
- `scripts/`: Utility scripts for setup, testing, and maintenance

## Building Embeddings

Index your documents:

```bash
python scripts/build_embeddings.py \
    --input-dir /path/to/documents \
    --output-dir data/vectordb \
    --vector-store faiss
```

## Testing

```bash
./scripts/run_tests.sh
```

## License

MIT
