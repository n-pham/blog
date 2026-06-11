+++
title = 'Vector Databases for Data Engineers'
featured_image = 'images/vector-db.png'
date = 2026-06-11T11:10:00+07:00
draft = false
tags = ['ai', 'vector-db', 'rag']
+++
# TL;DR
* Vector DBs are essential for RAG (Retrieval Augmented Generation).
* Choose **Pinecone** for managed ease, **Milvus** for scale, or **pgvector** for SQL compatibility.
* Your ETL now includes "Embedding Generation."

# The New ETL Pipeline
Data engineering for AI involves a new step: turning text into vectors using models like OpenAI's `text-embedding-3`.

1. **Extract**: Pull text from SQL/NoSQL.
2. **Transform**: Chunk text and generate embeddings.
3. **Load**: Insert into a Vector DB.

```python
# Conceptual pgvector insertion
cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", 
            (text, embedding_vector))
```
