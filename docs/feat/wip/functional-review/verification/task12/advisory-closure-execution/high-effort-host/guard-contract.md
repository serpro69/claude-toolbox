# Receipt-verification successor

Task 12.21's independent completion review identified one P2 source gap: the
original preflight guard checks audit hashes/names but not successful receipt
content, so an overall/review PASS declaration could bind a known FAIL record.
Fix this required verification behavior without changing any captured input,
actor instruction, runtime setting, prompt, criterion or historical freeze.

The selected entry point for future operations is `guarded_successor.py`, which
delegates to the frozen launcher and replaces only its preflight verification.
Before the original approval/state/calibration/retention gate, it independently
reruns the pinned Claude receipt audit against each sealed binding and selected
source, then requires the retained audit to equal that successful result. Empty,
failed, incomplete or stale audit records cannot satisfy the check. All original
preflight prerequisites remain required after these checks.

`guard-freeze.json` separately pins the new verifier, tests and this declaration
and binds the original host execution freeze
`be7d605b7aabe88855051362a3f92bc99a0cf56a6fe22b0805adfc1763830764`.
Source review and offline checks precede this pin. This is a verification-only
identity, not a claim that past probes used new runtime code. Captures retain
their actual original source/runtime identity. Grader inputs, results, expected
outcomes and original assertion grades are unchanged; no fresh calibration or
model capture is needed to validate this local rejection behavior.

Regression checks use the actual complete baseline and incomplete candidate
captures: complete baseline passes; missing candidate reads fail before any
nominally approved original guard can run; empty/failed audit records fail despite
valid baseline raw evidence; guard-dependency drift fails. No test launches actors
or edits frozen captures. The passing baseline does not imply candidate readiness.

The frozen original launcher remains historical and must not be selected alone
for later preparation/measurement. A later capture successor must carry forward
this recomputation requirement. No additional actor run or changed binding prompt
is selected by this correction; the candidate's eight missing reads keep preflight
BLOCKED. Preserve independent-review failure and resolution provenance.
