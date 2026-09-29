# Final consumer applicability audit — 2026-09-29

Status: independently assessed. **All 40 preserved WIP reader-answer verdicts remain PASS**, with each initial and handoff-retry comparison scoring **5/5 → 5/5**. The oracle source corrections and four oracle-shape normalizations preserve applicable acceptance. All five consumer results remain applicable to shared-procedure SHA256 `5908c353733671baffd74e0e8e17bfac2b9c3eb62bd3423643896613b7590e35`.

The initial unchanged-resume assertion **7.3 remains FAIL**; its separate handoff retry remains PASS. No initial or retry oracle, artifact, trace or verdict was replaced.

## Evidence and independent assessment

- [Exact grader request](grader-request.md), [manifest and actual session metadata](manifest.json), [readable trace](grader-trace.md), [raw trace](grader-trace.jsonl), and [complete verdicts](verdicts.json).
- Corrected-source oracle snapshots and exact diffs: [refinement](oracles/clarity-refined-documents-only/expected.json), [refinement diff](oracles/clarity-refined-documents-only/delta.diff), [unchanged resume](oracles/clarity-unchanged-resume/expected.json), [resume diff](oracles/clarity-unchanged-resume/delta.diff). These are the intermediate corrected-source versions before subsequent shape normalization.
- Final shared [source snapshot](document-clarity.md) and [exact delta](shared-delta.diff) against the previously audited shared file.
- Later normalization [manifest](oracle-shape-normalization/manifest.json) and exact [grader addendum](oracle-shape-normalization/grader-addendum.md). Each case directory preserves before.json, after.json and delta.diff: [after drafting](oracle-shape-normalization/clarity-after-drafting/after.json), [refinement](oracle-shape-normalization/clarity-refined-documents-only/after.json), [resume](oracle-shape-normalization/clarity-unchanged-resume/after.json), [profile](oracle-shape-normalization/clarity-preserves-profile/after.json). These after.json files are the final normalized oracle snapshots.

The fresh general-purpose grader used `fork_turns="none"` and actual recorded gpt-6-astra/xhigh settings, CLI 0.159.0, session `01a0eeb7-41a3-7500-bbbe-003b4b3504c4`. Model build and temperature are unexposed.

## Results

| Assessment | Result |
| --- | --- |
| WIP source-isolation corrections | PASS: absent after-drafting references and inapplicable conditional clauses were removed; no applicable acceptance was weakened |
| Initial refinement readers | PASS: 5/5 → 5/5; fidelity and assertions 6.1–6.4 remain supported |
| Handoff-retry refinement readers | PASS: 5/5 → 5/5; fidelity and assertions 6.1–6.4 remain supported |
| Initial unchanged-resume readers | PASS: 5/5 → 5/5; fidelity remains supported; historical assertion 7.3 remains FAIL |
| Handoff-retry unchanged-resume readers | PASS: 5/5 → 5/5; fidelity and assertions 7.1–7.3 remain supported |
| Four oracle-shape changes | PASS: only baseline_defects changes from scalar to a singleton array; element 0 exactly equals the old scalar |
| Final shared-source applicability | PASS for all five consumers: PR outcome wording is outside their artifact scope; removing “any” does not change caller ownership of required review |
| Evidence audit | PASS: 192 declared hash comparisons plus eight normalization hashes match; exact diffs reproduce |

The grader found no disagreements with prior comprehension or fidelity conclusions. It retained the operator-guide baseline's FAIL/PARTIAL answers and the initial handoff failure.

This is retrospective grading and reasoned applicability, **not fresh editor or reader execution against final oracle/shared-file bytes**. It does not behaviorally validate the changed PR branch, test automated-harness compatibility with the JSON field type, or establish human-comprehension improvement. Route coverage remains instruction inspection rather than lifecycle execution. Allowed-file manifests and visible traces provide shared-filesystem controls, not OS isolation; hidden reasoning and unexposed model settings were not audited.
