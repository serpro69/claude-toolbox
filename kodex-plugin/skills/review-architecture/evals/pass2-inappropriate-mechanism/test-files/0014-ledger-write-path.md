# 14. Ledger write-path scaling

Date: 2026-08-31

## Status

Proposed

## Context

The `ledger` service records financial transactions. The workload is overwhelmingly
write-heavy: roughly 92% of operations are appends (recording new transactions) and
about 8% are reads (occasional account-statement queries). Two constraints frame this
decision:

- Once an append has been acknowledged to a client, it must never be lost.
- Append throughput must scale to at least 50,000 appends/sec as volume grows;
  account-statement reads must return in under 100 ms.

## Decision

We propose three changes to the write path:

- **Statement-read latency.** Introduce a write-through Redis cache in front of
  Postgres. Every append writes through the cache to Postgres, and account-statement
  reads are served from the cache, meeting the sub-100 ms read target.
- **Write scaling.** Partition the `transactions` table by a hash of `account_id` so
  append load spreads evenly across shards and no single node caps throughput.
- **Overload protection.** Bound the number of in-flight appends with a fixed-size
  admission queue; requests that cannot be admitted are rejected with a 503 before any
  acknowledgment. The bound can be raised, or the queue removed, as capacity grows.

## Consequences

- The cache and the partitioned store both add operating surface (failover, warm-up,
  cross-shard tooling) to the ledger.
- Statement reads and appends are served through different paths.
