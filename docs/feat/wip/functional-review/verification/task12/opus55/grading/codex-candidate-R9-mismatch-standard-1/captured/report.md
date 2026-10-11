I’m using `$kk:review-code` to review the staged change, trace its affected behavior, and check compatibility.


Preparation is complete: the staged scope is two Python files, with 10 additions and 4 deletions. I’ve read all six common instruction parts, the Python index, and both checklist parts covering security, SOLID, code quality, and removal guidance. Python is the only matching profile; the other seven detection rules did not match. I’ll now check the documented ID contract and the affected readers and writers.


I found a regression: IDs are trimmed correctly, but the reader now bypasses the repository’s retry policy. Both staged tests pass because the new transient-error test expects the broken behavior. Separate checks through `Preferences.read` confirm that recovery after transient errors fails and exhausted reads stop after one attempt instead of three; immediate success and immediate permanent errors still behave correctly.


**REQUEST_CHANGES — one P1 finding.**

**P1: Preserve retries when normalizing IDs** — [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R9-mismatch-standard-1/reader.py:2)

Replacing `read_resilient` with `read_once` bypasses the documented three-attempt retry policy. Through `Preferences.read`, outcomes `[TransientRead("busy"), {"color": "blue"}]` now raise immediately instead of returning the successful result. This makes recoverable backend failures user-visible.

Use `repository.read_resilient(key.strip())`. Update [test_transient_error](/tmp/fr-opus55-matrix-20261011/codex-candidate-R9-mismatch-standard-1/tests/test_reads.py:13), which currently asserts the regression, to expect recovery and normalized keys on both attempts.

Profile: `python` · Checklist: `code-quality-checklist.md` · Trigger: `.py` files. **Confidence: 100%** — independently reproduced against the staged candidate and verified against the README contract and HEAD behavior.

Reviewed both staged files (+10/−4) against `HEAD 7c0410c`, including the unchanged public entry point and repository. No feature task scope was available; the README explicitly requires normalization while preserving resilient reads.

| Executed scenario | Candidate result |
|---|---|
| Immediate success, existing or padded ID | Supported |
| Success after one or two transient failures | Blocked: raises on first failure |
| Three transient failures | Blocked: stops after one attempt |
| Immediate permanent error | Supported |
| Transient followed by permanent error | Blocked: never reaches permanent error |

Both staged tests pass; separate contract checks expose the failures above. Verification used local scripted backends, with no production assessment. Deployment and migration combinations are not applicable to this helper change.

Indexed the systemic finding as `kk:review-findings`. No repository files were changed.
