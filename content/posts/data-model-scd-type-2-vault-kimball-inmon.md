+++
title = 'Data Model SCD Type 2, Vault, Kimball, Inmon'
date = 2026-01-22T17:52:39+07:00
draft = false
tags = ['datamodel', ]
+++
# SCD Type 2, 6NF/7NF, Data Vault

```text
SCD Type 2: One big table, all attributes together, duplicates on change.

 ProductID | Name    | Category    | Price | ValidFrom  | ValidTo
-----------+---------+-------------+-------+------------+----------
 456       | iPhone9 | Electronics | 1000  | 2020       | 2021
 456       | iPhone9 | Electronics | 900   | 2021       | 2022
 456       | iPhone9 | Computers   | 900   | 2022       | NULL


6NF/7NF:   Each table per attribute 

 ProductID | Name    | ValidFrom  | ValidTo
-----------+---------+------------+----------
 456       | iPhone9 | 2020       | NULL


 ProductID | Price | ValidFrom  | ValidTo
-----------+-------+------------+----------
 456       | 1000  | 2020       | 2021
 456       | 900   | 2021       | NULL


 ProductID | Category    | ValidFrom  | ValidTo
-----------+-------------+------------+----------
 456       | Electronics | 2020       | 2022
 456       | Computers   | 2022       | NULL


Data Vault: Source-based grouping 

 ProductID | BusinessKey
-----------+-------------
 456       | iPhone9

 ProductID | Category    | Price | Source           | LoadDate
-----------+-------------+-------+------------------+----------
 456       | Electronics | 1000  | Dell ERP         | 2020
 456       | Electronics | 900   | Distributor Feed | 2021
 456       | Electronics | 900   | Dell ERP         | 2021
 456       | Computers   | 900   | Dell ERP         | 2022
```

# Inmon vs Kimball

Inmon builds Kimball-like views in Data Mart from core 3NF EDW

```sql
create view SalesMart.DimProduct as
select 
    md5_hash(p.ProductID || ph.EffectiveDate) AS ProductSK, 
    *
from CoreEDW.Product p
join CoreEDW.ProductCategory c on p.CategoryID = c.CategoryID
join CoreEDW.ProductPriceHistory ph on p.ProductID = ph.ProductID;
```
