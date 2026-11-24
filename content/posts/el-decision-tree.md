+++
title = 'EL Decision Tree'
date = 2026-11-24T10:00:00+07:00
draft = false
tags = []
+++

# Extract Decision Tree

| Source | Tool | Notes |
| :--- | :--- | :--- |
| API |  dlt | Auth, pagination, rate-limit retries |
| Nested JSON |  dlt | flattening |
| RDBMS |  dlt | incremental load and schema evolution |
| Object Storage | DuckDB | target lake handles schema evolution |
| Multi-Source Join | DuckDB |  |

(Polars can be added anytime for type conversion)


# Load Decision Tree

| Target | Tool | Notes |
| :--- | :--- | :--- |
| Partition Overwrite |  DuckDB | use lookback window |
| Row Merge |  dlt | use `incremental(..., lag=...)` and `write_disposition="merge"` |
