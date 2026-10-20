# Repository evidence cleanup — 2026-10-20

The maintainer ran the prepared history filter, the exact lease-protected atomic
push, linked-worktree index alignment, reflog expiry and garbage collection.
The assistant verified the resulting trees, refs and release asset metadata.
This record describes those observations; release promotion remains separate.

## Verified results

| Check | Observed result |
| --- | --- |
| Merged pre-rewrite master | `d447d5c3017fce7a16858f6153c193dd9213be57` |
| Rewritten master | `723d6940026291cfe3ac10a2bb0bb91cf36c1ac7` |
| Intended tracked paths removed | 78,623 |
| Retained tracked paths | 2,323, with identical modes and blob IDs |
| Unexpected additions / retained-file modifications | 0 / 0 |
| Filtered paths still in locally reachable ref history | 0 |
| Changed remote refs verified | `master`, `gh-pages`, and eight tags, all matching their rewritten local values |
| Local-only branch | `claude_settings` rewritten locally; not created on the remote |
| Local objects after GC | 14,335 packed objects, one pack, 6.11 MiB; no loose objects or garbage |
| Uploaded evidence after rewrite | All 27 asset IDs, names, sizes, states and SHA-256 digests still match the verified receipt |

The ordinary `origin/master` → `master` diff also reported 78,623 changed files
and 4,322,662 deleted lines, with no non-deletion differences. After GC the complete
master tree still matched the saved post-filter tree. The main worktree was clean
before this documentation follow-up. These measurements precede its new commits;
they are not claims about GitHub's internal storage or future pack sizes.

The linked `claude_settings` worktree initially retained 5,482 filtered entries
in its index. Its index was reset to its rewritten HEAD without changing working
files. The existing `.gitignore` edit remained byte-identical, and the index has
no staged changes. Working copies there became untracked; local archives and
other ignored working files were not deleted or made part of the new history.

## Preserved revision mapping

The filter's original output is retained verbatim:

- [Commit map](records/history-rewrite-20261020/commit-map.txt): 904 original commit mappings.
- [Ref map](records/history-rewrite-20261020/ref-map.txt) and
  [changed refs](records/history-rewrite-20261020/changed-refs.txt).
- [Remote refs before](records/history-rewrite-20261020/remote-refs-before.tsv)
  and [verified changed remote refs after](records/history-rewrite-20261020/remote-refs-after-push.tsv).
- [Tree/ref comparison](records/history-rewrite-20261020/tree-comparison.json):
  expected remote leases, resulting object IDs and preservation counts.

The filter's ref-map and the observed remote lease snapshot have distinct
provenance; neither is rewritten to resemble the other. Plain mapping records
do not keep the old Git objects reachable. Archive manifests retain original
revision identities rather than substituting rewritten IDs.

## Evidence references and retained material

The 549 Markdown links into removed captures now resolve to retained feature
archive notes. Each link title names the exact original `payload/...` member
and any original section anchor. Labels and historical findings/grades are
unchanged. The destinations were checked against the verified extracted archives;
they are not invented replacements for absent evidence.

Keep design/implementation/task decisions, compact results, useful small reviews,
canonical evals/oracles, maintained tools and generated counterparts in Git.
Internal archival records under `docs/archives/` are excluded from the public
MkDocs build, like `docs/feat/` and `docs/reviews/`.

The [release receipt](release-assets.json) supplies v0.24.0 asset URLs and
authenticated API IDs for the current draft. The missing temporary-input limit
remains accepted; no historical experiment was rerun or regraded.

## Documentation and tooling checks

- All 549 archive-member titles resolve to members in the verified extracted
  archives, and no remaining Markdown links target filtered captures.
- All 1,026 local links in the changed/new Markdown documents resolve after relocation.
  The seven modified historical documents outside functional-review preserve
  their non-link prose exactly.
- All six retained mapping/comparison files are byte-identical to the saved
  rewrite observations; the archive register and release receipt parse as JSON.
- The 15 portable tooling tests pass on Python 3.12.11 from a temporary copy
  outside the repository after capture removal.
- `make docs-build` passes under strict mode. Two existing ADR links outside
  the documentation tree and the retained-tooling README link now use their
  repository URLs. Internal archive records use the same public-site exclusion
  as feature/review records. The graph's existing cycle warning is nonfatal.
- Authored-document whitespace validation passes.

Independent [closure review](../../feat/done/functional-review/reviews/archive-cleanup-review.md)
approves without findings. The review sampled redirects/maps and attributes
exhaustive checks above to the parent session. Final status reconciliation and
relocation of the 25 retained feature documents to `docs/feat/done/functional-review/`
followed review; their path/link validation passes and is parent-owned. Task 13.7 and Task 13
are complete. The closure review is retained alongside the existing documents.
Ignored remnants at the original worktree path were not moved into Git.

## Remaining release action

Commit and normally push the documentation/reference updates, then promote
v0.24.0 when ready. No further force-push is needed for these ordinary new commits.
Publishing the draft has not been performed by the cleanup.
