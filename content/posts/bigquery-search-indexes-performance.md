+++
title = 'BigQuery Search Indexes Performance'
featured_image = 'images/bq-search.png'
date = 2026-06-11T10:15:00+07:00
draft = false
tags = ['bigquery', 'performance', 'sql']
+++
# TL;DR
* Search indexes speed up `SEARCH()` and `CONTAINS_SUBSTR()`.
* Best for "needle-in-a-haystack" queries on large logs or JSON.
* Costs are primarily for storage and indexing throughput.

# When to use Search Indexes

## 1. Log Analytics
If you are searching for a specific `trace_id` or `error_code` in a table with billions of rows, a standard scan is expensive and slow.

```sql
-- Without index: Full scan
-- With index: Instant lookup
CREATE SEARCH INDEX my_index ON `my_project.logs.app_logs`(ALL COLUMNS);

SELECT * FROM `my_project.logs.app_logs` 
WHERE SEARCH(log_message, 'error-500');
```

## 2. JSON Blobs
BigQuery can index JSON fields, allowing you to search deep within nested structures without unnesting.

```sql
SELECT * FROM `my_project.events.raw_json` 
WHERE SEARCH(json_field, 'user_uuid_1234');
```

## 3. Performance vs Cost
While Search Indexes reduce query bytes processed, they add costs for **Data Management** and **Storage**. Use them selectively for tables with high query volume but low needle-to-haystack ratio.
