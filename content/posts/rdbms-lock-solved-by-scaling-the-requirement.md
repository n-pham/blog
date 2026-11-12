+++
title = 'RDBMS Lock Solved By Scaling The Requirement'
date = 2026-11-11T10:00:00+07:00
draft = false
tags = ['database', 'datamodel']
+++
# RDBMS Lock Solved By Scaling The Requirement

A list with adjustable admin ordering created global database locking on save.

| item_id | item_name  | position |
| :--- | :--- | :--- |
| 1       | A | 1                |
| 2       | B  | 2                |
| 3       | C | 3                |
| 4       | D | 4                |

It was solved by actually scaling the requirement: optionaly letting each user define their own ordering.

| user_id | item_id | position |
| :--- | :--- | :--- |
| 1       | 3       | 1        |
| 1       | 1       | 2        |
| 1       | 4       | 3        |
| 1       | 2       | 4        |

```sql
SELECT 
    i.item_id,
    i.item_name,
    COALESCE(uip.position, i.position) AS position
FROM items i
LEFT JOIN user_item_positions uip 
    ON i.item_id = uip.item_id 
   AND uip.user_id = :user_id
ORDER BY position ASC;
```
