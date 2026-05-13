"""Test Ollama installation and performance."""
import requests
import time
import json
from typing import Dict, Any


def test_ollama_connection() -> bool:
    """Test if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def test_embedding_model(model: str = "nomic-embed-text") -> Dict[str, Any]:
    """Test embedding model performance."""
    print(f"\nTesting embedding model: {model}")

    test_text = "This is a test sentence for embedding."

    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model, "prompt": test_text},
            timeout=30
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            embedding = data.get("embedding", [])
            return {
                "success": True,
                "model": model,
                "embedding_dim": len(embedding),
                "time_seconds": round(elapsed, 2),
                "tokens_per_second": round(len(test_text.split()) / elapsed, 2)
            }
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def test_generation_model(model: str = "llama3.1:7b") -> Dict[str, Any]:
    """Test generation model performance."""
    print(f"\nTesting generation model: {model}")

    test_prompt = "What is object-oriented programming? Answer in one sentence."

    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": test_prompt, "stream": False},
            timeout=60
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            generated_text = data.get("response", "")
            return {
                "success": True,
                "model": model,
                "response": generated_text[:100] + "..." if len(generated_text) > 100 else generated_text,
                "time_seconds": round(elapsed, 2),
                "response_length": len(generated_text)
            }
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """Run all Ollama tests."""
    print("="*60)
    print("Ollama Installation Test")
    print("="*60)

    # Test connection
    print("\n1. Testing Ollama connection...")
    if test_ollama_connection():
        print("✓ Ollama is running")
    else:
        print("✗ Ollama is not running or not installed")
        print("\nPlease install Ollama from: https://ollama.com/download")
        print("Then run: ollama serve")
        return

    # Test embedding models
    print("\n2. Testing embedding models...")
    embedding_models = ["nomic-embed-text", "mxbai-embed-large"]

    for model in embedding_models:
        result = test_embedding_model(model)
        if result["success"]:
            print(f"✓ {model}")
            print(f"  - Dimension: {result['embedding_dim']}")
            print(f"  - Time: {result['time_seconds']}s")
        else:
            print(f"✗ {model}: {result.get('error', 'Unknown error')}")
            print(f"  Run: ollama pull {model}")

    # Test generation models
    print("\n3. Testing generation models...")
    generation_models = ["llama3.1:7b", "llama3.2:3b", "mistral:7b"]

    for model in generation_models:
        result = test_generation_model(model)
        if result["success"]:
            print(f"✓ {model}")
            print(f"  - Time: {result['time_seconds']}s")
            print(f"  - Response: {result['response']}")
        else:
            print(f"✗ {model}: {result.get('error', 'Unknown error')}")
            print(f"  Run: ollama pull {model}")

    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)


if __name__ == "__main__":
    main()
