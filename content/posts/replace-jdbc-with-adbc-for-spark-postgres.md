+++
title = 'Replace JDBC with ADBC for Spark - Postgres'
date = 2026-06-11T22:00:00+07:00
draft = false
tags = ['spark', ]
+++
# Replace JDBC with ADBC for Spark - Postgres

Apache Arrow removes the data serialization overhead between JDBC and Postgres.
* reading Postgres with Arrow-powered JDBC will eliminate row-to-column data serialization
* writing Postgres with ADBC will eliminate data serialization and thousands of INSERT INTO statements

## Read data from Postgres

Ensure Postgres `pg_flight` extension is enabled.

```python
spark = ... \
    .config("spark.jars.packages", "org.apache.arrow:flight-sql-jdbc-driver:15.0.0")
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:arrow-flight-sql://postgres-host:32010") \
    .load()
```

## Write data to Postgres
```python
import adbc_driver_postgresql.dbapi as adbc_psql
import pyarrow

pandas_df = spark_df.to_pandas()
arrow_table = pyarrow.Table.from_pandas(pandas_df)
with adbc_psql.connect("postgresql://user:password@host:5432/db") as conn:
    with conn.cursor() as cursor:
        cursor.adbc_ingest("target_table", arrow_table, mode="append")
```