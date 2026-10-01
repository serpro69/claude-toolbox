# JS/TS — test artifacts

Consumed by the `/kk:test` skill when the `js_ts` profile is active. Read both files before running checks or changing tests. The preflight in `validators.md` gates command execution; `testing.md` guides test selection and authoring.

## Always load

- [validators.md](validators.md) — discover the owning package's toolchain, check tool availability, select one-shot validation commands, and report unavailable checks accurately.
- [testing.md](testing.md) — JS/TS test quality: runtime boundaries, async assertions, deterministic timers, isolation, type contracts, and UI/integration coverage where applicable.

## Conditional

_None._ Apply framework- and runtime-specific guidance only when the project uses those tools; this profile does not select a test framework.
