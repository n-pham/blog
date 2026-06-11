+++
title = 'RisingWave vs Flink: Streaming SQL'
featured_image = 'images/streaming.png'
date = 2026-06-11T11:35:00+07:00
draft = false
tags = ['streaming', 'sql', 'flink']
+++
# TL;DR
* Flink is the heavyweight champion of streaming; RisingWave is the SQL-first newcomer.
* RisingWave looks and feels like Postgres but handles streaming data.
* Use Streaming SQL for real-time dashboards and fraud detection.

# The Postgres of Streaming
RisingWave allows you to create materialized views that update in real-time as data flows through Kafka.

```sql
CREATE MATERIALIZED VIEW live_sales AS
SELECT item_id, SUM(price) as total_revenue
FROM sales_stream
GROUP BY item_id;
```
No need to write complex Java/Scala Flink jobs for simple aggregations.
