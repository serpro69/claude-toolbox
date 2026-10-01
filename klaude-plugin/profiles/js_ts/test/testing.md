# JS/TS — testing guidance

Use the established runner, naming, fixtures, and test locations. Apply browser and framework advice only to projects that use them. Look up unfamiliar test APIs against the installed version through `/kk:dependency-handling`; examples from another runner are not interchangeable.

## Test observable behavior

- Turn the requirement or bug into an input, action, and observable outcome. Prefer public results, emitted events, persisted effects, or visible UI over assertions on internal helpers and call order. Interaction assertions are useful when the interaction itself is part of the contract.
- Add focused regression coverage for meaningful behavior changes; demonstrate that it catches the original defect when practical. Avoid tests that duplicate implementation logic or merely assert constants in low-impact prose/config changes.
- Use named table cases for meaningful boundaries: missing values, valid `0`/`false`/empty strings, empty collections, malformed external data, numeric limits, and rejection paths. Include only cases relevant to the contract. Check preservation of caller-owned inputs when mutation would be a bug.
- Keep snapshots small and intentional. Inspect differences and assert important behavior directly; accepting a new snapshot is not evidence that the new behavior is correct.

## Make asynchronous assertions part of the test

- Return or await the operation and every asynchronous assertion, including `rejects`/`resolves` matchers and subtests. A test body that starts a promise chain and returns nothing can finish before its assertions run. Use the runner's promise or callback completion model consistently. See [Node's asynchronous tests](https://nodejs.org/docs/latest-v24.x/api/test.html) and [Jest's async test guidance](https://jestjs.io/docs/asynchronous).
- Distinguish synchronous throws from promise rejection; use the appropriate assertion and verify the error contract. A `catch` block containing assertions can silently miss the case where the promise unexpectedly resolves unless resolution also fails the test.
- For batching, verify returned values and ordering as well as rejection/partial-result semantics. For cancellation or replacement requests, deliberately complete the older operation after the newer one and assert that stale results do not win.
- Control completion with deferred promises, explicit events, or the project's existing fake timers. Avoid arbitrary sleeps and timeout increases as fixes for races. Await the condition being tested; do not rely on a particular machine's timing.

## Isolate clocks, mocks, and resources

- Mock at owned boundaries such as transport, clock, randomness, or storage. Keep real parsing, validation, and domain behavior under test. A test that mocks the subject's whole implementation proves little about it.
- Restore spies, replaced globals, environment variables, and timers in teardown. Clearing recorded calls and restoring an original implementation are different operations; use the installed runner's APIs deliberately. Isolate module-level caches and shared fixtures when they affect other tests.
- With fake timers, advance the relevant clock and settle the associated promise work before asserting. Follow the runner's timer semantics instead of assuming timer advancement flushes every promise. Restore real timers and clean up pending work according to the fixture's lifecycle. See [Jest timer mocks](https://jestjs.io/docs/timer-mocks).
- Close servers, sockets, subscriptions, workers, and temporary resources even when assertions fail. Concurrent tests must not race on a shared port, path, mock, or global state; isolate resources or serialize the specific conflicting suite.

## Check runtime and type contracts separately

- TypeScript annotations do not validate JSON, environment variables, or network responses. Exercise malformed runtime inputs at those boundaries alongside valid typed inputs; do not cast test fixtures to a trusted type and treat compilation as validation.
- Follow the project's type-test conventions for public type APIs. When it uses `@ts-expect-error` or type assertion helpers for negative cases, run the checker that evaluates them; a transpile-only test run cannot prove the expected type error occurred.
- Preserve the deployed module/runtime contract in tests. A DOM emulator cannot establish layout, navigation, or all native browser behavior, and a bundler-assisted test import may hide an invalid published package entry point. Use the relevant integration or browser suite for those guarantees.

## UI and integration coverage, when applicable

- Exercise interactions and accessible outcomes: roles, names, visible status, validation messages, and focus. With Testing Library, use queries matching user access and await asynchronous appearance/disappearance instead of polling private component state. See [Testing Library queries](https://testing-library.com/docs/queries/about/).
- For components and hooks, test loading, success, empty, and failure states that belong to the requirement, plus cleanup or stale-request behavior when relevant. Reuse existing providers and routing fixtures. Avoid adding React, a DOM environment, or a new UI test library to unrelated utilities.
- Match mocks to real boundary behavior: an HTTP error response differs from a transport rejection, and cancellation differs from an application failure. Use deterministic local fixtures for unit tests; exercise serialization, persistence, and critical cross-component paths through the project's integration setup.
- Use coverage reports to identify unexercised decisions, not as a substitute for useful assertions. Measure performance changes with the project's repeatable benchmark setup when relevant; avoid wall-clock speed assertions in ordinary unit tests.
