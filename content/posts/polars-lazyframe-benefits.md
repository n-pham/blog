+++
title = 'Polars LazyFrame: Stop Being Eager'
date = 2026-05-18T10:00:00+07:00
draft = false
tags = ['polars', 'python', 'dataframe', 'spark']
+++

# Eager vs. Lazy

In the data world, being "Eager" means doing work immediately. Being "Lazy" means building a plan first and executing it only when absolutely necessary.

| Feature | Eager (`DataFrame`) | Lazy (`LazyFrame`) |
| :--- | :--- | :--- |
| **Execution** | Immediate (like Pandas) | Deferred until `.collect()` |
| **Optimization** | None | **Query Optimizer** kicks in |
| **Memory** | Loads everything now | Only loads what it needs |

# The Magic of Pushdowns

When you use `LazyFrame`, Polars looks at your entire query and optimizes it before touching a single byte on disk.

1.  **Predicate Pushdown:** Filters are moved to the very beginning. If you query 10 years of data but filter for last week, Polars only reads last week's data from the Parquet file.
2.  **Projection Pushdown:** If your table has 100 columns but you only use 3, Polars only reads those 3 columns.

```python
import polars as pl

# Building the plan (Zero cost)
query = (
    pl.scan_parquet("huge_data.parquet")
    .filter(pl.col("category") == "Electronics")
    .select(["user_id", "price"])
    .group_by("user_id")
    .agg(pl.col("price").sum())
)

# Execution (The Optimizer makes this fast)
result = query.collect()
```

# Polars vs. DuckDB vs. Apache Spark

Spark is the king of distributed data, but Polars and DuckDB are the twin kings of the **Single Machine**.

| Feature | Polars | DuckDB | Apache Spark |
| :--- | :--- | :--- | :--- |
| **Language** | Rust | C++ | Scala (JVM) |
| **Primary API**| DataFrame/Expressions | **SQL** | DataFrame/SQL |
| **Out-of-Core**| Supported (Streaming) | **Excellent** | Excellent |
| **Scaling** | Vertical (Multi-core) | Vertical (Multi-core) | Horizontal (Cluster) |
| **Startup** | Instant | Instant | Slow |

# Parallelism: Multi-core without the Overhead

A common concern is: *"Spark uses all my cores for heavy computation, can Polars/DuckDB do that?"*

The answer is **Yes**, and they often do it better.

*   **Polars** is written in Rust and uses a high-performance thread pool (Rayon) to automatically parallelize almost every operation. It splits your data into chunks and processes them across all available cores without you writing a single line of "parallel" code.
*   **DuckDB** is a vectorized engine that parallelizes query execution by default. 

### Why they are faster than local Spark:
Even in "local" mode, Spark still suffers from **JVM overhead** and **Serialization/Deserialization**. Data must be moved between the Python process and the JVM, and often between the "Driver" and "Executor" threads using internal protocols.

Polars and DuckDB operate directly on your data in the same process memory. There is no "shuffle" over a local network loopback; there is just pure, raw CPU utilization.

### What if I use Java/Scala (No PySpark overhead)?

Even if you remove the Python-to-JVM bridge by writing pure Java or Scala, Polars and DuckDB still hold a "native" advantage:

*   **Memory Layout:** Spark (JVM) stores data as objects. Even with Spark's "Project Tungsten" optimizations, it still has to manage garbage collection (GC) and object overhead.
*   **SIMD & Vectorization:** Polars (Rust) and DuckDB (C++) are designed for **vectorized execution**. They use SIMD (Single Instruction, Multiple Data) to process whole chunks of data directly on the CPU registers. The JVM's JIT compiler is getting better at this, but it cannot yet match the manual, hardware-level optimization of a native engine.
*   **Zero-Copy:** In the native world, "sharing" data between Polars and DuckDB is just passing a pointer to an Arrow memory address. In the JVM, moving data between components often involves copying or serializing into `byte[]` buffers.

| Feature | Polars/DuckDB | Spark (Java/Scala) |
| :--- | :--- | :--- |
| **Execution** | Vectorized (Native) | Row-based/Tungsten (JVM) |
| **CPU Efficiency** | **SIMD / Cache-local** | JIT dependent |
| **Memory Management** | Manual/RAII (No GC) | Garbage Collected (GC) |

### What if I must use PySpark?

If you are stuck in PySpark but want to minimize the Python-to-JVM "tax," there are a few mandatory optimizations:

1.  **Enable Arrow:** Use `spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")`. This uses Apache Arrow to move data between Python and JVM significantly faster than default "pickling."
2.  **Pandas UDFs (Vectorized):** Instead of standard Python UDFs (which process row-by-row), use `@pandas_udf`. These transfer data in batches using Arrow and allow you to use vectorized operations (Pandas/Numpy), which is much closer to JVM performance.
3.  **Avoid `.map()` or `.apply()`:** These force data out of the optimized JVM "Tungsten" format into the Python interpreter. Stick to the **DataFrame API** (which is just a wrapper for JVM code).

### Is Java/Scala always better?

**Technically, yes.** 

In Java or Scala, there is **zero Inter-Process Communication (IPC)**. The code runs directly where the data lives. In PySpark, even with Arrow, you are still moving data between two different processes. 

If your pipeline consists of complex, custom row-level logic that can't be expressed in standard SQL, **Java/Scala is 2x-10x faster**. But for 90% of data engineering tasks, PySpark + Arrow is "good enough"—though Polars/DuckDB on a single node will still likely run circles around both.

| Feature | PySpark (Default) | PySpark (Arrow) | Spark (Java/Scala) |
| :--- | :--- | :--- | :--- |
| **Data Transfer** | Pickle (Slow) | **Arrow (Fast)** | None (Direct) |
| **Logic Execution** | Row-by-row | Vectorized (Pandas) | Native JVM |
| **IPC Cost** | High | Medium | **Zero** |

# The "Power Couple": Polars + DuckDB

Polars and DuckDB aren't just competitors; they are best friends. Because both are built on **Apache Arrow**, they can share data in memory with **zero copying**.

*   **DuckDB** is amazing for complex SQL, reading from diverse formats (S3, SQLite, Postgres), and handling data larger than your RAM.
*   **Polars** is amazing for the final "wrangling" and high-speed transformations using its expressive Python API.

```python
import polars as pl
import duckdb

# Use DuckDB to read and join complex sources
rel = duckdb.sql("SELECT * FROM read_parquet('huge_data.parquet') WHERE id > 1000")

# Hand off to Polars for fast transformations (Zero Copy via Arrow)
df = rel.pl() 

# Continue with Polars Lazy API
result = df.lazy().filter(pl.col("status") == "active").collect()
```

# When to stop using Spark?

If your dataset fits on a single machine (even a beefy one with 512GB RAM), **stop using Spark**. 

Between Polars' speed and DuckDB's SQL versatility, the network shuffle and JVM overhead of a Spark cluster are simply not worth it. 

> **Rule of thumb:** If it fits on your laptop, use Polars/DuckDB. If it fits on a single cloud instance, use Polars/DuckDB. If you need 100 machines to store it, *then* call the Spark engineers.
