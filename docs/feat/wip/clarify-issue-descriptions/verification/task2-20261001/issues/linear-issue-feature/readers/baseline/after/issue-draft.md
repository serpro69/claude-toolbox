# EXPORT later?? queue thing maybe!!!

Exports currently build the CSV synchronously in the request, so large exports
keep users waiting when they want to carry on working. The [current source](export.py)
was inspected at revision `export-2.1`.

The [accepted intent](requirements.md) is to let users keep working while an export
is prepared and download it when ready. For example, a user starts an export of
selected rows, continues working, and later downloads those rows in the same
column order. This feature is not implemented.

## Acceptance and scope

The only agreed acceptance criterion is that the downloaded CSV contains the
originally selected rows in their original column order. Notifications are out of
scope. No download-expiry duration, performance target or row cap has been agreed.

## Decisions and next steps

Mira must decide download expiry before implementation. Maintainers can then
choose the mechanism. Arun's background queue and download token are a candidate
solution from the [discussion](discussion.md); Mira has accepted the user outcome
but has not approved that mechanism.

- [x] Agree continuation and download intent
- [ ] Mira: decide download expiry before implementation
- [ ] Choose mechanism after that decision
