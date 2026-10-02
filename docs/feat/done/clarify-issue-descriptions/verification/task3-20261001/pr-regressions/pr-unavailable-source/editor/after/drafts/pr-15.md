Restaurant defaults let users avoid repeating preparation times. The product owner has confirmed the intended contract: with a restaurant default of 15, `null` inherits 15, while an explicit `0` stays 0.

The author reports that this PR implements runtime resolution and that all tests pass. Both claims remain unverified: exact base/head commit IDs, the review diff, source, and test output are unavailable. The platform identifies base `main` and head `prep`, but those branch names alone do not establish this PR's increment or which tests it adds.

Persistence and scheduling remain future work outside this PR's scope.

Before review can establish delivery, the PR author must provide the exact base/head revisions, diff, and test output. Reviewers should check that runtime resolution preserves the distinction between `null` and explicit zero, and assess which cases the tests exercise. Validation results are unavailable for this draft beyond the author's unverified report.

The badge decision remains open and belongs to the product owner; the next step is for that owner to resolve it.
