# Python — test guidance

Consumed by `$kk:test` when `.py` or `.pyi` files activate the Python profile. Load both core files and any matching conditional guidance before running checks. The validator protocol selects the project's existing tools and checks their availability in the chosen environment.

Resolve the conditional using planned tests and bounded signal inspection of in-scope Python files and their relevant tests. Include unchanged enclosing declarations. Comments, docstrings, string literals, an installed package alone, and unrelated files do not satisfy code signals.

## Always load

- [testing.md](testing.md) — Behavioral coverage, isolation, fixtures, mocks, and meaningful assertions.
- [validators.md](validators.md) — Project-aware runner selection, environment checks, configured validators, and accurate result reporting.

## Conditional

- [async.md](async.md) — Async test execution, fixture lifetimes, cancellation, and cleanup assertions. **Load if:** in-scope `.py` or `.pyi` files or their relevant tests contain, or the planned tests introduce, `async def`, `await`, `async for`, or `async with`; imports of `asyncio`, `anyio`, `trio`, or `pytest_asyncio` via `import` or `from` (including submodules and aliases); or `IsolatedAsyncioTestCase` or `AsyncMock` imports/usages. Also load when the applicable pytest configuration explicitly sets `asyncio_mode` or `anyio_mode`, or relevant tests use `pytest.mark.asyncio`, `pytest.mark.anyio`, or `pytest.mark.trio` (including imported aliases).
