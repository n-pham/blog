+++
title = 'dbt Model Versioning'
featured_image = 'images/dbt-model-versioning.png'
date = 2025-04-25T14:15:00+07:00
draft = false
tags = ['dbt', 'datamodel']
+++
# dbt model versioning to avoid breaking downstream consumers

Models A -> B -> Consumers.

There is a major change in B to be observed on production for some time before publishing to consumers.

Versioning model B is the perfect approach for this use case to test-drive new logic while limiting code changes to a single model.


Existing consumers:
> SELECT * FROM b;

New logic data:
> SELECT * FROM b_v2;

```yaml
models:
  - name: b
    latest_version: 1
    versions:
      - v: 1
        defined_in: b
        config:
          alias: b
      - v: 2
        defined_in: b_v2
```
