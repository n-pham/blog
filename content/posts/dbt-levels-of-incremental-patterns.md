+++
title = 'dbt Levels of Incremental Patterns'
date = 2026-07-13T10:00:00+07:00
draft = false
tags = ['dbt', 'datamodel', 'python']
+++

# dbt Levels of Incremental Patterns

Incremental models are needed for efficient data pipelines. However, there is another often forgotten pattern to enable efficient backfill: incremental backfill.

Note: DataFrame is chosen for these patterns because it allows for a much simpler and more readable implementation.

## Level 1: Full Load, no Incremental
The baseline. Your logic must be idempotent, allowing a complete rebuild from scratch.

```python
# Full Load: Just read and write
def model(dbt, session):
    return dbt.ref("stg_events")
```

## Level 2: Incremental Load
Processing only records newer than the current maximum timestamp in the destination.

```python
# Level 2: High-water mark
def model(dbt, session):
    df = dbt.ref("stg_events")
    if dbt.is_incremental:
        max_ts = session.table(dbt.this).select(max("ts")).collect()[0][0]
        df = df.filter(df.ts > max_ts)
    return df
```

## Level 3: Incremental Backfill
Surgical replacement of a specific time window. This is critical when upstream history is corrected.

```python
# Level 3: Windowed override
start = dbt.config.get("start_date") # e.g. "2024-01-01"
df = dbt.ref("stg_events").filter((col("ts") >= start) & (col("ts") < end))
```

---

# Hard Mode: SCD Type 2 with DataFrames

While `dbt snapshot` is a common choice for SCD2, it **fails during backfills** because it cannot reconstruct historical "chains" from past data. We need to implement the "Expire & Insert" logic manually.

### 1. Incremental Load (Daily)
We find keys that changed, "close" their current active record, and insert the new version.

```python
# Simplified SCD2 Incremental
new_data = dbt.ref("stg_source")
active_now = dbt.this.filter(col("is_current") == True)

# Join to find records to expire
expired = active_now.join(new_data, "id", "inner").with_column("valid_to", new_data.ts)
# Union back and insert
return dbt.this.join(expired, "id", "left_anti").union(expired).union(new_data)
```

### 2. Incremental Backfill (The Chain)
If you backfill a month in 2023, you must re-calculate the timeline for any ID touched in that window to ensure `valid_to` always matches the next `valid_from`.

**The Rule:** For SCD2, a backfill isn't a date-range filter; it's an **ID-range filter**. 

1.  Identify IDs that had changes in the backfill window.
2.  Pull **all** history for those specific IDs.
3.  Use a Window function to recalculate the chain:
    ```python
    window = Window.partitionBy("id").orderBy("valid_from")
    df.withColumn("valid_to", lead("valid_from").over(window))
    ```
4.  Replace only those IDs in the final table.

This approach makes backfilling deterministic and avoids the "broken timeline" trap common in SQL-based incremental updates.
