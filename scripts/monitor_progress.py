"""Monitor indexing progress."""
import sys
from pathlib import Path

output_file = Path(sys.argv[1]) if len(sys.argv) > 1 else None

if output_file and output_file.exists():
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Count key events
    chunks_created = sum(1 for line in lines if 'Created' in line and 'chunks' in line)
    embeddings_done = sum(1 for line in lines if 'Embedding' in line and 'new chunks' in line)
    added_to_store = sum(1 for line in lines if 'Added' in line and 'chunks to' in line)
    errors = sum(1 for line in lines if 'ERROR' in line)

    print(f"Progress Summary:")
    print(f"  Chunking operations: {chunks_created}")
    print(f"  Embedding batches: {embeddings_done}")
    print(f"  Store additions: {added_to_store}")
    print(f"  Errors: {errors}")
    print(f"\nLast 5 lines:")
    for line in lines[-5:]:
        print(f"  {line.strip()}")
else:
    print("Output file not found or not specified")
