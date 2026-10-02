# Final instruction revision and fresh PR reruns

The parent prepared a same-word-count clarification of the PR validation sentence
after inspecting the preserved first visibility draft. The final procedure hash is
`9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539`;
it still contains 1,248 words. The entry point is unchanged. The complete candidate
preflight was recorded by the parent before applying the operative wording.
See [instruction-retry.diff](instruction-retry.diff) for the complete change.

Fresh PR editors, revised readers and an independent grader will use this revision
in `contract-only-pr-retry/` and `destination-visibility-retry/`. The first attempt's
workspaces, results, frozen instructions and grader inputs remain unchanged.
Scenario prompts and grading criteria remain fixed; editor/revised-reader harness
paths are the only prompt differences.

The parent explicitly authorized reuse of the two independent original readers
because their inputs, questions and settings are unchanged. Their evidence is
copied byte-for-byte into each retry directory; their settings and submission
receipts retain the actual original session and prompt paths. The temporary retry
original-reader copies are staging artifacts and receive no new reader session.
The corresponding revised readers must use the same actual model and effort.
[retry-fixture-comparison.json](retry-fixture-comparison.json) verifies that all
fixture, eval and oracle bytes match the first attempt, and each reused reader's
artifact matches the retry's original draft exactly.
