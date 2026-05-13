#!/bin/bash

# Run tests for RAG Pipeline

echo "Running tests..."

# Activate virtual environment
source .venv/bin/activate || source .venv/Scripts/activate

# Run pytest with coverage
pytest tests/ \
    --verbose \
    --cov=src \
    --cov-report=html \
    --cov-report=term-missing \
    "$@"

echo "Tests complete!"
echo "Coverage report available in htmlcov/index.html"
