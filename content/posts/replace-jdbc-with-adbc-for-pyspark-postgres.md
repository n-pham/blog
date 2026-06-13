+++
title = 'Replace JDBC with ADBC for PySpark - Postgres'
date = 2026-06-11T22:00:00+07:00
draft = false
tags = ['spark', ]
+++
# Replace JDBC with ADBC for PySpark - Postgres

Apache Arrow removes the data serialization overhead between Python and Postgres.
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

## Write driver data to Postgres

*When dataframe is already on the driver.*

```python
import adbc_driver_postgresql.dbapi as adbc_psql
import pyarrow

pandas_df = spark_df.to_pandas()
arrow_table = pyarrow.Table.from_pandas(pandas_df)
with adbc_psql.connect("postgresql://user:password@host:5432/db") as conn:
    with conn.cursor() as cursor:
        cursor.adbc_ingest("target_table", arrow_table, mode="append")
```

## Write distributed data to Postgres

*Set options for Bulk Copy, ADBC is not needed.*

```python
(spark_df.write
    .format("jdbc")
    .option("url", "jdbc:postgresql://host:5432/db")
    .option("dbtable", "target_table")
    .option("user", "username")
    .option("password", "password")
    .option("batchsize", "10000")
    .option("reWriteBatchedInserts", "true") # Critical for Postgres performance
    .mode("append")
    .save())
```

*Or use COPY protocol via psycopg2 for even higher performance.*

# Scala Spark - Postgres

## Read data from Postgres

*No other option is needed.*

```scala
val df = spark.read
  .format("jdbc")
  .option("url", "jdbc:postgresql://host:5432/db")
  .option("dbtable", "target_table")
  .option("user", "username")
  .option("password", "password")
  .load()
```

## Write data to Postgres

*Still need options for Bulk Copy.*

```scala
df.write
  .format("jdbc")
  .option("url", "jdbc:postgresql://host:5432/db")
  .option("dbtable", "target_table")
  .option("user", "username")
  .option("password", "password")
  .option("batchsize", "10000")
  .option("reWriteBatchedInserts", "true")
  .mode("append")
  .save()
```