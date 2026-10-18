# Pre-capture local verification

Parent-executed on 2026-10-18, with the declared Python 3.12.11 interpreter first
on PATH and `-B -m unittest discover -s <directory> -p 'test_*.py' -v`.

- `bootstrap-loading/`: **7 tests pass**, 6.974 seconds. Tests cover actual
  baseline/candidate binding and measured preparation, inherited launch validation,
  unchanged measured prompts/high effort/PAL exclusion, no-overwrite refusal,
  freeze drift, resealed wrong-prompt rejection before transport, actual retained
  baseline/candidate receipt distinction, invalid audit rejection, strict gate
  ordering and CLI adapter restoration. Initial output was returned in this
  session's tool results; no full saved log is claimed for that invocation.
- After the independent review's historical-evidence integrity correction,
  **8 successor tests pass**, 9.412 seconds; full output is in
  [successor-tests.txt](successor-tests.txt). The additional test proves that
  changed inherited evidence cannot pass verification or be resealed by a new
  freeze. It mocks returned hashes without editing historical files.
- `high-effort-host/`: **14 tests pass**, 20.020 seconds; complete output is in
  [predecessor-tests.txt](predecessor-tests.txt).
- Parent `advisory-closure-execution/`: **26 tests pass**, 4.096 seconds;
  complete adapter/receipt output is in [adapter-tests.txt](adapter-tests.txt).
- Original guarded `verify` passes with restored sealed inputs and pinned
  runtime executables. `git diff --check` passes.

The Codex executable's version check reports inability to create PATH aliases
inside the sandbox but exits successfully with the declared version. No test
launches an actor or calls an external model. These checks establish local
plumbing behavior, not actual bootstrap loading or readiness.

## Post-capture verification successor

Both approved binding probes completed. Their original receipt auditor rejected
two contract-allowed instruction filename listings. Independent assessment and
source review selected a verification-only successor, preserving all raw evidence.
The [initial eleven tests](listing-tests.txt) pass; after fixing the reviewer's
normalized-alias uniqueness finding, [all twelve final tests](listing-tests-final.txt)
pass in 2.839 seconds. They use actual retained captures plus synthetic negative
controls and never launch actors or modify sealed files.

The verifier freeze is
`4659cc668c11a7ff81f44afa735c5523250f3a1aa609987e96ac11a6fe0a457b`.
Re-auditing and recomputing both retained receipts succeed: baseline 13/13 complete
Reads, candidate 21/21 complete Reads, including all eight detection files and
five required child sources. The candidate's two lists contain 6/17 filenames and
remain distinct from Reads. All 40/44 capture files and ten retained runtime
configuration files verify. Final review and strict preflight attestation are
recorded separately; this note does not itself approve readiness.
