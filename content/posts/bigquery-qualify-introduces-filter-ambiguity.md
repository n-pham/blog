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

# UNION with QUALIFY

<table>
<tr>
<td>

```sql
with t1 as (
  select 1 as id, 'a' as val
  union all select 1, 'b'
),
t2 as (
  select 1 as id, 'c' as val
  union all select 1, 'd'
)
select *
from t1
union all
select *
from t2
qualify row_number() over (
  partition by id order by val) = 1
/*
id val
 1   a   
 1   b  
 1   c    QUALIFY only works on t2
*/
```

Surprise: `QUALIFY` runs **only on t2**!
</td>
<td>

```sql
with t1 as (
  select 1 as id, 'a' as val
  union all select 1, 'b'
),
t2 as (
  select 1 as id, 'c' as val
  union all select 1, 'd'
)
select * from (
  select * from t1
  union all
  select * from t2
)
qualify row_number() over (
  partition by id order by val) = 1
/*
id val
 1   a    QUALIFY works on both
*/

 
```

Wrap in subquery to apply QUALIFY to both.
</td>
</tr>
</table>
