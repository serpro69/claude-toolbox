# JS/TS — validation commands

Use the project's existing toolchain. A passing runtime test, a successful typecheck, and a successful build establish different facts; report them separately.

## Preflight before execution

1. Identify the packages owning the changed JS/TS files and their tests. Read the applicable `package.json` scripts, workspace configuration, lockfile, runner configuration, and CI commands when present. Include inherited TypeScript configuration. Standalone scripts may have no package metadata.
2. Select the runtime and package manager from the project's documented setup, `packageManager` field, and owning workspace's lockfile. Resolve conflicting evidence before installing or changing anything. Preserve the configured working directory and workspace filters; a root script may orchestrate several packages.
3. Check runtime/package-manager availability with `command -v <binary>`. For package-local runners, linters, and compilers, also check the installed project environment: local/workspace binaries or the configured resolver, including Yarn Plug'n'Play. A missing global `vitest` or `tsc` does not imply the project-local tool is absent; a script naming a tool does not prove it is installed.
4. If a required executable, dependency installation, browser, or service is unavailable, report the affected check and the concrete prerequisite, using the repository's setup instructions. Continue independent checks that can run. Do not download tools through `npx`, `dlx`, `bunx`, or similar fallbacks, install a new runner, or change dependency metadata just to obtain a green result. Dependency changes that are part of the task follow `$kk:dependency-handling`; use the lookup cascade in [the profile overview](../overview.md#looking-up-jsts-dependencies).
5. Choose commands only after identifying the actual runner and installed version. Package-manager flag forwarding and runner flags differ. Do not append Vitest flags to a script backed by Jest, Node, or a custom wrapper.

## Select applicable checks

| Check | When it applies | How to run it |
| --- | --- | --- |
| Runtime tests | Existing tests cover the changed package or behavior | Use its test script and configuration; run focused tests while iterating, then the relevant package suite and repository-required checks. |
| Type checking | Changed TypeScript, declarations, or checked JavaScript are covered by a project typecheck | Use the configured typecheck script, including project references or framework-specific checkers. Preserve its `tsconfig`; do not substitute `tsc file.ts`, which ignores project configuration. |
| Lint and format checks | The project configures them for the changed files | Use the existing check scripts. Avoid auto-fix, rule disabling, or unrelated formatting changes as a side effect of verification. |
| Build or package checks | Changed imports, exports, declarations, bundling, or runtime entry points need verification | Run the owning package's build/check scripts and exercise the relevant emitted entry point when practical. Unit-test transforms can hide ESM/CJS or alias-resolution problems. |
| Browser or integration tests | The changed behavior depends on browser APIs, services, persistence, or multiple components and the project has a corresponding suite | Use that suite's documented setup and isolated test environment. Report missing prerequisites and remaining coverage instead of silently substituting a mocked unit test. |

Runtime transpilation does not establish TypeScript correctness. For example, Vitest's runtime tests and its [type-testing mode](https://vitest.dev/guide/testing-types) are distinct. Likewise, runtime input validation needs executable tests even when static types pass.

## One-shot execution

- Prefer an existing CI or one-shot script. If adapting a script that starts watch mode, use the identified runner's supported option without dropping setup hooks, coverage settings, or workspace selection. [Vitest's `run` command](https://vitest.dev/guide/cli#vitest-run) is one example, not a universal test flag.
- For an existing Node test suite, `node --test` runs once; preserve the project's selected test paths and runtime options. Do not run `.ts` tests directly with Node unless the configured runtime/version or loader supports the required syntax and semantics. See [Node's test runner](https://nodejs.org/docs/latest-v24.x/api/test.html).
- Treat failed tests, unhandled rejections, open handles, and unexpected zero-test runs as evidence to investigate. Do not add pass-with-no-tests flags, force process exit, skip assertions, or update snapshots merely to make the command succeed.
- Re-run affected checks after fixes. Once required checks pass, broaden or repeat only for remaining coverage gaps, additional changes, or repository requirements.

## Report what was verified

Record each command, its working directory/package scope, and the result. Distinguish **passed**, **failed**, **skipped because unavailable**, and **not applicable**. State missing prerequisites and meaningful limits such as untested browser behavior or an unavailable typecheck. An unavailable runner is not a passing suite; a filtered run is not evidence that all tests passed.
