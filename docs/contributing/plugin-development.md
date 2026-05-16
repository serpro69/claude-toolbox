# Plugin Development

The kk plugin lives in `klaude-plugin/` and is the canonical source of truth. This guide covers how to add and modify skills, commands, agents, hooks, and profiles.

## Skills

Skills live in `klaude-plugin/skills/<name>/` with a required `SKILL.md` file and optional supporting files.

### SKILL.md Structure

```
klaude-plugin/skills/<skill-name>/
  SKILL.md          # Main skill definition (required)
  shared-*.md       # Symlinks to _shared/ instructions
  evals/            # Evaluation scenarios (optional)
```

### Naming Conventions

- **Imperative verbs over noun phrases**: `design` not `analysis-process`
- **Self-documenting over acronyms**: `chain-of-verification` beats `cove`
- **Family prefixes for grouped skills**: `review-design`, `review-spec`, `review-code`

### Description Budget

Skill descriptions are truncated at **1,536 characters** per entry. Lead with trigger keywords — truncation happens at the tail.

## Commands

Commands live under `klaude-plugin/commands/<name>/`:

- `default.md` — standard variant, invoked as `/kk:<name>:default`
- `isolated.md` — isolated sub-agent variant, invoked as `/kk:<name>:isolated`

## Agents

Agent definitions in `klaude-plugin/agents/*.md`. Names describe the **role** (`code-reviewer`, `design-reviewer`), not the skill that invokes them.

## Hooks

Hooks are defined in `klaude-plugin/hooks/hooks.json`. Each hook specifies a `PreToolUse` or `PostToolUse` event and runs a script from `klaude-plugin/hooks/scripts/`.

## Profiles

See [Profiles](../user-guide/profiles.md) for what profiles provide. To add a new profile:

1. Copy an existing profile: `cp -r klaude-plugin/profiles/go klaude-plugin/profiles/<name>`
2. Rewrite `DETECTION.md` with the new profile's signals
3. Rewrite `overview.md` with what the profile covers
4. Populate phase subdirectories (`review-code/`, `design/`, `implement/`, `test/`, `document/`)
5. Each phase needs an `index.md` listing its content files
6. Add the profile name to `EXPECTED_PROFILES` in `test/test-plugin-structure.sh`
7. Add to the Known profiles list in `klaude-plugin/skills/_shared/profile-detection.md`
8. Run `bash test/test-plugin-structure.sh`

### Bidirectional Index Invariant

Every phase `index.md` must satisfy:

- **Forward**: every markdown link resolves to a file on disk
- **Reverse**: every `.md` file in the directory (except `index.md`) is referenced by a link

This is enforced by the structure tests.

## Shared Instructions

Instructions used by multiple skills live in `klaude-plugin/skills/_shared/<name>.md`. Each consuming skill gets a symlink:

```bash
ln -s ../_shared/<name>.md klaude-plugin/skills/<skill>/shared-<name>.md
```

## Vendored Content

Some profiles vendor from external repos via `cmd/vendor-profiles/`. Edit the manifest at `scripts/<profile>-vendor-manifest.yml`, then run `make vendor-profiles`.
