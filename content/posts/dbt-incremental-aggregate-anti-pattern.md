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
      inner join active_customers a
        on t.customer_id = a.customer_id
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
