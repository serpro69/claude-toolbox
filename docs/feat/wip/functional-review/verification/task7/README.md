# Task 7 staging verification

Date: 2026-10-09. Review base: `f2e6023f2ad1f50fbcc2f8a73b7f95c630219965`.

The staging helper preserves flat fixtures and builds complete before/after repositories with optional ordered historical commits. `HEAD` and `eval-base` identify the PR base; historical tags expose released source without including it in the current files or staged diff. Inputs are validated before destination creation, and existing destinations are refused. The harness playbook documents these semantics. No frozen fixture, actor instruction workflow, model, capture policy or acceptance threshold changed.

## Verification

- [Check summary](checks.json): all ten `test/test-*.sh` suites passed, with 644 helper assertions and no skips. The staging suite contains [20 passing integration tests](staging-after-review.txt), including actual R1/R3 and all five legacy review fixtures.
- Tests exercise additions, modifications, deletions, unchanged/hidden/ignored files, executable mode, local symlinks, empty snapshots, ordered historical trees/tags, malformed pairs/manifests/paths/refs, reserved Git and grading entries, escaping links, existing destinations and isolated Git configuration. Comparisons verify source bytes remain unchanged and metadata/oracles/wrappers do not enter actor repositories.
- [Seed hashes](seed-hashes.json): all 51 entries across R1, R3, I1 and I2 still match the Task 2 freeze. R1/R3 are staged through the real helper; I1/I2 receive hash verification only.
- [Final generation](generation-after-review.txt) and [second generation](generation-final-freshness.txt) passed generator tests and both structure suites. [Freshness](freshness.json) shows no changes across 685 generated files. Canonical/generated `setup.sh` bytes are identical.
- [Plugin graph](plugin-graph.txt): no broken edges or orphans; the existing cycle warning remains. [Go tests](go-tests-retry.txt) passed. Shell syntax and whitespace checks passed; the whitespace check uses a per-command `core.whitespace=blank-at-eol,blank-at-eof,space-before-tab` override to avoid the user's tabs-only preference rejecting embedded Python indentation.

These are offline staging and repository checks. They do not establish actor review quality, exact reviewer handoff contents or paired behavioral acceptance. Task 2 gate 2B and Tasks 8–13 remain open under the existing run contract.

## Failed attempts and corrections

The first focused test run exposed Python 3.14's non-strict resolution of cyclic symlinks. Validation now resolves links strictly, with a separate contained-dangling-link fallback; the regression passes. That initial run's output remains in the session transcript.

The independent reviewer requested a focused probe of `eval-base/released`. [The probe](reserved-tag-probe.json) demonstrated a conflict at base-tag creation; the helper safely removed its owned destination. Validation now reserves the `eval-base/` namespace before any Git operation or destination creation. The new regression wraps Git and verifies that no invocation occurs for this invalid input. See [review disposition](review.md).

[Initial generation](generation-initial.txt) failed while cleaning sandbox-protected `.codex/agents`; an approved retry regenerated all output. Initial [Go](go-tests.txt), [manifest](test-manifest-jq.txt) and [template-cleanup](test-template-cleanup.txt) checks encountered sandbox restrictions on existing build/uv caches. Approved retries passed, without persistent configuration changes. Template tests use per-command `commit.gpgsign=false` for disposable fixture commits.

Two controller mistakes are retained: [a nonexistent test filename](test-settings-merge-retry.txt), followed by the actual remaining suites; and [an incorrect I2 directory name](seed-hashes-wrong-path.json), followed by the correct-directory hash verification. Neither is counted as a passing check or fixture mutation.
