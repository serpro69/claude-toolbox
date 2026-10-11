## Review Summary (Isolated Mode)

**Reviewers:**
- **code-reviewer** (`kk:code-reviewer` sub-agent): finished. It read all the source it was given.
- **PAL:** didn't run. The `pal` MCP server failed to connect (`CONNECTION_CLOSED`), so there's no external review and nothing could be corroborated.
- **Shell:** Bash was denied this session. I couldn't run `git diff --cached`, get the base copy of `routes.py`, or run tests.

**Files reviewed:** `preview.py` (new) and `routes.py` (changed), plus the unchanged `config.py`, `settings.py`, `tests/test_routes.py`, `README.md` and `tasks.md`. All of this was read from the working tree, which I assumed matches the staged version because the session-start status showed nothing unstaged. The actual `routes.py` diff was not inspected.

**Overall assessment: COMMENT.** No defects found. It isn't APPROVE only because one Task 1 requirement, "Preserve existing routes", can't be checked without the base `routes.py`.

**Intent and scope:**
- Source: `README.md:5-10` and `tasks.md:3-8`.
- In scope: Task 1, "Prepare preview module" (in progress).
- Out of scope: Task 2, "Implement and enable export preview" (pending).
- Reviewed: staged changes against base `f1a16b5`.

**Baselines:** base `f1a16b5` vs. the staged changes. There's no deployed baseline; the README says no deployment inventory is kept.

**Profiles:** only `python` applies (`.py` files). All four of its checklists were used: security, SOLID, code quality, removal plan.

### Behavior and Compatibility
All of this comes from reading the code. No tests were run.

| Scenario | Expected | Result | Conclusion |
|---|---|---|---|
| `get("/settings")` | `(200, {"theme":"light"})` | `routes.py:7-8` is checked first, and `settings.py` is unchanged | Supported |
| `get("/unknown")` | `(404, None)` | Ends at `routes.py:11` | Supported |
| `get("/export-preview")` with the flag off | `(404, None)` | `config.py:1` sets the flag to `False`, and the `and` check stops before `render_preview()` | Supported |
| Can a request or environment variable turn the flag on? | No | It's a hard-coded constant in the code | Supported |
| Importing `routes` | No side effects | `preview.py` only defines a function, and nothing shadows the module name | Supported |
| Shipping Task 1 on its own while Task 2 is pending | All reachable paths work | `render_preview` can't be reached | Supported |
| No route from the base version was removed or changed (`tasks.md:7`) | No regression | The base `routes.py` couldn't be retrieved | **Unknown** |
| Persistence, migration, deployed environment | — | No state is involved and there's no deployment inventory | Not applicable |

### Code Reviewer Findings
No P0–P3 findings.

The `NotImplementedError` stub and the guarded route can't be reached today. That's intended: Task 1 asks for them (`tasks.md:8`), so they aren't leftover dead code to remove.

### Notes for Task 2 (not current defects)
These only matter once Task 2 starts:
- **Flipping the flag first breaks the endpoint.** If `EXPORT_PREVIEW_ENABLED` is turned on before `render_preview` is written, `/export-preview` raises an uncaught error. The existing `test_preview_route` would fail and catch this.
- **Tests must patch the right name.** `routes.py:1` copies the flag at import time with `from config import …`, so Task 2's tests must patch `routes.EXPORT_PREVIEW_ENABLED`. Patching `config.EXPORT_PREVIEW_ENABLED` has no effect on routing.
- **The `preview` import could take down every route.** `routes.py:2` always imports `preview`. If Task 2 gives `preview` its own imports and one fails, every route breaks, including `/settings`. Moving that import inside the guarded branch would avoid this.

### Outstanding Evidence
1. **Base `routes.py` comparison** (the reviewer asked for this). Run `git diff --cached -- routes.py` and confirm the change only adds the two imports and the guarded branch. If so, this becomes APPROVE; if a base route was dropped, it becomes REQUEST_CHANGES. I couldn't get it because Bash was denied, and I didn't try to route around that.
2. **Test run:** `python3 -B -m unittest discover -s tests`, which hasn't been run.
3. **External review:** reconnect PAL if you want the second, independent review.

The knowledge base was empty, so there were no earlier findings to compare against. No findings to index. I created no temporary files, so there's nothing to clean up.

To finish the review, allow Bash for `git diff --cached` and the test command. I'll then close the Unknown row and give a final verdict, without changing any code.
