# Python idioms and project compatibility

## Establish the project's constraints

- Check declared Python support (`requires-python`, existing packaging configuration, and CI environments) before choosing syntax or standard-library APIs. The interpreter installed locally does not establish the project's minimum version. If these sources disagree, surface the discrepancy before relying on the newer version.
- Follow the existing package layout, environment manager, formatter, linter, and test commands. Adding this profile does not require adopting a particular tool or migrating configuration.
- Keep new syntax and imports compatible with supported runtimes. Check the versioned documentation when availability is uncertain; apply `$kk:dependency-handling` for added or changed dependencies.

## Keep boundaries simple

- Use small functions for transformations and classes when state or a lifecycle requires them. Prefer composition and explicit collaborators over inheritance introduced solely for reuse.
- Keep network calls, filesystem writes, process launches, and application startup out of module import paths. Put command-line execution behind an entry point or `if __name__ == "__main__":` guard.
- Respect existing public names and call signatures. Do not restructure a package or introduce an abstraction framework to make a local change.
- Validate external data at the boundary using the project's existing approach. Do not execute or unpickle untrusted data, interpolate values into SQL, or build shell commands from untrusted strings.

## Make ownership and absence explicit

- Allocate mutable function defaults per call when callers should have independent state. Use a sentinel when `None` is itself a meaningful input. Python evaluates defaults once when defining the function. See [default argument values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values).
- For dataclass fields, use `field(default_factory=...)` for independent mutable values. `frozen=True` prevents field assignment; it does not make nested lists or dictionaries immutable. See [dataclasses](https://docs.python.org/3/library/dataclasses.html).
- Decide whether a function mutates caller-owned input or returns a new value, and preserve that contract. A shallow copy still shares nested objects; copy only as deeply as the ownership contract requires.
- Distinguish missing values from valid falsey values: use `is None` when zero, an empty collection, or `False` is valid. Use `==` for value equality and `is` for identity checks.

## Preserve collection semantics

- Use comprehensions for readable transformations and ordinary loops when control flow or side effects dominate.
- Treat iterators as consumable. If multiple passes are needed, require a reusable collection or deliberately materialize a bounded input.
- Stream large inputs where possible; avoid unbounded lists, caches, or queues. Preserve ordering and duplicate semantics when changing a collection type.
- When creating callbacks in a loop, bind each iteration's value deliberately instead of accidentally sharing the loop variable.
