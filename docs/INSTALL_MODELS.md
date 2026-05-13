# Ollama Model Installation Guide

## Current Status
✓ Ollama is installed and running
✗ No models installed yet

## Required Models

### 1. Embedding Model (Choose one)

**Option A: nomic-embed-text (RECOMMENDED)**
- Size: ~274 MB
- Best for: General text embeddings
- Speed: Fast on GTX 1650Ti

```powershell
ollama pull nomic-embed-text
```

**Option B: mxbai-embed-large**
- Size: ~669 MB
- Best for: Higher quality embeddings
- Speed: Slower but more accurate

```powershell
ollama pull mxbai-embed-large
```

### 2. Generation Model (Choose one)

**Option A: llama3.1:7b (RECOMMENDED)**
- Size: ~4.7 GB
- Best for: Quality/speed balance
- Will use most of your 4GB VRAM

```powershell
ollama pull llama3.1:7b
```

**Option B: llama3.2:3b (If VRAM issues)**
- Size: ~2 GB
- Best for: Faster, lighter
- Use if 7B model is too slow

```powershell
ollama pull llama3.2:3b
```

**Option C: mistral:7b (Alternative)**
- Size: ~4.1 GB
- Best for: Alternative to llama3.1

```powershell
ollama pull mistral:7b
```

## Installation Steps

Open PowerShell and run:

```powershell
# Step 1: Pull embedding model (REQUIRED)
ollama pull nomic-embed-text

# Step 2: Pull generation model (REQUIRED)
ollama pull llama3.1:7b

# Step 3: Test the models
ollama run llama3.1:7b "Hello, test message"
```

## Expected Download Times
- nomic-embed-text: ~1-2 minutes
- llama3.1:7b: ~5-10 minutes (depending on internet speed)

## After Installation

Run this to verify:
```bash
python -c "import requests; print(requests.get('http://localhost:11434/api/tags').json())"
```

You should see both models listed.

## Next Steps

Once models are installed, we'll proceed with:
1. Testing embedding performance
2. Testing generation performance
3. Implementing Ollama adapter for RAG pipeline
