# Next Steps: Install Ollama Models

## Current Status
✅ Ollama installed and running
✅ Ollama adapter code ready
⏳ Waiting for models to be installed

## What You Need to Do Now

Open **PowerShell** and run these commands:

### Step 1: Install Embedding Model (~1-2 minutes)
```powershell
ollama pull nomic-embed-text
```
Expected output:
```
pulling manifest
pulling 970aa74c0a90... 100%
...
success
```

### Step 2: Install Generation Model (~5-10 minutes)
```powershell
ollama pull llama3.1:7b
```
Expected output:
```
pulling manifest
pulling 8eeb52dfb3bb... 100%
...
success
```

### Step 3: Verify Installation
```bash
python scripts/test_ollama_models.py
```

This will test:
- Embedding generation (nomic-embed-text)
- Text generation (llama3.1:7b)
- Streaming responses
- Performance metrics on your GTX 1650Ti

## What to Expect

### Embedding Model (nomic-embed-text)
- Download size: ~274 MB
- Embedding dimension: 768
- Speed: ~1-2 seconds per document
- VRAM usage: ~500 MB

### Generation Model (llama3.1:7b)
- Download size: ~4.7 GB
- Speed: ~10-30 seconds per query
- Tokens/sec: ~5-15 on GTX 1650Ti
- VRAM usage: ~4 GB (will use most of your VRAM)

## After Models Are Installed

I'll continue with Phase 3:
1. ✅ Ollama client (done)
2. ✅ Ollama embedder (done)
3. ⏳ Multi-vector store manager
4. ⏳ Embedding cache system
5. ⏳ Index all 4 documents
6. ⏳ Test retrieval performance

## Troubleshooting

**If download is slow:**
- Models are large (especially llama3.1:7b at 4.7 GB)
- Be patient, it's a one-time download

**If you get VRAM errors:**
- Use smaller model: `ollama pull llama3.2:3b` instead
- Close other GPU applications

**If Ollama stops responding:**
- Restart Ollama service
- Check Task Manager for ollama.exe

## Ready?

Once you've run the `ollama pull` commands, let me know and I'll test the models and continue with Phase 3!
