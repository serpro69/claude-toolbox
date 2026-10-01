# JS/TS — per-task gotchas

Read before editing JavaScript or TypeScript. These pitfalls can survive a successful build and fail only with real inputs, concurrent requests, or a different runtime. Apply TypeScript advice to TypeScript (or existing checked JSDoc) and React advice only when the task uses React; neither a `.tsx` extension nor this profile requires adopting React.

For a new dependency, version change, or unfamiliar API, follow `/kk:dependency-handling` before writing the call. See [Looking up JS/TS dependencies](../overview.md#looking-up-jsts-dependencies) for the lookup cascade. Preserve the project's language, framework, and package-manager choices.

## Establish the execution environment

- Inspect the owning package's `package.json`, lockfile, scripts, and relevant `tsconfig`/build configuration when present, including inherited settings. In a workspace, the root and the target package can have different responsibilities. Use the versions the project resolves.
- Identify where the changed code runs: Node, browser, worker, server rendering, or a shared module. Available globals and package entry points differ. A bundler accepting an import does not prove every deployed runtime can execute it.
- Preserve existing strictness, lint rules, and module settings. Do not disable checks or switch module systems to make a local change compile. Treat broader configuration migrations as separate work unless requested.

## Types do not validate runtime input

- Validate data where it enters the application: JSON, storage, forms, environment variables, and remote responses. In TypeScript, keep untrusted values as `unknown` until checks establish their shape. Use the project's existing validator or explicit guards; a type assertion, generic response type, non-null assertion, or `satisfies` expression adds no runtime validation. [TypeScript's type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions) are erased during compilation.
- Narrow unions through checked properties or discriminants. Handle `null` before accessing objects and check array contents as well as the container. A user-defined type predicate must actually prove its claim; its return annotation alone is not evidence. Keep exhaustive handling when extending a discriminated union. See [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html).
- Avoid spreading `any`, double assertions (`as unknown as T`), or suppression comments to silence a mismatch. Fix the boundary or model the actual values. JavaScript needs the same runtime checks without introducing TypeScript syntax into `.js` files.

## Own async completion and failure

- Return or await promises when the caller depends on their completion. `forEach(async ...)` does not wait for its callbacks, and `map(async ...)` produces promises. Use a sequential loop for dependent work or await a collection when work is independent; bound concurrency when the input can grow.
- Choose batch failure semantics deliberately. `Promise.all` rejects when an input rejects; it does not cancel work already started. Use `allSettled` when all outcomes must be observed, whether for partial success or cleanup before propagating failure, and inspect rejected outcomes. See [Promise aggregation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all).
- Detached work still needs an error owner: `void task()` alone does not handle rejection. Catch at a boundary that can recover, translate, or report the failure; otherwise propagate it. In JavaScript anything can be thrown, so narrow a caught value before reading `message` or other properties.
- For `fetch`, inspect HTTP status as required by the endpoint contract; a 404 or 500 response does not itself reject the promise. Propagate cancellation signals to supported operations and release timers/listeners in cleanup. A timeout implemented only with `Promise.race` stops waiting but leaves the underlying work running. See [Fetch errors and cancellation](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).
- Prevent stale completions from overwriting newer state. Cancellation can save work, but correctness must also account for results that arrive after the caller stops caring. Do not retry side effects unless their contract makes retries safe.

## Keep module and runtime boundaries explicit

- Follow the package's ESM/CJS contract: file extensions, the nearest applicable `package.json` `type`, published `exports`, and the project's module-resolution settings. Interoperability depends on the actual runtime and toolchain; do not assume every `require`/`import` combination works. See [Node package boundaries](https://nodejs.org/api/packages.html).
- TypeScript aliases and compiler `lib` declarations do not install runtime resolvers or polyfills. Confirm that emitted imports and the APIs used work in the deployed environment, including code executed directly without a bundler.
- Keep Node-only imports and secrets out of browser entry points and their transitive dependencies. Build-time environment substitutions in client bundles are visible to users. Shared or server-rendered modules must not access `window`, `document`, or browser storage at import time.
- Preserve public exports and import-time behavior. Avoid adding global initialization or dependency cycles through convenience re-exports; both can make module loading order observable.

## Preserve value and ownership semantics

- Use nullish defaults when only `null`/`undefined` mean missing. Truthiness also rejects valid `0`, `false`, and empty strings. Defaulting is not validation: check required types, finite numbers, integer/range constraints, and empty collections explicitly.
- Avoid mutating caller-owned arrays or objects. `sort`, `reverse`, and `splice` mutate arrays; object/array spread copies only one level. Copy at the boundary where ownership changes, and supply a numeric comparator when sorting numbers.
- Keep request- or user-specific state out of shared module globals unless isolation and lifetime are explicit. Async functions can interleave at `await` even on a single event loop; a read-modify-write sequence may still need a transaction or another concurrency control.
- Avoid synchronous I/O and large CPU loops on latency-sensitive event-loop paths. An `async` declaration does not move CPU work to another thread.

## React components and hooks, when applicable

- Keep rendering pure and derive values from props/state during rendering when possible. Use event handlers for user actions and Effects for synchronization with external systems.
- Respect Hook ordering and dependency rules; repair stale closures instead of suppressing dependency warnings. Use functional state updates when the next value depends on the previous one, and preserve state immutability and stable list keys.
- Pair subscriptions, timers, and external resources with cleanup. For requests, abort or ignore obsolete results so an older response cannot replace newer state. Do not disable Strict Mode to hide missing cleanup. Prefer the project's existing framework/data-loading mechanism when it owns the request lifecycle. See [React Effect synchronization](https://react.dev/learn/synchronizing-with-effects).

## Verify using the project's toolchain

- Run the owning package's relevant typecheck, lint, test, and build scripts. Transpiling TypeScript can succeed without type checking; use the project's typecheck command when present. Use installed tools rather than downloading a different compiler through an ad hoc command.
- Exercise the changed behavior's failure and boundary cases: rejected promises, invalid input, valid falsy values, cancellation/stale results, and the actual runtime entry point as applicable. Use the existing test framework and avoid watch mode for one-shot verification.
- Report unavailable checks explicitly. Keep lockfile changes tied to intentional dependency changes; a missing local tool is not a reason to rewrite project dependencies.
