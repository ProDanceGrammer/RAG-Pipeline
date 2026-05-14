# Ollama Installation Guide

## Installation Steps

### Windows Installation
1. Download Ollama from: https://ollama.com/download/windows
2. Run the installer (OllamaSetup.exe)
3. Ollama will install and start automatically

### Verify Installation
```bash
ollama --version
```

### Pull Required Models

**For Embeddings (choose one):**
```bash
# Option 1: Smaller, faster (recommended for GTX 1650Ti)
ollama pull nomic-embed-text

# Option 2: Alternative
ollama pull mxbai-embed-large
```

**For Generation (choose one):**
```bash
# Option 1: Llama 3.1 7B (recommended)
ollama pull llama3.1:7b

# Option 2: Mistral 7B (alternative)
ollama pull mistral:7b

# Option 3: Smaller if VRAM issues
ollama pull llama3.2:3b
```

### Test Ollama
```bash
# Test generation
ollama run llama3.1:7b "Hello, how are you?"

# Test embedding (via Python)
python -c "import requests; print(requests.post('http://localhost:11434/api/embeddings', json={'model': 'nomic-embed-text', 'prompt': 'test'}).json())"
```

## Expected Performance on GTX 1650Ti (4GB VRAM) + 16GB RAM

**Note**: These are estimates based on typical hardware performance, not measured values.

### Embedding (nomic-embed-text)
- Model size: ~274MB
- VRAM usage: ~500MB (estimated)
- Speed: ~1-2 seconds per document (estimated)
- Batch size: 10-20 documents (estimated)

### Generation (llama3.1:8b)
- Model size: ~4.7GB
- VRAM usage: ~4GB (will use full VRAM)
- Speed: Measured 30-68 seconds per query (2 queries)
- Tokens/sec: ~5-15 tokens/sec (estimated)

### Tips for GTX 1650Ti
- Use `nomic-embed-text` for embeddings (lightweight)
- Use `llama3.1:7b` for generation (good quality/speed balance)
- If VRAM issues occur, use `llama3.2:3b` instead
- Close other GPU applications during use
- Consider CPU fallback for embeddings if needed

## Next Steps
After installation, run:
```bash
python scripts/test_ollama.py
```
