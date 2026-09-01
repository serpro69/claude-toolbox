# 13. Orders service resilience invariants

Date: 2026-08-31

## Status

Accepted

## Context

The `orders` service is live and calls the `payments` service synchronously on the
create-order path. This ADR records two independent resilience invariants: one for
availability when a downstream dependency fails, one for correctness when a client
retries.

## Decision

- **Payments dependency.** The `orders` service survives the `payments` service
  failing: every call to `payments` is wrapped in a circuit breaker so a payments
  outage cannot cascade into `orders`.
- **Retry safety.** Order creation is idempotent under client retries: the
  create-order mutation is guarded by an idempotency key with a unique constraint,
  so a retried request never creates a duplicate order.

## Consequences

- A payments outage degrades order creation without taking `orders` down.
- Clients may safely retry create-order requests.
