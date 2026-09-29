# Task 3 focused reruns

Date: 2026-09-29. Two new general-purpose sessions, `fork_turns="none"`,
`gpt-6-astra` / `xhigh`; model build and temperature are not exposed. They inherit
no editor/author context. Input and instruction hashes are recorded in
[manifest-hashes.txt](manifest-hashes.txt) and [instruction-hashes.txt](instruction-hashes.txt).
Unchanged implement instructions for the route inspection have their own
[hash manifest](implementation-instruction-hashes.txt).

The original [19 PASS / 2 PARTIAL run](../task3-20260929/verdicts.md) is preserved.
Assertions are unchanged. The documentation instruction now explicitly requires
reporting its in-session fidelity limit and caller-owned further review. The
routing prompt now asks how a separate explicit documentation request affects
standalone completion; this is a clarified input, not an identical-prompt repeat.

The exact spawn message for each case used the same form as the original run:

> Carry out the evaluation request in /tmp/clarify-docs-task3-08Xji4xM/retry1/CASE/request.md. Read only that request, the instruction tree and case workspace it permits. Follow its execution boundaries; do not inspect the repository or other cases.

`CASE` was `clarity-preserves-profile` or `implementation-mode-coverage`. Requests
were written before dispatch; committed copies omit only the terminal blank line,
with verbatim runtime text retained in each read trace. Staging, allowed-file restrictions,
trace filtering and evidence-only draft copying follow the [original protocol](../task3-20260929/run.md).
These are procedural checks; no comprehension readers or implementation lifecycle
execution are claimed. Shared filesystem access still requires a trace audit.
