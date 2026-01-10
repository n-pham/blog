# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "python-dotenv",
#     "tqdm",
#     "numpy",
# ]
# ///

import os
import glob
import re
import json
import numpy as np
import auth
from google import genai
from google.genai import types
from tqdm import tqdm

client = auth.get_client()

# Configuration
CONTENT_DIR = "content/posts"
OUTPUT_FILE = "knowledge.json"
EMBEDDING_MODEL = "text-embedding-004"

def parse_hugo_post(file_path):
    """Reads a markdown file and removes Hugo TOML frontmatter."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Matches content between the first two +++ delimiters
    content = re.sub(r"^\+\+\+.*?\+\+\+", "", content, flags=re.DOTALL)
    return content.strip()

def chunk_text(text, chunk_size=1000):
    """Simple chunking by splitting on double newlines."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) < chunk_size:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def build_index():
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    print(f"Found {len(files)} posts in {CONTENT_DIR}")

    knowledge_base = []

    for file_path in tqdm(files, desc="Processing Posts"):
        filename = os.path.basename(file_path)
        text = parse_hugo_post(file_path)
        if not text:
            continue

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding using the new SDK
                result = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=chunk,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT",
                        title=filename
                    )
                )
                
                knowledge_base.append({
                    "file": filename,
                    "chunk_id": i,
                    "content": chunk,
                    "embedding": result.embeddings[0].values
                })
            except Exception as e:
                print(f"Failed to embed {filename} chunk {i}: {e}")

    print(f"Saving {len(knowledge_base)} text chunks to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f)
    print("Done!")

if __name__ == "__main__":
    build_index()