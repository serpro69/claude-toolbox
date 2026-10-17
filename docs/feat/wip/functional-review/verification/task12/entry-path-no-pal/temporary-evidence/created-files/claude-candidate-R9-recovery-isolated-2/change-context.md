# Change context (parent-prepared, factual)

Repository: /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R9-recovery-isolated-2
Review base: HEAD 7c0410c ("Review base"), branch master
Selector: staged changes (`git diff --cached`); no unstaged changes. Worktree files for
reader.py and tests/test_reads.py are identical to the index (`git diff --quiet` succeeded),
so the worktree paths are the reviewed candidate.

## Intent and authority (explicit)
Source: README.md (repository root). Preference IDs with surrounding whitespace must be
accepted; trim the ID before lookup; preserve the resilient-read contract: up to three
attempts on TransientRead, returning the first success; exhausted transient errors propagate;
MissingPreference is permanent and propagates on the first attempt; reads have no side effects.
Public entry point: Preferences.read. Repository.read_resilient owns the bounded retry policy;
read_once performs one attempt.

## Change boundary
reader.py: read_preferences now passes key.strip() to repository.read_resilient.
tests/test_reads.py: replaced test_existing_key with trim/transient/retry-limit/permanent tests.
Unchanged: preferences.py (entry point), repository.py (retry policy, ScriptedBackend).
No docs/feat/wip feature directory exists.

## Baselines
Review base = HEAD 7c0410c. No separate release/deployed baseline is named. Base versions of
both changed files are fully contained in the diff hunks (reader.py 2 lines; test file 11 lines).

## Attributed verification
Parent ran `python3 -B -m unittest discover -s tests -v`: 4 tests, all OK (test_permanent_error,
test_retry_limit, test_transient_error, test_trim_key). Reviewers have source-only access.

## Rejected approaches
None known.
