+++
title = 'BigQuery QUALIFY Introduces Filter Ambiguity'
date = 2026-09-11T10:00:00+07:00
draft = false
tags = ['bigquery', 'sql']
+++

# BigQuery QUALIFY Introduces Filter Ambiguity

To show rows where latest tasks failed:

<table>
<tr>
<td>
  
```sql
with t as (
  select 1 as task_id,
         1001 as modified_ts,
         'passed' as status
  union all select 1, 1002, 'failed'
  union all select 2, 2001, 'failed'
  union all select 2, 2002, 'passed'
)
select *
from t
where 1=1

and status = 'failed'
qualify row_number() over(
  partition by task_id
  order by modified_ts desc) = 1
/*
task_id	modified_ts	status
1       1002        failed
2       2001        failed      WRONG
*/
```

`status = 'failed'` runs **BEFORE** `qualify`
</td>
<td>

```sql
with t as (
  select 1 as task_id,
         1001 as modified_ts,
         'passed' as status
  union all select 1, 1002, 'failed'
  union all select 2, 2001, 'failed'
  union all select 2, 2002, 'passed'
)
select *
from t
where 1=1

qualify row_number() over(
  partition by task_id
  order by modified_ts desc) = 1
and status = 'failed'
/*
task_id	modified_ts	status
1       1002        failed
                                CORRECT
*/
```

`status = 'failed'` runs **AFTER** `qualify`
</td>
</table>