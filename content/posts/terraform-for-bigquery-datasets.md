+++
title = 'Terraform for BigQuery Datasets'
featured_image = 'images/terraform-bq.png'
date = 2026-06-11T11:15:00+07:00
draft = false
tags = ['terraform', 'iac', 'bigquery']
+++
# TL;DR
* Stop creating datasets manually in the GCP Console.
* Use Terraform to version control your schemas and access rights.
* Leverage `google_bigquery_table` for critical production tables.

# Infrastructure as Code (IaC)
Defining your warehouse in code ensures that Dev, Staging, and Prod environments are identical.

```hcl
resource "google_bigquery_dataset" "raw_zone" {
  dataset_id                  = "raw_data"
  friendly_name               = "Raw Data Zone"
  location                    = "US"
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "orders" {
  dataset_id = google_bigquery_dataset.raw_zone.dataset_id
  table_id   = "orders"
  schema     = file("schemas/orders.json")
}
```
