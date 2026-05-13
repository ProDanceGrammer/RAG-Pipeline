"""Demo script to test chunking strategies on real documents."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chunking import (
    StructureChunker,
    HierarchicalChunker,
    SlidingWindowChunker,
    SemanticChunker
)
import json


def load_document(file_path: Path) -> dict:
    """Load a markdown document."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return {
        'text': text,
        'source': file_path.name
    }


def test_chunking_strategy(chunker, document, strategy_name):
    """Test a chunking strategy on a document."""
    print(f"\n{'='*70}")
    print(f"Testing: {strategy_name}")
    print(f"Document: {document['source']}")
    print(f"{'='*70}")

    chunks = chunker.chunk(document['text'], document['source'])
    stats = chunker.get_stats(chunks)

    print(f"\nStatistics:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Total tokens: {stats['total_tokens']:,}")
    print(f"  Avg tokens/chunk: {stats['avg_tokens']:.2f}")
    print(f"  Min tokens: {stats['min_tokens']}")
    print(f"  Max tokens: {stats['max_tokens']}")

    # Show first 3 chunks
    print(f"\nFirst 3 chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  Chunk {i+1}:")
        print(f"    Tokens: {len(chunk)}")
        section = chunk.metadata.get('section', 'N/A')
        # Remove emojis for console output
        section_clean = section.encode('ascii', 'ignore').decode('ascii')
        print(f"    Section: {section_clean}")
        if 'subsection' in chunk.metadata:
            subsection = chunk.metadata['subsection']
            subsection_clean = subsection.encode('ascii', 'ignore').decode('ascii')
            print(f"    Subsection: {subsection_clean}")
        preview = chunk.text[:100].replace('\n', ' ')
        preview_clean = preview.encode('ascii', 'ignore').decode('ascii')
        print(f"    Preview: {preview_clean}...")

    return chunks, stats


def main():
    """Run chunking demo."""
    data_dir = Path("data/raw")

    # Load one document for testing
    doc_path = data_dir / "OOP.md"

    if not doc_path.exists():
        print(f"Error: {doc_path} not found")
        return

    print("Loading document...")
    document = load_document(doc_path)
    print(f"Loaded: {document['source']}")
    print(f"Size: {len(document['text'])} characters")
    print(f"Words: {len(document['text'].split()):,}")

    # Test all strategies
    strategies = [
        (StructureChunker(), "Structure-Based Chunking"),
        (HierarchicalChunker(), "Hierarchical Chunking"),
        (SlidingWindowChunker(chunk_size=512, overlap=50), "Sliding Window (512/50)"),
        (SemanticChunker(embedder=None), "Semantic Chunking (Fallback)")
    ]

    results = {}

    for chunker, name in strategies:
        chunks, stats = test_chunking_strategy(chunker, document, name)
        results[name] = {
            'chunks': len(chunks),
            'stats': stats
        }

    # Summary comparison
    print(f"\n{'='*70}")
    print("STRATEGY COMPARISON")
    print(f"{'='*70}")
    print(f"\n{'Strategy':<40} {'Chunks':<10} {'Avg Tokens':<15}")
    print("-" * 70)

    for strategy_name, data in results.items():
        print(f"{strategy_name:<40} {data['chunks']:<10} {data['stats']['avg_tokens']:<15.2f}")

    # Save results
    output_path = Path("docs/chunking_demo_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    print(f"\n{'='*70}")
    print("RECOMMENDATIONS")
    print(f"{'='*70}")
    print("""
1. Structure-Based: Best for semantic coherence
   - Preserves natural topic boundaries
   - Ideal for educational content

2. Hierarchical: Best for multi-level queries
   - Handles both broad and specific questions
   - Parent chunks for context, children for details

3. Sliding Window: Baseline for comparison
   - Consistent chunk sizes
   - May break semantic units

4. Semantic: Experimental validation
   - Requires embeddings (slower)
   - Use to validate structure-based approach
    """)


if __name__ == "__main__":
    main()
