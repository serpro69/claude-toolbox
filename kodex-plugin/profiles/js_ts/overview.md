# JS/TS profile

## What this profile covers

Idiomatic JavaScript and TypeScript source code: type safety and `strict` flags, async patterns (Promises, async/await, cancellation), module boundaries (ESM vs. CJS), React/JSX discipline where applicable, bundler/build hygiene, runtime duality (Node vs. browser), and SOLID principles adapted to JS/TS idioms.

## When it activates

Any file with one of these extensions in scope: `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts`. See [DETECTION.md](DETECTION.md) for the authoritative rule. Activation is additive with other profiles on the same diff.

## Populated phases

- `implement/` — pre-write gotchas consumed by `$kk:implement` (runtime validation, typing, async ownership, module/runtime boundaries, shared state, and React lifecycles where applicable).
- `review-code/` — checklists consumed by `$kk:review-code` (security, SOLID, code-quality, removal-plan).
- `test/` — validation preflight and testing guidance consumed by `$kk:test` (project-local tool discovery, runtime tests versus type checking, async assertions, isolation, and applicable UI/integration checks).

Other phase subdirectories are not populated for this profile: generic per-phase behavior is sufficient. Implementation guidance loads for both standalone and plan-mode tasks through the shared profile loader. Test guidance loads when `$kk:test` detects JS/TS source in scope, including verification invoked by `$kk:implement`; neither phase needs additional detection signals. Package metadata alone does not activate the profile.

## Looking up JS/TS dependencies

When adding or upgrading a dependency, follow the `$kk:dependency-handling` skill's cascade:

1. **capy-first** — query the project's indexed `kk:lang-idioms` / `kk:project-conventions` / prior context7 fetches.
2. **context7** — fetch current docs for the library, framework, or tool (React, Next.js, Vite, Vitest, Prisma, etc.).
3. **web** — fall back to [npmjs.com](https://www.npmjs.com), the project's own repository README, or TypeScript-type-definition packages (`@types/…`) only if the first two yield nothing.

Project dependency metadata lives in `package.json` with `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` for resolved versions. TypeScript settings live in `tsconfig.json`. Version-specific behaviors must be verified against the version the lockfile actually resolves to, not the latest available.
