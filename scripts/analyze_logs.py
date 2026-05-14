#!/usr/bin/env python3
"""
Analyze logs to extract performance metrics.
"""
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import statistics

def parse_log_file(log_path: Path) -> Dict:
    """Parse rag_console.log to extract performance metrics."""

    generation_times = []
    query_times = []
    retrieval_times = []

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse generation times: "Generation took 30.84s"
    for line in lines:
        match = re.search(r'Generation took ([\d.]+)s', line)
        if match:
            generation_times.append(float(match.group(1)))

    # Parse query completion times: "Query completed in 35.03s"
    for line in lines:
        match = re.search(r'Query completed in ([\d.]+)s', line)
        if match:
            query_times.append(float(match.group(1)))

    # Calculate retrieval times (query_time - generation_time)
    if len(query_times) == len(generation_times):
        retrieval_times = [q - g for q, g in zip(query_times, generation_times)]

    # Extract vector count from logs
    vector_count = None
    for line in lines:
        match = re.search(r'Loaded structure store.*\((\d+) vectors\)', line)
        if match:
            vector_count = int(match.group(1))
            break

    # Extract query count
    query_count = 0
    for line in lines:
        match = re.search(r'Query #(\d+):', line)
        if match:
            query_count = max(query_count, int(match.group(1)))

    return {
        'generation_times': generation_times,
        'query_times': query_times,
        'retrieval_times': retrieval_times,
        'vector_count': vector_count,
        'query_count': query_count,
    }

def calculate_stats(values: List[float]) -> Dict:
    """Calculate min, max, avg, median statistics."""
    if not values:
        return {'min': None, 'max': None, 'avg': None, 'median': None, 'count': 0}

    return {
        'min': min(values),
        'max': max(values),
        'avg': statistics.mean(values),
        'median': statistics.median(values),
        'count': len(values),
    }

def main():
    project_root = Path(__file__).parent.parent
    log_path = project_root / 'logs' / 'rag_console.log'

    if not log_path.exists():
        print(f"ERROR: Log file not found: {log_path}")
        return

    print("Analyzing logs...")
    print(f"Log file: {log_path}")
    print("=" * 80)

    data = parse_log_file(log_path)

    # Generation times
    gen_stats = calculate_stats(data['generation_times'])
    print("\nGENERATION LATENCY:")
    print(f"  Count: {gen_stats['count']} queries")
    if gen_stats['count'] > 0:
        print(f"  Min: {gen_stats['min']:.2f}s")
        print(f"  Max: {gen_stats['max']:.2f}s")
        print(f"  Avg: {gen_stats['avg']:.2f}s")
        print(f"  Median: {gen_stats['median']:.2f}s")
        print(f"  Raw values: {[f'{v:.2f}s' for v in data['generation_times']]}")

    # Query times
    query_stats = calculate_stats(data['query_times'])
    print("\nQUERY LATENCY (total):")
    print(f"  Count: {query_stats['count']} queries")
    if query_stats['count'] > 0:
        print(f"  Min: {query_stats['min']:.2f}s")
        print(f"  Max: {query_stats['max']:.2f}s")
        print(f"  Avg: {query_stats['avg']:.2f}s")
        print(f"  Median: {query_stats['median']:.2f}s")
        print(f"  Raw values: {[f'{v:.2f}s' for v in data['query_times']]}")

    # Retrieval times
    ret_stats = calculate_stats(data['retrieval_times'])
    print("\nRETRIEVAL LATENCY:")
    print(f"  Count: {ret_stats['count']} queries")
    if ret_stats['count'] > 0:
        print(f"  Min: {ret_stats['min']:.2f}s")
        print(f"  Max: {ret_stats['max']:.2f}s")
        print(f"  Avg: {ret_stats['avg']:.2f}s")
        print(f"  Median: {ret_stats['median']:.2f}s")
        print(f"  Raw values: {[f'{v:.2f}s' for v in data['retrieval_times']]}")

    # Other metrics
    print("\nOTHER METRICS:")
    print(f"  Vector count: {data['vector_count']}")
    print(f"  Total queries logged: {data['query_count']}")

    # Write results to file
    output_path = project_root / 'docs' / 'LOG_ANALYSIS.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LOG ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: 2026-05-13\n")
        f.write(f"Log file: {log_path}\n\n")

        f.write("GENERATION LATENCY:\n")
        f.write(f"  Count: {gen_stats['count']} queries\n")
        if gen_stats['count'] > 0:
            f.write(f"  Min: {gen_stats['min']:.2f}s\n")
            f.write(f"  Max: {gen_stats['max']:.2f}s\n")
            f.write(f"  Avg: {gen_stats['avg']:.2f}s\n")
            f.write(f"  Median: {gen_stats['median']:.2f}s\n")
            f.write(f"  Raw values: {data['generation_times']}\n")

        f.write("\nQUERY LATENCY (total):\n")
        f.write(f"  Count: {query_stats['count']} queries\n")
        if query_stats['count'] > 0:
            f.write(f"  Min: {query_stats['min']:.2f}s\n")
            f.write(f"  Max: {query_stats['max']:.2f}s\n")
            f.write(f"  Avg: {query_stats['avg']:.2f}s\n")
            f.write(f"  Median: {query_stats['median']:.2f}s\n")
            f.write(f"  Raw values: {data['query_times']}\n")

        f.write("\nRETRIEVAL LATENCY:\n")
        f.write(f"  Count: {ret_stats['count']} queries\n")
        if ret_stats['count'] > 0:
            f.write(f"  Min: {ret_stats['min']:.2f}s\n")
            f.write(f"  Max: {ret_stats['max']:.2f}s\n")
            f.write(f"  Avg: {ret_stats['avg']:.2f}s\n")
            f.write(f"  Median: {ret_stats['median']:.2f}s\n")
            f.write(f"  Raw values: {data['retrieval_times']}\n")

        f.write("\nOTHER METRICS:\n")
        f.write(f"  Vector count: {data['vector_count']}\n")
        f.write(f"  Total queries logged: {data['query_count']}\n")

    print(f"\nResults written to: {output_path}")

if __name__ == '__main__':
    main()
