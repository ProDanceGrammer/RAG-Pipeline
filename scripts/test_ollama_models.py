"""Test Ollama models after installation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ollama_client import OllamaClient
from src.core.ollama_embedder import OllamaEmbedder
import time


def test_ollama_connection():
    """Test basic Ollama connection."""
    print("="*60)
    print("Testing Ollama Connection")
    print("="*60)

    client = OllamaClient()
    models = client.list_models()

    print(f"\nInstalled models: {len(models)}")
    for model in models:
        print(f"  - {model}")

    return len(models) > 0


def test_embedding_model():
    """Test embedding model."""
    print("\n" + "="*60)
    print("Testing Embedding Model")
    print("="*60)

    embedder = OllamaEmbedder(model_name="nomic-embed-text:latest")

    # Check availability
    if not embedder.is_available():
        print("\nERROR: nomic-embed-text:latest not found!")
        print("Please run: ollama pull nomic-embed-text")
        return False

    print("\nModel: nomic-embed-text:latest")
    print("Status: Available")

    # Test embedding
    print("\nTesting embedding generation...")
    test_text = "This is a test sentence for embedding."

    start_time = time.time()
    embedding = embedder.embed_single(test_text)
    elapsed = time.time() - start_time

    print(f"  Text: {test_text}")
    print(f"  Embedding dimension: {len(embedding)}")
    print(f"  Time: {elapsed:.2f} seconds")
    print(f"  First 5 values: {embedding[:5]}")

    # Test batch embedding
    print("\nTesting batch embedding...")
    test_texts = [
        "Machine learning is a subset of AI.",
        "Python is a programming language.",
        "Object-oriented programming uses classes."
    ]

    start_time = time.time()
    embeddings = embedder.embed_texts(test_texts)
    elapsed = time.time() - start_time

    print(f"  Texts: {len(test_texts)}")
    print(f"  Embeddings shape: {embeddings.shape}")
    print(f"  Time: {elapsed:.2f} seconds")
    print(f"  Avg time per text: {elapsed/len(test_texts):.2f} seconds")

    # Test similarity
    print("\nTesting similarity...")
    sim = embedder.cosine_similarity(embeddings[0], embeddings[1])
    print(f"  Similarity (ML vs Python): {sim:.4f}")

    return True


def test_generation_model():
    """Test generation model."""
    print("\n" + "="*60)
    print("Testing Generation Model")
    print("="*60)

    client = OllamaClient(model_name="llama3.1:latest")

    # Check availability
    if not client.is_available():
        print("\nERROR: llama3.1:latest not found!")
        print("Please run: ollama pull llama3.1")
        return False

    print("\nModel: llama3.1:latest")
    print("Status: Available")

    # Test generation
    print("\nTesting text generation...")
    prompt = "What is object-oriented programming? Answer in one sentence."

    print(f"  Prompt: {prompt}")
    print("  Generating...")

    start_time = time.time()
    response = client.generate(prompt, max_tokens=100, temperature=0.7)
    elapsed = time.time() - start_time

    print(f"\n  Response: {response}")
    print(f"\n  Time: {elapsed:.2f} seconds")
    print(f"  Tokens/sec: ~{len(response.split()) / elapsed:.2f}")

    return True


def test_streaming():
    """Test streaming generation."""
    print("\n" + "="*60)
    print("Testing Streaming Generation")
    print("="*60)

    client = OllamaClient(model_name="llama3.1:latest")

    if not client.is_available():
        print("\nSkipping (model not available)")
        return False

    prompt = "List 3 benefits of Python programming."
    print(f"\nPrompt: {prompt}")
    print("Streaming response: ", end="", flush=True)

    start_time = time.time()
    full_response = ""

    for chunk in client.generate_stream(prompt, max_tokens=100):
        print(chunk, end="", flush=True)
        full_response += chunk

    elapsed = time.time() - start_time

    print(f"\n\nTime: {elapsed:.2f} seconds")

    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("OLLAMA MODEL TESTING")
    print("="*60)

    # Test connection
    if not test_ollama_connection():
        print("\nERROR: No models installed!")
        print("\nPlease install models:")
        print("  ollama pull nomic-embed-text")
        print("  ollama pull llama3.1:7b")
        return

    # Test embedding
    embedding_ok = test_embedding_model()

    # Test generation
    generation_ok = test_generation_model()

    # Test streaming
    if generation_ok:
        test_streaming()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Embedding model: {'OK' if embedding_ok else 'FAILED'}")
    print(f"Generation model: {'OK' if generation_ok else 'FAILED'}")

    if embedding_ok and generation_ok:
        print("\nAll tests passed! Ready for Phase 3.")
    else:
        print("\nSome tests failed. Please install missing models.")

    print("="*60)


if __name__ == "__main__":
    main()
