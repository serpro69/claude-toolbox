# Coordinator retry audit

The retry editor reads only its request, the two new frozen instructions, declared
fixture inputs, checkout and selected output. Instruction call 19 finishes before
first subject reads at 25. Revision IDs, changed-file names and head membership at
32, followed by requirements/diff/base contract/head resolver at 39, precede output
existence check 51 and the single patch 56. Verification reads at 61 cover the new
output and unrelated pre-existing draft. No runtime tests or network calls run.

Only docs/feat/wip/prep/pr-12-draft.md changes by snapshots/hashes. Both readers read
only their requests and artifact copies; original calls are 10 and 19, revised
calls are 10 and 19. All source/oracle/other-version content stays outside their
manifests and observed reads. Both use gpt-6-astra, xhigh, summary none. No model
build or temperature is recorded.

Fixture input hashes, actual Git refs, eval assertions, oracle, and all three
request texts match the initial attempt after substituting only workspace and
instruction prefixes. Reader copies match their evidence artifact bytes. The new
instruction SHA256 is recorded separately; the initial snapshot remains unchanged.

The new draft explicitly identifies added tests in the current increment. Its
answer accuracy, fidelity and impact on prior passes are reserved for the fresh
independent grader. Standard shared-filesystem and ambient shell-startup limitations
remain as recorded for the initial runs.

