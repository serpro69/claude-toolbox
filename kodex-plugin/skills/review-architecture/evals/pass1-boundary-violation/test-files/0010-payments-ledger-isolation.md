# 10. Isolate payments, ledger, and reporting boundaries

Date: 2026-08-25

## Status

Accepted

## Context

Three services were carved out of the monolith: `payments`, `ledger`, and `reporting`. To keep them independently deployable, cross-service coupling must go through published APIs, never through another service's internal schema package.

## Decision

- The `payments` service must not depend on the `ledger` schema module directly; it reads balances only through the ledger service's published API.
- The `reporting` service must not depend on the `payments` schema module directly; it consumes payment data only through the `payments` API.

## Consequences

- Each service owns its schema package privately; a schema change never forces a lock-step deploy of a consumer.
