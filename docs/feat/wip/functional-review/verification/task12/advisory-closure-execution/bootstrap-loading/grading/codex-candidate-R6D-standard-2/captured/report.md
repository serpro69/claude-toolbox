I’m using `$kk:review-code` to review the staged change, following its required checks before inspecting the diff.

Preparation is complete for the staged diff: two Python files, five additions and five deletions. All six common instruction parts, the Python index, and both checklist parts are loaded, covering `security-checklist.md`, `solid-checklist.md`, `code-quality-checklist.md`, and `removal-plan.md` under `profiles/python/review-code/`. Python matched; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles did not. I’ll now check the report contract and affected callers.

The staged change preserves counts, mode selection, and mean formatting. All four tests pass, and 30 comparisons against HEAD show only the intended label change. An empty batch in detailed mode still raises `ZeroDivisionError`; HEAD does too, so that is a pre-existing issue rather than a regression in this increment.

**APPROVE** — no regressions found. No changes recommended for this staged increment.

Reviewed two files, with 5 additions and 5 deletions, against HEAD `2b50e59`. The change satisfies the README contract: `Items` becomes `Records`, preserving counts, mode selection, calculations, and the mean suffix.

- All four tests pass for both HEAD and the staged snapshot.
- Thirty scenario comparisons confirm that only the label changes.
- Validation used Python 3.12.11; historical deployment settings were not assessed.

One **pre-existing P2 issue** remains: detailed reporting of an empty batch raises `ZeroDivisionError` at [stats.py:4](/tmp/fr-advisory-bootstrap-20261018/codex-candidate-R6D-standard-2/stats.py:4). Confidence: 100%, reproduced in both revisions. Python boundary-condition guidance applies. Separate follow-up: handle empty detailed batches and add a regression test.

No findings to index. No files changed.
