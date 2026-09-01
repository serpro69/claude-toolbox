# 7. Split billing off the orders service

Date: 2026-08-20

## Status

Accepted

## Context

The monolith couples order management and billing in one service and one schema. Order write traffic is heavy — creation and status updates dominate the workload — and the read path for order status must meet a p99 latency of under 200ms for the storefront. Billing needs order data but must never be on the critical path for order writes.

## Decision

We split billing into its own service. Concretely:

- The `orders` service is the sole mutating owner of the Order entity, and the `billing` service reads orders only through a read-only `orders` API and must not depend on the order schema directly.
- We put a Redis read-through cache in front of the `orders` read API to meet the p99 < 200ms latency target.
- Order creation is made idempotent via a unique constraint on an `idempotency_key` column in the orders table, so retried creates do not duplicate orders.
- The `orders` API will expose a `/v2/` versioned route so that `billing` can migrate to breaking schema changes on its own timeline.
- Service-to-service calls to the `orders` API are authenticated with mTLS.

## Consequences

- `orders` and `billing` become independently deployable, at the cost of a network hop on the billing read path.
- Choosing Redis over an in-process cache is a two-way door: it can be reverted without a data migration if the operational cost is not justified.
- The team will adopt trunk-based development for the `orders` service to keep the split moving.
