# Reader comparison

Fix the five neutral questions, source-backed answers, protected claims and orientation expectations in [oracle/expected.json](oracle/expected.json) before the editor runs. Stage only test-files/ and the tested instruction package for the editor; do not stage this README, eval.json or oracle/.

Capture the three completed drafts immediately before the final shared clarity pass. Those copies are the original reader artifacts; accepted.md is editor/grader source evidence and must never substitute for original draft prose. Both readers receive only their version of design.md, implementation.md and tasks.md. If the completed baseline already meets all declared requirements, the final pass should leave it unchanged.

Launch original and revised readers as separate general-purpose read-only sessions with no inherited history and the same model/settings. Give each only the five questions and its explicit artifact manifest from the oracle, without expected answers, source-only evidence or editing instructions. Require pointers and explicit uncertainty.

A separate general-purpose grader receives all source evidence, traces, artifacts, reader answers and the oracle. Report every eval assertion as PASS/FAIL/PARTIAL, comprehension separately from fidelity, and audit allowed-file access. PARTIAL is not pass. Record exact requests, input/output hashes, model metadata, session IDs and raw tool traces. These are AI-reader observations, not evidence of human comprehension. Preserve all failed attempts.
