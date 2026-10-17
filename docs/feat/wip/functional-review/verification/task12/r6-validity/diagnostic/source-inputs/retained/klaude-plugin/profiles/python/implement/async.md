# Python async implementation

## Preserve the runtime's execution model

- Follow the existing async backend and lifecycle. Do not mix asyncio-specific primitives into Trio code or introduce another runtime for a local change.
- Keep blocking I/O and long CPU work off the event-loop thread. Use an async API already supported by the project or its established executor boundary. A synchronous helper called from `async def` still runs on that thread.
- Avoid nested event-loop runners in a running loop. Await work from async callers and leave loop ownership to the application or framework.
- Async synchronization primitives are not general thread synchronization. Check thread ownership when callbacks or executors share state. See [developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html).

## Own tasks, failures, and cancellation

- Every started task needs an owner that awaits completion, observes failure, and handles shutdown. Keep references to intentionally backgrounded tasks and define their cleanup.
- For related asyncio tasks, prefer `TaskGroup` when the supported Python floor is at least 3.11. On older versions, use the existing supervision pattern and explicitly handle sibling cancellation and awaiting; do not raise the runtime floor to use a newer API.
- Let cancellation propagate after cleanup. `try/finally` and `async with` arrange cleanup, but neither makes awaited cleanup immune to cancellation. Do not swallow the backend's cancellation exception or convert it to a successful return.
- For AnyIO/Trio level cancellation, use established cancellation-safe cleanup. If required cleanup awaits can be interrupted in a cancelled scope, protect them with a backend-native shield bounded by a cleanup deadline, then propagate the original cancellation. Merely entering `__aexit__` does not shield it. See [AnyIO finalization](https://anyio.readthedocs.io/en/stable/cancellation.html#finalization) and [Trio cancellation](https://trio.readthedocs.io/en/stable/reference-core.html#cancellation-and-timeouts).
- Bound fan-out and queues. A semaphore around I/O does not bound the number of task objects if every input is scheduled up front.
- Apply a finite timeout or deadline to external work. Check the chosen API's cancellation behavior: a timeout or cancellation of an await does not guarantee that work offloaded to a thread has stopped.

See [asyncio tasks and cancellation](https://docs.python.org/3/library/asyncio-task.html) for task-group availability, lifecycle, and timeout semantics.

## Verify lifecycle behavior

- Exercise success, a child failure, timeout, and caller cancellation where relevant. Check that failures remain visible and owned resources are released.
- Use the repository's existing async test support. Avoid sleeps as coordination; use explicit events or controlled collaborators to make lifecycle assertions deterministic.
