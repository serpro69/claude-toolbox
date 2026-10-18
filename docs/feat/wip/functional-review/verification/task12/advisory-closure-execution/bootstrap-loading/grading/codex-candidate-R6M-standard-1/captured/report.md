I’m using `$kk:review-code` to review the staged change, trace its effect on batch reporting, and check compatibility with existing callers.


Preparation is complete: the staged diff covers two Python files, and all eight profile rules were checked. Only Python applies. I’ve read all six common instruction parts, the Python index, and both checklist parts covering security, SOLID, code quality, and removal guidance. I’m now checking the reporting contract and affected callers.


All four existing tests pass, but the default change breaks empty batches: `report([])` now raises `ZeroDivisionError` instead of returning `Items: 0`. I reproduced this against both HEAD and the staged files. Explicit detailed mode already had this defect; enabling it by default exposes it to previously successful calls.


**REQUEST_CHANGES — one P1 finding.**

::code-comment{file="config.py" line="1" severity="P1"}
Enabling detailed reports breaks empty batches. `report([])` and `report([], detailed=None)` previously returned `"Items: 0"`; both now raise `ZeroDivisionError` because `summarize()` divides by `len(values)` unconditionally in detailed mode. This violates the README’s explicit empty-batch contract.

Skip mean calculation for empty batches and add coverage for default and explicitly detailed empty reports.
::

Location: [config.py:1](/tmp/fr-advisory-bootstrap-20261018/codex-candidate-R6M-standard-1/config.py:1). **Confidence: 100%** — reproduced using both HEAD and staged source. The explicit-detailed failure is inherited; exposing it through the default is the regression.

Profile: `python` · Checklist: `code-quality-checklist.md` · Trigger: `.py` files.

Reviewed the staged increment against `HEAD a2103644`: two files, two additions and two deletions. Intent and acceptance criteria came from the README; no feature task scope exists.

All four existing tests pass. Additional comparisons confirmed populated defaults, explicit overrides, counts, and zero/negative/fractional means. Empty plain reports remain supported; empty default reports are blocked by this finding. Traced configuration through reporting, aggregation, and formatting. Historical installation settings and live deployments were not assessed.

The systemic pattern was indexed under `kk:review-findings`. No repository files were changed.
