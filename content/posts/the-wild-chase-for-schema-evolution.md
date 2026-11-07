+++
title = 'The Wild Chase for Schema Evolution'
date = 2026-11-07T10:00:00+07:00
draft = false
tags = ['data', ]
+++
# The Wild Chase for Schema Evolution

We have been chasing wild Schema Evolution through major technology milestones:

* JSON

  Pipelines broke with data type changes, column renames and parsing OOMs.

* Kafka with Schema Registry

  Pipelines broke with constantly out-of-date schemas and serialization CPU hog.

* Column-oriented Parquet and Iceberg catalog

  Pipelines broke under unchecked column explosion and the overhead of keeping metadata and catalog up-to-date.

* Data Mesh

  While every Data Product is respecting its Data Contract, the transaction source still emits a single events table with a dozen event types, breaking all downstream Data Products with each new type.
