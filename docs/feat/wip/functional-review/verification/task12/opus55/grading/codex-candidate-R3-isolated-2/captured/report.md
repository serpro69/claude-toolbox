I’m using `kk:review-code` in isolated mode to review the staged receipt handling. I’ll load the review guidance, run the independent reviewers, and verify their findings without changing the code.

The scope is two staged Python files. I’ve loaded all common guidance and the four Python checklists; none of the other seven profiles apply. PAL is unavailable in this session, so isolated mode will proceed with the independent code reviewer and that limitation noted.

The README requires this client increment to work with the provider at `eval-release`, even with enhanced settings disabled. I found that provider’s source in local Git and supplied it to the independent reviewer. I’m checking the caller’s result and stored values against that baseline.

The staged unit test passes, but the compatibility check fails: the released provider applies the settings, then the new client reports an error because the response lacks `applied`. The previous client reports success with the same provider. This also happens with enhanced settings disabled; the independent reviewer is finishing its assessment.

**REQUEST_CHANGES — one P1 finding.**

**P1: Mandatory receipts break saves against the supported provider** — [client.py:5](/tmp/fr-opus55-matrix-20261011/codex-candidate-R3-isolated-2/client.py:5).

The provider at `eval-release` applies the settings and returns only `{"ok": True}`. The staged client then raises `RuntimeError` because `applied` is absent—even with `enhanced_settings=False`. The previous client reports success. This violates the documented requirement that each client increment remain independently releasable.

Preserve legacy success handling until provider receipt support is established. Keep receipt-aware coverage and add a compatibility test asserting both applied values and caller-visible success. The updated mock currently hides this regression.

*Independent code-reviewer finding; confidence 100%; Python code-quality checklist.*

Verification and scope:

- Reviewed both staged files (+4/−2), feature contracts, review-base sources at `ac09e55`, and actual provider source at `eval-release` (`2214073`).
- The staged unit test passed. My executed compatibility check reproduced completed writes followed by client errors with the flag both off and on. Receipt-bearing success and explicit failure controls behaved as expected.
- Supported-provider compatibility is **blocked**. Task 2 remains outside scope; live deployment was not assessed.
- Isolated reviewer: `code-reviewer` (`gpt-6.1-sol`). PAL was unavailable, so there is no second-reviewer corroboration.

Indexed the systemic pattern under `kk:review-findings`. No repository files or staged changes were modified.
