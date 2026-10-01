# Python profile

## What this profile covers

Idiomatic Python source code and stubs: type hints and `typing` usage, mutability and aliasing, context managers, exception hygiene, packaging boundaries, async idioms, testing/mocking pitfalls, and SOLID principles adapted to Python's duck-typed model. Implementation and test guidance respect the consumer project's supported Python versions and existing tools.

## When it activates

Any file with a `.py` or `.pyi` extension in scope. See [DETECTION.md](DETECTION.md) for the authoritative rule. Activation is additive with other profiles on the same diff.

## Populated phases

- [implement/](implement/index.md) — guidance consumed by `$kk:implement` before edits: project compatibility and idioms, type contracts, exceptions, and resource ownership. Async guidance loads only for concrete async constructs or async-runtime imports in target files or planned edits; the index defines the exact conditions.
- `review-code/` — checklists consumed by `$kk:review-code` (security, SOLID, code-quality, removal-plan).
- [test/](test/index.md) — guidance consumed by `$kk:test`: behavioral coverage, fixtures and mocks, project-aware runner/validator selection, environment availability, and accurate result reporting. Async testing guidance loads for the concrete code or configuration signals defined in the index.

Other phase subdirectories are not populated for this profile; those phases use generic guidance. Neither implementation nor testing prescribes a package manager, linter, type checker, framework, or new minimum Python version. Test commands use the existing environment; missing tools and zero-test runs are reported without claiming complete verification.

## Looking up Python dependencies

When adding or upgrading a dependency, follow the `$kk:dependency-handling` skill's cascade:

1. **capy-first** — query the project's indexed `kk:lang-idioms` / `kk:project-conventions` / prior context7 fetches.
2. **context7** — fetch current docs for the package; most mainstream PyPI packages are indexed there.
3. **web** — fall back to [pypi.org](https://pypi.org), the project's own repository README, or [readthedocs.io](https://readthedocs.io) mirrors only if the first two yield nothing.

Project dependency metadata lives in `pyproject.toml`, `requirements.txt`, or `poetry.lock` / `pdm.lock`. Version-specific behaviors must be verified against the version the project resolves to, not the latest available.
