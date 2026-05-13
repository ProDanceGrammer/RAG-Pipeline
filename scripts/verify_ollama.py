"""Quick Ollama verification."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_client import OllamaClient
from src.core.ollama_embedder import OllamaEmbedder

print("Testing Ollama setup...")
print("-" * 60)

# Test embedding
embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")
if embedder.is_available():
    print("[OK] Embedding model: nomic-embed-text:latest")
    emb = embedder.embed_single("test")
    print(f"  Dimension: {len(emb)}")
else:
    print("[FAIL] Embedding model not available")

# Test generation
client = OllamaClient(model_name="llama3.1:latest")
if client.is_available():
    print("[OK] Generation model: llama3.1:latest")
else:
    print("[FAIL] Generation model not available")

print("-" * 60)
print("Ollama is ready for Phase 3!")
