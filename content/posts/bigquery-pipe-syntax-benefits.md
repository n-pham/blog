+++
title = 'BigQuery Pipe syntax benefits'
featured_image = 'images/bigquery-pipe-syntax-benefits.png'
date = 2025-02-06T17:52:39+07:00
draft = false
tags = ['bigquery', 'pipe', 'sql', 'simplicity']
+++
# End of Subquery Madness

<blockquote>

"pipe operator can see every alias that exists"

</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```sql
with products as (
    select 'p1' as product_id, 5 as price
    union all
    select 'p2', 10
),
product_classification as (
    select
        *,
        case
            when price > 5
            then 'Expensive'
            else 'Cheap'
        end as classification
    from products
)
select product_id, classification
from product_classification
where classification = 'Cheap'

-- error without subquery
with products as (
    select 'p1' as product_id, 5 as price
    union all
    select 'p2', 10
)
select
    product_id,
    case
        when price > 5
        then 'Expensive'
        else 'Cheap'
    end as classification
from products
where classification = 'Cheap'
-- ERROR Unrecognized name: classification
```
  
</td>
<td>

```sql
with products as (
    select 'p1' as product_id, 5 as price
    union all
    select 'p2', 10
) select * from products
|> extend
    case
        when price > 5
        then 'Expensive'
        else 'Cheap'
    end as classification
|> where classification = 'Cheap'
|> select product_id, classification









```

</td>
</tr>
</table>
