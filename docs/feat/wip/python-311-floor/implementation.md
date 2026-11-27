# Implementation: Python 3.11 floor

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)

Read design.md first; it explains why each of these steps is shaped the way it is.

## Orientation

| Path | What it is |
| --- | --- |
| `install.sh` | Standalone installer. A bash prelude runs a Python heredoc (the bootstrap) under `python3`. The bootstrap parses on 3.6 and checks the floor itself. |
| `kk/bin/kk` | Release dispatcher. It is copied to `$KK_HOME/bin/kk` at activation, and the copy is digest-checked against the release. It resolves the release from `state.json` with `jq`, then runs `python3 -I -B <release>/kk/lib/run.py`. |
| `kk/lib/run.py` | kk entry point. It parses on 3.6 and holds `FLOOR`. `load_cli` imports `cli.py` as a package. |
| `kk/lib/cli.py` | The release lifecycle. `prepare`, `activate_staged` and `main` are the functions involved in the transition (design §3). |
| `kk/lib/validation.py` | Candidate self-test. It runs the candidate's dispatcher, its `guard.py` under `sys.executable`, and its hook handlers. |
| `klaude-plugin/scripts/guard/guard.sh` | Fail-closed hook wrapper. It owns the interpreter candidate loop. |
| `klaude-plugin/scripts/guard/run-guard.py` | Guard launcher. It parses on 3.6, holds `FLOOR`, and exits `TOO_OLD` (3) below the floor. |
| `klaude-plugin/scripts/guard/guard.py` | Guard engine. It must stay runnable on 3.9 (design §3, Rule 2). |
| `kodex-guard/scripts/guard/*` | Generated copy. Never edit it; run `make generate-guard`. CI runs `make check-guard`. |
| `pyrightconfig.json` | Strict pyright over `kk/lib` and the canonical guard. |
| `.github/workflows/machine-delivery.yml` | Runs the guard, Codex-hook and kk suites on a Python matrix, plus a `typecheck` job. |
| `test/test-hooks.sh`, `test/fixtures/guard/interpreter.sh` | Wrapper tests and the stand-in interpreter (`GUARD_FIXTURE_MODE=too-old` and others). Read/Bash p95 latency is measured here. |
| `test/guard/test_guard.py` | Engine tests, AST drift checks (`test_engine_parses_at_the_floor` area) and the launcher floor test. |
| `test/kk/test_install.py` | Entry-point grammar checks and the `run.py` floor test. |
| `test/kk/codex`, `test/kk/claude` | Fake vendor CLIs used by every kk test. |

Prior art to follow:

- the ADR 0016 commit (`ea143442`) for how floor checks, messages and tests are wired;
- `docs/feat/done/codex-launch-overrides/` for task execution notes.

## Interpreter search list

Shared by Tasks 2 and 3.

One bash function, byte-identical in `guard.sh`, `kk/bin/kk` and `install.sh`, prints candidates one per line in the order of design §1:

1. For N = 19 down to 11:
   - `/opt/homebrew/bin/python3.N`, `/usr/local/bin/python3.N`, `/usr/bin/python3.N` and `$HOME/.local/bin/python3.N`,
   - then the bare `python3.N`.
2. Then the bare-`python3` list:
   - on macOS (`OSTYPE` darwin*): `/opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 python3`;
   - elsewhere: `/usr/bin/python3 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3`.

Constraints:

- **No subshells or external commands.** A function that fills a bash array, or a loop the caller iterates, both work. Command substitution would fork, so avoid it.
- The existence test lives in the caller:
  - `guard.sh` already uses `command -v -- "$candidate"`;
  - the dispatcher and installer can do the same.
- `$HOME` may be unset in odd hook environments, so skip that entry rather than producing `/.local/bin/…`.
- `guard.sh` runs with `set -f`, so the function must not rely on globbing.
- Delimit the function with marker comments, such as `# BEGIN kk-python-candidates` / `# END kk-python-candidates`, so a test can compare the blocks.

`KK_GUARD_INTERPRETERS` keeps its meaning in `guard.sh`. When the variable is set, including set to empty, it replaces the generated list.

## Task 1: Guard latency baseline

Record the "before" numbers so Task 10 compares like with like.

- On a 3.11+ interpreter at the current HEAD, run the wrapper latency probes in `test/test-hooks.sh` with `CI` unset. Pin the interpreter with `KK_GUARD_INTERPRETERS=<python3.N>`, and use the same interpreter again in Task 10.
- Record the host, OS, Python version, Read p95 and Bash p95 in Task 1's execution context in tasks.md. They move to `docs/contributing/testing.md` in Task 9.
- If the machine has Homebrew or several Pythons, record which interpreter the default (unpinned) list selects too. Task 2 changes that selection.

