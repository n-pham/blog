+++
title = 'DBT Incremental Aggregate Anti-Pattern'
date = 2026-09-26T10:00:00+07:00
draft = false
tags = ['dbt', 'sql']
+++


# DBT Incremental Aggregate Anti-Pattern

When we build an incremental model that aggregates transactional data by entity (e.g., customer) over all history, we often fall into a subtle trap: filtering raw source transactions directly by date.

The moment we apply `where transaction_date >=` directly on raw source records, we calculate aggregations on only incremental data and corrupt lifetime metrics like total_transactions, first_transaction_date.

The Solution: `Affected Entity Pattern` to separate partition pruning from historical re-aggregation.

1. active_customers: Filter transactions by date to identify customer IDs active within the lookback window.
2. affected_customer_history: Join back to pull complete historical transactions ONLY for those active customers.

```sql
with active_customers as (
    select distinct customer_id
    from {{ ref('stg_transactions') }}
    {% if is_incremental() %}
      where transaction_date >= (
        select max(last_transaction_date)
        from {{ this }}) - interval '3 days'
    {% endif %}
),
affected_customer_history as (
    select
        t.customer_id,
        t.transaction_date,
        t.amount
    from {{ ref('stg_transactions') }} t
    {% if is_incremental() %}
      where t.customer_id in (select customer_id from active_customers)
    {% endif %}
)
select
    customer_id,
    count(1) as total_transactions,
    min(transaction_date) as first_transaction_date,
    max(transaction_date) as last_transaction_date
from affected_customer_history
group by 1
```

Why this works:

* Data Accuracy: Guarantees correct lifetime metrics by re-aggregating full history for modified entities.
* Cost Efficiency: Uses partition pruning on transaction date to isolate affected keys without scanning inactive historical records.
* Scalability: Compute overhead scales with active entities in the run window rather than total historical dataset volume (with customer_id being clustered).

## Partition Pruning Note: `WHERE IN` vs `INNER JOIN`

The `affected_customer_history` CTE uses `where t.customer_id in (select customer_id from active_customers)` instead of an `inner join`. This matters because:

* **`INNER JOIN` without a date filter** forces a full scan of `stg_transactions` — the optimizer cannot push the `customer_id` predicate into the table scan before the join, so all partitions are read.
* **`WHERE IN` (semi-join)** allows the optimizer to push the `customer_id` filter directly into the `stg_transactions` scan. With `customer_id` clustering, BigQuery prunes to only the blocks containing active customers, skipping partitions for inactive customers entirely.

If your warehouse doesn't optimize semi-joins well, you can also materialize `active_customers` as a temp table and join — but the `WHERE IN` pattern is the standard dbt idiom for this reason.

# BigQuery: `enable_change_history`

BigQuery offers a native alternative to the Affected Entity Pattern via the `enable_change_history` table option. When enabled, BigQuery tracks which partitions have changed since the last incremental run and automatically prunes to only those partitions.

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    enable_change_history=true,
    unique_key='customer_id'
) }}

select
    customer_id,
    count(1) as total_transactions,
    min(transaction_date) as first_transaction_date,
    max(transaction_date) as last_transaction_date
from {{ ref('stg_transactions') }}
{% if is_incremental() %}
  -- No manual date filter or join needed!
  -- BigQuery reads only partitions with changes since last run
{% endif %}
group by 1
```

## Why this works better

| Aspect | Affected Entity Pattern | `enable_change_history` |
|--------|------------------------|------------------------|
| **Code complexity** | Two CTEs, semi-join logic | Single query, config-only |
| **Partition pruning** | Manual via `customer_id` clustering | Automatic via change tracking |
| **Late-arriving data** | Handled by lookback window | Handled automatically |
| **Schema changes** | Manual migration | Automatic |
| **Cost predictability** | Scales with active entities | Scales with changed partitions |

## How `enable_change_history` works

1. **First run**: Full scan, builds change history metadata
2. **Subsequent runs**: BigQuery compares the source table's change history against the target's last processed snapshot timestamp
3. **Only changed partitions** are read — no `WHERE` clause, no join, no lookback window needed
4. **Merge** updates existing `customer_id` rows, inserts new ones

## Requirements & Caveats

* **Partitioned source table** — `stg_transactions` must be partitioned (by `transaction_date`)
* **Incremental strategy must be `merge`** — `append` + `enable_change_history` is not supported
* **Unique key required** — for the merge deduplication
* **Change history retention** — 7 days by default; adjust with `change_history_retention_period` if your incremental runs are less frequent

# When to use which

* **Use Affected Entity Pattern** when: warehouse-agnostic, need fine-grained control, or on warehouses without change tracking (Snowflake, Redshift, Postgres)
* **Use `enable_change_history`** when: BigQuery-only, want minimal boilerplate, have partitioned source tables, and can accept preview features

The `enable_change_history` approach is essentially "Affected Entity Pattern as a managed service" — BigQuery handles the active entity detection and partition pruning internally, with better handling of edge cases like late-arriving data and schema evolution.

# Business Definition Drives Performance

The entire discussion above assumes you need **lifetime metrics** (e.g., `total_transactions` all-time, `first_transaction_date`). But what if the business only needs a **rolling window**?

```sql
-- Lifetime metric: requires full history re-aggregation
count(1) as total_transactions

-- Rolling 30-day metric: only last 30 partitions needed
count(1) as total_transactions_last_30_days
```

| Metric Type | Partitions Scanned | Clustering Needed? | `enable_change_history`? |
|-------------|-------------------|-------------------|-------------------------|
| Lifetime (`total_transactions`) | All history | Yes (customer_id) | Helpful |
| Rolling 30-day | Last 30 partitions | No | Not needed |
| Rolling 7-day | Last 7 partitions | No | Not needed |

**If the metric is `total_transactions_last_30_days`**, you don't need the Affected Entity Pattern, clustering on `customer_id`, or `enable_change_history`. A simple date filter is sufficient:

```sql
select
    customer_id,
    count(1) as total_transactions_last_30_days
from {{ ref('stg_transactions') }}
{% if is_incremental() %}
  where transaction_date >= current_date - interval '30 days'
{% endif %}
group by 1
```

This works because:
* **Partition pruning** on `transaction_date` reads only the last 30 partitions — no full scan
* **No join/semi-join** — the date filter is pushed directly into the table scan
* **No clustering needed** — partitioning by date alone handles it
* **Correct by default** — the rolling window naturally excludes stale data

The insight

**Business definitions are performance requirements.**

* "Total lifetime transactions" → requires complex incremental logic (Affected Entity Pattern, change history)
* "Transactions in last 30 days" → simple date filter, partition pruning does all the work

Before reaching for advanced incremental patterns, ask: *Does the business actually need lifetime metrics, or is a rolling window sufficient?* Often the answer changes the implementation from "hard" to "trivial."
