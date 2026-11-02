+++
title = 'Cloud Orchestration Matrix'
date = 2026-10-31T10:00:00+07:00
draft = false
tags = []
+++

# Cloud Orchestration Matrix

All features:
* Airflow
* AWS MWAA
* Azure ADF / Fabric
* Databricks Lakeflow Jobs
* GCP Composer


| Feature | AWS | Azure | GCP |
| :--- | :--- | :--- | :--- |
| **Cron Triggers** | * EventBridge Scheduler | * Logic Apps Recurrence | * Scheduler |
| **Polling** | * Step Functions<br/> * Glue Workflows | * Logic Apps | * Workflows |
| **Dependencies** | * Step Functions<br/> * Glue Workflows | * Logic Apps | * Workflows |
| **Retries** | * Step Functions<br/> * Glue Workflows | * Logic Apps | * Workflows |
| **Backfill** | * Glue Workflows | * needs ADF / Fabric | * needs Composer |
| **Lineage & Metadata** | * Glue Workflows<br/> * Step Functions (CloudWatch) | * Logic Apps (Azure Monitor / Log Analytics) | * Workflows (Cloud Logging) |
| **Long Run** | * Step Functions (1 year)<br/> * Glue Workflows (48 hrs) | * Logic Apps (90 days) | * Workflows (1 year)<br/> * needs Composer |
| **Definition Format** | * EventBridge Scheduler (JSON/Console)<br/> * Step Functions (JSON/YAML/CDK)<br/> * Glue Workflows (Python/CloudFormation) | * Logic Apps (Visual / ARM / Bicep / JSON) | * Scheduler (YAML/Console)<br/> * Workflows (YAML/JSON) |
| **Pricing Model** | * EventBridge Scheduler (Per request)<br/> * Step Functions (Per transition)<br/> * Glue Workflows (DPU-hr) | * Logic Apps (Per action / Consumption) | * Scheduler (Per job)<br/> * Workflows (Per step)<br/> |
