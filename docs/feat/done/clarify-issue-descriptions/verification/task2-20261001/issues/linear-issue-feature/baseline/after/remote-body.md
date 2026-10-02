# EXPORT later?? queue thing maybe!!!

Queue plus a token sounds like the approach from [discussion](discussion.md).
Mira still needs to choose download expiry; queue was a suggestion, not signed off.
Today [export](export.py) builds the CSV in the request. Large exports hold people
on that request when they want to carry on working. We accepted continuing work
and downloading when ready in [requirements](requirements.md); this is a proposal,
there is no implementation yet. For example start an export of the selected rows,
keep working, and later download those rows with the same column order.

Acceptance: the downloaded CSV contains the originally selected rows in their
original column order. No expiry value agreed. Notifications are out of scope.

- [x] Agree continuation and download intent
- [ ] Mira: decide download expiry before implementation
- [ ] Choose mechanism after that decision
