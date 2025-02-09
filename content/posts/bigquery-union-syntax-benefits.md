+++
title = 'BigQuery UNION syntax benefits'
featured_image = 'images/bigquery-union-syntax-benefits.png'
date = 2025-02-09T17:52:39+07:00
draft = false
tags = ['bigquery', 'pipe', 'sql', 'simplicity']
+++
# UNION with Fewer Columns

<blockquote>

LEFT UNION ALL BY NAME

</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price
    union all
    select 'p2', 10
),
products_2 as ( -- secondary source
    select 'p1' as product_id
    union all
    select 'p3'
),
products_new as (
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)
select product_id, price
from products_1
union all
select product_id, null
from products_new
```
  
</td>
<td>

```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price
    union all
    select 'p2', 10
),
products_2 as ( -- secondary source
    select 'p1' as product_id
    union all
    select 'p3'
)
select * from products_1
|>  left union all by name
( -- products_new
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)


 
```

</td>
</tr>
</table>

# UNION with New Column 

<blockquote>

New column `weight` is added in primary source first, then both.

LEFT UNION ALL BY NAME needs **no change**.

</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price, 1 as weight
    union all
    select 'p2', 10, 2
),
products_2 as ( -- secondary source without weight
    select 'p1' as product_id
    union all
    select 'p3'
),
products_new as (
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)
select product_id, price, weight
from products_1
union all
select product_id, null, null
from products_new
```
  
</td>
<td>

```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price, 1 as weight
    union all
    select 'p2', 10, 2
),
products_2 as ( -- secondary source without weight
    select 'p1' as product_id
    union all
    select 'p3'
)
select * from products_1
|>  left union all by name
( -- products_new
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)


 
```

</td>
</tr>

<tr>
<td>
  
```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price, 1 as weight
    union all
    select 'p2', 10, 2
),
products_2 as ( -- secondary source with weight
    select 'p1' as product_id, 1 as weight
    union all
    select 'p3', 3
),
products_new as (
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)
select product_id, price, weight
from products_1
union all
select product_id, null, weight
from products_new
```
  
</td>
<td>

```sql
with products_1 as ( -- primary source
    select 'p1' as product_id, 5 as price, 1 as weight
    union all
    select 'p2', 10, 2
),
products_2 as ( -- secondary source with weight
    select 'p1' as product_id, 1 as weight
    union all
    select 'p3', 3
)
select * from products_1
|>  left union all by name
( -- products_new
    select p2.*
    from products_2 p2
    left outer join products_1 p1
        on p1.product_id = p2.product_id
    where p1.product_id is null
)


 
```

</td>
</tr>
</table>