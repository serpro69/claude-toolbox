# Python async tests

## Use the project's async test runner

- Ensure coroutine tests are actually awaited by the existing runner. Pytest-style `async def` test functions need a compatible async plugin; a bare coroutine declaration is not proof its body ran.
- With pytest-asyncio, honor the configured mode. Strict mode handles tests marked for asyncio and async fixtures declared with `pytest_asyncio.fixture`; auto mode takes ownership of async tests and fixtures. Do not force auto mode in a project sharing async backends. See [pytest-asyncio discovery modes](https://pytest-asyncio.readthedocs.io/en/stable/concepts.html#test-discovery-modes).
- Keep AnyIO or Trio test conventions when the project uses them. Verify its installed plugin/backend configuration rather than mixing asyncio-specific decorators or loop primitives into those tests.
- `unittest.IsolatedAsyncioTestCase` manages its own loop, including when pytest collects those cases. Preserve the suite's existing runner and use its async cleanup facilities; these cases do not require a pytest async plugin. See [IsolatedAsyncioTestCase](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase) and [pytest's unittest support](https://docs.pytest.org/en/stable/how-to/unittest.html).

## Control lifecycle and scheduling

- Keep loop-bound clients, tasks, and fixtures within compatible event-loop lifetimes. With pytest-asyncio, the fixture's loop scope must be at least as broad as its caching scope; check the installed plugin version before changing scope options. See [async fixture scopes](https://pytest-asyncio.readthedocs.io/en/stable/reference/decorators/index.html).
- Coordinate concurrent tests with explicit events or controlled collaborators instead of sleeps chosen to make timing work. Bound waits so a failed synchronization condition does not hang the suite.
- Own every task created by the test: observe failures and cancel/await unfinished work during cleanup. Assert the required shutdown behavior before relying on the runner's automatic loop teardown, which can otherwise hide leaks.
- Exercise success, failure, timeout, and caller cancellation when the changed behavior depends on them. For a cancellation test, wait until the work has started, cancel it, await the resulting termination, and assert owned-resource cleanup; do not merely check that cancellation was requested.
- Cleanup that awaits can itself be cancelled. For AnyIO/Trio, follow the backend's cancellation-safe resource protocol or use a bounded shield when needed, then preserve cancellation propagation. Verify completion of cleanup, not just entry into `finally`. See [AnyIO cancellation and finalization](https://anyio.readthedocs.io/en/stable/cancellation.html#finalization).
- Match async collaborators with async fakes or `AsyncMock`, and assert they were awaited when required. Do not treat a skipped test or an unawaited-coroutine warning as a successful async assertion.
