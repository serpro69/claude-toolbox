# Contributing

Contributions are welcome! This guide covers the development workflow and conventions for working on claude-toolbox.

## Getting Started

1. Fork the repository
2. Run the test suite: `for test in test/test-*.sh; do $test; done`
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Key Workflows

| Task | Command |
|------|---------|
| Edit skills | Modify files in `klaude-plugin/`, run `make test-structure` |
| Edit profiles | Modify files in `klaude-plugin/profiles/`, run `make test-structure` |
| Regenerate Codex output | `make generate-kodex` |
| Update vendored Go content | `make vendor-profiles` |
| Run all generation + tests | `make generate-all && make test-structure` |

## Commit Conventions

Prefix commit messages with a category in parentheses:

- `(feat)` — new feature
- `(fix)` — bug fix
- `(refactor)` — code restructuring
- `(docs)` — documentation changes
- `(chore)` — maintenance, dependencies, CI
- `(test)` — test additions or fixes

## Sections

- [Architecture](architecture.md) — component overview and data flows
- [Plugin Development](plugin-development.md) — skills, commands, agents, hooks, profiles
- [Testing](testing.md) — test suites and conventions
- [ADRs](adrs.md) — architecture decision records
