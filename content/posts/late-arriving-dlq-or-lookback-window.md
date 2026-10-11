+++
title = 'Late-Arriving DLQ or Lookback Window' 
date = 2026-10-09T10:00:00+07:00
draft = false
tags = []
+++

# Late-Arriving DLQ or Lookback Window

| Feature | Dead Letter Queue | Lookback Window |
| --- | --- | --- |
| Code | Complex, Duplicated Logic | Simple, Single Logic |
| Compute | Focused processing | Redundant window reprocessing |
| Storage | Key-based merge | Bulk partition overwrite |
| Best for | Stream, Real-time SLA <br/> Kappa Architecture | Analytics, DBT <br/> Lambda Batch layer |
