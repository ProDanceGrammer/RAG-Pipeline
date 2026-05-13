#!/bin/bash

# Setup environment for RAG Pipeline

echo "Setting up RAG Pipeline environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate || source .venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/cache
mkdir -p data/embeddings
mkdir -p data/vectordb
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Configuration
LOG_LEVEL=INFO
CACHE_ENABLED=true
EOF
    echo ".env file created. Please update with your API keys."
fi

echo "Setup complete!"
echo "Activate the environment with: source .venv/bin/activate"
