# Local RAG for Hugo Blog

## Context
This project enhances a standard [Hugo](https://gohugo.io/) static site with a local Retrieval-Augmented Generation (RAG) system. It allows the user to "chat" with their blog posts using Google's Gemini models without requiring external vector databases or complex infrastructure.

## Architecture

### Core Design Principles
1.  **Zero Infrastructure**: No external services (Pinecone, Milvus, etc.) except the LLM API.
2.  **Local State**: The vector index is a simple local JSON file (`knowledge.json`).
3.  **Tooling**: Uses `uv` for script execution and dependency management via PEP 723 inline metadata.
4.  **SDK**: Uses the modern `google-genai` Python SDK.

### Workflow
1.  **Ingestion (`scripts/build_index.py`)**:
    *   Scans `content/posts/*.md`.
    *   Strips Hugo TOML frontmatter (`+++ ... +++`).
    *   Chunks text into paragraph-sized segments (~1000 chars).
    *   Generates embeddings using `text-embedding-004`.
    *   Saves the resulting list of objects (content + embedding vector) to `knowledge.json`.

2.  **Retrieval & Answer (`scripts/ask.py`)**:
    *   Loads `knowledge.json`.
    *   Embeds the user's query using `text-embedding-004`.
    *   Calculates Cosine Similarity to find the top 5 most relevant chunks.
    *   Constructs a prompt with these chunks as context.
    *   Generates the final answer using `gemini-2.0-flash`.

## Components & Configuration

### Scripts
*   **`scripts/build_index.py`**: Index builder. Run this after adding/editing posts.
*   **`scripts/ask.py`**: CLI query interface.

### Models
*   **Embedding**: `models/text-embedding-004` (768-dimensional, optimized for retrieval).
*   **Generation**: `gemini-2.0-flash` (Updated for 2026 standards, high speed).

### Data Structure (`knowledge.json`)
A flat list of objects:
```json
[
  {
    "file": "filename.md",
    "chunk_id": 0,
    "content": "extracted text...",
    "embedding": [0.123, -0.456, ...]
  }
]
```

### Environment
*   **.env**: Stores `GEMINI_API_KEY`.
*   **.gitignore**: Excludes `knowledge.json`, `.env`, and `.venv/`.

## Usage

**Prerequisites:**
1.  Install `uv`.
2.  Set `GEMINI_API_KEY` in `.env`.

**Commands:**
```bash
# Rebuild the index
uv run scripts/build_index.py

# Ask a question
uv run scripts/ask.py "How do I optimize BigQuery costs?"
```
