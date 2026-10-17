# Advisory-closure preflight declaration

> Task: 12.21, selected 2026-10-17
> Authority: the user requested runtime preflight after the adapter/calibration commit
> Measured actor sessions and PAL: not selected

Run the existing `runner.py binding` operation once for each declared pair,
serially: Claude baseline, Claude candidate, Codex baseline, Codex candidate.
Use the unchanged [execution freeze](execution-freeze.json), verified fresh
[calibration](calibration-results.json), archived inputs and runtime/model policy
in [execution-contract.md](execution-contract.md). Temporary evaluation plugin,
cache and project-trust setup/owned cleanup are included in this preflight request.
Do not overwrite normal entries, change policies or run the 64-session matrix.

Each binding workspace is a fresh child of `/tmp/fr-advisory-actors-20261017`.
Only the selected filtered plugin and synthetic subject are supplied. The binding
prompt asks the parent and actual named reviewer to load instructions and stop
before behavioral investigation. Assess each side against its own instructions;
the pre-feature baseline must not receive candidate-only methodology.

Retain all sealed public events, reports, launch metadata and actual runtime files.
Audit successful instruction bytes, parent/child linkage, selected models and
roots, full-read coverage, no subject edits, evaluator access and PAL absence.
A request/path, final self-report or clean runtime exit alone cannot prove receipt.
Unknown exact submitted prompt fields remain unknown; do not extend the existing
receipt/use fallback to measured cases. No OS-wide confinement is claimed.

Use the archived `probe_state.py` to create exactly two separate fresh Capy
workspaces under `/tmp/fr-advisory-actors-20261017/state-probes`, with evidence in
`state-probe/`. Require empty separate stores, successful indexing/retrieval,
absent foreign markers and unavailable private vaults. Preserve raw calls/results,
stderr and summary. These workspaces and stores must never seed measured runs.

Stop the affected sequence on setup, capture or binding failure. Preserve the
attempt; no implicit retry, policy change or source mutation. Complete independent
unaffected checks where possible. Any necessary successor declaration must be
explicitly identified and reviewed before a replacement attempt.

After successful captures, independently review the audited evidence. Only then
write `preflight.json` with this execution-freeze hash, calibration-result hash,
all four binding-manifest hashes, state summary/raw-evidence hashes and the
independent review hash/status. Run `Adapter.preflight()` to verify the concrete
attestation. Keep a separate preflight checksum manifest; previous preparation and
calibration manifests remain unchanged.

A passing preflight permits later preparation under the frozen comparison when
measurement is selected. It establishes runtime/input readiness only, not review
quality, adoption, full feature acceptance or Task 13 completion.
