# Runtime PR retry harness

The first run is retained in `../runtime-pr/`. A fresh editor will receive the
identical scenario prompt, fixture content, frozen instructions, oracle and
assertions. The local base/head commit identities are unchanged. Only the neutral
read-only Git harness gains this requirement before dispatch:

> Read-only Git harness: every Git query must use `git --no-optional-locks` or `GIT_OPTIONAL_LOCKS=0` so read-only queries cannot refresh the index.

The initial traces also show blocked ambient navi logger initialization from the
default login shell. The retry therefore records this additional neutral setting
before dispatch:

> Shell harness: set `login:false` on every shell command to avoid unrelated login-shell initialization.

This prevents incidental Git index refresh; it supplies no expected editorial
answers. The editor and both original/revised readers will be fresh general-purpose
sessions with no inherited conversation and no model overrides. Both fresh readers
receive the same non-login shell harness setting, identical fixed questions, and
only their respective artifact. The original reading artifact is byte-identical
to the first run; the first-run reader's evidence remains in `../runtime-pr/`.

The retry stage is `/tmp/clarify-issue-task1/regressions/runtime-pr-retry/`.
Complete input hashes include Git metadata. `before/checkout/` captures the exact
repository before the retry; `before/snapshots/` remains grader-only evidence.
