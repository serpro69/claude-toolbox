# Preserved sandbox-limited effort attempt

The reviewed effort correction and nine offline controls pass, as do 26
predecessor adapter/receipt tests. Freeze:
`44f5beea2ea585f9fdb19647db7d3efb70a5f3c70bebc453528e7f42cb0d3352`.

The first baseline probe failed normal startup inside the outer Codex sandbox:
SessionStart reported EROFS for Claude's session-env directory, Capy startup
failed, and only API retries followed. No instruction receipt was established.
The parent interrupted tool session 24643; its returned exit was 130. No controller
completion/finalization record was produced, so graceful cleanup is unverified.
The retained partial files have a separate parent-labeled incomplete manifest.
No candidate or measured session ran under this freeze.

The reviewed [host-execution successor](../high-effort-host/run-contract.md)
uses separate paths and a new freeze; this failed attempt is never reused as
binding evidence. Original source, calibration and preflight seals still verify.