## Task 2: Guard discovery and floor

Files:

- `klaude-plugin/scripts/guard/guard.sh`
- `klaude-plugin/scripts/guard/run-guard.py`
- the generated `kodex-guard/` copy, via `make generate-guard`
- `test/test-hooks.sh`
- `test/fixtures/guard/interpreter.sh`
- `test/guard/test_guard.py`
- `pyrightconfig.json`
- `.github/workflows/machine-delivery.yml`

Steps:

1. Replace `default_interpreters` in `guard.sh` with the search list above. Keep the loop body unchanged: exit 0, exit 2 validation, exit 3 continue, and the broken-shim retry.
2. Update the final `fail_closed` text to the design §1 wording, naming 3.11 and the three install routes.
3. In `run-guard.py`, set `FLOOR = (3, 11)` and update its stderr text. Keep the 3.6-parseable form.
4. Update the fixture's `too-old` message and the assertions that match it (`test-hooks.sh` around the `too-old` cases; `test_guard.py` `test_launcher_refuses_interpreters_below_the_floor`).
5. Add wrapper tests for discovery. Use a private directory of stand-in interpreters and a controlled `PATH`/`HOME`, without `KK_GUARD_INTERPRETERS`:
   - only `python3.12` (on `PATH`) exists, plus a `python3` stand-in in `too-old` mode → the call is decided by the `python3.12` stand-in, and the too-old one is never invoked;
   - `$HOME/.local/bin/python3.11` exists and `PATH` excludes it → it is found;
   - no versioned name, and a bare `python3` in `too-old` mode → denial with the new message.

   The real absolute directories (`/usr/bin`, `/opt/homebrew/bin`) are on the test host too. Write assertions that hold whatever happens to exist there. One way is to make the stand-ins record their invocation and assert which one ran first. If a case cannot be isolated from the host, mark it skipped with the reason; do not weaken the assertion.
6. Keep `guard.py` 3.9-runnable:
   - `test_engine_parses_at_the_floor` keeps `(3, 9)` for `guard.py`; rename it or adjust its docstring so it says "3.9 for the v0.27 upgrade self-test", not "the floor";
   - in `pyrightconfig.json`, add `executionEnvironments` with `klaude-plugin/scripts/guard` at `pythonVersion` 3.9 and `kk/lib` at 3.9. Task 3 moves `kk/lib` to 3.11.
7. CI: change the matrix to `['3.11', '3.x']`. The 3.9 leg would now fail the wrapper suites, because a real 3.9 interpreter is refused.
8. Run `make generate-guard`, then `make check-guard`.

→ verify:

- `bash test/test-guard.sh`, `bash test/test-hooks.sh` and `bash test/test-codex-hooks.sh` pass on 3.11+;
- `make typecheck` is clean;
- `make check-guard` reports no differences.

## Task 3: kk discovery and floor

Files:

- `kk/bin/kk`
- `install.sh`
- `kk/lib/run.py`
- `test/kk/test_install.py`
- a new parity test, placed with the other structure checks (for example in `test/kk/test_install.py` or `test/test-plugin-structure.sh`)
- `pyrightconfig.json`

Steps:

1. **`kk/bin/kk`.**
   - Add the search-list block and select the first existing candidate into a variable.
   - If none exists, print `kk: no Python 3.11+ interpreter found; install Python 3.11 or newer (uv, Homebrew, or your distribution's python3.11 package)` and exit 1.
   - Use the selected interpreter for both the self-location `-c` snippet and the final exec lines. Today all three are hard-coded `python3`.
   - Leave the `jq` release selection byte-for-byte unchanged. The transition in Task 4 depends on its `.active // .candidate.version` behavior.
2. **`install.sh`.**
   - Add the same block before the `exec … <<'PY'`, select the same way, and run the heredoc under the result.
   - Set the bootstrap's floor check to `(3, 11)`, with matching text and the install hint.
   - The bootstrap stays 3.6-parseable.
3. **`run.py`.**
   - Set `FLOOR = (3, 11)` and append the install hint to the message.
   - Remove the `exec_module` pyright ignore and its comment, since kk is now checked at 3.11. Keep the 3.6-parseable form otherwise.
