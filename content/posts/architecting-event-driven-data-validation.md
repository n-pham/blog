+++
title = 'Architecting Event-Driven Data Validation'
featured_image = 'images/event-validation.png'
date = 2026-06-11T10:20:00+07:00
draft = false
tags = ['architecture', 'data-quality', 'events']
+++
# TL;DR
* Don't wait for the nightly batch to find errors.
* Use Cloud Pub/Sub or Kafka triggers to run validations on arrival.
* Route invalid data to a **Dead Letter Table** for manual fix.

# The Shift to Proactive Quality

## 1. Validation on Arrival
Instead of scheduling a dbt test every hour, trigger a validation function when a new file lands in S3/GCS.

```python
def on_file_landed(event, context):
    file_path = event['name']
    if not validate_schema(file_path):
        quarantine_file(file_path)
        send_alert("Schema Mismatch!")
```

## 2. The Dead Letter Pattern
If a record fails validation, don't stop the whole pipeline. Append the bad record to a "dead letter" table with an error message, allowing the healthy data to flow.

```sql
INSERT INTO `processed.orders`
SELECT * FROM `raw.orders` WHERE is_valid = true;

INSERT INTO `audit.invalid_orders`
SELECT *, error_reason FROM `raw.orders` WHERE is_valid = false;
```

## 3. Real-time Feedback Loops
Integrating validation results into your observability stack (e.g., Datadog, Grafana) allows you to see data quality trends as they happen, not after the dashboard breaks.
