# Retained tooling review — Task 13.7 preparation

Date: 2026-10-20. Reviewer: independent `code-reviewer` sub-agent, without author
conversation. Final source verdict: **APPROVE**. Python review guidance and the
functional method loaded before source investigation. PAL remains deferred.

Scope: the nine retained tooling/test files under
`scripts/functional-review-evals/` and `test/test-functional-review-tools.sh`.
Historical evidence supplied as read-only copies outside the worktree, bound to
revision `73c8b69ad5bea7bffff7d4d60f4e6a67072d83b0` and the original SHA-256 values
in `provenance.json`. The reviewer inspected complete new files because they were
untracked; ordinary `git diff` would omit them.

The initial review found one P2: the extracted receipt collector requested
supplementary thread metadata before saving successfully fetched items. An RPC
failure would lose evidence that the historical adapter preserved. The corrected
collector saves sanitized items first, then requests metadata and propagates its
failure. A synthetic metadata-error regression verifies retained items and absent
metadata. Targeted independent re-review confirms the issue resolved; no findings
remain. No systemic P0/P1 pattern requires indexing.

Source inspection supports module independence, bundle filtering, seal validation,
public history traversal, process ownership, inventory comparisons and documented
usage. It does not certify live provider behavior, model reliability, archive
retrieval or historical source recovery. The reviewer ran no tests.

Parent execution evidence: all 13 repository shell suites passed; following the
receipt fix, all 15 extracted tests passed on both Python 3.11.13 and 3.12.11 from
temporary copies outside the repository. Historical evidence and distributed
plugin/agent files have no diff. Preparation does not close the human archive step.
