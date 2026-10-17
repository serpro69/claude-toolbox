## Code review summary

**Files reviewed**: 2 files, +6 lines (staged: `preview.py` added, `routes.py` modified)
**Overall assessment**: **APPROVE**
**Intent and scope**: This is Task 1 of `tasks.md`, "Prepare preview module". It should add the preview module and a guarded route while keeping existing routes unchanged with preview disabled. Task 2 is pending and is out of scope: it implements `render_preview`, adds tests for the enabled path and turns the setting on. `README.md` says the acceptance contract is the existing `GET /settings` response and routing behaviour, and that the increment must stay compatible on its own. I reviewed it mid-implementation.
**Baselines**: The review base is `f1a16b5` (HEAD). The candidate is the staged index; there are no unstaged changes, so the working tree matches the index. There's no separate release or deployed baseline, since `README.md` says no deployment inventory is kept.

## Behaviour and compatibility

| Contract | Before → after | Evidence |
| --- | --- | --- |
| `GET /settings` → `(200, {"theme": "light"})` | Unchanged; this branch runs before the new one | `routes.py:7-8`, `test_current_settings` passes |
| Unknown path → `(404, None)` | Unchanged | `test_unknown_route` passes |
| `/export-preview` with the checked-in build | Still `(404, None)`. `config.EXPORT_PREVIEW_ENABLED = False` is a constant in the repo, and the `and` stops before `render_preview()` would be called, so the stub's `NotImplementedError` can't be reached | `config.py:1`, `routes.py:9`, `test_preview_route` (already in the base) passes |
| Importing `routes` | The new imports of `config` and `preview` load cleanly and have no side effects at import time | Tests import `routes` successfully |

- **Existing routing, against `f1a16b5`:** Supported. I traced the source, and `python3 -B -m unittest discover -s tests` ran 3 tests, all passing.
- **Shipping Task 1 without Task 2:** Supported. The guarded path can't be reached in the checked-in build, and `preview.py` is in the same change as the import that needs it.
- **Enabled preview path:** Not applicable. It belongs to pending Task 2, and `tasks.md` already requires implementing it and adding tests before the setting is changed.
- **Deployed environments:** Not applicable. No deployment inventory exists and no release check was requested.

The Python checklists (security, SOLID, code quality and removal) turned up nothing. The only input is a string compared for equality, with nothing that reaches I/O or gets deserialised. Two routes in an if-chain don't amount to an open/closed (OCP) problem. The `NotImplementedError` stub is scaffolding for a pending task, not something to remove.

## Findings

None at P0, P1, P2 or P3.

**Indexing:** No findings to index. The `kk:review-findings` and `kk:lang-idioms` knowledge searches came back empty because the knowledge base has nothing in it yet.

**Not covered:** The enabled preview path, including what `render_preview()` returns and the 200 response shape, is Task 2's job. Task 2 should be reviewed when it lands.

I don't recommend any changes; Task 1 is ready as staged.
