# /kk:clarify-docs reader-task refinement

Reviewed 2026-10-02 through standalone `/kk:implement`.

This records the first refinement. The subsequent checklist change and executed
behavioral trials are recorded in [the consolidation results](clarify-docs-consolidation/results.md).

## Change

The [shared clarity procedure](../../../klaude-plugin/skills/_shared/document-clarity.md)
now addresses the full reading path: group practical instructions and their
qualifications, keep supporting evidence accessible, and remove obsolete history
only when it carries no unique protected meaning. Verification walks representative
reader tasks before the separate fidelity check. Scope, visibility, no-op behavior
and the absence of a word-count target remain unchanged.

[Case 25](../../../klaude-plugin/skills/clarify-docs/evals/long-integration-guide/eval.json)
provides a 2,062-word synthetic integration guide with a clear opening and fragmented
later instructions. Its grader-only oracle separates task discoverability from
fidelity, including decision provenance, open decisions and evidence limits.
Codex copies were regenerated from the canonical files.

## Review

The independent code reviewer found one P2 in the new Python fixture: invalid bulk
rules returned the inactive-mode error before validation. The correction validates
the rule first; 10 invalid and six valid rule/mode probes passed with no writes on
rejection. The reviewer approved the correction with no remaining findings.

PAL/Gemini reported no findings, but its metadata reported zero embedded files.
Treat that result as limited supplementary evidence. No systemic P0/P1 findings or
new project conventions required indexing.

## Verification and limits

- All nine shell suites passed: 600 assertions, zero failures. Three template-sync
  network checks skipped resolution of `master`, `HEAD` and `latest`.
- `make generate-kodex` passed its Go and structure tests. Generated scenario files
  and shared instructions match the source transformations.
- `make plugin-graph` passed its Go tests and found no broken edges or orphans;
  it retained its cycle warning.
- All 25 evaluation definitions passed ID, assertion-number and fixture-path checks.
  The new oracle parses, and representative Python model outcomes passed.
- Whitespace checks passed. Sandbox cache failures were rerun successfully with
  offline cache access. Temporary Git fixture signing was disabled per process;
  no global Git configuration changed.

At this review, the new behavioral evaluation had **not** been model-run. The repository supplies
manual scenarios rather than an automated runner; fixture checks and review do not
establish measured comprehension improvement. The skill maintainer's next behavioral
validation is to stage case 25 with baseline/revised instructions and fresh readers,
alongside `already-clear`, `source-disagreement` and `cross-file-preservation`, using
the [evaluation protocol](../../../klaude-plugin/skills/clarify-docs/evals/README.md#long-integration-guide-scenario).
Record manifests, instruction hashes, traces, reader answers and separate
discoverability/fidelity verdicts before claiming a behavioral pass.
