+++
title = 'DBT Macro is Bad for Business Logic'
date = 2026-04-19T10:00:00+07:00
draft = false
tags = ['dbt', 'datamodel', 'macro']
+++
# DBT Macro is Bad for Business Logic

Macro is good for technical logic (e.g. format, SCD2 from and to dates), but is bad for business logic:

* invisible in in data lineage
* macro cannot be unit tested
* every other re-use in model needs a redundant unit test
* technically complex for business user to work on

For business logic re-use, apply a design pattern that puts logic in a single upstream model, instead of macro.
