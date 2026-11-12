+++
title = 'DBT Early Production Detection Of Source Schema Breaks'
date = 2026-11-12T10:00:00+07:00
draft = false
tags = ['dbt', 'datamodel']
+++
# DBT Early Production Detection Of Source Schema Breaks

DBT model schema breaks are detected in development.

Meanwhile, source schema breaks are only detected after the production pipeline fails.

Use this zero-cost pre-flight production schema validation:
```bash
dbt build --select stg_* staging --empty
```

Your staging models following DBT design pattern should already select each field and therefore will fail in case of a rename or removal.
