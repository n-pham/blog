+++
title = 'Spark Data Processing Patterns'
featured_image = 'images/spark-patterns.png'
date = 2026-06-11T10:00:00+07:00
draft = false
tags = ['spark', 'architecture', 'performance']
+++
# TL;DR
* Use **Broadcast Join** for small-to-large table joins to avoid shuffles.
* Implement **Window Functions** for time-series and ranking instead of self-joins.
* Leverage **Salting** to handle data skew in heavy aggregations.

# Common Patterns

## 1. The Lookup (Broadcast) Pattern
When joining a large fact table with a small dimension table, standard shuffle joins are overkill. Broadcasting the small table avoids moving the large dataset across the network.

```python
from pyspark.sql.functions import broadcast

# Efficient: small_df is sent to all executors
result = large_df.join(broadcast(small_df), "key")
```

## 2. The Incremental Window Pattern
For calculating running totals or identifying the "previous" state without expensive self-joins, use window functions.

```python
from pyspark.sql.window import Window
import pyspark.sql.functions as F

window_spec = Window.partitionBy("user_id").orderBy("timestamp")
df = df.withColumn("prev_value", F.lag("value").over(window_spec))
```

## 3. The Anti-Skew (Salting) Pattern
Skewed keys cause "straggler" tasks. By adding a random "salt" to the key, you distribute the load across more partitions.

```python
# Add salt to the skewed key
df = df.withColumn("salt", (F.rand() * 10).cast("int"))
df = df.withColumn("salted_key", F.concat(F.col("key"), F.lit("_"), F.col("salt")))

# Join with a similarly exploded dimension table
```
