+++
title = 'Relational Database Update in Batches'
featured_image = 'images/relational-database-update-in-batches.png'
date = 2024-09-19T09:45:00+07:00
draft = false
tags = ['relational', 'database', 'batch', 'update', 'lock', 'transaction']
+++
# Heavy Update Transactions

```sql
UPDATE inventory SET quantity = <select from another table>
```

That query is running for more than 5 mins, then customers complain that orders cannot be completed.

The only fix is to cancel the update, and wait for hours for the database to complete rollback.

Above is a very common scenario with relational database, which can be avoided by the method **update in batches**.

# Relational Database Lock with Heavy Update Transactions

Reason for the issue is database lock and transaction.

To ensure ACID, relational databases keep **locks in all rows being updated for the whole duration of the update transaction**.

If the query above updates 10K rows in inventory table, to be finished in 5 mins then in 5 mins all related orders cannot be placed.

# Update in Batches

Divide the update into **batches of smaller updates and commit after each batch**.

For example if using 20 batches, each batch will update 10K/20=500 rows, finish in 5m/20=15s, orders wait for maximum 15s only.

```sql
-- Update in Batches
-- start_id = 1
-- batch_size = 499
-- run multiple times
UPDATE inventory
SET quantity = <select from another table>
WHERE inventory.id BETWEEN :start_id AND :start_id + :batch_size ;
COMMIT;
-- start_id = start_id + batch_size + 1
```


<br/>
<br/>
<br/>


Note: there are other work-arounds such as running UPDATE during off-peak hours or even a maintenance duration.