# Filter archived captures from Git history

Prepared against `90e0e25a` after archive upload/download verification. Run this
after merging the branch into `master`. This file supplies the command; no
rewrite, merge or push was executed while preparing it.
It uses the normal full local rewrite, not a `master`-only `--refs` restriction.

```bash
git filter-repo \
  --path-regex '^docs/feat/(wip|done)/(functional-review|brainstorm-skill|clarify-docs|clarify-issue-descriptions)/verification/' \
  --path-regex '^docs/feat/(wip|done)/(codex-support|go-vendor-integration|isolated-review-agents)/\.sessions/' \
  --path-regex '^docs/feat/(wip|done)/kubernetes-support/(kubernetes-support/)?\.sessions/' \
  --path-regex '^docs/feat/reviews/clarify-docs-consolidation/(?!(?:results|protocol)\.md$).+' \
  --invert-paths \
  --force
```

The multiple expressions select a union of paths; inversion removes that union.
Both `wip/` and `done/` are covered because filtering does not follow renames.
[Official filter-repo reference](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt).

## What stays

This applies the individual [retention decisions](README.md), not wholesale
deletion of every feature directory included in an archive:

- Root design/implementation/task/verification summaries and written reviews.
- All `design-skill-refinement/.reviews/` reports.
- Consolidation `results.md` and `protocol.md`.
- `docs/archives/`, compact result copies, maintained scripts, source, fixtures,
  oracles, profiles, tests and generated plugin files.
- Ignored local archives, which are not Git objects and do not match these filters.

All other files beneath the consolidation experiment are archive-only: captured
evidence, snapshots, instruction copies, requests, detailed grades and manifests.
The complete experiment is already included in the clarify-docs archive.

## Checked scope

Read-only matching against current tracked files and locally available Git
history selects **78,623 current paths** and **82,652 distinct historical paths**.
Every current match exists in a verified archive. The match set equals the
explicit capture/session/consolidation removal list; 1,995 current protected
paths were checked and none matched.

| Current removal area | Tracked paths |
| --- | ---: |
| Functional-review verification | 73,141 |
| Brainstorm verification | 866 |
| Clarify-docs verification | 1,720 |
| Issue-extension verification | 2,814 |
| Codex support, Go vendoring and isolated-review sessions | 3 |
| Kubernetes support nested sessions | 6 |
| Consolidation, except its two retained root records | 73 |

Shell syntax and regex compilation pass. This is a filename-scope check, not an
executed filter-repo dry run or a claim that every historical file revision was
archived. Archives preserve the available snapshots and attempts described in
the retention records. Recheck scope if the merge introduces new capture data.

## Two adjustments to the proposed sequence

Before filtering, save the origin URL, the exact remote `master` OID for the push
lease, and a listing of the merged local tree (`git ls-tree -r --full-tree master`)
outside tracked paths. A normal full filter removes `origin`, rewrites refs and
prunes old objects. Afterward, compare the saved tree listing with the rewritten
tree; preserved paths must have identical modes/blob IDs. Do not rely on the old
`origin/master` or its objects surviving locally.
[Filter-repo behavior](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt).

For the master push, use the saved remote URL and an explicit
`--force-with-lease=refs/heads/master:<saved-remote-oid>`. A master-only push does
not rewrite other remote branches/tags that retain the old history. Inspect
`.git/filter-repo/changed-refs` and decide which other remote refs to update or
retire; this command deliberately does not choose a remote push/deletion scope.
[Git push reference](https://git-scm.com/docs/git-push).

Keep `.git/filter-repo/commit-map` and `ref-map` for original-revision lookup.
Repair references to removed evidence using the v0.24.0 archive asset/member
locators before release; a path filter does not rewrite Markdown links. The
maintainer owns that already-recorded cleanup follow-up.
