# 16. Device telemetry ingestion via the DeviceCloud agent platform

Date: 2026-09-01

## Status

Accepted

## Context

A fleet of roughly 200k battery-powered field devices reports telemetry over
intermittent radio links. Agent rollouts propagate over 6–12 months and never
reach the whole fleet, so whatever agent a device shipped with must keep
working for the life of that device. Delta-sync (transmitting only changed
readings) is required to fit the radio airtime budget. The platform team is
two engineers, and the company's differentiation is telemetry analytics, not
device infrastructure.

## Decision

- **Vendor platform.** Telemetry ingestion is built on DeviceCloud's
  proprietary device-agent SDK and message envelope. This is a one-way door:
  the envelope format is embedded in 200k deployed agents that cannot be
  force-updated, so migrating off DeviceCloud would mean a fleet-wide agent
  replacement spanning years. We accept that because DeviceCloud is the only
  offering with delta-sync over intermittent links; building an in-house agent
  was estimated at 18 engineer-months, and MQTT with a custom agent was
  weighed and rejected (no delta-sync, roughly doubles airtime per report).
- **SDK containment.** Every ingest handler consumes device messages
  exclusively through the shared `envelope` package; no handler imports the
  DeviceCloud SDK directly. The `envelope` package is the only module that may
  depend on the SDK.
- **Trade-off.** We accept the vendor-dependency risk in exchange for not
  building device infrastructure ourselves, because our differentiation is
  analytics, not device plumbing.

## Consequences

- New message fields arrive through `envelope` package updates; handlers stay
  SDK-agnostic.
- A future migration off DeviceCloud is scoped, on the server side, to the
  `envelope` package; the deployed agent fleet remains the irreversible part.
