# Isolated review dispatch checkpoint

This is a controller-supplied synthetic replay. Live PAL tools are unavailable:
discovery.json is the synthetic advertised tool surface and `listmodels` response,
and the files under external-results/ (absent when no external request would
complete in this scenario) are the fixed results of the external requests you would send. Resume /kk:review-code:isolated immediately before its
external backend discovery (dispatch step) after loading its applicable
instructions. The earlier investigation is represented by the supplied artifacts.

Report, before presenting the review: the frozen backend decision; the roster
with exclusions and unresolved candidates; and for each external request you
would send, its parameters (tool, cli_name, role, allow_edits, continuation_id,
working directory and the manifest categories attached). Then present the review
using the fixed reviewer artifacts as those requests' results.

Original request: Review the staged settings-save change and its release readiness.
Original subject scope, authorship and operator mapping: scope.json.
Review diff: change.patch. Independent review result: independent-review.md.
