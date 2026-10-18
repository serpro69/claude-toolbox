I’m using the `kk:review-code` skill to review the staged preference ID normalization change. I’ll load its review guidance, then inspect the affected behavior and compatibility contracts.

Preparation is complete: all six common-instruction parts, the Python index, and both checklist parts are loaded. The staged scope is two Python files (+21/−4); Python applies, while Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill-file rules do not. I’ll now check the contract and trace the normalization through its consumers.

The change keeps the existing retry policy and trims the ID before calling it. The contract requires up to three attempts for transient errors and immediate propagation of permanent errors. I’ll run the staged tests and verify third-attempt recovery and later reads against both HEAD and the staged version.

**APPROVE — no findings.**

Reviewed the staged changes against HEAD `7c0410c`: two files, +21/−4 lines. The normalization satisfies the README contract: IDs are trimmed before lookup, while the existing resilient-read policy remains intact.

Verified using isolated staged and HEAD snapshots:

- All four staged tests pass.
- Success on attempts one, two, and three returns immediately.
- Transient failures stop after three attempts.
- Permanent failures propagate without further retries.
- Later reads receive a fresh retry budget.

Compatibility is supported against HEAD within these checks. Validation used Python 3.12 and the scripted backend; other Python versions were not exercised.

No findings to index. No changes recommended; the staged files remain unchanged.
