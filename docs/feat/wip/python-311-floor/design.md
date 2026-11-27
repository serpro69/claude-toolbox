# Design: Python 3.11 floor

> Issue: [#213](https://github.com/serpro69/agentstakk/issues/213)
> Supersedes the floor in [ADR 0016](../../../adr/0016-python-runtime.md); recorded as ADR 0017 by Task 9.

## Problem

ADR 0016 raised the floor for `kk`, its installer and the permission guard from 3.8 to 3.9. Python 3.9 and 3.10 are past upstream end of life. 3.11 is the oldest version that still receives security fixes (until October 2027), and it adds `tomllib`, `hashlib.file_digest`, `typing.Self`, `NotRequired` and atomic regex groups.

The version checks are already in place. ADR 0016 made `kk/lib/run.py`, the `install.sh` bootstrap and the guard's `run-guard.py` refuse interpreters below a `FLOOR` constant. They stay parseable on Python 3.6 so they can say so. `guard.sh` already tries its next candidate when `run-guard.py` exits 3.

The gap is **finding** a 3.11 interpreter:

- `install.sh` and `kk/bin/kk` run plain `python3`.
- `guard.sh` tries only names spelled `python3`.

On the platforms the issue names, a newer Python usually goes by a versioned name only:

| Host | `python3` | Newer Python |
| --- | --- | --- |
| RHEL/Alma/Rocky 9, Amazon Linux 2023 | 3.9 for the distribution's life | `dnf install python3.11` / `python3.12` installs `/usr/bin/python3.N` only. Red Hat (BZ 2211019) and AWS say not to repoint `/usr/bin/python3`, because dnf breaks. |
| Ubuntu 22.04 | 3.10 | The jammy-updates `python3.11` package is 3.11.0~rc1, and deadsnakes adds `/usr/bin/python3.N`. |
| Any OS, uv | — | `uv python install 3.12` adds only `~/.local/bin/python3.12`. Bare `python3` needs the experimental `--default`. uv is the most common route on older distributions. |
| macOS | Command Line Tools 3.9.6 | Homebrew links `python3.N` into `$HOMEBREW_PREFIX/bin`. Non-default `python@3.N` formulae link nothing else there. Whether the default `python` formula also links bare `python3` there could not be confirmed. |

The facts above were checked by isolated verification on 2026-11-27. Sources: Red Hat BZ 2211019, the AWS AL2023 user guide, Launchpad (jammy `python3.11`), formulae.brew.sh, and the uv docs for python-versions and preview features.

Raising the constant alone would therefore leave every one of these adopters with a guard that denies every matched call, and a `kk` that refuses to run.

A second problem is upgrading from released code. `kk upgrade` on v0.27.x runs v0.27's code under v0.27's `python3`. That code runs the candidate's `guard.py` and imports the candidate's `cli.py` in its own process. The new release has to survive that sequence; see §3.

## Who and success

**Primary users:**

- Machine-install adopters (`install.sh` / `kk`) on macOS and Linux.
- Plugin-only adopters, who get the guard with no installer to check anything first.

**Secondary users:** maintainers and agents who change kk and the guard. The 3.11 rework is in scope only where it costs the primary users nothing, such as guard latency or a second Codex guard review.

**Success:**

1. **Discovery.** Suppose `python3` is older than 3.11, but `python3.11` or a newer versioned interpreter is installed (distribution package, uv or Homebrew). Then `install.sh`, `kk` and the guard run under the qualifying interpreter with no configuration. On a Mac with the Command Line Tools Python and Homebrew Python, both `kk` and the guard pick Homebrew.
2. **Refusal.** With no 3.11+ interpreter:
   - the guard denies matched calls with a message that names 3.11 and how to install it,
   - `install.sh` stops before it downloads release code,
   - `kk upgrade` stops, leaving the previous release active and no candidate in `activating`.
3. **Safe transition.** An upgrade from real v0.27.0, run under a 3.9 `python3`, never reaches the `place` checkpoint while running under 3.9. It either stops with a message that gives the exact command to finish, or it completes under a qualifying interpreter.
4. **No regression.**
   - Guard, kk and Codex-hook suites pass on 3.11 and the newest release.
   - pyright strict is clean.
   - Guard Read/Bash p95 on 3.11+ is measured before and after, recorded in `docs/contributing/testing.md`, and no worse. The 30 ms Read target stays a separate open item.
5. **One Codex review.** Every `kodex-guard` byte change ships in one release.

## Constraints and size

- **Standard library only, no compiled artifacts** (ADR 0016). The guard keeps shipping from Git for plugin-only installs.
- **Released code is fixed.** v0.27.0's dispatcher runs `python3`. Its `validation.validate` runs the candidate's `guard.py` under its own interpreter. Its `activate_staged` imports the candidate's `cli.py` in-process.
- **Entry points parse on 3.6:** `run.py`, `run-guard.py` and the `install.sh` bootstrap.
- **Fail closed, without a self-inflicted outage.** A too-old or broken interpreter must not block every call when a later candidate works. Selection adds no spawn on the normal path.
- **kk never writes adopter-owned configuration** (ADR 0014/0015). `config/read` stays the source of Codex origins.
- **Generated copies are never edited.** Edit `klaude-plugin/scripts/guard/`, then run `make generate-guard`.

**Size and lifetime.**

- One-off migration: about 3,400 lines of `kk/lib`, 2,000 lines of guard, three shell entry points, two CI configs and about seven doc pages.
- Permanent code: interpreter discovery, which runs on every `kk` command and every guarded tool call.
- The transition path only matters for adopters upgrading from v0.27.x or earlier.

## Design

### 1. Interpreter discovery

`install.sh`, `kk/bin/kk` and `guard.sh` each carry an identical bash function. It lists interpreter candidates in this order:

1. **Versioned names, newest first, from `python3.19` down to `python3.11`.** For each version it lists:
   - the absolute paths `/opt/homebrew/bin/python3.N`, `/usr/local/bin/python3.N`, `/usr/bin/python3.N` and `$HOME/.local/bin/python3.N`,
   - then the bare name `python3.N`, resolved on `PATH`.
2. **Bare `python3`:**
   - the guard's existing absolute list (Homebrew first on macOS, `/usr/bin/python3` first elsewhere),
   - then `python3` on `PATH`.

**Why it is shaped this way:**

- **A versioned name proves its own version.** Any `python3.N` with N ≥ 11 qualifies without spawning it. Only a bare `python3` needs the existing floor gate, and it comes last.
- **The absolute candidates cover the defaults of the three install routes:** Homebrew on both architectures, distribution packages, and uv's default bin directory.
  - Agent hooks inherit the agent's environment, and a desktop-launched agent may lack `~/.local/bin` or Homebrew's `bin` on `PATH`.
  - A custom uv bin directory still works through the `PATH` lookup.
- **Each check is a builtin** (`[[ -x ]]`, `command -v`). A missing name costs about 20 µs (strace: no fork). The whole list is about 50 checks, well under 1 ms, against about 7 ms for one Python start. It must stay that way: no spawn, no directory listing.
- **Newest first** gives one deterministic rule: the newest qualifying interpreter anywhere wins. On macOS the Command Line Tools Python is 3.9 and never qualifies, so "Homebrew first" holds without a special case.
- **The upper bound `3.19`** keeps unreleased names cheap. A newer default `python3` is still found by the bare fallback. Extending the list later is a one-line edit, kept identical in all three scripts by a test.

How each consumer uses the list:

- **`guard.sh`** iterates the candidates exactly as it does today:
  - `KK_GUARD_INTERPRETERS` still overrides the whole list.
  - Exit 3 still means "try the next one".
  - The final denial reads: *no working Python 3.11+ interpreter; install Python 3.11 or newer (uv, Homebrew, or your distribution's python3.11 package)*.
- **`kk/bin/kk`** executes the first candidate that exists.
  - If it reaches bare `python3`, `run.py` refuses an old one with the floor message plus the same install hint.
  - If there is no candidate at all, the dispatcher says so itself, instead of letting bash report `python3: command not found`.
  - The dispatcher's own path resolution (`python3 -I -c '…resolve()'`) also uses the selected interpreter.
- **`install.sh`** selects the same way and runs the heredoc under the result. The bootstrap's own floor check stays as the backstop for a bare `python3`.

Plugin-only installs get the guard behavior with nothing else to install. Codex adapters call `guard.sh` and inherit it.

### 2. Floor constants and messages

The floor rises to 3.11 in four places: `run.py` `FLOOR`, `run-guard.py` `FLOOR`, the `install.sh` bootstrap check and the `guard.sh` denial text.

The entry points still avoid `from __future__ import annotations`. They have to parse on 3.6 to refuse it.

### 3. Upgrading from v0.27.x

Verified against the v0.27.0 tag. When v0.27.0 runs `kk upgrade`:

1. `validation.validate(stage)` runs before the candidate is moved to `staging/` (`cli.py:227`).
   - It runs the candidate's `kk/bin/kk status`, which uses the candidate's own discovery.
   - It runs the candidate's `guard.py` directly under **v0.27's `sys.executable`** for four decisions.
   - It runs both vendors' hook handlers through the candidate's `guard.sh`.
2. The candidate moves to `staging/<v>` and is recorded as `staged` (`cli.py:230`, `:236`).
3. `activate_staged` imports the candidate's `cli.py` in-process as `_kk_preflight` (`cli.py:278`). This happens before the `place` checkpoint and before `staging/` is renamed.
   - A `ValueError` raised there is caught by `main` and printed as `kk: …` with exit 1. State stays `staged`, the previous release stays active and `staging/<v>` persists.
   - A `SyntaxError` or `ImportError` there is an uncaught traceback.

So when v0.27's `python3` is older than 3.11 but discovery finds a qualifying interpreter, the candidate passes step 1 and is then imported under 3.9 in step 3. The design handles this with two rules.

**Rule 1: the candidate's `cli.py` refuses an old interpreter at import.**

- Its first executable statement, before any sibling import, compares `sys.version_info` with the floor and raises `ValueError`.
- When the module lives at `<home>/staging/<version>/kk/lib/` and `<home>/state.json` exists, the message names the exact command to finish: `KK_HOME=<home> <home>/staging/<version>/kk/bin/kk upgrade`.
- That staged dispatcher selects the active (v0.27) release through its unchanged `jq` logic and runs v0.27's `run.py` under the qualifying interpreter. v0.27 supports 3.11, and its owner check (`cli.py:515`) passes.
- The upgrade then resumes from the staged candidate without downloading, revalidates under 3.11 and activates.
- `KK_HOME` is spelled out because the staged dispatcher falls back to the default home when it is unset.
- Loaded from anywhere else, for example an older `install.sh` bootstrapping a first install, the message is the plain floor message.

**Rule 2: the guard engine stays runnable on 3.9.**

Step 1 runs `guard.py` under v0.27's own interpreter before anything is staged. If that fails, the user sees `kk: guard self-test expected allow for Bash, exit 1: <traceback>`, nothing is staged, and Rule 1's command never appears.

`guard.py` therefore keeps all of the following:

- 3.9 syntax (no `match`, no `except*`),
- 3.9 standard-library APIs,
- 3.9 regex syntax (no possessive quantifiers or `(?>…)`),
- `from __future__ import annotations`, with runtime-evaluated aliases under `TYPE_CHECKING`.

This is cheap: the guard needs nothing from 3.10+ at runtime. Production still refuses 3.9 through `run-guard.py`; only v0.27's direct self-test ever runs the engine there.

Enforcement:

- pyright checks the guard in an execution environment pinned to `pythonVersion` 3.9.
- `guard.py`'s AST drift test stays at 3.9.
- A CI job performs a real v0.27.0 → candidate upgrade with a 3.9 `python3` and a qualifying `python3.N`.

If a future guard change needs 3.10+ at runtime, the rule can be retired only together with dropping direct upgrades from v0.27.x. That would need a separate decision.

**Rollback** from the new release to v0.27 already works:

- The new dispatcher runs v0.27's code under the qualifying interpreter.
- Rollback restores v0.27's dispatcher, which uses `python3` and runs on 3.9.

### 4. 3.11 rework

The rework stays in proportion and touches only code we run:

- **`hashlib.file_digest`** replaces the chunked loops in `payload.fingerprint` and in `guard_identity` for regular files. The manifest's special case stays as it is.
  - `payload.py` also runs under the bootstrap's interpreter (`intact()` via `runpy`); the new `install.sh` guarantees 3.11 there.
  - `guard_identity.py` lives in `kk/lib`, not in the guard engine, so Rule 2 does not apply to it.
- **`tomllib` in tests only.**
  - The fake Codex's hand-written TOML value reader (`test/kk/codex`) becomes a `tomllib` parse of `v = <text>`. It still falls back to a plain string the way Codex does.
  - `test-codex-structure.sh` drops its tomli/venv fallback chain.
  - `test_codex.py` drops its `skipTest`.
  - Production keeps the `config/read` origin lookup. Parsing Codex's TOML would mean reimplementing its layering (user, trusted project, managed, session flags), which ADR 0015 already rejected for the trust read. Only the reason "no TOML parser" goes away.
- **Typing.**
  - One tool-driven pass (`pyupgrade --py311-plus` or ruff's `UP` rules) over `kk/lib` and `test/kk` converts to builtin generics, `X | Y` and `Self`. It contains no hand-written refactoring.
  - The guard is excluded by Rule 2.
  - `TypedDict` with `NotRequired` describes the `state.json` record, its `candidate`, and the per-release records. `state.load` narrows parsed JSON to that type after its existing format check, so it doesn't validate more than today.
- **Compatibility shims:**
  - `run.py` drops the `exec_module` pyright ignore, which existed for stubs before 3.10. `run-guard.py` keeps it, because it is checked at 3.9.
  - The AST drift checks for non-entry `kk/lib` modules move from 3.9 to 3.11.
- **Guard regexes, measure first.**
  - Timed adversarial inputs go into the guard tests for `CODE_STRING`, `ARGV_GAP`, `ARGV_END`, `LINE_END`, `CLOSER`, `ARGUMENT_END`, `COMMAND_LITERAL` and `PROSE`. The test pattern is the existing ReDoS regression test (a timed `fullmatch` on a banner input).
  - A pattern is rewritten only if its time grows faster than linear with input length. The rewrite uses the lookahead+backreference form, `(?=(?P<name>…))(?P=name)`, which is equivalent to an atomic group on every version:
    - it was identical across a 36,000-case differential fuzz on 3.9 and 3.12,
    - it adds a named group, so each use needs a unique name, and code must not rely on numbered groups or `findall` over that pattern,
    - it costs about twice the matching time for that group.
  - The guard corpus must stay green.
- **Latency.** Guard Read/Bash p95 is measured on 3.11+ before any change and again at the end, and both numbers are recorded in `docs/contributing/testing.md`.

### 5. Documentation and decision record

- **ADR 0017** supersedes ADR 0016's floor decision. The rest of ADR 0016 stands. ADR 0017 records:
  - the 3.11 floor,
  - discovery by versioned name,
  - the separately installed Python on macOS and the RHEL-family / 22.04 hosts,
  - the transition rules,
  - why `tomllib` does not replace `config/read`,
  - an updated reopening condition.

  ADR 0016's status and the ADR index note the partial supersession, as ADR 0014 / 0015 did.
- **Prerequisite pages** describe the cross-platform install step: uv on any OS, Homebrew on macOS, or the distribution's `python3.11` package. They say that `python3` itself may stay older. Affected pages:
  - `docs/getting-started/install.md`
  - `docs/getting-started/plugin-only.md`
  - `README.md`
  - `docs/user-guide/configuration.md`
  - `docs/providers/claude-code.md`
  - `klaude-plugin/README.md`
- **The release notes for the shipping release must state:**
  - the breaking floor,
  - the macOS / RHEL-family / 22.04 install step,
  - the one-time Codex guard review,
  - the staged-dispatcher command for upgrades run under an old `python3`.

  ADR 0016 established that release notes carry such items.

## Assumptions

1. Ubuntu jammy's `python3.11` 3.11.0~rc1 includes `tomllib`, `hashlib.file_digest` and atomic-group support. They landed before the 3.11 feature freeze. Check during Task 3 if a jammy image is at hand; otherwise record it as unverified.
2. Agent hooks inherit a `PATH` from the agent process. The absolute candidates cover default Homebrew, distribution and uv locations whether or not that `PATH` includes them.
3. Upgrades from releases older than v0.27.0 go through the same `validate` → preflight `load_cli` sequence. Task 4 confirms this for the v0.26.x tag, or narrows the transition claim.
4. The guard needs no 3.10+ runtime feature for anything this design asks of it.
5. About 50 builtin existence checks add under 1 ms to a guard call. Task 10's latency comparison confirms this.
6. `actions/setup-python` can provide a 3.9 interpreter and a 3.11+ one in the same job. If it can't, the transition test builds a private bin directory with explicit symlinks.

## Not Doing

- **Production use of `tomllib`:** `config/read` reports every Codex layer, and parsing TOML would mean reimplementing that layering.
- **A `KK_PYTHON` override for kk:** `PATH` already controls this, and the guard keeps `KK_GUARD_INTERPRETERS`.
- **Possessive quantifiers or `(?>…)` in `guard.py`:** they would break Rule 2.
- **Hand-written modernization sweeps** (`match`, `zip(strict=)`, `contextlib.chdir`): use them only where touched code is simpler for it. `str.removeprefix` is already available on 3.9.
- **A floor for `cpr.py` and `prepare_instructions.py`:** they run on any `python3`, and nothing needs 3.11 there.
- **Changing v0.27.x, or making `install.sh` upgrade an existing installation:** released code is fixed, and Rule 1's command covers the gap.
- **Recording the selected interpreter in `state.json`:** see Rejected Alternatives.

## Rejected Alternatives

- **Keep `python3` as the only name and ask adopters to make it 3.11+.** Red Hat and AWS forbid repointing `/usr/bin/python3`, and uv users normally have no `python3`. Every RHEL-family hook would also pay a wasted 3.9 start.
- **`run.py` re-execs itself under a versioned interpreter.** The guard and the stdin heredoc installer still need shell discovery, so the number of places to keep in sync doesn't drop. The transition fix would also become a hand-typed interpreter command, because the staged dispatcher would pick `python3` again.
- **Record the interpreter at install time.**
  - The published dispatcher's bytes are digest-checked against the release.
  - A `state.json` field would need every older release's `jq` and loader to tolerate it on rollback.
  - Plugin-only guards have no state to read.
- **Possessive quantifiers throughout the guard.** No current pattern has a measured backtracking problem; the last ReDoS was fixed by stripping comments before matching. Native syntax would also break the v0.27 upgrade self-test.
