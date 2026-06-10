+++
title = 'BigQuery Policy Tag Limitation with Partition'
date = 2026-05-17T10:00:00+07:00
draft = false
tags = ['bigquery', 'security', 'partition', 'cost']
+++

# BigQuery Policy Tag Limitation with Partition

1. Issue with BQ Policy Tag on Partition

```sql
-- Range Partition customer_id
-- customer_id has policy tag
SELECT * 
FROM orders
WHERE customer_id = 999123
-- Scans 100% of table bytes 
-- (or throws Access Denied)
```

2.  Non-Sensitive Bucket Hash

```sql
-- Partition bucket_hash = MOD(customer_id, 100)
-- customer_id has policy tag
SELECT * 
FROM orders
WHERE customer_id = 999123
  AND bucket_hash = 23 -- MOD(999123, 100)
-- Pruning works, only 1/100th of the table scanned
```

3. Hiding Details from Users

```sql
CREATE VIEW project.dataset.orders_view AS
SELECT * 
FROM project.dataset.orders
WHERE bucket_hash = MOD(customer_id, 100);

-- User Query
SELECT * 
FROM project.dataset.orders_view
WHERE customer_id = 999123;
-- Result: BigQuery "pushes" the customer_id into the view logic,
-- calculates MOD(999123, 100) = 23, and prunes to bucket_hash = 23.
```

4. Optimization for Authorized Users
* Add **Search Index** on customer_id in the base orders table
* Same SQL  
```sql
SELECT * 
FROM project.dataset.orders_view
WHERE customer_id = 999123;
-- Result: BigQuery optimizer should skip the partition pruning entirely 
-- and use the Search Index for a point lookup (scanning ~0 bytes).
```


**Note:** Always verify the "Bytes Processed" in the query plan, as complex view nesting can sometimes break predicate pushdown.
