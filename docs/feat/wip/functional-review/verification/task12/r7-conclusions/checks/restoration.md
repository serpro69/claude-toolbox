# Operative restoration

The failed R7 keep criterion rejects candidate bf873de6. Its two-file patch is
retained in ../candidate-method.patch and its immutable source archive remains in
../source-inputs/candidate/. Both operative method files were restored to
cc07a614, without changing the running comparison's frozen bundles.

`make generate-kodex` regenerated successfully, but its structure-test phase ran
with the default Python 3.10.12 and failed seven TOML parser assertions because
that interpreter lacks `tomllib`. This is a verification-environment failure.
Rerunning `make test-structure` with the already declared Python 3.12.11 at the
front of PATH passes; see restored-structure.log. No dependency was installed.

`git diff --exit-code -- kodex-plugin .codex/agents
klaude-plugin/skills/review-code/functional-review.md` passes after generation.
The previously kept Task 12.12 correction and all other operative files remain
at their starting HEAD bytes.
