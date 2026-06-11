+++
title = 'Data Observability vs Data Quality'
featured_image = 'images/observability.png'
date = 2026-06-11T11:25:00+07:00
draft = false
tags = ['observability', 'data-quality']
+++
# TL;DR
* **Data Quality**: "Is this specific value correct?" (dbt tests).
* **Data Observability**: "Is the whole system healthy?" (Volume, Freshness, Schema changes).
* You need both for a reliable data platform.

# Monitoring the "Unknown Unknowns"
Tests catch what you expect to break. Observability catches the anomalies you didn't anticipate, like a source suddenly sending 0 rows or a column name changing without notice.

**Key Pillars:**
1. **Freshness**: When was the table last updated?
2. **Volume**: Did we get 1 million rows or 100?
3. **Distribution**: Did the average order value drop by 90%?
