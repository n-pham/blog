+++
title = 'DBT Gotchas'
date = 2026-10-27T10:00:00+07:00
draft = false
tags = ['dbt', ]
+++

# Confusing logs

> dbt run --full-refresh -s m

> OK created sql **incremental** model m [CREATE TABLE]

I want full-refresh, **incremental** makes me think model m was not full-refreshed.<br/>
(Although it was, hinted by **CREATE TABLE**.)


# Inconsistent DBT compile

DBT compile produces inconsistent SQL depending on target, vars, full-refresh param and table existence.


# Macro code change triggers state:modified+ 

With `state:modified+`, a single macro code change will trigger all related and downstream models, together with data tests, metrics and semantic layers.


# Elusive full table scan

* partition field in where is wrong data type or wrapped in function or compared with dynamic value 
* read from {{ this }} without partition filter
* unique_key is not in partition or cluster configuration

# Select parameter needs Math

Can you spot the incorrect dbt select lines?
```
dbt run --select \
            m+   \
           +m    \
           +m+   \
            m+1  \
          1+m    \
            m++  \
          ++m    \
            tag:schedule-1+1
```