4. **pyright.** Move the `kk/lib` execution environment to `pythonVersion` 3.11.
5. **Tests.**
   - `test_install.py`:
     - update `test_entry_point_refuses_python_below_the_floor` to a 3.10 version tuple and the new message;
     - in the grammar test, move non-entry modules from `(3, 9)` to `(3, 11)`;
     - entry points (`run.py`, the bootstrap) stay at the 3.6 grammar and keep the no-`__future__` assertion.
   - Add a dispatcher discovery test: with a private `PATH`/`HOME` holding a `python3.12` link to the test interpreter and a too-old `python3` stand-in, `kk/bin/kk status` from a checkout succeeds. Use whatever `test_install.py` already does to run the dispatcher from a checkout.
   - Add the parity test: extract the marked blocks from the three scripts and assert they are identical.

→ verify:

- `bash test/test-kk.sh` passes on 3.11+;
- `make typecheck` is clean;
- the parity test fails when one block is edited (check this once by hand, then revert).

## Task 4: Upgrade from v0.27.x

Files:

- `kk/lib/cli.py`
- a new transition test (for example `test/kk/test_transition.py`)
- `.github/workflows/machine-delivery.yml`

Steps:

1. **Floor check at the top of `cli.py`.** Its first statements after the module docstring and `__future__` import compare `sys.version_info` with `(3, 11)`, importing only `sys` and `pathlib`. The check must come before `from . import …`. On failure it raises `ValueError` with one of two messages:
   - The module resolves to `<home>/staging/<version>/kk/lib/cli.py` and `<home>/state.json` is a file: *kk `<version>` needs Python 3.11 or newer, but this upgrade is running under `<x.y.z>`. The release is staged; finish with: `KK_HOME=<home> <home>/staging/<version>/kk/bin/kk upgrade`*. Quote the paths with `shlex.quote`.
   - Otherwise: the plain floor message from `run.py`.

   Put the floor value in one place. A small constant in `cli.py` that a test compares with `run.FLOOR` is enough, because `run.py` cannot be imported before the check without defeating its purpose. A comment at the check explains why it exists: older releases import this module in their own process during `kk upgrade` (design §3).
2. **Transition test.** It needs a real v0.27.0 tree and two interpreters:
   - `old`: a 3.9 or 3.10 interpreter, from `KK_TEST_OLD_PYTHON`;
   - `new`: the 3.11+ test interpreter.

   Steps:
   1. Extract `git archive v0.27.0` into a temp directory. The approach is noted in the capy entry `kk:test-patterns:kk-fake-codex-fixtures-in-scratch-home` and used by earlier upgrade tests.
   2. Build a private bin directory: `python3` → `old`, `python3.<new minor>` → `new`, plus the fake `claude`, `codex` and `jq` handling the kk tests already use. Run with `PATH=<private bin>:<what the fakes need>`. Remember the guard and dispatcher also probe absolute directories; on CI those hold system Pythons that qualify, which is acceptable because the assertions are about outcomes.
   3. Install v0.27.0 with that tree's `install.sh --local <tree>` (runs under `old`).
   4. Run `kk upgrade --local <checkout>`. Assert:
      - exit 1;
      - stderr contains the staged-dispatcher command;
      - `state.json` still has `active` = the v0.27.0 release, the candidate `phase` = `staged` and no `step`;
      - `$KK_HOME/staging/<v>` exists.
   5. Run the printed command. Assert exit 0, and that `active` is the new release with no candidate.
   6. Run `kk status`. It reports ready.
   7. Run `kk rollback`. It restores v0.27.0, and the restored dispatcher still runs under `old`.

   Skip with a clear reason when `KK_TEST_OLD_PYTHON` is unset or the tag is unavailable. In CI the variable is always set, so the skip never hides a CI result.
3. **Older tags.** Check v0.26.x the same way by hand or in the same test, if the tag is reachable. Record the result in Task 4's execution context and update design.md Assumption 3.
4. **CI.** Add a `transition` job to `machine-delivery.yml`:
   - set up Python 3.9 and 3.12 with `actions/setup-python` (multi-line `python-version`);
   - export `KK_TEST_OLD_PYTHON` as the 3.9 path;
   - run only the transition test under 3.12.

   If setup-python cannot expose both at stable paths, use the paths from its step outputs (design.md Assumption 6).

→ verify: the transition test passes locally (uv can install 3.9 or 3.10) and in the CI job. Run it once, with the floor check temporarily removed, to see it fail, so you know it can catch a regression.

