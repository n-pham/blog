+++
title = 'dbt Tests: Beyond Generic'
featured_image = 'images/dbt-tests.png'
date = 2026-06-11T10:05:00+07:00
draft = false
tags = ['dbt', 'data-quality']
+++
# TL;DR
* Move beyond `unique` and `not_null`.
* Use **Singular Tests** for complex business logic.
* Implement **Relationship Tests** across different sources.

# High-Quality Testing in dbt

## 1. Singular Tests for Business Logic
Generic tests are great for schema validation, but they can't verify that "Total Revenue must equal Sum of Line Items". For this, use a singular test in the `tests/` directory.

```sql
-- tests/assert_revenue_matches_items.sql
select
    order_id,
    revenue,
    item_sum
from {{ ref('orders') }}
where abs(revenue - item_sum) > 0.01
```

## 2. Cross-Source Integrity
Ensuring that data in your warehouse matches your source system is critical. Use `dbt_utils.equality` or custom relationship tests.

```yaml
models:
  - name: dim_customers
    tests:
      - dbt_utils.equality:
          compare_model: ref('stg_crm__customers')
          compare_columns: ['customer_id', 'email']
```

## 3. Data Contracts
Define what your data *should* look like before it breaks downstream. Use `contracts` in dbt 1.5+ to enforce schema at the model level.
