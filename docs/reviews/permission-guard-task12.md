# Permission guard: Task 12 final verification

Date: 2026-10-26. Tasks 12.1–12.4 are complete. Task 12 and the feature remain
in progress because macOS performance acceptance (12.5) is still open.

## Scope and baselines

The full-feature review compares `de005839dead3c36c65c6ff0de2d5d8ab52451f4`
with `23768453e7689a2a176a062ad8170e7aa1da7f4d` and this task's corrections.
It covers Tasks 1–10, 13 and current Task 12: the shared engine and declaration,
wrapper/launcher, adapters, generated projections, template sync, tests and
operative documentation. Unrelated `.codex/config.toml` and auto-review-policy
documentation changes were excluded. Optional Task 11 and issues #179–#184
remain outside completion criteria. No deployed baseline was established.

The initial selected diff was 60 paths, +8,061/−293 lines. The focused correction
snapshot has SHA256 `f965c253008ca31bf3f34a62a4e506d9d946ed6b910b833916e457ec72e20220`.
Evidence and full historical blobs remain under `/tmp/kk-guard-task12.hJcnKK/`.

## Findings and resolution

| Source | Finding | Resolution |
|---|---|---|
| Code reviewer, P1 | Literal relative `cd` lost possible protected-path anchors | Retain candidate directories for secret/selfmod checks while keeping temporary exemptions uncertain |
| Code reviewer, P1 | Unquoted wildcard operands were checked only as literal strings | Preserve quote/escape context and inspect existing filename matches without reading contents |
| Spec reviewer, P1 SPEC_DEV | Escaped interpreter literals bypassed protected-path checks | Decode common static escapes in both read scans and write arguments; preserve raw strings; never evaluate expressions |
| Spec reviewer, P2 OUTDATED_DOC | Task 2 still prescribed Bash-variable payload buffering | Reconcile the live plan with the previously accepted private-file, byte-preserving implementation |
| Both reviewers, P2 | macOS Read p95 remains above the required 30 ms | **Open under Task 12.5**, explicitly retained by the user |

Synthetic regressions fail against the previous engine and pass against the
correction, including ordinary files, quoted wildcards and raw-string controls.
The initial wildcard correction changed one existing corpus denial category;
evaluation order was corrected without relaxing its assertion. The canonical
engine and regenerated Codex copy compare identical.

## Verification

| Check | Result / captured evidence |
|---|---|
| All 15 Bash suites | Passed: hook run `db2a0ad9-a28a-4f87-b171-6fd9475e2e54`, remaining suites `105649c9-f5da-4bea-92b3-5e8a058948e9` |
| Baseline Go, both generators/freshness, graph, static checks | Passed: `4083047f-d913-4de8-b11a-79090c77957c` |
| Corrected engine | 96 tests each on Python 3.10 and 3.12, including 159 corpus rows: `30382d77-8dfc-4fb6-a474-8a54216a8c8a` |
| Corrected wrapper / Codex adapters | 51 cases / 248 assertions and 29 / 165, same correction run |
| Corrected generator / structure / graph | Passed: `50957ee5-a589-4874-84be-2d551e5912cc` |
| Strict documentation build | Passed in a disposable snapshot; original successful run `8609766b-68f7-4eba-8548-31615b90a395`; final prose refresh `975a4716-13bb-4ade-8302-a107b0c8fd6e` |

Unchanged suites retain their baseline results; changed shared behavior received
focused re-verification. The first documentation build failed because its
disposable snapshot lacked the root license snippet; adding that source file
fixed the build. No repository assertion or timing threshold was relaxed.

Serial Linux Read/Bash p95 changed from **23.52/40.34 ms** to **23.66/41.59 ms**
under the same benchmark and default wrapper interpreter, with `CI` unset.
Both targets and local gates pass there. This does not supersede the historical
macOS **31.10/34.75 ms** result or verify the corrected engine on that host.

## Review coverage and limits

Independent `code-reviewer` and `spec-reviewer` agents used gpt-6.1-sol (OpenAI),
without authoring-session history. Both reviewed the initial feature and the
focused correction. No P0/P1 issue remains. Code corrections are approved;
aggregate code review remains `REQUEST_CHANGES` and spec review
`DEVIATIONS_FOUND` solely for the known performance acceptance item. Both reviews
are source inspections; execution results above belong to the parent agent.

Capy path/cwd and batch compatibility were verified against complete source at
`31c0ef259ad8dbcc5f67fc12c7fc9cd5ec15730c`. Versioned Codex patch-parser/PathUri
source was unavailable at the recorded locations and in a bounded local search.
That comparison remains narrowly uncorroborated, with no demonstrated defect or
new acceptance gate. If further source corroboration is required, an unassigned
owner can retrieve the tagged Codex 0.164.0 parser/path implementation and compare
its whitespace and lexical-`..` semantics with `check_patch`.

One-time PAL discovery chose clink because no API review provider was available.
Claude was the only eligible client, with Anthropic identity assumed from PAL's
shipped manifest; configured/observed model unknown. Codex was absent and shares
the authoring provider; agy was absent; gemini retired/absent. The 79-path bundle
included all eight common/Python criteria plus source, history and context.
Claude timed out after 300 seconds, returning no findings or observable receipt.
No retry, external corroboration or external approval is claimed. The corrected
snapshot received local independent review only. Optional transport follow-up
is already tracked in #184.

Actual Python 3.8 runtime, current macOS timing, deployed installations and the
broader hook-trust lifecycle were not exercised. Existing historical runtime
observations retain their stated host/version/trust limits. No additional
knowledge-index entry duplicates the existing literal-spelling lessons or the
correction's documentation in design §7.3. No intentional deviation was accepted.

## Remaining action

The user selected **"Keep the 30 ms requirement open pending macOS verification"**.
Owner is unassigned. Run the unchanged hook benchmark on macOS with `CI` unset,
record runtime versions and Read/Bash p95, and optimize if the 30/50 ms targets
are missed. Task 12.5, Task 12 and feature completion stay open until satisfied.
No release, tag or version bump is part of this work.
