# Task 4: local document and routing verification

Fresh verification of original `/kk:clarify-docs` scenarios 1–10 completed on
2026-10-02: **40 PASS, 0 FAIL, 0 PARTIAL**. All 30 revised reader answers pass.
The original answers retain their measured 23 PASS, 1 FAIL and 6 PARTIAL judgments.
See the [independent verdicts](grader/verdicts.json) and
[final grader access audit](grader/grader-final-access-audit.json).

| ID | Scenario | Assertions | Observed result |
| --- | --- | --- | --- |
| 1 | dense-source | 5 PASS | Purpose and worked default-change example precede technical references. |
| 2 | source-disagreement | 5 PASS | Mandatory intent and conflicting current behavior remain explicit, with owner and next step. |
| 3 | missing-context | 5 PASS | Missing retention decision stays unresolved; the data steward owns the next step. |
| 4 | cross-file-preservation | 5 PASS | Required sections, links, task state, optionality and approval gate survive. |
| 5 | already-clear | 4 PASS | All files remain byte-identical after source inspection. |
| 6 | clear-factual-error | 4 PASS | Only the source-backed maximum changes from 60 to 90. |
| 7 | skill-instruction-target | 3 PASS | Boundary explanation and implementation suggestion; no edit or automatic handoff. |
| 8 | agent-instruction-target | 3 PASS | Boundary explanation and implementation suggestion; no edit or automatic handoff. |
| 9 | code-non-trigger | 3 PASS | Correct null-override explanation; no editorial activation or writes. |
| 10 | brevity-non-trigger | 3 PASS | One-sentence answer; no tools, editorial activation or writes. |

Each editor received the unmodified natural eval request, a file-access manifest,
an offline staged workspace and the current canonical skill catalog entry. The
canonical entry point and shared procedure are copied under `instructions/`;
`source-identity.json` records their hashes and repository revision. Cases 7–10
permit workspace-local artifacts so their routing assertions are not enforced by
an independent write prohibition. Cases 9/10 expose the description and normal
instruction-loading path without preloading the skill body.

Cases 1–6 used separate fresh original and revised readers with identical neutral
questions and settings. Each sees only its oracle-declared reader files. The
editor and readers have no access to eval specifications, oracles or prior runs.
The grader is a separate fixture-capable default agent. All participants use
`fork_turns=none` and no model or reasoning override. Actual native settings are
captured per participant. All 22 editor/reader sessions and the accepted final
grader record `gpt-6-astra`, `max` effort. No operative fix was required.

Every plaintext prompt was saved by native `apply_patch` before dispatch. Native
dispatch receipts, encrypted transport payloads, filtered visible tool/message
projections, final answers, access ledgers, source snapshots and original session
hashes are retained beside each case. The [cohort checks](cohort-integrity.json)
confirm canonical/fixture equality and identical reader questions/settings. The
[filtered export audit](filtered-integrity-summary.json) confirms preservation of
all 141 visible participant records. The grader independently rehashed the portable
package, checked all 22 dispatch pairs, replayed all six patch calls, and validated
the cross-file links and exact task state.

Encrypted transport cannot independently establish plaintext bytes; the evidence
retains pre-dispatch plaintext and receipt linkage. Shared filesystem boundaries
are enforced by prompts and trace audits, not OS isolation. Original session logs
stay outside the repository, identified by path/hash. Model-reader judgments do
not establish improved human comprehension or statistical comparisons.

The first grader was interrupted during an evidence packaging correction that
removed harness boilerplate and hidden reasoning from repository exports. Its
incomplete, invalid attempt is preserved separately from final verdicts. All
editor/reader visible records and artifacts remain unchanged. See
[capture-format.md](capture-format.md) and [filter-correction.json](filter-correction.json).

The coordinator and final grader each encountered a read-only path-hook rejection
for a literal directory name ending in `target/`; permitted captured-record or
manifest-driven reads recovered the same evidence. The grader's initial long
manifest rendering was truncated and fully reread. Diagnostic-script corrections
and the interrupted first grading attempt remain in the traces. No required
grading material remains unread and no final assertion remains unresolved.
