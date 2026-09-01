# 12. Inventory service boundaries and ownership

Date: 2026-08-30

## Status

Accepted

## Context

The `inventory` and `pricing` services are live. This ADR records their boundary and ownership invariants and proposes one future extraction.

## Decision

- The `inventory` service must not depend on the `pricing` schema module directly; it reads prices only through the pricing service's published API.
- The `recommendations` service is the sole mutating owner of the Recommendation entity; other services read recommendations only through its API.
- We will introduce a `catalog` service. Its dependency direction will run one way: `catalog` will read prices only through the pricing API, and `pricing` will never import the `catalog` package.

## Consequences

- Each boundary keeps the services independently deployable.
