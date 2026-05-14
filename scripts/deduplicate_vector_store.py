"""Detect and report duplicate chunks in vector store."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.multi_store_manager import MultiStoreManager
import hashlib


def find_duplicates(store_name: str):
    """Find duplicate chunks in a vector store.

    Args:
        store_name: Name of the store to check (e.g., "structure")
    """
    manager = MultiStoreManager(Path("data/vector_stores"))

    try:
        manager.load_store(store_name, 768)
    except Exception as e:
        print(f"Error loading store '{store_name}': {e}")
        return

    store = manager.get_store(store_name)

    if not hasattr(store, 'metadata') or not store.metadata:
        print(f"Store '{store_name}' has no metadata")
        return

    seen = {}
    duplicates = []

    for i, meta in enumerate(store.metadata):
        section = meta.get('section', 'Unknown')
        text = meta.get('text', '')

        # Hash first 200 chars to detect duplicates
        text_hash = hashlib.md5(text[:200].encode()).hexdigest()
        key = (section, text_hash)

        if key in seen:
            duplicates.append({
                'section': section,
                'original_idx': seen[key],
                'duplicate_idx': i,
                'text_preview': text[:100]
            })
        else:
            seen[key] = i

    # Print results
    print(f"\n{'='*60}")
    print(f"Duplicate Chunk Analysis: {store_name}")
    print(f"{'='*60}\n")
    print(f"Total chunks: {len(store.metadata)}")
    print(f"Unique chunks: {len(seen)}")
    print(f"Duplicates found: {len(duplicates)}")
    print(f"Duplicate rate: {len(duplicates) / len(store.metadata) * 100:.1f}%\n")

    if duplicates:
        print(f"{'='*60}")
        print("Duplicate Details:")
        print(f"{'='*60}\n")

        # Group by section
        by_section = {}
        for dup in duplicates:
            section = dup['section']
            if section not in by_section:
                by_section[section] = []
            by_section[section].append(dup)

        for section, dups in by_section.items():
            print(f"Section: '{section}'")
            print(f"  Occurrences: {len(dups) + 1} (1 original + {len(dups)} duplicates)")
            print(f"  Indices: {dups[0]['original_idx']}, {', '.join(str(d['duplicate_idx']) for d in dups)}")
            print(f"  Preview: {dups[0]['text_preview']}...")
            print()
    else:
        print("✓ No duplicates found!")

    return duplicates


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect duplicate chunks in vector store")
    parser.add_argument(
        "--store",
        type=str,
        default="structure",
        help="Name of the vector store to check (default: structure)"
    )

    args = parser.parse_args()
    find_duplicates(args.store)
