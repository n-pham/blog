+++
title = 'BigQuery Partitioning with Policy Tags: The Hidden Cost'
date = 2026-05-17T10:00:00+07:00
draft = false
tags = ['bigquery', 'security', 'partition', 'cost']
+++

# The Full Table Scan Trap

When you apply a **Policy Tag** (Column-level security) to a column used for **Partitioning**—like a sensitive `customer_id`—users without the `Data Catalog Fine-Grained Reader` role trigger a silent cost explosion or a hard error.

> **The Problem:** BigQuery cannot "read" the partitioning column to perform pruning. 
> 
> 1. **Access Error:** By default, users without the `Data Catalog Fine-Grained Reader` role will get an access denied error when trying to query the table if it includes the sensitive column.
> 2. **Pruning Failure:** If they *can* run the query (e.g., via masking or specific access), the query engine falls back to a **Full Table Scan**, ignoring the `WHERE` clause even if you filter by that ID.

# The "Hashed Bucket" Pattern

If your security policy forbids copying the exact `customer_id` into a shadow column, use a **Hashed Bucket**. This obfuscates the exact ID while still allowing BigQuery to prune the majority of the data.

<table>
<tr>
<th>The Problem (Strict Security)</th>
<th>The Workaround (Hashed Bucket)</th>
</tr>
<tr>
<td>

```sql
-- Range Partitioned on customer_id
-- customer_id HAS policy tag
SELECT * 
FROM orders
WHERE customer_id = 999123

-- Scans 100% of table bytes 
-- (or throws Access Denied)
```

</td>
<td>

```sql
-- Partitioned on id_bucket (INT64)
-- id_bucket = MOD(customer_id, 100)
-- customer_id HAS policy tag
SELECT * 
FROM orders
WHERE customer_id = 999123
  AND id_bucket = 23 -- MOD(999123, 100)

-- Pruning works! 
-- Only 1/100th of the table scanned.
```

</td>
</tr>
</table>

# Implementation

Create a "bucket" column that doesn't reveal the full ID.

```sql
CREATE TABLE project.dataset.orders (
    order_id INT64,
    -- sensitive PII
    customer_id INT64, 
    -- non-sensitive hash/bucket for partitioning
    -- e.g., MOD(customer_id, 100)
    id_bucket INT64 
)
PARTITION BY RANGE_BUCKET(
    id_bucket, 
    GENERATE_ARRAY(0, 100, 1)
)
CLUSTER BY order_id;
```

# Why this works for Security

*   **No PII Leakage:** The `id_bucket` (e.g., `23`) contains hundreds or thousands of different `customer_id` values. It is impossible to reverse-engineer a specific ID from the bucket alone.
*   **Performance:** While not as "surgical" as partitioning by exact ID, scanning 1% of a petabyte-scale table is still a **99% cost saving** compared to a full table scan.

> **Pro-tip:** To make this user-friendly, wrap the table in a **View** that automatically calculates the `id_bucket` in the `WHERE` clause, or use BigQuery's **Search Indexes** if the table isn't too large for them.

# How to solve the "Query Friction"

Asking users to remember `AND id_bucket = MOD(customer_id, 100)` is a recipe for failure. The ideal experience is for a user to simply query `WHERE customer_id = 123` and have pruning happen automatically.

### The "Smart View" Pattern

You can create a view that uses the `customer_id` from the user's query to calculate the `id_bucket`. Because of BigQuery's **predicate pushdown**, if the user filters on `customer_id`, the engine can often infer the bucket and prune the partitions.

```sql
-- The View
CREATE VIEW project.dataset.orders_view AS
SELECT 
    * 
FROM project.dataset.orders_base
WHERE id_bucket = MOD(customer_id, 100);

-- The User Query
SELECT * 
FROM project.dataset.orders_view
WHERE customer_id = 999123;

-- Result: BigQuery "pushes" the customer_id into the view logic,
-- calculates MOD(999123, 100) = 23, and prunes to id_bucket = 23.
```

*Note: Always verify the "Bytes Processed" in the query plan, as complex view nesting can sometimes break predicate pushdown.*

### Other Options
1.  **Standardize "Performance Columns":** Establish a naming convention (like `p_customer_id`) and educate users that filtering on this column is mandatory for large-scale performance.
2.  **Use Search Indexes:** For authorized users, a **Search Index** on the original `customer_id` column is the "modern" way to solve this. It provides point-lookup performance even on un-partitioned columns, completely bypassing the need for manual bucket logic.

# Comparison of Workarounds

| Approach | Security | Pruning | Complexity |
| :--- | :--- | :--- | :--- |
| **Hashed Bucket** | **Highest** | **High (99%)** | Low (1 extra column) |
| **Exact Shadow** | Medium | Full | Low (Leaks PII) |
| **Data Masking** | Medium | Partial | Medium |
| **Authorized Views**| High | Full | High (maintenance) |
| **Role Granting** | Low | Full | Very Low |

> **Pro-tip:** The Hashed Bucket pattern is the gold standard for **SOC2/GDPR compliance** because it provides performance without ever duplicating sensitive PII values.
