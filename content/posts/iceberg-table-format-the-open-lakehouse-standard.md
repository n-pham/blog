+++
title = 'Iceberg Table Format: The Open Standard'
featured_image = 'images/iceberg.png'
date = 2026-06-11T11:45:00+07:00
draft = false
tags = ['iceberg', 'data-lake', 'architecture']
+++
# TL;DR
* Apache Iceberg brings SQL-like ACID transactions to your Data Lake.
* It supports "Time Travel" and "Schema Evolution."
* Works with Spark, Trino, Flink, and Snowflake.

# Hidden Metadata
Iceberg tracks every file in your lake via a metadata tree. This allows it to perform **Partition Evolution**—you can change how a table is partitioned without rewriting the entire dataset.
