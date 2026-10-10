# Python test design

## Assert observable behavior

- Follow the project's existing pytest, unittest, or framework-specific style. Keep names, layout, and parametrization consistent with neighboring tests.
- Test the contract that changed: returned values, public effects, exception types, and ownership of mutable inputs. Do not reproduce the implementation's calculation as the expected result or assert private call sequences without a behavioral reason.
- For a bug fix, add the smallest regression that fails for the original defect and passes with the correction. Verify both outcomes when practical. Respect a verification-only request: report gaps without changing source or tests.
- Choose boundary cases that can alter behavior: absent versus falsey values, empty inputs, invalid data, repeated calls with mutable defaults, iterator exhaustion, and partial failure. Use named parametrized cases or subtests where they clarify the contract.
- Assert the specific expected exception and relevant context. An unrelated exception must not satisfy a test intended to prove input validation or cleanup.

## Keep state and resources isolated

- Each test should be independently runnable. Restore patched environment variables, working directories, globals, caches, and clocks; do not depend on execution order.
- Prefer temporary paths and controlled collaborators to real user files, live services, wall-clock timing, or nondeterministic random values. Exercise real integration boundaries through the project's established fixtures when that is the behavior under test.
- Give mutable fixtures the narrowest useful lifetime. Shared session/module fixtures must not leak state between tests.
- Register cleanup as acquisition succeeds. A pytest yield fixture that fails before reaching `yield` cannot run the teardown after that yield; use smaller fixtures or appropriate cleanup registration for partial setup. See [pytest fixture teardown](https://docs.pytest.org/en/stable/how-to/fixtures.html#safe-teardowns).
- Verify resources are released on failures as well as on success. Assertions should distinguish an empty successful result from an error that was swallowed.

## Use mocks at boundaries

- Patch the name where the code under test looks it up. Prefer a small fake or a mock constrained to the collaborator's interface; use autospeccing where it helps expose invalid calls.
- Keep the behavior under test real. Mock network/time/process boundaries rather than replacing the function whose result the test claims to verify.
- Match synchronous and asynchronous protocols. Calling an `AsyncMock` and awaiting it are separate events; use awaited-call assertions when the contract requires awaiting. See [unittest.mock](https://docs.python.org/3/library/unittest.mock.html).

## Match verification to the requirement

- Use existing property-based tools for meaningful invariants and existing benchmark tooling for performance claims. Do not add a test framework, benchmark dependency, or a fragile wall-clock threshold to every change.
- Preserve the project's coverage configuration and thresholds. Coverage indicates execution, not correctness; useful assertions and failure paths matter more than a percentage alone.
- For stubs and annotation changes, verify public typing contracts with the configured checker and, when available, relevant runtime tests. Syntax parsing alone does not establish stub/runtime consistency.