## Task 5: `file_digest` and `tomllib` in tests

Files:

- `kk/lib/payload.py`
- `kk/lib/guard_identity.py`
- `test/kk/codex`
- `test/test-codex-structure.sh`
- `test/kk/test_codex.py`

Steps:

1. `payload.fingerprint`: hash regular files with `hashlib.file_digest(stream, "sha256")`.
2. `guard_identity`: use `file_digest` for regular files other than `MANIFEST`. The manifest is hashed after `with_version`, so it keeps its own path.
3. The digest outputs must not change. A changed digest would invalidate journaled candidates and guard receipts. The existing payload and guard-identity tests cover this; if one doesn't pin a known digest, add a fixture with its expected value computed before the change.
4. `test/kk/codex`: replace `toml_value`'s hand parser with `tomllib.loads("v = " + text)["v"]`.
   - Keep the fallback: an unparseable value returns the raw text, as Codex does. Keep the docstring's meaning.
   - The fake runs under the test interpreter (`#!/usr/bin/env python3`); confirm the kk tests invoke it with 3.11+.
5. `test-codex-structure.sh`: `validate_toml` becomes a single `tomllib` check. Fail with a clear message if `python3` lacks it; don't silently pass.
6. `test_codex.py` `test_toml_round_trip`: drop the `skipTest` branch.

→ verify:

- `bash test/test-kk.sh` and `bash test/test-codex-structure.sh` pass;
- digest values are unchanged (compare an existing release fingerprint before and after);
- `make typecheck` is clean.

## Task 6: Typing pass for kk

Files: every module under `kk/lib` except `run.py`, plus `test/kk/*.py`. This is a mechanical change.

1. Run `pyupgrade --py311-plus` (or `ruff check --select UP --target-version py311 --fix`) over `kk/lib/*.py`, excluding `run.py`, and over `test/kk/*.py`. Run the tool from a scratch environment; do not add it as a project dependency.
2. Review the diff for anything that is not a pure rewrite. In particular, `typing` imports should become unused and be removed, never moved.
3. Keep `from __future__ import annotations` in these modules. It is harmless, and removing it is churn.
4. Do not touch `klaude-plugin/scripts/guard/` (Rule 2) or the entry points.

→ verify: `make typecheck` is clean, and `bash test/test-kk.sh` passes. This is the only check needed for a mechanical rewrite.

## Task 7: `TypedDict` state records

Files:

- `kk/lib/state.py`, which defines the types
- `kk/lib/payload.py`, where `JSONObject` lives
- the modules that read or write the record: `cli.py`, `codex_profile.py`, `codex_plugins.py`, `migrate.py`, `notice.py`, `codex_launch.py`, `claude_launch.py`, `mixed.py`, `codex_trust.py`

Steps:

1. **Define the types in `state.py`.**
   - `StateRecord` covers `format_version`, `active`, `rollback_target`, `candidate`, `releases` and `installed_paths`.
   - Optional keys use `NotRequired`: `pending_entry`, `pending_entry_sha256`, `codex_paths`, `codex_plugins`, `codex_claim`, `codex_override_hash`, and any others found.
   - `Candidate` and `ReleaseRecord` follow the same pattern.
   - Derive the key set from every place the code reads or writes the record (about 180 sites, mostly in `cli.py` and `codex_*`). Don't derive it from memory.
   - Values the code treats as opaque stay `JSONObject`.
2. **`state.load`** returns `StateRecord`. After its existing format check, narrow with a `cast`. No new validation: this types the program, not the data (ADR 0016 Consequences).
3. **Change signatures** that take or return the record from `JSONObject` to these types. Fix the pyright findings this produces. If a finding reveals a real inconsistency, such as a key written but never read or read with two different types, record it in the execution context. Fix it only if the fix is local and behavior-preserving; otherwise leave a `TODO` and a note.
4. **The on-disk format is unchanged.** `format_version` stays 1, and older releases must still read the file on rollback.

Treat this as M. Most of the diff is mechanical signature changes. If pyright fallout grows beyond one coherent commit, split by module behind temporary `cast`s at the boundary, and record the split.

