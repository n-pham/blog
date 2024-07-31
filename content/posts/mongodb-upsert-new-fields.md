+++
title = 'MongoDB upsert new fields'
featured_image = 'images/mongodb-upsert-new-fields.png'
date = 2024-07-31T15:52:39+07:00
draft = false
tags = ['mongodb', 'spark', 'upsert']
+++
# operationType update
When MongoDB Spark Connector upserts data, fields that are not in the data frame are **removed by default**.

In cases where we only want to upsert new fields while keeping existing fields, remember to set `operationType` to `update` in `options`.

This is much more effective than:

1. read all documents out into memory
2. declare or infer the schema
3. add new fields to data frame
4. write data frame back into MongoDB



# Sample Code
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.config(
    "spark.jars.packages",
    "org.mongodb.spark:mongo-spark-connector_2.12:10.2.2",
).getOrCreate()

URI = "mongodb+srv://<user>:<password>@<url>/<database>"
options = {
    "collection": "test_upsert_partial",
    "connection.uri": URI,
}

# Set up test data
df_existing = spark.createDataFrame(
    [
        ("A", "A1", "A2"),
        ("B", "B1", "B2"),
    ],
    schema="_id:string,field_1:string,field_2:string",
)
(
    df_existing.write.format("mongodb").mode("append")
    .options(**options)
    .save()
)

spark.read.format("mongodb").options(**options).load().show()
"""
+---+-------+-------+                                                           
|_id|field_1|field_2|
+---+-------+-------+
|  A|     A1|     A2|
|  B|     B1|     B2|
+---+-------+-------+
"""
df_new = spark.createDataFrame(
    [
        ("B", "B1_NEW"),
        ("C", "C1"),
    ],
    schema="_id:string,field_1:string",
)
df_new.show()
'''
+---+-------+
|_id|field_1|
+---+-------+
|  B| B1_NEW|
|  C|     C1|
+---+-------+
'''

# Test writing new fields WITHOUT 'update' as 'operationType'


options = {
    "collection": "test_upsert_partial",
    'connection.uri': URI,
    # operationType != 'update' will REMOVE existing fields
    # "operationType": "update",
}
(
    df_new.write.format("mongodb").mode("append")
    .options(**options)
    .save()
)


spark.read.format('mongodb').options(**options).load().show()
'''
+---+-------+-------+                                                           
|_id|field_1|field_2|
+---+-------+-------+
|  A|     A1|     A2|
|  B| B1_NEW|   null| <-- field_2 of _id B was removed
|  C|     C1|   null|
+---+-------+-------+
'''
```
