# Python — implementation guidance

Consumed by `$kk:implement` before writing `.py` or `.pyi` files. Load the core guidance for every Python task, then resolve the conditional entry before editing.

For conditional loading, use the task's planned constructs and bounded inspection of its target files (including unchanged enclosing declarations), plus any diff so far. A new file can qualify from the task requirements alone. Comments, docstrings, string literals, dependency metadata, and unrelated files do not satisfy code signals.

## Always load

- [idioms.md](idioms.md) — Project compatibility, module boundaries, mutability, and collection semantics.
- [typing.md](typing.md) — Useful type contracts, runtime validation boundaries, and stub consistency.
- [errors-and-resources.md](errors-and-resources.md) — Exception propagation, resource ownership, and predictable cleanup.

## Conditional

- [async.md](async.md) — Event-loop safety, task ownership, cancellation, and bounded concurrency. **Load if:** a target `.py` or `.pyi` file contains, or the planned edits introduce, an `async def`, `await`, `async for`, or `async with` construct, or imports `asyncio`, `anyio`, or `trio` via an `import` or `from` statement (including submodules and aliases).
