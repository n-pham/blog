+++
title = 'AWS S3 API Pagination Strategy'
date = 2024-08-22T21:15:00+07:00
draft = false
tags = ['aws', 's3', 'strategy', 'pagination', 'api-design']
+++
# Strategy: Designing for Unbounded Result Sets

In distributed systems, APIs that return lists of resources must account for scale. The "tactical" approach is to simply call the list API, but the "strategic" approach is to treat all collection-based responses as potentially unbounded.

## The Principle of Page-First Consumption

AWS S3's `ListObjectsV2` is a prime example of an API designed for high availability and consistency at the expense of client-side simplicity. By limiting results to 1000 items per request, the service ensures that:

1.  **Response Latency is Predictable**: Large responses don't block the network or the service's internal workers.
2.  **Memory Pressure is Managed**: Both the server and the client can process data in fixed-size chunks.
3.  **Resiliency is Improved**: If a single request fails, only 1000 items need to be re-fetched, not the entire dataset.

## Cursor-Based vs. Offset Pagination

S3 uses **Cursor-Based Pagination** via the `ContinuationToken`. This is strategically superior to Offset Pagination (e.g., `LIMIT 1000 OFFSET 2000`) because:

*   **Consistency**: Cursors are generally more resilient to data being added or removed between requests.
*   **Performance**: Offsets require the database to scan and skip rows, which becomes progressively slower ($O(n)$). Cursors allow for direct seeking ($O(1)$).

## Strategic Implementation Guidelines

When building or consuming APIs that handle large datasets:

*   **Always Assume More**: Even if you expect 5 items today, write the loop for 1,000,000.
*   **Encapsulate Pagination**: Use generators or iterators to hide the pagination logic from the business logic.
*   **Handle Tokens Opacity**: Treat continuation tokens as opaque strings. Do not try to parse or generate them on the client.
