# Candidate 3 declaration and temporary PAL exception

Declared before measurement. Inherit runtime, provider, model, permissions,
fixtures, rubric, grader, isolation and two-run threshold from
[the original Task 12 contract](../run-contract.md).

Candidate: `f7bbcc81c4760167d38622d9b698c2b2da54e5d9`, frozen from the three
current operative trees in `/tmp/fr-task12-candidate3-source-20261010`.
It includes candidate 2's documented-lifecycle/detection-ledger fixes and the
independent review correction preserving existing ENOENT/root-resolution
fallbacks. Candidate 2 ran only its loading probe; it has no measured results.
Baseline remains `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.

The user instructed **“ignore pal-based verification for now.”** PAL-dependent
receipt/use, corroboration and live-integration checks are therefore deferred.
Continue named independent review and other behavioral verification. Preserve
literal full-assertion grades, with deferred PAL components identified separately;
never relabel missing receipt as PASS or claim full two-reviewer acceptance.
Owner: implementing agent when verification resumes; restore the existing local
PAL API configuration, prove startup and rerun affected matching pairs to close
that deferred coverage. No credential values enter artifacts or prompts.

The configured PAL service may remain unavailable in actor sessions; keep its
actual failure visible and do not coach actors around it. All relevant non-PAL
obligations still need two fresh passing observations. R8's synthetic degraded
reporting checks remain useful and do not certify transport.

Run isolated/implementation sessions serially. Candidate 1's parallel isolated
runs both used `/tmp/kk-evidence-enhset`; their possible shared scratch state is
an explicit isolation limitation, not acceptance evidence. Before subsequent
runs, archive and remove only controller-attributed temporary outputs from
completed actor sessions, then audit new reads/writes for cross-run access.
