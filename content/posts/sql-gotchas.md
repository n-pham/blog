+++
title = 'SQL Gotchas'
featured_image = 'images/sql-gotchas-not-in-null.gif'
date = 2026-11-05T10:00:00+07:00
draft = false
tags = ['bigquery', 'sql']
+++

# SQL Gotchas

<table>
<tr>
<td>
  
```sql
with a as (
  select 1 as id
  union all select 2
),
b as (
  select 2 as id
  union all select 3
  union all select NULL
)
select *
from a
left join b on a.id = b.id
where b.id = 2

-- id    id
--  2     2
 
```

</td>
<td>

```sql
with a as (
  select 1 as id
  union all select 2
),
b as (
  select 2 as id
  union all select 3
  union all select NULL
)
select *
from a
left join b on a.id = b.id
            and b.id = 2

-- id    id
--  1  NULL
--  2     2
```

</td>
</tr>
<tr>
<td>
  
```sql
with a as (
  select 1 as id
  union all select 2
),
b as (
  select 2 as id
  union all select 3
  union all select NULL
)
select *
from a
where id not in (
  select id from b)

-- 0 row
 
```

</td>
<td>

```sql
with a as (
  select 1 as id
  union all select 2
),
b as (
  select 2 as id
  union all select 3
  union all select NULL
)
select *
from a
where not exists (
  select 1 from b
  where b.id = a.id)
-- id
--  3
```

</td>
</tr>
</table>
