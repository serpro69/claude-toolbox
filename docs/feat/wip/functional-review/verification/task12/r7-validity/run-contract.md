# Task 12.14 diagnostic declaration

Declared 2026-10-14 before binding or measurement. User authority: “Proceed with
implementing 12.14.” The fixture/rubric must pass independent validity review and
the adapter must pass source review before actor launch.

## Identity and scope

Use unchanged operative instructions from
`6bc277ea6d1ee023cb30a1246c983456eff86fdb`. Build the filtered source bundle with
the existing prepare-bundles.py; retain source, exclusion and byte manifests.
The new fixtures and rubric are separately frozen working-tree inputs, excluded
from actor bundles. No operative instructions or original fixtures change.

Exactly four measured sessions: R7M standard twice, R7B standard twice, all Claude.
A separate instruction-loading probe precedes measurement and is not graded as
behavior. Historical transport labels the sole launched side “candidate”; both
internal snapshot aliases point to the same unchanged source. There is no
baseline/candidate comparison or new candidate in this diagnostic.

The immutable freeze records fixture files, assertions/oracles, ordinary prompt,
rubric, grader, controllers, runtime versions and actor snapshot identity.
No input may change after freezing. Retain all attempts and stop on setup/capture
failure; do not silently retry, pool old results or expand the four-session scope.

## Runtime

Claude Code 2.1.296, `claude-opus-5-5` at high effort. The inherited binding
probe's named reviewer is forced to that same model; measured standard review
does not require a child. Host Darwin, controller/actor Python 3.15.0, Capy
`v0.17.0-20-gdb4897b`; exact strings enter freeze.json. Codex's version is also
recorded by the historical freezer but no Codex actor is launched.

Reuse the reviewed Task 12.13 explicit-PAL-exclusion adapter and owned-process
capture. Its launch uses normal hooks, --plugin-dir, a run-specific plugin registry,
project/local settings only, disabled auto-memory, strict MCP configuration,
the existing explicit tool allowlist and dontAsk. PAL is absent from the actual
MCP file; its historical verification deferral remains unchanged.

The old capture helper was declared on Linux. This host's Python exposes the
same waitid/WNOWAIT primitives; [Python 3.15 documentation](https://docs.python.org/3.15/library/os.html#os.waitid)
documents macOS support since 3.13. Offline process success/failure/interruption
checks must pass here before launch. Initial inherited checks failed five cases
because Darwin rejects a signal to an unreaped zombie-only process group with
EPERM. No actor launched. The controller-only `host_runtime.py` handles that
case only after waitid observes the exited leader and a bounded process-table
query establishes that every member is a zombie. Live/unknown membership and
other permission failures remain errors. It preserves group ownership and reaps
the leader only after cleanup; historical helpers are unchanged. The successor
tests include a macOS process-table observation for descendant cleanup rather
than relying on absent Linux /proc. Freeze this successor before binding.
This is a new runtime declaration, not equivalence with historical Linux evidence.

## Isolation, capture and grading

Each run stages a new repository outside any SKILL.md ancestor, with complete
before/after files, a real staged diff and an independent empty Capy store.
The vault key is absent and the vault path is run-private. Exercise real
index/search and cross-store marker isolation in separate probes first.
Use no real knowledge/vault data and no prior actor mutations.

Only filtered instructions and subject files reach actors; oracles, rubrics and
controller evidence stay outside workspaces/catalogs. Verify bundle hashes and
actual loading before measurement. Capture observable tool events and final
reports, excluding private reasoning. Seal initial/final files, prompts, commands,
launch configuration and hashes. Audit actual access; claim no OS read confinement.
Keep source archives for later user-directed evidence retention.

Use [rubric v1](rubric.md), eval 19/20 assertions and their grader-only oracles.
Pin the existing workflow grader at ../../task2b/grader.md (its actual hash enters
freeze.json). Independent fresh eval-grader agents use their role's configured
model/effort, `gpt-6.1-sol`/xhigh, without inherited conversation. They receive
only sealed evidence and grading instructions; no live fixture or actor access.
Calibrate conclusion examples and ordering PASS/FAIL/PARTIAL controls before
grading real captures. The old adapter's manifest rubric_version is explicitly
set to r7-validity-v1 by this successor; original evidence is never rewritten.

## Decision and limits

All assertions remain required for a full diagnostic pass. The rubric separates
behavioral conclusions from procedural/capture problems. Report whether the
material case avoids unsupported readiness and the benign case earns justified
scoped approval in both repetitions. Select investigate/defer/no-change using
the predeclared rubric; no automatic skill patch or broader batch follows.

No live PAL, exact Codex handoff, no-spec resilience, isolated-review or full-feature
acceptance claim is made. Original R7 grades, Task 12 acceptance, legacy controls
and Task 13 remain open. Owner: implementing agent.
