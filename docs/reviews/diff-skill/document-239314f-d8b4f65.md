# diff-skill: document (239314f → d8b4f65)

## Summary

**Verdict: No issues.** Zero accidental degradations, zero complexity regressions and no actionable code-review findings in the document skill. The branch preserves its original documentation responsibilities and makes instruction loading and explanation quality more explicit. No findings to index.

Reviewed on 2026-09-30 using `/kk:review-code` and `/kk:diff-skill`. Compared the branch base (`239314f`) with HEAD (`d8b4f65`), and separately compared the pre-pivot state (`3c06264`) with `1179fda`. The last commit changes only the design skill. See the [design review](design-239314f-d8b4f65.md) for shared validation and the generated design-file finding.

## Preserved Requirements

| Original requirement | Current location and result |
| --- | --- |
| List filenames, detect profiles, load their document rubrics, then read feature content | `SKILL.md`, Workflow Steps 1–4, preserved |
| Apply always-load and matching conditional profile guidance | Workflow Step 3, unchanged |
| Discover and update the project's actual documentation structure | Guidelines item 1, unchanged |
| Record non-obvious architectural choices in ADRs | Guidelines item 2, unchanged |
| Cover each required topic with content, explicit N/A reason or inherited-source citation | Guidelines item 3, unchanged |
| Search prior architecture decisions and project conventions before writing | Closing Capy instruction, unchanged |

The entire Guidelines section and both linked shared protocols are byte-identical to the branch baseline. No original documentation obligation was deleted or weakened.

## Improvements

- The mandatory loading gate now explicitly includes shared protocols, including invocations that eventually need no edits. The bounded inspection exception reconciles this gate with profile detection's need to inspect signals.
- Workflow Step 5 now requires purpose and applicable current/planned behavior before reference detail, retaining evidence limits and unresolved decisions. This is a concrete drafting requirement added by `1179fda`.
- The optional clarification suggestion names created or materially revised outputs and is omitted for unchanged documents. Rubric topics, N/A reasons and inherited citations remain drafting's responsibility, and the suggestion cannot replace project-prescribed review.
- The new evals exercise profile retention and no-op behavior. Their assertions no longer pretend that a recommendation performs an editorial pass or independently verifies fidelity.

## Intentional Pivot Trade-off

The pre-pivot version loaded and ran the shared clarity procedure automatically. That required a distinct source investigation, protected-meaning inventory, audience/access checks and final comparison with the original and evidence. Those additional guarantees are now available only when the user chooses the separate clarification workflow.

This is the explicit decision in [ADR 0009](../../adr/0009-optional-document-clarification.md). It reduces automatic verification and instruction-loading cost; it does not regress the document skill's contract at branch base. Ordinary drafting still owes accurate explanations and required rubric coverage, but the replacement sentence is not equivalent to executing the removed verification procedure.

No residual references point to the removed per-skill clarity symlink. The underlying shared procedure is unchanged by the pivot. The linked instruction set returns from four files before the pivot to three at HEAD, removing a 127-line, 7,273-byte procedure from ordinary invocations.

## Neutral Changes

- Clarification is recommended rather than invoked; no extra required gate or verification claim was introduced.
- Formatting and phase wording make the workflow explicit without removing the original Guidelines.
- Oracle files remain outside staged `test-files/`. The Kustomize fixture is deliberately empty and serves profile detection, not deployment validation.

## Verification and Limits

The three-file reachable instruction set was checked at both branch endpoints and the pivot revisions; no missing file links were found. Changed document files match their generated Codex counterparts under the declared transformations. All six integration eval definitions across design/document passed JSON, assertion-ID and fixture-existence checks. The plugin structure suite passed 184 assertions; the scoped whitespace check was clean.

The behavioral scenarios were reviewed rather than executed. No fresh independent-reader comparison was performed. The conclusion is that the written workflow is stronger than the branch baseline, with the explicitly accepted loss of the automatic clarification pass relative to the intermediate implementation.
