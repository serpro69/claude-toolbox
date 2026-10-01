# EXPORT later?? queue thing maybe!!!

Users need to keep working while an export is prepared and download the CSV when
it is ready. Today, [exports](export.py) build the CSV synchronously in the request,
so large exports keep users waiting on that request.

The [accepted requirements](requirements.md) establish the continuation and
download outcome. For example, a user starts an export of selected rows, continues
working, and downloads those rows when the export is ready. This feature is not
implemented; the supplied current source is revision `export-2.1`.

## Acceptance and scope

The only agreed acceptance criterion is that the downloaded CSV contains the
originally selected rows in their original column order. Notifications are out of
scope. No performance target or row cap has been agreed.

## Decisions before implementation

Mira must decide download expiry before implementation; no duration has been
agreed. Once she records that decision, the export maintainers can choose the
mechanism.

Arun proposed a background queue and download token in the
[discussion](discussion.md). This remains a candidate solution and has not been
approved.

- [x] Agree continuation and download intent
- [ ] Mira: decide download expiry before implementation
- [ ] Choose mechanism after that decision
