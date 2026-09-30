# Offline read-only PR response

URL: https://example.invalid/kitchen/pull/12 (synthetic; do not contact).
Body is remote-body.md. Target: kitchen. Audience: established repository reviewers;
all checkout files are tracked and unrestricted. Actual base/head in staged checkout/:
review-base and review-head. Head is checked out. The stack title says `schema-only`.
Current feature: docs/feat/wip/prep/. Its existing pr-draft.md belongs to a different PR.
Validation record: the three assertions in test_resolve.py passed at head; no
persistence or deployment validation. Requirements are checkout/requirements.md.
