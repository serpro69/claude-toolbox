Restaurant defaults are intended to avoid repeating preparation times. Under the
product-owner-confirmed contract, a restaurant default of 15 means a null
preparation time inherits 15, while an explicit zero stays zero.

Whether this PR delivers runtime resolution remains unverified. The available PR
context identifies repository `kitchen`, base branch `main` and head branch `prep`,
but provides no commit IDs, review diff or source. Branch names alone do not
establish what this PR changes or what it inherits. Test results are also
unavailable, so the claim that all tests pass is unverified.

The PR author must provide the exact base/head revisions, diff and test output.
Reviewers can then identify the current increment, check whether runtime resolution
implements the null-inheritance and explicit-zero contract, and assess which cases
the tests exercise. Until that evidence is available, the confirmed contract should
not be treated as verified runtime delivery.

Persistence and scheduling remain outside this PR's scope and are deferred to
later work. The badge decision remains open; the product owner must resolve it.
