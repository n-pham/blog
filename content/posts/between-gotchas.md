+++
title = 'BETWEEN Gotchas'
date = 2026-08-24T10:00:00+07:00
draft = false
tags = ['sql', 'spark']
+++

# BETWEEN Gotchas

*  ```sql
   WHERE timestamp BETWEEN '2026-01-01' AND '2026-01-02'
   ```
*  ```python
   df.filter(df.timestamp.between('2026-01-01', '2026-01-02'))
   ```

Both wrongly include records on Jan 02 because `BETWEEN` is inclusive of the upper-bound value.
This is the most common reason for off-by-one counts.

Fix: Explicitly write the condition with `>=` and `<`.

*  ```sql
   WHERE timestamp >= '2026-01-01' AND timestamp < '2026-01-02'
   ```
*  ```python
   df.filter((df.timestamp >= '2026-01-01') & (df.timestamp < '2026-01-02'))
   ```