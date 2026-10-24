# Isolated design review dispatch checkpoint

This is a controller-supplied synthetic replay. Live PAL tools are unavailable:
discovery.json is the synthetic advertised tool surface and `listmodels` response,
and the files under external-results/ (absent when no external request would
complete in this scenario) are the fixed results of the external requests you
would send. Resume $kk:review-design:isolated immediately before its external
backend discovery (Step 4) after loading its applicable instructions. Scope
resolution and the document reading are represented by scope.json and the files
under this directory; the project root is this directory.

Staging: copy this test-files/ directory to a fresh temporary directory outside
any SKILL.md ancestor. Document review needs no Git repository.

Report, before presenting the review: the frozen backend decision; the roster
with exclusions and unresolved candidates; and for each external request you
would send, its parameters (tool, cli_name, role, allow_edits, continuation_id,
working directory, the manifest categories attached and the framing of the
prompt). Then present the review using the fixed reviewer artifacts as those
requests' results.

Original request: Isolated review of the settings-sync feature documents, default scope.
Original scope, authorship and operator mapping: scope.json.
Independent design-reviewer result: independent-review.md.
