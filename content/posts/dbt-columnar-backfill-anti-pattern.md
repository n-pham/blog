+++
title = 'DBT Columnar Backfill Anti-Pattern'
date = 2026-11-23T10:00:00+07:00
draft = false
tags = ['dbt']
+++


# DBT Columnar Backfill Anti-Pattern

To backfill new columns in dbt BigQuery, the standard `--full-refresh` rewrites petabytes of historical data, burns compute, and completely ignores BigQuery and some others' actual superpower: true columnar storage.

Instead, use these 2 SQLs:

```sql
-- instant metadata schema evolution
ALTER TABLE `your_project.your_dataset.your_table`
ADD COLUMN new_field STRING;

-- targeted partition-aware update
UPDATE `your_project.your_dataset.your_table`
SET new_field = subquery.calculated_value
FROM (
    -- logic to derive the historical value
    SELECT id, some_logic AS calculated_value
    FROM `your_project.your_dataset.source_table`
) AS subquery
WHERE `your_project.your_dataset.your_table`.id = subquery.id
  -- ALWAYS filter by partition/date to control costs:
  AND `your_project.your_dataset.your_table`.date_partition >= '2025-01-01';
```

Then configure dbt so future incremental runs include the new field without rebuilding history:

```yaml
models:
  - name: your_table
    config:
      materialized: incremental
      on_schema_change: append_new_columns
```
