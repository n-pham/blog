+++
title = 'Spark Join Clean Code'
featured_image = 'images/spark-join-clean-code.png'
date = 2024-01-13T15:52:39+07:00
draft = false
tags = ['spark', 'join']
+++
# TL;DR
* If inner join columns have the same name, then use `on` parameter.
* If join columns are different, then `drop` the redundant column after join.

# Schema of a Spark join
Joining 2 Spark dataframes will combine columns from both, including the join columns. This requires an additional cleanup step after the join.

```python
df_a = spark.createDataFrame([(1, 'A')], 'id:int,a_name:string')
df_b = spark.createDataFrame([(1, 'B')], 'id:int,b_name:string')
df_a.join(df_b, df_a.id == df_b.id).printSchema()
"""root
 |-- id: integer (nullable = true)
 |-- a_name: string (nullable = true)
 |-- id: integer (nullable = true)         <----- TODO clean up
 |-- b_name: string (nullable = true)"""

df_a = spark.createDataFrame([(1, 'A')], 'a_id:int,a_name:string')
df_b = spark.createDataFrame([(1, 'B')], 'b_id:int,b_name:string')
df_a.join(df_b, df_a.a_id == df_b.b_id).printSchema()
"""root
 |-- a_id: integer (nullable = true)
 |-- a_name: string (nullable = true)
 |-- b_id: integer (nullable = true)       <----- TODO clean up
 |-- b_name: string (nullable = true)"""
```

# Join clean code
Following is how to make the additional step as clean as possible:

* If inner join columns have the same name, then use `on` parameter. The result will contain de-duplicated join columns and no cleanup is needed.
    ```python
    df_a = spark.createDataFrame([(1, 'A')], 'id:int,a_name:string')
    df_b = spark.createDataFrame([(1, 'B')], 'id:int,b_name:string')
    df_a.join(df_b, on="id").printSchema()
    """root
    |-- id: integer (nullable = true)
    |-- a_name: string (nullable = true)
    |-- b_name: string (nullable = true)"""
    ```

* If join columns are different, then `drop` the redundant column(s) after join.
    ```python
    df_a = spark.createDataFrame([(1, 'A')], 'a_id:int,a_name:string')
    df_b = spark.createDataFrame([(1, 'B')], 'b_id:int,b_name:string')
    df_a.join(df_b, df_a.a_id == df_b.b_id).𝐝𝐫𝐨𝐩("𝐛_𝐢𝐝").printSchema()
    """root
    |-- a_id: integer (nullable = true)
    |-- a_name: string (nullable = true)
    |-- b_name: string (nullable = true)"""
    ```
