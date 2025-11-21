+++
title = 'BigQuery Pipe syntax examples'
date = 2025-11-21T17:52:39+07:00
draft = false
tags = ['bigquery', 'pipe', 'sql']
+++
# BigQuery Pipe syntax examples
  
```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', cast(NULL as integer)
) select * from products
|> aggregate count(*) as count_all, count(price) as count_not_null
|> extend if(count_all = count_not_null, 'PASS', 'FAIL') as test_result
-- count_all    count_not_null    test_result
--         2                 1           FAIL
```