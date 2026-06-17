+++
title = 'Locality: from Data to Code to AI Context'
date = 2026-08-10T10:00:00+07:00
draft = false
tags = ['data', 'ai']
+++

# Locality: from Data to Code to AI Context

* Traditionally, data on disk is read sequentially batch by batch, so Locality is the high performance pattern for data. 
* Now for AI Agents, Locality is again helping with a high-density, localized context.

| Data Locality | Code Locality | AI Context |
| :--- | :--- | :--- |
| **Data Clustering**: Physically grouping related rows on disk to minimize IO "jumps." | **Code Monolithing**: Packing related functions, types, and docs into a single file or prompt. | **Attention Locality**: Prevents the agent's attention from fragmenting across multiple files. |
| **Bruin / Single-File**: Inlining SQL, Python, and YAML metadata in one definition. | **Single-File Bundlers**: Combining source code, types, and unit tests into a single `.md` manifest. | **Deterministic Retrieval**: The agent reads one source of truth; no need to "guess" relationships between `/src` and `/tests`. |
| **SQLMesh**: Native engine understanding of column-level state and data lineage. | **AST-Aware Context**: Passing structured Abstract Syntax Trees and call graphs instead of raw text snippets. | **Structural Reasoning**: Moves the agent from "Grep-based" keyword matching to semantic, architectural understanding. |

# The New Architecture: Linear Density
We are witnessing a shift from **Random Access** to **Sequential Scan** at every layer of the stack:

1.  **In Data:** We moved from traditional database indexes (random point lookups) to modern data warehouses like BigQuery and Snowflake that favor massive sequential scans of localized, compressed data.
2.  **In Code:** We are moving away from hyper-fragmented **Microservices** (optimized for independent human teams) back toward **Monoliths** (optimized for AI locality). A monolith reduces the "seek distance" for an agent, allowing it to reason about the entire system without jumping across repository boundaries or network hops.
3.  **In AI:** We are moving from fragile **RAG** (point lookups of text snippets) to large-context agents that "scan" entire localized codebases in one go.
