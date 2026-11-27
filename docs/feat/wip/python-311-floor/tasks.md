# Tasks: Python 3.11 floor

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Issue: [#213](https://github.com/serpro69/agentstakk/issues/213)
> Status: pending
> Created: 2026-11-27
> Not Doing: production tomllib use, `KK_PYTHON` override, possessive quantifiers or `(?>…)` in guard.py, hand-written modernization sweeps, floor for cpr.py/prepare_instructions.py, changing v0.27.x or making install.sh upgrade, recording the interpreter in state.json

## Task 1: Guard latency baseline
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#task-1-guard-latency-baseline](./implementation.md#task-1-guard-latency-baseline)

### Subtasks
- [ ] 1.1 At current HEAD, run the Read/Bash p95 probes in `test/test-hooks.sh` with `CI` unset and `KK_GUARD_INTERPRETERS` pinned to a 3.11+ interpreter; record host, OS, Python version and both p95 values in this task's execution context
- [ ] 1.2 Record which interpreter the unpinned default list selects on this host

## Task 2: Guard discovery and floor
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Slicing:** Risk-First — the guard runs on every tool call, for plugin-only installs too, and fails closed
- **Can run in parallel with:** Task 8
- **Docs:** [implementation.md#task-2-guard-discovery-and-floor](./implementation.md#task-2-guard-discovery-and-floor), [design.md#1-interpreter-discovery](./design.md#1-interpreter-discovery)

### Subtasks
- [ ] 2.1 In `klaude-plugin/scripts/guard/guard.sh`, replace `default_interpreters` with the marked interpreter search block (versioned `python3.19`…`python3.11` across Homebrew, `/usr/bin`, `$HOME/.local/bin`, then `PATH`, then the existing bare-`python3` list); keep the candidate loop and `KK_GUARD_INTERPRETERS` semantics unchanged; no forks
- [ ] 2.2 Update the final denial to name 3.11 and the uv / Homebrew / distribution install routes
- [ ] 2.3 `run-guard.py`: `FLOOR = (3, 11)` and new stderr text, still 3.6-parseable
- [ ] 2.4 Update the `too-old` fixture text in `test/fixtures/guard/interpreter.sh` and its assertions in `test/test-hooks.sh` and `test/guard/test_guard.py`
- [ ] 2.5 Wrapper discovery tests with private stand-ins and controlled `PATH`/`HOME`: versioned name beats a too-old `python3`, `$HOME/.local/bin/python3.11` found off-`PATH`, bare too-old only → new denial → verify: `bash test/test-hooks.sh`
- [ ] 2.6 Keep `guard.py` at the 3.9 AST check, reworded as the v0.27 self-test requirement; add pyright `executionEnvironments` (guard 3.9, `kk/lib` 3.9 for now) → verify: `make typecheck`
- [ ] 2.7 CI matrix in `.github/workflows/machine-delivery.yml` → `['3.11', '3.x']`
- [ ] 2.8 `make generate-guard` → verify: `make check-guard`, `bash test/test-guard.sh`, `bash test/test-codex-hooks.sh`

## Task 3: kk discovery and floor
- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 8
- **Docs:** [implementation.md#task-3-kk-discovery-and-floor](./implementation.md#task-3-kk-discovery-and-floor)

### Subtasks
- [ ] 3.1 `kk/bin/kk`: add the identical search block; use the selected interpreter for self-location and both exec lines; explicit "no Python 3.11+ interpreter found" error; leave the `jq` release selection byte-for-byte unchanged
- [ ] 3.2 `install.sh`: add the identical block, run the heredoc under the selected interpreter; bootstrap floor `(3, 11)` with install hint, still 3.6-parseable
- [ ] 3.3 `kk/lib/run.py`: `FLOOR = (3, 11)` plus install hint; remove the pre-3.10 `exec_module` pyright ignore
- [ ] 3.4 Move the `kk/lib` pyright environment to 3.11 → verify: `make typecheck`
- [ ] 3.5 `test/kk/test_install.py`: floor-message test at 3.10; non-entry grammar checks at 3.11; entry points stay at 3.6 with the no-`__future__` assertion
- [ ] 3.6 Dispatcher discovery test: private `python3.12` link plus a too-old `python3` → `kk status` from a checkout succeeds
- [ ] 3.7 Parity test asserting the marked block is identical in `guard.sh`, `kk/bin/kk` and `install.sh` → verify: `bash test/test-kk.sh`; editing one block by hand makes it fail

## Task 4: Upgrade from v0.27.x
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Slicing:** Risk-First — the only path that runs fixed, released code against the new floor
- **Can run in parallel with:** Task 5, Task 8
- **Docs:** [implementation.md#task-4-upgrade-from-v027x](./implementation.md#task-4-upgrade-from-v027x), [design.md#3-upgrading-from-v027x](./design.md#3-upgrading-from-v027x)

### Subtasks
- [ ] 4.1 Floor check as the first statements of `kk/lib/cli.py`, before any sibling import, raising `ValueError`; staged-location message names `KK_HOME=<home> <home>/staging/<v>/kk/bin/kk upgrade` (shell-quoted), otherwise the plain floor message; comment explains why the check exists
- [ ] 4.2 Test that the `cli.py` floor constant equals `run.FLOOR`
- [ ] 4.3 Transition test (`test/kk/test_transition.py` or similar): install a real `git archive v0.27.0` tree under `KK_TEST_OLD_PYTHON` as `python3`, `kk upgrade --local <checkout>` → exit 1 with the command, state still `staged`, previous release active, staging present; run the printed command → new release active; `kk status` ready; `kk rollback` restores v0.27.0 → verify: passes locally; fails with 4.1 temporarily removed
- [ ] 4.4 Check v0.26.x the same way if the tag is reachable; record the result and update design.md Assumption 3
- [ ] 4.5 CI `transition` job: setup-python 3.9 and 3.12, export `KK_TEST_OLD_PYTHON`, run the transition test

## Task 5: `file_digest` and tomllib in tests
- **Status:** pending
- **Depends on:** Task 3
- **Size:** S
- **Can run in parallel with:** Task 4, Task 6, Task 8
- **Docs:** [implementation.md#task-5-file_digest-and-tomllib-in-tests](./implementation.md#task-5-file_digest-and-tomllib-in-tests)

### Subtasks
- [ ] 5.1 `kk/lib/payload.py` `fingerprint` and `kk/lib/guard_identity.py` (regular files except `MANIFEST`): `hashlib.file_digest` → verify: digests unchanged against a pinned expected value
- [ ] 5.2 `test/kk/codex`: replace the hand TOML value reader with `tomllib`, keeping the raw-string fallback
- [ ] 5.3 `test/test-codex-structure.sh`: single `tomllib` validation that fails loudly when unavailable; `test/kk/test_codex.py`: drop the `skipTest` → verify: `bash test/test-kk.sh`, `bash test/test-codex-structure.sh`

## Task 6: Typing pass for kk
- **Status:** pending
- **Depends on:** Task 3
- **Size:** S
- **Can run in parallel with:** Task 4, Task 5, Task 8
- **Docs:** [implementation.md#task-6-typing-pass-for-kk](./implementation.md#task-6-typing-pass-for-kk)

### Subtasks
- [ ] 6.1 Run `pyupgrade --py311-plus` (or ruff `UP`, target py311) from a scratch environment over `kk/lib/*.py` except `run.py`, and `test/kk/*.py`; never the guard
- [ ] 6.2 Review the diff for non-mechanical changes; remove now-unused `typing` imports; keep `from __future__ import annotations` → verify: `make typecheck`, `bash test/test-kk.sh`

## Task 7: TypedDict state records
- **Status:** pending
- **Depends on:** Task 6
- **Size:** M
- **Can run in parallel with:** Task 4, Task 8
- **Docs:** [implementation.md#task-7-typeddict-state-records](./implementation.md#task-7-typeddict-state-records)

### Subtasks
- [ ] 7.1 Derive the record's key set from all read/write sites; define `StateRecord`, `Candidate` and `ReleaseRecord` in `kk/lib/state.py` with `NotRequired` for optional keys
- [ ] 7.2 `state.load` returns `StateRecord` via `cast` after the existing format check; no new validation
- [ ] 7.3 Switch record-typed signatures in `cli.py` and the `codex_*`, `migrate`, `notice`, `mixed`, `claude_launch` modules; record any inconsistency pyright exposes; fix only local, behavior-preserving ones → verify: `make typecheck`, `bash test/test-kk.sh` (including rollback compatibility in `test_lifecycle.py`)

## Task 8: Guard regex timing
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 2, Task 3, Task 4, Task 5, Task 6, Task 7
- **Docs:** [implementation.md#task-8-guard-regex-timing](./implementation.md#task-8-guard-regex-timing)

### Subtasks
- [ ] 8.1 In `test/guard/test_guard.py`, add timed growth probes at two or more input sizes for `CODE_STRING`, `ARGV_GAP`, `ARGV_END`, `LINE_END`, `CLOSER`, `ARGUMENT_END`, `COMMAND_LITERAL` and `PROSE`, using each pattern's real call site
- [ ] 8.2 Only for superlinear patterns: rewrite in `guard.py` with lookahead+backreference atomic emulation (unique names) or restructuring; check consumers for numbered-group, `findall` and `lastindex` shifts
- [ ] 8.3 Record per pattern: sizes, ratio, changed or not → verify: `bash test/test-guard.sh`, `bash test/test-hooks.sh`, pyright clean in the guard's 3.9 environment
- [ ] 8.4 If `guard.py` changed: `make generate-guard` → verify: `make check-guard`

## Task 9: Documentation and ADR 0017
- **Status:** pending
- **Depends on:** Task 2, Task 3, Task 4
- **Size:** M
- **Can run in parallel with:** Task 5, Task 6, Task 7, Task 8
- **Docs:** [implementation.md#task-9-documentation-and-adr-0017](./implementation.md#task-9-documentation-and-adr-0017), [design.md#5-documentation-and-decision-record](./design.md#5-documentation-and-decision-record)

### Subtasks
- [ ] 9.1 Write `docs/adr/0017-python-311-floor.md` (floor, versioned discovery, separate Python on macOS / RHEL family / 22.04, transition rules including the 3.9-runnable guard and when it may be retired, why tomllib does not replace `config/read`, one Codex review, reopening condition)
- [ ] 9.2 ADR 0016 status line and `docs/contributing/adrs.md` row: floor superseded by 0017
- [ ] 9.3 Prerequisite pages: `docs/getting-started/install.md`, `plugin-only.md`, `README.md`, `docs/user-guide/configuration.md` (including the wrapper's candidate order), `docs/providers/claude-code.md`, `klaude-plugin/README.md`
- [ ] 9.4 `docs/contributing/testing.md`: matrix, `KK_TEST_OLD_PYTHON` and the transition test, Task 1 baseline numbers; `test/guard/test_guard.py` module docstring → verify: `make docs-build`, `bash test/test-plugin-structure.sh`

## Task 10: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 10.1 Re-run Task 1's latency probes with the same pinned interpreter and with default discovery; record both in `docs/contributing/testing.md`; an unexplained regression blocks completion
- [ ] 10.2 Run `/kk:test`: all `test/test-*.sh`, `make typecheck`, `make check-guard`, `make docs-build`; CI green on the 3.11 and `3.x` legs and the `transition` job. Broaden only for a concrete unresolved risk, such as an uncovered platform in the candidate list
- [ ] 10.3 Run `/kk:document` skill to update any relevant docs
- [ ] 10.4 Run `/kk:review-code` skill with language input Python and Bash
- [ ] 10.5 Run `/kk:review-spec` skill to verify the implementation matches design and implementation docs
- [ ] 10.6 Draft the release-note items design §5 requires (breaking floor, install step, one Codex guard review, staged-dispatcher command) where the release maintainer will find them
- [ ] 10.7 In case any outstanding, non-blocking, tasks are present - ask user on how they'd prefer to follow up on those, for example by creating follow-up github issues or recording follow-up in some other way.
- [ ] 10.8 Move completed feature docs from `docs/feat/wip/` to `docs/feat/done`, updating all the markdown references

## Dependency Graph

```
Task 1 ─┬─→ Task 2 ─→ Task 3 ─┬─→ Task 4 ─────────────┐
        │                     ├─→ Task 5 ─────────────┤
        │                     └─→ Task 6 ─→ Task 7 ───┤
        └─→ Task 8 ───────────────────────────────────┤
              Task 2, 3, 4 ─→ Task 9 ─────────────────┼─→ Task 10
```
