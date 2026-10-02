# EXPORT later?? queue thing maybe!!!

Users need to keep working while an export is prepared and download it when ready.
This outcome is accepted in the [requirements](requirements.md), but the feature
is not implemented. Today, [export](export.py) builds the CSV synchronously in the
request, so users with large exports must stay on that request while it completes.

For example, a user should be able to start an export of selected rows, continue
working, and later download those rows with the same column order.

## Acceptance and scope

The only agreed acceptance criterion is that the downloaded CSV contains the
originally selected rows in their original column order. Notifications are out of
scope. No performance target or row cap has been agreed.

## Decisions before implementation

Mira must decide how long downloads remain available before implementation; no
expiry duration has been agreed. The maintainers can then choose the mechanism.
Arun proposed a background queue and a download token in the
[discussion](discussion.md), but Mira has not approved that mechanism. Her
acceptance covers the continuation and download outcome.

- [x] Agree continuation and download intent
- [ ] Mira: decide download expiry before implementation
- [ ] Choose mechanism after that decision
