+++
title = 'DuckDB: The Data Swiss Army Knife'
featured_image = 'images/duckdb.png'
date = 2026-06-11T11:00:00+07:00
draft = false
tags = ['duckdb', 'python', 'sql']
+++
# TL;DR
* DuckDB is the "SQLite for Analytics."
* It can query CSV, Parquet, and JSON files directly without a database server.
* Ideal for local data exploration and CI/CD pipelines.

# Why DuckDB is a Game Changer

## 1. Zero Setup
Unlike Postgres or BigQuery, DuckDB is a single binary or a Python package. You don't need to manage a cluster to process 100GB of data.

```python
import duckdb

# Query a parquet file directly
duckdb.query("SELECT * FROM 'data/*.parquet' WHERE price > 100").show()
```

## 2. Format Agnostic
DuckDB treats files as tables. You can join a local CSV with a remote Parquet file in a single SQL statement.

```sql
SELECT * 
FROM read_csv_auto('users.csv') 
JOIN read_parquet('s3://my-bucket/orders.parquet') ON users.id = orders.user_id;
```
