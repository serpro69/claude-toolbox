# Python type contracts

## Describe the behavior callers can rely on

- Follow the project's annotation policy; annotate new or changed public boundaries and non-obvious return shapes. Avoid unrelated annotation churn.
- Accept the narrowest required capability: `Iterable` for one pass, `Sequence` for indexing, or `Mapping` for read access. These interfaces do not guarantee that the underlying object is immutable.
- Model absence explicitly. An optional argument with a default is not necessarily nullable; include `None` only when the contract allows it.
- Use a small `Protocol` when consumers need structural behavior, and a `TypedDict` for a known dictionary shape. Add abstractions only when they clarify a real boundary.
- Prefer narrowing uncertain values to spreading `Any`. Keep casts or type-checker suppressions local and explain why the value is safe.

Annotations, `TypedDict`, and `cast()` do not validate external data at runtime. Parse and validate at the boundary before trusting a typed value. See [Python typing](https://docs.python.org/3/library/typing.html).

## Preserve compatibility and runtime behavior

- Choose annotation syntax and typing APIs supported by the project's Python versions and configured checker. A new typing convenience does not justify raising the runtime floor or adding a backport dependency by default.
- Before moving an import under `TYPE_CHECKING` or changing annotation evaluation, check whether the application inspects annotations at runtime. Frameworks and serializers may need those names to resolve.
- For `.pyi` changes, preserve the stub's imports, exported names, defaults, overloads, and sync/async shape. Match an available implementation; when it is absent, state that limitation rather than inventing runtime behavior. Validate with the existing checker when available.
