# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA for GPU acceleration with FAISS

## Installation Steps

### 1. Clone and Navigate

```bash
cd RAG-Pipeline
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional Configuration
LOG_LEVEL=INFO
CACHE_ENABLED=true
```

### 6. Configure Models

Edit `config/model_config.yaml` to set your preferred models and parameters.

### 7. Create Data Directories

```bash
mkdir -p data/cache data/embeddings data/vectordb logs
```

## Optional: GPU Support

For FAISS with GPU acceleration:

```bash
pip uninstall faiss-cpu
pip install faiss-gpu
```

## Verify Installation

```python
from src.core.model_factory import ModelFactory

factory = ModelFactory()
llm = factory.create_default_model()
print("Setup successful!")
```

## Troubleshooting

### Import Errors

Ensure you're in the project root and the virtual environment is activated.

### API Key Errors

Verify your `.env` file exists and contains valid API keys.

### FAISS Installation Issues

Try installing the CPU version first:
```bash
pip install faiss-cpu
```

## Next Steps

- Index your documents: `python scripts/build_embeddings.py --input-dir /path/to/docs`
- Run tests: `./scripts/run_tests.sh`
- See `docs/README.md` for usage examples
