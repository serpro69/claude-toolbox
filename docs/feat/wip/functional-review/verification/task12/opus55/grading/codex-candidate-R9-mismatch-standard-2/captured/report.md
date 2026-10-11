I’m using `kk:review-code` to review the staged preference ID normalization change, including its compatibility with existing preference data.


The staged diff contains two Python files, with 10 added and 4 removed lines. I’m finishing the required checklist loading before tracing the normalization behavior and its tests.


Preparation is complete for `HEAD → staged index`. Python matched both `.py` files; Go, Java, JS/TS, Kotlin, Kubernetes, Kubernetes Operator, and skill-md did not match. All six bootstrap parts, the Python index, and both checklist parts are loaded, covering `profiles/python/review-code/{security-checklist,solid-checklist,code-quality-checklist,removal-plan}.md`.


The change trims IDs correctly, but it also replaces the retrying read with a single attempt. The README explicitly requires preserving retries, while the new test expects the first transient error to propagate. I’m checking recovery, exhaustion, and permanent-error cases against both HEAD and the staged code.


**REQUEST_CHANGES — one P1 finding.**

**P1: ID normalization bypasses the required retry policy** — [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R9-mismatch-standard-2/reader.py:2)

Replacing `read_resilient` with `read_once` makes `Preferences.read` propagate the first `TransientRead`, even when the next attempt would succeed. This affects both `"w"` and `" w "` and violates the README’s requirement to preserve resilient reads.

Restore the policy-bearing call:

```python
return repository.read_resilient(key.strip())
```

The new [transient-error test](/tmp/fr-opus55-matrix-20261011/codex-candidate-R9-mismatch-standard-2/tests/test_reads.py:13) asserts the regression. It should expect successful recovery and two lookups using `"w"`.

Profile: `python` · Checklist: `code-quality-checklist.md` · Trigger: `.py` files. **Confidence: 99%** — reproduced through the public entry point against HEAD and staged snapshots; the contract is explicit.

**Coverage and evidence:** Reviewed both staged files, **+10/−4 lines**, against HEAD `7c0410c`, plus the unchanged public entry point and repository. Intent comes from README; no feature task scope exists.

| Scenario | Staged result |
|---|---|
| First-attempt success and whitespace trimming | Supported |
| Recovery on attempt 2 or 3 | Blocked: raises on attempt 1 |
| Three transient failures | Blocked: stops after the first |
| Immediate `MissingPreference` | Supported: propagates immediately |
| Transient failure followed by `MissingPreference` | Blocked: never reaches attempt 2 |

Both staged tests pass, but the added error assertion contradicts the required behavior. Verification used the local scripted backend; no production environment was assessed.

Indexed the systemic finding under `kk:review-findings`. No source changes made.
