+++
title = 'Relational Database Batch Update Strategy'
date = 2024-09-19T09:45:00+07:00
draft = false
tags = ['relational', 'database', 'strategy', 'high-availability', 'migration']
+++
# Strategy: Maintaining High Availability during Data Mutations

In relational databases (RDBMS), every `UPDATE` or `DELETE` is a trade-off between **Consistency** and **Availability**. A large, single-transaction update is tactically simple but strategically dangerous.

## The Lockdown Risk

Relational databases use row-level or page-level locks to ensure ACID compliance. A monolithic update that touches 10% of your table might:

1.  **Block Reads/Writes**: Prevent other users from completing transactions.
2.  **Exhaust Resources**: Fill up the undo/redo logs or temp space.
3.  **Risk Catastrophic Rollback**: If the query fails at 99%, the database must spend hours rolling back, during which time it is under heavy load.

## The Strategy: Controlled Batching

**Controlled Batching** is the strategic decision to break a single logical unit of work into multiple physical transactions.

*   **Fixed Transaction Boundaries**: Instead of one transaction of 1,000,000 rows, use 1,000 transactions of 1,000 rows.
*   **Release Locks Frequently**: Between batches, the database can process other pending requests, maintaining high availability for end-users.
*   **Checkpoint Progress**: If a batch fails, you've already committed the previous ones. You only need to resume from the last successful ID.

## Implementation Guidelines

*   **Use Indexed Keys**: Always batch based on an indexed column (usually the Primary Key) to avoid full table scans for each batch.
*   **Monitor Throttle**: Add a small "sleep" between batches if the database CPU or IOPS are hitting limits.
*   **Balance Batch Size**: Too small increases overhead; too large increases lock duration. Start with 500-2000 rows and adjust based on performance.

## Conclusion
A strategic migration is one that no one notices. By batching updates, you prioritize the overall health and availability of the system over the speed of a single administrative task.
