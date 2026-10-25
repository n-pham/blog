+++
title = 'Upgrade AWS Lambda for Modern Patterns'
date = 2026-10-22T10:00:00+07:00
draft = false
tags = ['lambda']
+++

# Upgrade AWS Lambda for Modern Patterns

* Durable Functions stop chaining Lambdas via SQS/EventBridge/DynamoDB
* Durable Functions `waitForCallback` avoids being billed waiting for external events
* Lambda MicroVMs hardware-level isolation secures multi-tenancy data
* Lambda MicroVMs can run interactive Jupyter notebooks with RAM and disk snapshot
* Web Functions avoid being billed for idle IO waits
* Web Functions bypass API Gateway in front of lambda
* Web Functions eliminate cold starts with multi-concurrency per execution environment
