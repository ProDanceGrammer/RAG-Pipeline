"""Cleanup utility for temporary files and caches."""
import shutil
from pathlib import Path
import argparse


def cleanup(target: str = "all"):
    """Clean up temporary files and caches."""
    base_path = Path(__file__).parent.parent

    targets = {
        "cache": base_path / "data" / "cache",
        "embeddings": base_path / "data" / "embeddings",
        "vectordb": base_path / "data" / "vectordb",
        "logs": base_path / "logs",
        "pycache": "__pycache__"
    }

    if target == "all":
        dirs_to_clean = targets.values()
    elif target in targets:
        dirs_to_clean = [targets[target]]
    else:
        print(f"Unknown target: {target}")
        return

    for dir_path in dirs_to_clean:
        if dir_path == "__pycache__":
            for pycache in base_path.rglob("__pycache__"):
                print(f"Removing {pycache}")
                shutil.rmtree(pycache, ignore_errors=True)
        elif dir_path.exists():
            print(f"Cleaning {dir_path}")
            shutil.rmtree(dir_path, ignore_errors=True)
            dir_path.mkdir(parents=True, exist_ok=True)

    print("Cleanup complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup temporary files")
    parser.add_argument(
        "--target",
        choices=["all", "cache", "embeddings", "vectordb", "logs", "pycache"],
        default="all",
        help="Target to clean"
    )
    args = parser.parse_args()

    cleanup(args.target)
