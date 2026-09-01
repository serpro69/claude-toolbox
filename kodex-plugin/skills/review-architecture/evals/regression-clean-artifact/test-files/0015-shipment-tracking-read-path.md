# 15. Shipment tracking read path and carrier integration

Date: 2026-09-01

## Status

Accepted

## Context

Customers poll shipment tracking status far more often than shipments change:
status lookups outnumber shipment mutations roughly 40:1. Tracking lookups must
answer in p95 < 150 ms. Carrier status feeds arrive from three contracted
carriers; all three emit EDI-214 status messages, and none offers a JSON API.
The carrier API is slow and occasionally unavailable, and must not be called on
the customer read path.

## Decision

- **Read path.** Tracking status lookups are served from a denormalized
  `tracking_status` table maintained by an event projector that consumes
  shipment events; lookups never call the carrier API or join shipment tables.
  This is the mechanism behind the p95 < 150 ms lookup target.
- **Boundary.** The `tracking` service must not depend on the `shipments`
  service's internal schema package; it consumes the published shipment
  events package only.
- **Carrier calls.** Every call from `shipments` to the external carrier API
  is wrapped in a per-call timeout with a bounded retry, so a slow carrier
  cannot stall shipment processing indefinitely.
- **Carrier message format.** We commit to EDI-214 as the canonical inbound
  status format. This is a one-way door: every carrier feed and the parsing
  pipeline are onboarded against it, and switching formats later means
  re-onboarding every carrier feed. We accept that because EDI-214 is the only
  format all three contracted carriers emit today; per-carrier custom JSON
  adapters were weighed and rejected (three bespoke parsers to maintain, no
  carrier-side versioning guarantees).

## Consequences

- Tracking reads stay fast and available even when the carrier API is slow or
  down.
- The projector introduces eventual consistency between shipment mutations and
  tracking reads; we accept seconds of staleness on a tracking page.
- When shipment-event volume passes 10k/min we will move event delivery to
  at-least-once with consumer-side dedup keyed by `event_id`; today's
  single-consumer setup does not need it.
