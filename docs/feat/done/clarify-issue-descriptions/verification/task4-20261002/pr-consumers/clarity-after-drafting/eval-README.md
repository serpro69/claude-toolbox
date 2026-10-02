# Behavioral regression

Stage only test-files/ and the tested instruction package for a fresh editor with
no inherited history. Do not expose this README, eval.json or oracle/ to the editor.
Use the eval prompt unchanged and capture the final response, artifacts and tool
trace. Keep oracle expectations fixed before execution.

Grade the completed three-document set against the accepted requirements and the oracle. There is no before/after editorial comparison: this case tests ordinary drafting followed by an optional suggestion.

A separate grader checks every eval assertion against the trace and artifacts,
using [oracle/expected.json](oracle/expected.json) for protected claims and document
quality. Its questions are artifact checks, not prompts for paired comprehension
readers. Grade PASS/FAIL/PARTIAL with evidence; PARTIAL or unavailable evidence is
not a pass. Audit allowed-file access and record input/output hashes, instruction
revision, session IDs, model settings and execution limits. Preserve failed attempts.

These are recommendation-routing and drafting regressions. They do not measure
an editorial pass or establish improved human comprehension.
