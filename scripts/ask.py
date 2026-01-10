# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "python-dotenv",
#     "numpy",
# ]
# ///

import os
import json
import sys
import time
import numpy as np
import auth
from google import genai
from google.genai import types
from google.genai.errors import ClientError

client = auth.get_client()

# Configuration
KNOWLEDGE_FILE = "knowledge.json"
EMBEDDING_MODEL = "text-embedding-004"
GENERATION_MODEL = "gemini-2.0-flash"

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        print(f"Error: {KNOWLEDGE_FILE} not found. Run 'uv run scripts/build_index.py' first.")
        exit(1)
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def find_best_chunks(query, knowledge_base, top_k=5):
    """Finds the most relevant chunks using cosine similarity."""
    # Embed the query
    try:
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=query,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        query_embedding = result.embeddings[0].values
        query_vec = np.array(query_embedding)
        
        scores = []
        for entry in knowledge_base:
            doc_vec = np.array(entry['embedding'])
            score = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))
            scores.append((score, entry))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]
    except Exception as e:
        print(f"Error embedding query: {e}")
        return []

def generate_with_retry(model, contents, retries=3, base_delay=10):
    """Generates content with retry logic for 429 Rate Limit errors."""
    for attempt in range(retries + 1):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents
            )
        except ClientError as e:
            # Check for 429 Resource Exhausted
            if e.code == 429:
                if attempt == retries:
                    print("\n❌ Max retries reached. Exiting.")
                    raise e
                
                # Exponential backoff with a cap
                sleep_time = min(base_delay * (2 ** attempt), 60)
                print(f"\n⚠️ Rate limit hit (429). Retrying in {sleep_time}s... (Attempt {attempt+1}/{retries})")
                time.sleep(sleep_time)
            else:
                raise e

def ask_gemini(query):
    knowledge_base = load_knowledge()
    relevant_chunks = find_best_chunks(query, knowledge_base)
    
    if not relevant_chunks:
        print("No relevant information found in the knowledge base.")
        return

    context_text = "\n\n---\n\n".join(
        [f"Source: {c[1]['file']}\nContent: {c[1]['content']}" for c in relevant_chunks]
    )
    
    prompt = f"""
    You are a helpful assistant for a technical blog. 
    Answer the user's question based strictly on the provided context below.
    If the answer is not in the context, say "I don't have information on that topic in the blog."
    
    Context:
    {context_text}
    
    Question: 
    {query}
    """
    
    try:
        response = generate_with_retry(
            model=GENERATION_MODEL,
            contents=prompt
        )
        
        print("\n" + "="*20 + " Answer " + "="*20 + "\n")
        print(response.text)
        print("\n" + "="*20 + " Sources " + "="*20)
        for score, entry in relevant_chunks:
            print(f"- {entry['file']} (Relevance: {score:.4f})")
            
    except Exception as e:
        print(f"Failed to generate answer: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/ask.py \"Your question here\"")
        sys.exit(1)
    
    question = sys.argv[1]
    ask_gemini(question)
