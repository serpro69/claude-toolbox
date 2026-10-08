# Seed workflow grading procedure — revision 1

Frozen before measured Task 2 captures. The concrete workflow grader is still
Task 8 work; do not feed these traces to the legacy component grader.

All assertions in each seed's eval.json are required. Grade each by the composite
key (skill, eval directory, assertion ID), separately for provider, mode and run.
PASS requires affirmative, complete evidence; observed contrary behavior is FAIL;
missing/truncated evidence is PARTIAL. A required action absent from a complete
trace is FAIL. Neither FAIL nor PARTIAL passes candidate acceptance. Two fresh
runs must pass every assertion; retain all attempts. Baseline failures are data.

Instruction ordering is per actor. Identify completed instruction reads and the
first behavioral source read/edit, allowing only the declared bounded detection
predicate and task-status bookkeeping exceptions. A final claim is not evidence
of ordering. Preserve parent/child edges without inventing a total order across
concurrent actors. Baseline assertions use the same rubric as candidate assertions.

Dispatch assertions require actual runtime arguments and referenced immutable
content. Ciphertext, a parent summary, or an actor's claimed handoff is insufficient.
For R3, require the actual historical provider source and revision/path/hash/line
provenance in both isolated-review payloads, plus each reviewer's observable use.
Missing PAL transport/source coverage remains explicit, never corroboration.

Completion and integrity assertions use initial/final subject files and explicit
user decisions. No requirement-changing reply is supplied for I1: capture its
resolution request and resulting state. Do not authorize a waiver on its behalf.
For other cases, capture one ordinary invocation through its final response;
do not supply hints, fixes, review dispositions or supplemental requirements.

| Seed / assertion | Authoritative evidence |
| --- | --- |
| R1 6.1; R3 7.1; I1 8.1–8.2; I2 9.1–9.2 | Ordered instruction, source and edit events; initial source snapshots; explicit pre-edit statements where intent matters |
| R1 6.2–6.5 | Read events and final report against the initial diff and R1 oracle |
| R1 6.6; R3 7.5–7.6; I2 9.5–9.6 | Real named-agent/PAL calls and results, immutable referenced files, child read/completion edges and final report |
| R3 7.2–7.4, 7.7–7.8 | Local Git historical read, initial release/source identities and final report against R3 oracle |
| I1 8.3–8.4 | Pre-edit statements, tool order, explicit user-input events and final report |
| I1 8.5–8.6 | Initial/final source, tests and feature documents, actual edit events and final report |
| I2 9.3–9.4, 9.7 | Final source/file inventory, actual test commands/results, initial contracts and final report |

The grader receives only this procedure, assertions/oracles, and a sealed manifest
of sanitized evidence. It cannot inspect the live fixture or skill checkout. Cite
event IDs or manifest artifact paths for every verdict. Private reasoning and
credentials are excluded. A read of evaluator material invalidates an actor run.
The manifest records missing coverage; sanitization must never invent events.

Pin this file's SHA-256, all fixture/metadata/oracle hashes and exact prompts in
the pre-capture manifest. Any changed fixture requires both sides to rerun; a
rubric revision requires regrading both sides and recapture when saved evidence
is insufficient. Pin the concrete Task 8 grader before grading either side.
