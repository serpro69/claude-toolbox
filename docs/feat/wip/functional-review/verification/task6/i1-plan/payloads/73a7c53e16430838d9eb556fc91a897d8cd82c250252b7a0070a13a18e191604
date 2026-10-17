# Python errors and resource ownership

## Preserve failures callers need to handle

- Catch the specific exception where recovery, translation, or reporting is possible. Let other failures propagate; fallible operations do not each need their own `try/except`.
- Keep the protected block narrow so a handler does not accidentally catch an unrelated failure. Use bare `raise` to rethrow; use `raise DomainError(...) from exc` when translating while preserving the cause.
- Do not turn failures into empty values or apparent success unless the API explicitly defines that fallback. Broad exception handling belongs at deliberate boundaries with a defined outcome; avoid swallowing `BaseException`, which includes termination signals.
- Use explicit exceptions for input and security validation. Assertions may be disabled and are appropriate only for internal invariants.
- Avoid returning or transferring control from `finally`: that can hide a pending failure or replace a result. See [errors and exceptions](https://docs.python.org/3/tutorial/errors.html).

## Give each resource an owner

- Use `with` for supported resource protocols; use `try/finally` when cleanup is manual. Register cleanup as soon as acquisition succeeds, including when later acquisition can fail. `ExitStack` helps with a variable number of resources.
- Close resources this function owns. For borrowed files, clients, and connections, follow the caller's ownership contract instead of closing them unexpectedly.
- Verify what a context manager actually does. A database transaction context may commit or roll back without closing its connection. Do not assume every `with` block releases every associated resource.
- For generator-based context managers, put cleanup in `finally` around the yield and propagate exceptions unless suppression is intentional. See [contextlib](https://docs.python.org/3/library/contextlib.html).

## Make operational failure understandable

- Add useful operation context without exposing credentials or sensitive payloads. Log at the boundary responsible for handling the failure; avoid duplicate stack traces at every layer.
- Bound external calls with the project's timeout policy. Retry only classified transient failures when repeating the operation is safe, with a finite attempt or time budget.
- Verify cleanup on both success and failure, and verify that the caller can distinguish failure from an empty successful result.
