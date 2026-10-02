# EXPORT later?? queue thing maybe!!!

Let users keep working while an export is prepared, then download it when ready.
This outcome is accepted in the [requirements](requirements.md), but the feature
is not implemented.

The [current export](export.py), inspected at revision `export-2.1`, builds the CSV
synchronously. The reported problem is that large exports keep users waiting on
the request when they want to carry on working. For example, a user should be able
to start an export of selected rows, keep working, and later download those rows
with the same column order.

## Acceptance and scope

The only agreed acceptance criterion is that the downloaded CSV contains the
originally selected rows in their original column order.

Notifications are out of scope. No download expiry duration, performance target,
or row cap has been agreed.

## Decisions before implementation

In the [discussion](discussion.md), Arun proposed a background queue and a download
token. This is a candidate solution; Mira accepted the user outcome but has not
approved that mechanism. Mira must record the download expiry decision before
implementation. The export maintainers can then choose the mechanism.

- [x] Agree continuation and download intent
- [ ] Mira: decide download expiry before implementation
- [ ] Export maintainers: choose mechanism after that decision

No implementation or runtime test results are available for this feature.
