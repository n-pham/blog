+++
title = 'Airflow vs Dagster: The Declarative Shift'
featured_image = 'images/orchestration.png'
date = 2026-06-11T11:05:00+07:00
draft = false
tags = ['airflow', 'dagster', 'orchestration']
+++
# TL;DR
* Airflow focuses on **workflows** (tasks); Dagster focuses on **data assets**.
* Dagster's declarative approach makes local testing and lineage easier.
* Airflow's maturity means better integration with legacy systems.

# Task-based vs Asset-based
In Airflow, you define "Do Task A, then Task B." If Task B fails, you don't inherently know which data is broken. 

In Dagster, you define "Asset B depends on Asset A." The orchestrator understands the state of your data, not just the success of your scripts.

```python
# Dagster Example
@asset
def raw_users():
    return pd.read_csv("users.csv")

@asset(deps=[raw_users])
def clean_users(raw_users):
    return raw_users.dropna()
```
