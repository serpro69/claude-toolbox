# ADR 0016: Keep machine delivery and the guard in Python

## Status

Accepted, 2026-11-26.

## Context

`kk` (`kk/lib/`, about 3,400 lines) and the permission guard (`klaude-plugin/scripts/guard/guard.py`, about 1,950 lines) were standard-library Python with a 3.8 floor. A rewrite of `kk` in Go or Rust was considered for two reasons: to remove Python from the user prerequisites, and because a statically typed language is easier for maintainers and agents to change safely. Go was the candidate. The repository already builds Go tools under `cmd/`, and `kk`'s work (subprocesses, JSON, file locks, archives) needs nothing Rust offers beyond that.

Python is required by more than `kk`:

| Component | Required by | Runs |
| --- | --- | --- |
| `install.sh` (Python in a heredoc) | Machine installs | Install and upgrade |
| `kk/lib` | Machine installs | `kk` commands and launches |
| Guard engine, in `klaude-plugin` and `kodex-guard` | Machine **and plugin-only** installs | Every matched tool call |
| `cpr.py`, `review-code/scripts/prepare_instructions.py` | Plugin users | Session start, `/kk:review-code` |

The guard is the binding constraint:

- **Plugin-only installs come from Git.** Claude Code and Codex install the public plugins from the `agentstakk` Git marketplace, which has no per-platform artifacts. A compiled guard would need binaries for linux/darwin × amd64/arm64 committed to Git on every release, a download on first use inside a fail-closed hook, or a Go toolchain on the user's machine.
- **Codex hashes every byte of the guard bundle.** Hook trust is stored per handler as a declaration hash and a bundle hash covering every file in the plugin ([machine-level delivery design](https://github.com/serpro69/agentstakk/blob/master/docs/feat/done/machine-level-delivery/design.md)). Rebuilt binaries change that hash, and adopters must review the guard again, unless the builds are reproducible across every platform in the bundle. Readable source also lets an adopter see what they are approving.
- **Two engines are not acceptable.** A Go guard for machine installs alongside a Python guard for plugin-only installs would duplicate a security policy engine. The shared case corpus would reduce divergence, not prevent it.

Rewriting `kk` alone therefore leaves the documented prerequisites (Bash, Git, curl, `jq`, Python) unchanged. It would add a per-platform release pipeline, architecture selection in the installer, and binary fingerprinting in `payload.py`.

Requiring Python costs adopters little. Mainstream desktop Linux distributions install `python3` by default; minimal and container images may not. On macOS, `/usr/bin/python3` and `/usr/bin/git` are both stubs until the Xcode Command Line Tools are installed, and Homebrew requires those tools too. A Mac that meets the Git prerequisite therefore already has the Command Line Tools' Python 3 (3.9.6 in current releases).

## Decision

`kk`, its installer and the guard stay in standard-library Python.

**The floor rises from 3.8 to 3.9**, the lowest Python adopters actually have: the Command Line Tools' 3.9.6 on macOS, and the default on RHEL 9 and its rebuilds and on Amazon Linux 2023. Only Ubuntu 20.04, now out of standard support, defaults to 3.8. RHEL 8 defaults to 3.6, below either floor. A 3.10 floor was rejected: Python 3.10 is past its upstream end of life (October 2026) like 3.9, and it would exclude every Mac that relies on the Command Line Tools Python while adding nothing important. A 3.11 floor, which brings `tomllib` and runtimes that still get upstream fixes, needs a separately installed Python on macOS. That change and the code rework it enables are tracked in [#213](https://github.com/serpro69/agentstakk/issues/213).

The entry points that run first stay loadable by Python 3.6, the oldest `python3` a distribution still ships (RHEL 8), and refuse older interpreters themselves. They therefore avoid `from __future__ import annotations`, which needs 3.7. The entry points are: `kk/lib/run.py`, the `install.sh` bootstrap and the guard's `run-guard.py`. A guard launcher below the floor exits with a dedicated status, and `guard.sh` tries its next candidate interpreter. Otherwise one old `/usr/bin/python3` would make the fail-closed wrapper block every matched call. An upgrade under an old interpreter stops at the candidate's self-test, and the previous release stays active.

Static checking comes from type annotations checked by pyright in strict mode, with `pythonVersion` set to the floor, over `kk/lib` and the canonical guard. mypy was rejected: 1.17 removed support for targeting Python 3.8, and 2.0 removed 3.9. It would have checked against a newer language version than the code runs on. The machine-delivery workflow keeps running the test suites on the floor version and the current release; pyright does not replace those runs.

Annotations must not add meaningful work to the guard's hook path.
- Every module except those entry points uses `from __future__ import annotations`. That loads only the small `__future__` module, about 0.1 ms on Linux under Python 3.12.
- The guard imports `typing` and `typing_extensions` only under a module-level `TYPE_CHECKING = False` constant, which pyright treats as true. The guard itself therefore never imports them.
- On Python 3.9 the standard library still loads `typing` on the hook path, about 5 ms. That cost exists with or without annotations.

## Consequences

- Adopters keep the current prerequisites, apart from the floor change, and plugin-only installs keep the guard. Ubuntu 20.04 adopters need a newer Python. Accepted ADRs 0012 and 0015 still describe the 3.8 floor that applied when they were written.
- Changes to type contracts in `kk/lib` and the guard are checked in CI. Parsed JSON stays dynamically typed (`Any`) until existing validation narrows it. Annotations do not validate external data.
- Annotating the guard changes the `kodex-guard` bundle. Codex adopters review the guard's handlers again once, after the release that ships the annotations.
- The release that ships this decision is breaking for hosts whose only Python is 3.8, such as Ubuntu 20.04, or 3.6, such as RHEL 8. Earlier guards happened to run on 3.6, below the documented 3.8 floor.
  - Once the plugin updates, the guard there blocks every matched tool call with a request for Python 3.9 or newer.
  - Plugin-only adopters get no installer check first.
  - The GitHub release notes for that release, which are otherwise generated from pull request titles, must state this and the one-time Codex guard review.
- The Go tools under `cmd/` remain build-time generators and analyzers, and their binaries never run on adopter machines. Their outputs do ship. For example, the generated Codex review skill includes the Python helper `prepare_instructions.py`, which adopters run under the same Python prerequisite.

**Reopening condition.** Revisit this decision if the machine installation becomes the only path that ships the guard, for example if plugin-only installs drop the guard or the provider marketplaces gain per-platform artifacts. Then a single Go `kk` binary, acting as installer, launcher, release manager and guard engine, would remove Python, `jq` and the installer heredoc from the prerequisites. The per-platform release tarballs would fit the existing release-directory and rollback model.
