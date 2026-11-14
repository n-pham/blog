+++
title = 'How Data Lakes Became Data Swamps'
date = 2026-11-14T10:00:00+07:00
draft = false
tags = ['data']
+++
# How Data Lakes Became Data Swamps

We tried hard to put **everything** into the cheap Data Lake thanks to schema-on-read.

Schema evolution tried hard to surface every field - from JSON, Glue crawlers, Parquet, and Iceberg to VARIANT.

Column lineage tried hard to trace where and how every field came in.

Semantics tried hard to define what every field was.

But only humans can answer why a field is calculated that way.\
With that knowledge, we have flexible schema data.\
Without that knowledge, the field is never trusted to be used, and we have a data swamp.

Data with undocumented values should stay as debt in the transactional system, IMO.
