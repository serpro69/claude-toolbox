# Change context (parent-prepared, factual)

## Intent and authority
- Source: README.md (repo root) and tasks.md (repo root). Explicit.
- README: "This increment prepares the export-preview module. The existing GET /settings
  response and routing behavior remain the acceptance contract. Export preview activation
  belongs to a later task; this increment must remain independently compatible while that
  task is pending. The checked-in build setting is fixed at False; it is not supplied by a
  request, environment variable or external config. No deployment inventory is maintained
  in this small source repository."
- tasks.md Task 1 (in-progress, the reviewed increment): "Preserve existing routes with
  preview disabled in the checked-in build. Add the preview module and guarded route for
  the next increment."
- tasks.md Task 2 (pending): "Implement render_preview and its enabled-path tests before
  changing the build setting."

## Change boundary
- Selector: staged changes (`git diff --cached`); no unstaged or untracked changes exist.
- Review base: commit f1a16b5 ("Review base"), branch master. Candidate: git index.
- Worktree files for preview.py and routes.py are identical to the index (verified by an
  empty `git diff --name-only`), so worktree paths are valid candidate source.
- Changed: preview.py (added), routes.py (modified). Unchanged: config.py, settings.py,
  tests/test_routes.py.

## Existing behavior (base)
- Base routes.py is fully contained in the diff hunk (all 7 original lines appear as
  context): imports current_settings; get("/settings") -> (200, current_settings());
  any other path -> (404, None).
- Only in-repo consumer of routes.get: tests/test_routes.py (grep over *.py).

## Delivery constraints
- Python 3.9+, standard library only.
- Increment must be independently compatible while Task 2 is pending.
- config.EXPORT_PREVIEW_ENABLED is a checked-in constant False (config.py line 1).

## Baselines
- Review base f1a16b5 vs index candidate. No release/deployed baseline exists in repo
  (README: no deployment inventory). Deployment state is Unknown and out of scope.

## Attributed verification (parent-executed, not independent)
- `python3 -B -m unittest discover -s tests -v` run by the parent against the worktree
  (identical to the index for reviewed files) on Python 3.10: 3 tests ran, all OK
  (test_current_settings, test_preview_route, test_unknown_route).
- tests/test_routes.py is unchanged by this diff; test_preview_route already existed at base.

## Knowledge base
- capy search of kk:review-findings and kk:lang-idioms: knowledge base empty (cold start).
