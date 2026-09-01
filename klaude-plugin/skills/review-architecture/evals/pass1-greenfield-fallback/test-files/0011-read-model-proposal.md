# 11. Introduce a CQRS read-model service

Date: 2026-08-28

## Status

Proposed

## Context

The write path and the reporting/list queries contend on the same tables. We propose splitting a dedicated read-model service off the write side. Nothing here is built yet.

## Decision

- We will introduce a read-model service. The write side will not import the read-model package; the read model will consume the write side's event stream, and the write side will never depend on the read model.
- The read-model service will be the sole owner of the projection store; the write side reads projections only through the read-model API.
- List queries will hit a Redis-backed projection cache to keep p95 under 100ms.
- The `analytics` component and the write side will be strictly isolated at the dependency tier.
- The dashboard will use a cache to stay responsive.

## Consequences

- Eventual consistency between the write side and the projections must be tolerated by consumers.
