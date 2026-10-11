## Code Review Summary

**Verdict: REQUEST_CHANGES.** The whitespace trimming works, but the change also drops the retry behaviour the README says must be kept. The updated tests check for the missing retry instead of catching it, so the suite still passes.

**Files reviewed**: 2 files, 10 insertions and 4 deletions
**Intent and scope**: Accept preference IDs with surrounding whitespace by trimming them, and keep the existing retry behaviour on transient read errors (`README.md:5-9`). The review covers only the staged diff (`git diff --cached`); there were no unstaged changes. No `docs/feat/wip` folder exists, so there was no task scope to check against.
**Baselines**: `7c0410c` ("Review base") compared with the staged files. No release or deployed version was assessed.

## Behavior and Compatibility

Call path: `Preferences.read` (`preferences.py:8`) → `read_preferences` (`reader.py:1`) → `Repository` → `ScriptedBackend.read`.

| Scenario (README contract) | Expected | Base `7c0410c` | Staged change |
| --- | --- | --- | --- |
| Key `" w "`, backend returns a value | Looks up `"w"` and returns the value | Looks up `" w "` untrimmed ✗ | ✓ |
| Key `" w "`, one `TransientRead` then a value | Returns the value after 2 attempts | Retries ✓ (key untrimmed) | **Raises `TransientRead` after 1 attempt ✗** |
| Three `TransientRead`s in a row | Raises after 3 attempts | ✓ | Raises after 1 attempt ✗ |
| `MissingPreference` | Raises on the first attempt | ✓ | ✓ (no retry at all now) |
| No side effects | — | ✓ | ✓ |

- **Executed:** `python3 -B -m unittest discover -s tests` passed both tests on the staged files. That green run includes `test_transient_error`, which checks for the regression described below.
- **Evidence limits:** The rows above come from reading the source, except the two tested scenarios. No test covers retries running out after 3 attempts or `MissingPreference`, in either the base or the change.
- **Compatibility:** Not applicable. Reads have no side effects and nothing is persisted, migrated or deployed.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[reader.py:2] The trim change also removed the retry on transient errors**
  - Profile: generic · Checklist: — (the Python `code-quality-checklist.md` error-handling section also applies)
  - Triggered by: — (the Python profile is active because of the `.py` files)
  - **What happens:** the call changed from `repository.read_resilient(key)` to `repository.read_once(key.strip())`. Every `Preferences.read` now makes exactly one attempt, so one temporary backend error fails a read that used to succeed on the second try. This breaks "preserve the existing resilient-read contract… up to three attempts" (`README.md:6-8`). The README also says `read_resilient` owns the retry logic (`README.md:11-12`), and this call skips it.
  - **The test hides it:** `tests/test_reads.py:13-17` (`test_transient_error`) feeds `[TransientRead, value]` and asserts that `TransientRead` is raised after a single attempt (`keys == ["w"]`). The contract says this input should return the value after two attempts.
  - Confidence: 97%. I read `Repository.read_resilient`/`read_once` (`repository.py:26-35`) and the README contract, and ran the suite. The only doubt is whether the author meant to drop retries, but the README rules that out.
  - **Suggested fix:**
    ```python
    def read_preferences(repository, key):
        return repository.read_resilient(key.strip())
    ```
    The trim runs once, before the retry loop, so every attempt uses `"w"`. Rewrite `test_transient_error` to expect `{"color": "blue"}` and `backend.keys == ["w", "w"]`. Add two cases: three `TransientRead`s raise after 3 attempts with `keys == ["w"] * 3`, and `MissingPreference` raises with `keys == ["w"]`.

### P2 / P3
(none)

---

## Notes
- **Indexed:** the P1 is recorded in the knowledge base as `kk:review-findings`. The pattern: a call moves from a retrying wrapper to its single-attempt primitive, and a test is changed to match. Both knowledge-base searches came back empty because nothing had been indexed yet.
- **Checked:** the Python security, SOLID and code-quality checklists (nothing beyond the P1), and the `.strip()` boundaries (only the ends are trimmed, which matches "surrounding whitespace").
- **Not covered:** what to do with an all-whitespace or `None` ID. The README doesn't say, so I'm not raising either as a finding.

**Required next step:** the P1 fix above, including the corrected tests. You asked for a review only, so I haven't edited anything. Say the word if you want me to apply the fix.
