#!/usr/bin/env python3
"""
Extract all numbers from documentation files for audit.
"""
import re
import os
from pathlib import Path
from typing import List, Dict, Tuple

def extract_numbers_from_file(filepath: str) -> List[Dict]:
    """Extract all numbers with context from a markdown file."""
    numbers = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Patterns to match numbers with units/context
    patterns = [
        # Percentages: 70%, 70-80%
        (r'\b(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*%', 'percentage'),
        # Time: 3s, 3.5s, 60-120s, 9.92 minutes
        (r'\b(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*(s|seconds?|ms|milliseconds?|min|minutes?|hours?|h)\b', 'time'),
        # Size: 1.4 MB, 179 vectors, 768 dimensions
        (r'\b(\d+(?:\.\d+)?)\s*(MB|GB|KB|bytes?|vectors?|dimensions?|chunks?|queries?|files?|tasks?)\b', 'size/count'),
        # Standalone numbers in technical context
        (r'\b(\d+(?:\.\d+)?)\b', 'number'),
    ]

    for line_num, line in enumerate(lines, 1):
        # Skip code blocks
        if line.strip().startswith('```') or line.strip().startswith('    '):
            continue

        for pattern, num_type in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                context_start = max(0, line_num - 2)
                context_end = min(len(lines), line_num + 1)
                context = ''.join(lines[context_start:context_end]).strip()

                numbers.append({
                    'file': os.path.basename(filepath),
                    'line': line_num,
                    'number': match.group(0),
                    'type': num_type,
                    'context': context[:200],  # First 200 chars of context
                    'full_line': line.strip()
                })

    return numbers

def main():
    docs_dir = Path(__file__).parent.parent / 'docs'

    # Documentation files to scan
    doc_files = [
        'ARCHITECTURE.md',
        'PROJECT_FINAL.md',
        'PROJECT_COMPLETE.md',
        'FINAL_STATUS.md',
        'CURRENT_STATUS.md',
        'PHASE3_COMPLETE.md',
        'PHASE4_COMPLETE.md',
        'PHASE5_COMPLETE.md',
        'PROGRESS_REPORT.md',
        'EVALUATION_RESULTS.md',
        'QUICK_START.md',
        'README.md',
        'CHUNKING_SUMMARY.md',
        'OLLAMA_SETUP.md',
        'INSTALL_MODELS.md',
    ]

    all_numbers = []

    for doc_file in doc_files:
        filepath = docs_dir / doc_file
        if filepath.exists():
            print(f"Scanning {doc_file}...")
            numbers = extract_numbers_from_file(str(filepath))
            all_numbers.extend(numbers)
            print(f"  Found {len(numbers)} numbers")
        else:
            print(f"  SKIP: {doc_file} not found")

    print(f"\n{'='*80}")
    print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
    print(f"{'='*80}\n")

    # Group by file
    by_file = {}
    for num in all_numbers:
        if num['file'] not in by_file:
            by_file[num['file']] = []
        by_file[num['file']].append(num)

    # Output detailed report
    output_file = docs_dir / 'NUMBER_EXTRACTION.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DOCUMENTATION NUMBER EXTRACTION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total numbers found: {len(all_numbers)}\n")
        f.write(f"Files scanned: {len(by_file)}\n\n")

        for filename in sorted(by_file.keys()):
            f.write(f"\n{'='*80}\n")
            f.write(f"FILE: {filename}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Numbers found: {len(by_file[filename])}\n\n")

            for num in by_file[filename]:
                f.write(f"Line {num['line']}: {num['number']} ({num['type']})\n")
                f.write(f"  Full line: {num['full_line']}\n")
                f.write(f"  Context: {num['context'][:150]}...\n")
                f.write("\n")

    print(f"Detailed report written to: {output_file}")

    # Summary by type
    by_type = {}
    for num in all_numbers:
        if num['type'] not in by_type:
            by_type[num['type']] = 0
        by_type[num['type']] += 1

    print("\nNumbers by type:")
    for num_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {num_type}: {count}")

if __name__ == '__main__':
    main()
