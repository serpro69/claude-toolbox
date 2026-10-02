# Stable final evidence

All three evaluation coordinators have completed their packages. The canonical
instructions, fixtures, assertions and oracle files remain unchanged.

- Aggregate: `../aggregate-verdicts.json` — 29 scenarios, exactly 133 PASS,
  0 FAIL/PARTIAL; exact assertion-ID coverage and hashes for all twelve verdict files.
- Documents: `../documents/README.md`, `../documents/summary.json`,
  `../documents/grader/verdicts.json`,
  `../documents/grader/grader-final-access-audit.json` — 40 PASS.
- Issues: `../issues/README.md`, `../issues/grading/verdicts.json`,
  `../issues/grading/coordinator-audit.md` — 47 PASS.
- PR/consumers: `../pr-consumers/README.md`, `../pr-consumers/grader/summary.md`,
  `../pr-consumers/coverage-index.json`, `../pr-consumers/grader/trace-audit.md`
  and ten per-case verdict files — 46 PASS.
- Root audit: `../checks/evidence-audit.json` — 1,335 files checked, 704 JSON files
  and 1,735 JSONL records parsed, no malformed or non-visible-context records,
  no ignored files, all twelve verdict hashes unchanged.
- Issue seal recheck: `../checks/issue-seal-audit.json` — all 310 hashes/sizes match.
- Repository checks: `../checks.md`; source review: `../review.md`.

The main `verification.md` and `tasks.md` now reflect completed behavioral evidence
and documentation/checks/source-review subtasks. Task 4 remains in progress solely
for this independent final spec review and closure. Re-read those updated files.
All four tasks remain in scope; no unfinished acceptance item is excluded.

Please finish your independent evidence/conformance audit and return concrete
findings or an explicit clean result. Claims remain bounded to the synthetic
scenario contracts; preserved invalid attempts, recovered truncations/capture gaps,
opaque transport and shared-filesystem limits are indexed in the cohort reports.
