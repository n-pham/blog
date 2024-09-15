+++
title = 'The Zen of Python, for SQL'
featured_image = 'images/the-zen-of-python-for-sql.png'
date = 2024-09-11T06:20:00+07:00
draft = false
tags = ['python', 'sql', 'readability', 'simplicity']
+++
# Naming convention

<blockquote>

"Beautiful is better than ugly."

"Readability counts."

<!-- \- The Zen of Python -->
</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with cte (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select count(*)
from cte
```
  
</td>
<td>

```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select count(*) as product_count
from products
```

</td>
</table>

# Explicit SELECT

<blockquote>

"Explicit is better than implicit."

<!-- \- The Zen of Python -->
</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with product_1 (product_id, price) as (
    select 'p1', 5
)
, product_2 (price, product_id) as (
    select 10, 'p2'
)
select * from product_1
union all
select * from product_2
-- ERROR: UNION types text and integer
-- cannot be matched
```
  
</td>
<td>

```sql
with product_1 (product_id, price) as (
    select 'p1', 5
)
, product_2 (price, product_id) as (
    select 10, 'p2'
)
select product_id, price from product_1
union all
select product_id, price from product_2


```

</td>
</tr>
</table>

# Simplicity

<blockquote>

"Simple is better than complex."

"Flat is better than nested."

<!-- \- The Zen of Python -->
</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select
	classification,
    count(*)
from (
    select
        case
            when price > 5
            then 'Expensive'
            else 'Cheap'
        end as classification
    from products
) t
group by classification
/*
classification |	count
Cheap	            1
Expensive	        1
*/
```
  
</td>
<td>

```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select
	count(*) as total,
	count(*) filter (
        where price > 5
    ) as expensive_count
from products







/*
total |	expensive_count
2	    1

*/

```

</td>
</tr>
<tr>
<td>
  
```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select product_id
from (
	select product_id,
    row_number() over(
        order by price desc) as rn
	from products
) t
where rn = 1
```
  
</td>
<td>

```sql
with products (product_id, price) as (
    select 'p1', 5
    union all
    select 'p2', 10
)
select product_id
from products
-- BigQuery syntax
qualify row_number() over(
    order by price desc) = 1
```

</td>
</tr>
<tr>
<td>

```sql
-- Added on 2024-09-15
with product_1 (product_id, price) as (
    select 'p1', 5
)
, product_2 (product_id, price) as (
    select 'p2', cast(NULL as integer)
)
select *
from product_1 as p1
inner join product_2 as p2
on p1.price != p2.price
   or p1.price is null
      and p2.price is not null
   or p1.price is not null
      and p2.price is null
```
  
</td>
<td>

```sql
-- PostgreSQL, SQL Server
with product_1 (product_id, price) as (
    select 'p1', 5
)
, product_2 (product_id, price) as (
    select 'p2', cast(NULL as integer)
)
select *
from product_1 as p1
inner join product_2 as p2
on p1.price is distinct from p2.price



```

</td>
</tr>
</table>

# Error handling

<blockquote>

"Errors should never pass silently."

<!-- \- The Zen of Python -->
</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
-- SQL Server
select try_cast('1.0' as int) as num
-- NULL

```
  
</td>
<td>

```sql
-- SQL Server
select cast('1.0' as int) as num
-- Conversion failed when converting
-- the varchar value '1.0' to data type int.
```

</td>
</table>