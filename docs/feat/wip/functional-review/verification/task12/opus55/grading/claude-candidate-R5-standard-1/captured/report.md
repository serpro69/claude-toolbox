## Code Review Summary

**Overall assessment**: APPROVE. This covers the code only. I couldn't run the tests, so the evidence is from reading the source.
**Files reviewed**: 2 files, 6 lines added (`preview.py` is new; `routes.py` is modified).
**What I reviewed**: the staged diff (there are no unstaged changes). The worktree matches the index, so what I read is exactly what you staged.
**Intent and scope**: Task 1 in `tasks.md`, "Prepare preview module". The requirements come from `README.md` and `tasks.md`:
- The `GET /settings` response and existing routing must not change.
- The new increment must be safe to ship on its own while Task 2 is pending.
- `EXPORT_PREVIEW_ENABLED` is a fixed `False` in the checked-in build, not something a request or the environment can set.

Task 2 (implement `render_preview` and turn it on) is pending, so it's out of scope.
**Baselines**: I compared `HEAD` (`f1a16b5`) against the staged index. There's no deployment inventory in this repo, so I didn't assess any deployed version.
**Review method**: the `python` profile was active (both files are `.py`), and I applied its security, SOLID, code-quality and removal checklists plus the general review method. The knowledge base had nothing indexed yet, so there was no history to check against.

## Behavior and Compatibility

| Scenario | Before | After (staged) | Evidence |
| --- | --- | --- | --- |
| `GET /settings` | `200, {"theme": "light"}` | Same. This branch is checked first and wasn't changed. | Source: `routes.py:7-8`, `settings.py` |
| `GET /export-preview`, flag `False` | `404, None` | `404, None`. The `and` stops at the `False` flag, so `render_preview` is never called. | Source: `routes.py:9`, `config.py:1` (same at `HEAD` and staged) |
| Any other path | `404, None` | `404, None` | Source: `routes.py:11` |
| Importing `routes` | Imports `settings` only | Also imports `config` and `preview`. Neither does anything on import, and there's no circular import. | Source |
| Flag `True` (not possible in this build) | n/a | `render_preview()` raises `NotImplementedError` | Source. Task 2 requires implementing this before the flag changes. |

- **Disabled flag**: Supported. The new route is guarded by a constant that is fixed in the checked-in build and can't be set from outside.
- **Existing callers of `routes.get`**: Supported. The signature and return shape are unchanged, and the only caller in the repo is `tests/test_routes.py`.
- **Shipping on its own**: Supported against `HEAD`. Nothing is migrated and no state is stored, so rolling back is just a revert.
- **Deployed environments**: Unknown and outside this review, because the repo doesn't track deployments. This doesn't affect the code verdict.

**Tests**: the three existing tests in `tests/test_routes.py`, all unchanged, cover the expected behavior:
- `/settings` returns 200.
- An unknown path returns 404.
- `/export-preview` returns 404 while preview is disabled.

**Limits**:
- My attempt to run `python3 -B -m unittest discover -s tests` was blocked by the permission mode. Everything in this review comes from reading the code. I haven't seen the tests pass.
- I didn't check the files in `.runner/`. They aren't tracked by git and aren't part of this diff.

---

## Findings

None at any severity (P0–P3).

Things I checked that turned out not to be problems:
- **The `NotImplementedError` stub**: the route that calls it can't be reached in this build, and Task 2 explicitly owns implementing it. It's planned scaffolding, not dead code to remove.
- **The `if`-chain in `get()`**: with two routes, adding a routing table would be abstraction before it's needed.
- **Importing the flag directly** (`from config import EXPORT_PREVIEW_ENABLED`): Task 2's enabled-path tests can still patch `routes.EXPORT_PREVIEW_ENABLED`, so this doesn't block testing.
- **Security**: nothing new is exposed while the flag is off, and the only input is an exact path string. The repo has no auth layer anywhere, so there's nothing for this route to be missing.

**Not covered**: whether the preview endpoint needs auth or other protections once enabled belongs to Task 2.

No findings to index. I don't recommend any changes.
