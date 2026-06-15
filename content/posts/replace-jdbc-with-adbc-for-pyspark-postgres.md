+++
title = 'Replace JDBC with ADBC for PySpark - Postgres'
date = 2026-06-11T22:00:00+07:00
draft = false
tags = ['spark', ]
+++
# Replace JDBC with ADBC for PySpark - Postgres

Apache Arrow removes the data serialization overhead between Python and Postgres. 
* **Reading** with Arrow-native protocols eliminates row-to-column serialization.
* **Writing** with ADBC eliminates thousands of `INSERT INTO` statements via bulk ingestion.

## Comparing Arrow-native Methods

| Feature | Arrow Flight SQL | ADBC | DataFusion Comet + ADBC |
| :--- | :--- | :--- | :--- |
| **Server Requirements** | Requires `pg_flight` extension | Standard Postgres | Standard Postgres |
| **Client Requirements** | JDBC Flight SQL Driver | ADBC JNI Drivers | Spark Plugin + ADBC JNI |
| **Transfer Protocol** | Flight SQL protocol | Native Postgres wire | Native Postgres wire |
| **I/O Strategy** | Columnar (Arrow) | Columnar (Arrow) | Columnar (Arrow) |
| **Execution** | JVM-based | JVM-based | **Vectorized (Native Rust)** |

## Read data from Postgres

### Standard JDBC (Baseline)
```python
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://host:5432/db") \
    .option("dbtable", "source_table") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
```

### Arrow Flight SQL (for reference)
*Requires the `pg_flight` extension on the Postgres server.*
```python
spark = ... \
    .config("spark.jars.packages", "org.apache.arrow:flight-sql-jdbc-driver:15.0.0")
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:arrow-flight-sql://postgres-host:32010") \
    .option("dbtable", "source_table") \
    .load()
```

### ADBC + DataFusion Comet (Recommended)
*No server extension required. Best performance for computation-heavy queries.*
```python
spark = ... \
    .config("spark.plugins", "org.apache.spark.CometPlugin") \
    .config("spark.comet.enabled", "true") \
    .config("spark.comet.experimental.sparkToColumnar", "true") \
    .config("spark.jars.packages", "com.tokoko:spark-adbc_2.12:0.1.0,org.apache.arrow.adbc:adbc-driver-postgresql:0.12.0")

df = spark.read \
    .format("com.tokoko.spark.adbc") \
    .option("driver", "org.apache.arrow.adbc.driver.jni.JniDriverFactory") \
    .option("jni.driver", "postgresql") \
    .option("uri", "postgresql://user:password@host:5432/db") \
    .option("dbtable", "source_table") \
    .load()
```

## Write data to Postgres

### Driver-side Write (ADBC Driver)
*When data is already collected on the driver.*
```python
import adbc_driver_postgresql.dbapi as adbc_psql
import pyarrow

arrow_table = pyarrow.Table.from_pandas(df.to_pandas())
with adbc_psql.connect("postgresql://user:password@host:5432/db") as conn:
    with conn.cursor() as cursor:
        cursor.adbc_ingest("target_table", arrow_table, mode="append")
```

### Standard JDBC Bulk Copy
```python
(df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://host:5432/db") \
    .option("dbtable", "target_table") \
    .option("user", "username") \
    .option("password", "password") \
    .option("batchsize", "10000") \
    .option("reWriteBatchedInserts", "true") \
    .mode("append") \
    .save())
```

### Distributed Write (ADBC Executors)
*Highly efficient for massive datasets.*
```python
(df.write
    .format("com.tokoko.spark.adbc")
    .option("driver", "org.apache.arrow.adbc.driver.jni.JniDriverFactory")
    .option("jni.driver", "postgresql")
    .option("uri", "postgresql://user:password@host:5432/db") \
    .option("dbtable", "target_table") \
    .mode("append") \
    .save())
```

# Scala Spark - Postgres

## Read data from Postgres
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
