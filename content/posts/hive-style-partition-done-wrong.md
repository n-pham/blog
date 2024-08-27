+++
title = 'Hive-style partition done wrong'
featured_image = 'images/hive-style-partition-done-wrong.jpg'
date = 2024-08-27T19:45:00+07:00
draft = false
tags = ['hadoop', 'hive', 'partition', 'datalake', 'storage']
+++
# Wrong Hive-style partition

More than once I have seen this nicely-done partition structure, only to be ruined by having *different* file types in the same place.

```
s3://bucket/
            year=2023/
            year=2024/
                      ..
                      month=07/
                      month=08/
                               raw.csv
                               processed.csv
```

Spark/Glue or Presto/Trino/Athena would have worked *directly* on top of this structure, if there is a single file type either raw or processed.

The other file types are to be put in separate buckets with similar structures.

# Right Hive-style partition

```
s3://raw-bucket/
                      year=2024/
                                month=08/
                                         raw.csv

s3://processed-bucket/
                      year=2024/
                                month=08/
                                         processed.csv
```
