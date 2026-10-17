# Independent review of Task 12 preparation

Reviewer `/root/review_task12_controller`, fresh `code-reviewer` role with no
author history, inspected the controller, tests, contract and task update plus
unchanged capture dependencies. Python's four review checklists and common
methodology were loaded before evidence. Review base:
`4fb1941779f6b24dbed4440c288f1d901f0c4609`.

Three integrity defects were corrected before measured capture:

1. Revalidate mutable actor bundle, prompt, subject files, runtime configuration,
   review identity and empty knowledge state immediately before transport.
2. Reject overlapping actor/evidence/controller/snapshot destinations before
   creating paths, preventing grading/results material from entering actor inputs.
3. Bind retained-manifest digest to the builder's revision identity and freeze;
   validate the source archive digest as well.

Focused re-review returned **APPROVE**, no remaining P0–P3 findings. It confirmed
the source guards; the parent executed 12 passing tests. Approval covers the
preparation slice only: runtime completeness, full matrix, Codex, controls,
grading and material-access audits remain separate obligations.

PAL `gemini-3.1-pro-preview`/max, continuation
`8610aa8c-aa4b-41bb-afdb-944726500efd`, returned no findings against the earlier
slice, while reporting **zero embedded files**. Its broad clean-review claims
are not adopted; source coverage is unverified and it does not corroborate the
independent review. No operative skill instructions changed in this slice.

## Instruction correction review

The same independent reviewer separately loaded all three skill-md checklists
and reviewed six canonical/generated instruction files against base `4fb194`.
It identified a provisional conflict with the existing detection ENOENT/root
fallback. That conflict was corrected before candidate 3 measurement, and the
reviewer verified the generated counterparts after regeneration.

Final **APPROVE**, no P0–P3 findings: one post-instruction investigation entry
remains; detection records distinguish skipped lookups from allowed unavailable
outcomes; component documentation and actual lifecycle transitions are bounded,
general requirements rather than fixture-specific hints. Source review does not
establish behavioral acceptance. PAL review was not repeated after the user
directed that PAL-based verification be ignored for now.

## Final controller review — REQUEST_CHANGES

The same independent reviewer reviewed eleven new controller/helper files
(702 lines), tracing unchanged capture, grading and MCP helpers. It found no
additional substantiated grading-package defect. It confirmed the candidate-4
instruction amendments and generated parity separately; that source approval
does not establish behavioral acceptance.

Three capture-runner defects remain **open**. No new actors may be launched
through these runners until the ownership and runtime-status issues are fixed:

| Severity | Trigger and consequence | Required correction and verification |
| --- | --- | --- |
| P1 | Root `run-claude-batch.sh:22` and `candidate2/run-batch.sh:14` launch a background capture before later fallible preparation. `set -e` can exit before the wait loop, abandoning earlier jobs. | Prepare all inputs first; on driver failure/interruption safely wait for or cancel and reap every owned capture through its cleanup path. Offline subprocess tests must prove ownership on preparation failure and interruption. |
| P2 | `controller.py:250` delegates to a helper that records nonzero actor exit in `completion.json` but returns normally. All batch scripts can report runtime authentication/model/launch failure as success. | Propagate runtime failure after sealing at a new identified batch boundary; distinguish it from behavioral assertion FAIL with runtime exit zero. Test both outcomes and missing completion. |
| P2 | `probe_pal.py:43` calls fallible `client.close()` before writing events and sealing. A buffered-stdin close error can leave stderr unsealed/unredacted. | Ensure cleanup failure cannot skip recording/sealing and retain the primary exception. Verify offline with a failing teardown; live PAL remains user-deferred. |

The existing twelve tests cover freeze/preparation drift, not these subprocess
and finalization paths. Their passing result does not close these findings.
Historical controllers, freezes and captured evidence must remain byte-identical;
corrections require new identified adapters rather than rewriting old identities.
These findings are retained at the repeated-verification stop; no correction or
re-review is claimed. Owner: implementing agent before Task 12 capture resumes.

The systemic P1 ownership/finalization pattern was indexed as
`kk:review-findings`. No duplicate project convention or test-pattern entry was
created from the already documented experiment rules.