→ verify: `make typecheck` is clean, `bash test/test-kk.sh` passes, and a `state.json` written by the new code is byte-compatible (`test_lifecycle.py`'s rollback cases).

## Task 8: Guard regex timing

Files:

- `test/guard/test_guard.py`
- possibly `klaude-plugin/scripts/guard/guard.py`, then regenerate

Steps:

1. **Timed probes.** For each pattern listed in design §4, add a probe that times the engine's actual use of the pattern (`fullmatch`, `match` or `finditer`, at the call site) on inputs built to provoke backtracking. Build them from the shapes the comments warn about: long runs of the pattern's repeated atom followed by a near-miss terminator, unterminated quotes, long comment banners and deep bracket nesting.
   - Measure at two or more sizes, such as 1× and 8×, and assert that the ratio stays near linear. Use a generous bound, because CI timing is noisy, and assert relative growth rather than absolute milliseconds.
   - Follow the existing timed ReDoS regression test for structure.
2. **Rewrite only what grows superlinearly.**
   - Use the lookahead+backreference atomic emulation with a unique group name, or a restructuring with no nested repetition.
   - Check every consumer of that compiled pattern: numbered groups, `findall`, `.groups()` and `lastindex` must not shift. `COMMAND_LITERAL` and `PROSE` are built by concatenating `CODE_STRING.pattern`, so a change there propagates.
3. **Keep the corpus green.** `test_guard.py` replays the corpus, so run it in full.
4. **Record per pattern:** probe sizes, measured ratio, and whether it was changed. Put this in Task 8's execution context.
5. **If anything changed in `guard.py`,** run `make generate-guard` / `make check-guard`. The change ships in the same release as Task 2.

→ verify: `bash test/test-guard.sh` and `bash test/test-hooks.sh` pass, `make check-guard` is clean, and pyright passes in the guard's 3.9 environment.

## Task 9: Documentation and ADR 0017

Files:

- `docs/adr/0017-python-311-floor.md` (new)
- `docs/adr/0016-python-runtime.md` (status line only)
- `docs/contributing/adrs.md`
- `docs/getting-started/install.md`
- `docs/getting-started/plugin-only.md`
- `README.md`
- `docs/user-guide/configuration.md`
- `docs/providers/claude-code.md`
- `klaude-plugin/README.md`
- `docs/contributing/testing.md`

Steps:

1. **ADR 0017** (Nygard template, in the voice and density of 0015 and 0016): what design §5 lists.
   - Context cites the verified platform facts from design.md §Problem.
   - Consequences cover:
     - the macOS / RHEL-family / 22.04 install step;
     - the transition command;
     - Rule 2, the 3.9-runnable guard, and when it may be retired;
     - the one Codex guard review;
     - extending the version list when CPython 3.20 approaches.
2. **ADR 0016** status becomes: *Accepted, 2026-11-26. The 3.9 floor is superseded by ADR 0017; the decision to stay in Python stands.* Update the index row to match.
3. **Prerequisite pages.**
   - Replace "Python 3.9+" with "Python 3.11+", plus one short, cross-platform install sentence: uv on any OS, Homebrew on macOS, or the distribution's `python3.11` package. Note that `python3` itself may remain older.
   - `configuration.md`'s wrapper paragraph (around "On macOS it prefers…") describes the new candidate order.
   - Keep each page's existing density; this is a prerequisite line, not a tutorial.
4. **`testing.md`.**
   - Move Task 1's baseline and Task 10's final latency numbers into the latency section, with host and interpreter.
   - Update the CI matrix description.
   - Document `KK_TEST_OLD_PYTHON` and the transition test.
5. **`test_guard.py` module docstring.** Update the floor paragraph: floor 3.11, and the engine held to 3.9 for the v0.27 upgrade self-test.
6. **`make docs-build`** must pass.

→ verify: `make docs-build` passes, `grep -rn "3\.9" docs README.md klaude-plugin/README.md` shows only intentional mentions (history, Rule 2, distro facts), and `bash test/test-plugin-structure.sh` passes.

## Task 10: Final verification

- Run Task 1's latency probes again with the same pinned interpreter. Also run them with the default discovery, to show what the new list costs.
  - Compare with the baseline and record both runs.
  - A regression beyond normal noise blocks completion until it is explained. The likely cause is the candidate list, if absolute checks turn out slower than measured.
- Run all `test/test-*.sh`, `make typecheck`, `make check-guard` and `make docs-build`.
- Then run `/kk:test`, `/kk:document`, `/kk:review-code` (language: Python, Bash) and `/kk:review-spec` per tasks.md.
- Sufficient evidence:
  - green suites on 3.11 and the newest release (CI);
  - the transition job green;
  - latency recorded;
  - review findings resolved or recorded.
- Broaden only for a concrete unresolved risk, for example a reviewer finding about the candidate list on a platform the tests do not cover.
