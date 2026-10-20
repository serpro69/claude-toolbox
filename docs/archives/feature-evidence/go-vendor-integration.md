# Go vendor integration retention

Archive the entire `docs/feat/done/go-vendor-integration/` directory, including
`.sessions/design-session.txt` (55,778 bytes).
Keep root design/implementation/tasks in Git.

The task record marks the feature done and reports passing vendor-tool unit/
integration tests, `make vendor-go`, plugin-structure checks and code/spec review.
It records that upstream `golang-http` did not exist in the selected v1.2.5 source,
so its proposed manifest entries were removed. Preserve that decision and the
original upstream identity; it is not a current upstream availability claim.

Reusable functionality already lives in `cmd/vendor-profiles/`,
`scripts/go-vendor-manifest.yml`, Make targets, maintained profile files and tests.
Nothing executable depends on the saved design session. No tooling extraction
or new dependency is needed.

Locator:
`payload/docs/feat/done/go-vendor-integration/.sessions/design-session.txt`.
Only the session is an eventual capture-cleanup candidate; retain the plans and
maintained toolchain. No current vendor fetch or test run is claimed here.
