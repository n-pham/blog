+++
title = 'DBT Hourly Refresh Anti-Pattern'
date = 2026-03-06T10:00:00+07:00
draft = false
tags = ['dbt', 'sql']
+++


# DBT Hourly Refresh Anti-Pattern

When we join a Daily heavy table (Fact) with an Hourly light table (Status update), we often fall into a costly trap: materializing the result as a table.

The moment it is materialized, data becomes stale. To keep statuses fresh, we are forced to run the entire heavy model hourly, wasting massive compute credits on data that hasn't actually changed.

The Solution: Base Table + View Pattern to break the dependency by separating heavy transformations from the "fresh" join.

1. fact_base (Table/Incremental): Run this Daily. Do all the heavy lifting, complex logic, and historical processing here.
2. fact_final (View): This view simply joins fact_base with Hourly status table.

```sql
-- fact_final (View)
select
    base.*,
    s.current_status
from {{ ref('fact_base') }} base
left join {{ ref('hourly_status_lookup') }} s
    on base.user_id = s.user_id
```

Why this works:

* Cost Efficiency: The heavy model only runs once a day.
* Instant Freshness: Since the final layer is a view, it fetches the latest statuses from the hourly table at query time.
* Cleaner Lineage: we stop the "chain reaction" of hourly refreshes from propagating through the entire DAG.
