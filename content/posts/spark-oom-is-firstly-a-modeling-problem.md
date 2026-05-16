+++
title = 'Spak OOM is firstly a Modeling Problem'
date = 2026-05-16T10:00:00+07:00
draft = false
tags = ['spark', 'datamodel']
+++

Some Qlik data modeling practices are actually underrated fixes for Spark OOM error.

# Underrated fix 1: Data Type

Spark infers schemas using "greedy" data types, change to an optimized schema:

* use `ShortType` instead of `IntegerType` if values never exceed 32,767.
* use `DecimalType` only when necessary; otherwise, use `FloatType` or `DoubleType`.

Before joining using `StringType` ID values, consider hashing them to an `IntegerType` or `LongType` (lesson from Qlik `Autonumber()`)

# Underrated fix 2: Cardinality

When Spark groups by a column with mostly the same/null values, those rows are sent to the same partition causing OOM for that executor. 

Add a salt column = `id % N`, then add the salt to the group by to evenly distribute data to N executors. Also see [Partition Salting Example]({{< relref "partition-salting-example.md" >}}).

Note on joins: just broadcast the small table.

# Underrated fix 3: avoid SELECT *

Enough said.
