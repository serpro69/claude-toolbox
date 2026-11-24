# Contributing

Thanks for your interest in contributing to Agentstakk! This guide covers everything you need: getting started, the plugin architecture, authoring conventions, common pitfalls, and the PR checklist.

## Getting Started

Fork `serpro69/agentstakk`, clone your fork and create a feature branch from `master`. If you already have a clone of claude-toolbox, run `git remote -v` and update only the remote that points to the original upstream. For example, a fork usually keeps its own `origin` and can update its `upstream` remote as follows.

```bash
git remote set-url upstream https://github.com/serpro69/agentstakk.git
```

Use `origin` in that command only for a direct clone of the upstream project. Projects created from the template have their own history and follow the [repository migration guide](../user-guide/template-sync.md).

Run the [test suites](testing.md#running-tests) from the checkout. To exercise installer changes, start with `bash test/test-kk.sh`, which uses temporary homes. To activate your checkout on your own account, see [installation modes](architecture.md#installation-modes).

## Development

See [Architecture](architecture.md) for how the components fit together and [Testing](testing.md) for test conventions. The authoritative reference for all conventions is [`AGENTS.md`](https://github.com/serpro69/agentstakk/blob/master/AGENTS.md) — this guide summarizes the most important rules for quick orientation.

### Key workflows

- **Editing skills:** Edit in `klaude-plugin/skills/`, then run `make generate-kodex` to regenerate the Codex variant.
- **Editing profiles.** Edit canonical files in `klaude-plugin/profiles/`. For vendored Go content, update the manifest and run `make vendor-profiles`. Run `make generate-kodex` to refresh the Codex copies.
- **Adding a profile:** Follow the "Adding a new profile" checklist in `AGENTS.md`.
- **Editing Codex configuration.** `.codex/config.toml` and `.codex/hooks.json` configure this repository. Machine defaults live in `kk/baseline/`. Edit agents in `klaude-plugin/agents/` and regenerate them with `make generate-kodex`. For guard changes, edit `klaude-plugin/scripts/guard/` and run `make generate-guard`.

### Commit conventions

- Use imperative mood in commit messages ("Add feature" not "Added feature")
- Keep the first line under 72 characters
- Include a blank line + body for non-trivial changes explaining the "why"

## Plugin Development

The kk plugin lives at `klaude-plugin/`. This section covers the practical rules for authoring each component. For the full specification, see [`AGENTS.md`](https://github.com/serpro69/agentstakk/blob/master/AGENTS.md).

### Skills

Each skill is a directory under `klaude-plugin/skills/<name>/` containing at minimum a `SKILL.md` entry point.

**SKILL.md structure:**

```yaml
---
name: skill-name
description: |
  Trigger-first description. Front-load the key use case.
---
# Skill Title

## Conventions
## Workflow
```

**Naming rules:**

- Imperative verbs over noun phrases: `design` not `analysis-process`.
- Family prefixes for grouped skills: `review-code`, `review-design`, `review-spec`.
- Write skill references as `/kk:review-code` in canonical content. Codex generation rewrites `/kk:` to `$kk:`.

**Description budget:** Claude Code truncates skill descriptions at 1,536 characters per entry. OpenCode's limit is 1,024. Lead with trigger keywords — truncation happens at the tail. Detailed rules, cascades, and examples belong in the SKILL.md body, not the description.

**Workflow ordering ([ADR 0004](../adr/0004-skill-workflow-ordering.md)):** Every skill MUST fully load its instructions before taking any action on its subject matter. This is the single most critical rule for skill authoring.

- "Instructions" = SKILL.md + referenced process files + shared protocols + resolved profile content.
- "Action on subject matter" = reading diff content, editing code, engaging with idea prose, running tests, producing findings.
- A narrow early scope is permitted (e.g., `git diff --stat` for filenames) to drive profile detection.
- Content-level read instructions appear exactly once in the workflow, after instruction loading.

Every skill's Workflow section must carry a mandatory-order directive at the top naming this rule by intent. The failure mode: once an LLM has diff content loaded, it has enough to pattern-match findings without methodology, and its efficiency bias favors the shortcut. The methodology becomes ceremony the agent optimizes away.

### Shared Instructions

Instructions consumed by multiple skills live at `klaude-plugin/skills/_shared/<name>.md`. Each consuming skill gets a symlink:

```bash
# In the consuming skill directory:
ln -s ../_shared/<name>.md shared-<name>.md
```

Reference in skill prose as `[shared-<name>.md](shared-<name>.md)`. The `shared-` prefix makes it obvious which files are shared vs. skill-specific. Only symlink into skills that actually reference the file.

Symlinks must stay inside the `skills/` tree — cross-boundary symlinks break under some plugin installers (see [ADR 0003](../adr/0003-plugin-root-referenced-content.md)).

### Commands

Commands live under `klaude-plugin/commands/<name>/`. For skills with standard + isolated modes:

- `default.md` — standard variant, invoked as `/kk:<name>:default`
- `isolated.md` — isolated sub-agent variant, invoked as `/kk:<name>:isolated`

### Agents

Agent definitions live at `klaude-plugin/agents/<name>.md` with frontmatter specifying `name`, `description`, and `tools` (an allowlist of tools the agent can use):

```yaml
---
name: code-reviewer
description: |
  Independent code reviewer with no authorship attachment.
tools:
  - Read
  - Grep
  - Glob
  - mcp__capy__capy_search
---
```

Agent names describe the **role** (`code-reviewer`, `design-reviewer`), not the skill that invokes them. Don't rename agent files when renaming skills.

Agents inherit the instruction-before-action rule — they must read provided checklists before analyzing subject matter, regardless of payload delivery order from the spawning skill.

### Hooks

Hook definitions in `klaude-plugin/hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Read|Edit|Write|NotebookEdit|Grep|Glob|mcp__.+__capy_(execute|execute_file|batch_execute)",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/guard/guard.sh",
            "timeout": 15,
            "onFailure": "block"
          }
        ]
      }
    ]
  }
}
```

The guard consumes the complete hook payload, allows with exit 0 (normally silently), and denies with JSON, a stderr reason and exit 2. The wrapper fails closed on missing interpreters, crashes and malformed output; the registration blocks hook failures/timeouts. See [Plugin Development › Hooks](plugin-development.md#hooks) for the contract, generator ownership and user-level `disable_selfmod` setup needed for agent edits of guard/settings files.

### Profiles

Profiles at `klaude-plugin/profiles/<name>/` provide domain-specific content to every workflow phase. See the [Profile Conventions](https://github.com/serpro69/agentstakk/blob/master/AGENTS.md#profile-conventions) section of `AGENTS.md` for the full specification.

**Required files:**

- `DETECTION.md` — three mandatory section headings: `## Path signals`, `## Filename signals`, `## Content signals`. All three must be present even if the body is empty. Optional: `## Design signals` for pre-code detection.
- `overview.md` — human-readable summary and dependency-lookup targets.

**Phase subdirectories:** `review-code/`, `design/`, `implement/`, `test/`, `document/`, `review-spec/`. Not every profile populates every phase. Each populated phase must have an `index.md` with always-load and conditional entries. Conditional entries need explicit `Load if:` clauses naming concrete diff properties — two agents evaluating the same diff must reach the same conclusion.

**Bidirectional index invariant** (enforced by `test/test-plugin-structure.sh`):

- Forward: every markdown link in `index.md` resolves to a file on disk.
- Reverse: every `.md` in the phase directory (except `index.md`) is referenced by the index.

An unreferenced `.md` inside a phase subdirectory is always a bug. Authoring notes belong in `overview.md` at the profile root, not inside phase subdirectories.

**Adding a new profile checklist:**

1. Create the profile directory by copying an existing one as a template.
2. Write `DETECTION.md` and `overview.md`.
3. Populate the phase subdirectories the profile needs (each with `index.md`).
4. Append the profile name to `EXPECTED_PROFILES` in `test/test-plugin-structure.sh`.
5. Append the profile name to the Known Profiles list in `klaude-plugin/skills/_shared/profile-detection.md`.
6. Run `bash test/test-plugin-structure.sh` and confirm green.

### Evaluations

Skills with non-trivial decision logic should ship evaluation scenarios under `klaude-plugin/skills/<skill>/evals/`. One directory per eval:

```
evals/<eval-name>/
  eval.json        # scenario definition
  test-files/      # real filesystem fixtures
```

`eval.json` schema:

```json
{
  "id": 1,
  "name": "eval-name-kebab-case",
  "description": "What this eval tests.",
  "skills": ["skill-name"],
  "prompt": "The user prompt that triggers the skill.",
  "trap": "The failure hypothesis — what a model is likely to get wrong.",
  "files": ["test-files/foo.yaml"],
  "assertions": [{ "id": "1.1", "text": "Specific, gradable behavior." }]
}
```

Use real filesystem fixtures in `test-files/`, not inline JSON strings. Include at least one regression eval proving the skill does NOT activate when it shouldn't.

## `${CLAUDE_PLUGIN_ROOT}` — Substitution Rules

The harness provides `${CLAUDE_PLUGIN_ROOT}` resolving to the installed plugin's root. Understanding its substitution boundary is critical ([ADR 0003](../adr/0003-plugin-root-referenced-content.md)):

**Substituted at plugin-load time** (safe to use `${CLAUDE_PLUGIN_ROOT}/...` freely):

- `SKILL.md` files
- `agents/*.md` files
- `hooks/*.json` command strings
- MCP config files

**NOT substituted by the `Read` tool** (the literal token reaches the agent):

- Everything in `skills/_shared/`
- Everything in `profiles/`
- Any file an agent reads at runtime

For runtime-read files, prefer explicit content (e.g., hard-coded profile name lists) over the token. If the file must describe a plugin-root path, instruct the agent to construct it using the resolved prefix it already knows from SKILL.md.

**Other rules:**

- Brace form required: `${CLAUDE_PLUGIN_ROOT}` works, bare `$CLAUDE_PLUGIN_ROOT` does NOT get substituted.
- `Glob` won't work against these paths — it's cwd-scoped and returns 0 matches for outside-cwd absolute paths. Use `Read` with the resolved path instead.
- To reference the variable name literally in prose, use bare `$CLAUDE_PLUGIN_ROOT` or `&#36;{CLAUDE_PLUGIN_ROOT}`.

## Capy Knowledge Protocol

Skills that interact with capy MCP tools use `kk:` namespaced source labels:

| Label                    | Contents                                      |
| ------------------------ | --------------------------------------------- |
| `kk:arch-decisions`      | Architecture decisions, design rationale      |
| `kk:review-findings`     | Code review patterns, recurring issues        |
| `kk:lang-idioms`         | Language best practices from external sources |
| `kk:project-conventions` | Discovered project patterns                   |
| `kk:test-patterns`       | Testing approaches, edge cases                |
| `kk:debug-context`       | Root causes, tricky bugs                      |

Only index non-obvious learnings not derivable from reading the code or git history. Empty results are normal for new projects — proceed with standard guidelines.

## Common Pitfalls

1. **Workflow ordering is the #1 failure mode.** If the agent sees subject matter before methodology, it shortcuts the methodology. Structure every workflow so instructions load first. See [ADR 0004](../adr/0004-skill-workflow-ordering.md).

2. **Stale generated files.** Run `make generate-kodex` after editing canonical skills, profiles or agents. CI checks tracked and untracked changes under `kodex-plugin/` and `kk/baseline/codex/agents/`. Guard changes use `make generate-guard`.

3. **Orphan files in profile phase directories.** Every `.md` file (except `index.md`) must be referenced by the phase's `index.md`. The bidirectional invariant test catches this.

4. **Symlinks outside `skills/`.** Per-skill symlinks must point within the `skills/` tree (`../_shared/<name>.md`). Cross-boundary symlinks break under some installers. Profile content uses `${CLAUDE_PLUGIN_ROOT}` references instead.

5. **Skill description truncation.** Descriptions are truncated from the tail. If your trigger keywords are at the end, the skill won't be matched. Lead with the use case.

6. **Stale Known Profiles list.** When adding a profile, you must update both `EXPECTED_PROFILES` in the test file and the Known Profiles list in `klaude-plugin/skills/_shared/profile-detection.md`. The list is the runtime enumeration — consumers iterate it rather than walking the filesystem.

7. **Renaming skills.** Update `EXPECTED_SKILLS` / `EXPECTED_COMMANDS` in tests. Don't rename agent files. Don't touch `docs/feat/done/` (frozen history). Watch for substring collisions in sed operations.

8. **Vague `Load if:` clauses.** Conditional entries in profile `index.md` must name concrete diff properties (field values, filenames, directory names) — not vague category labels. Two agents evaluating the same diff must reach the same conclusion.

## Pull Requests

- One logical change per PR
- All test suites must pass: `for test in test/test-*.sh; do $test; done`
- Regenerate the affected artifacts and include them in the PR. CI runs `make check-guard` and verifies Codex generation in a clean checkout. [Release checks](testing.md#validation-before-release)
- Update documentation if your change affects user-facing behavior

## Architecture Decisions

Non-trivial design decisions are recorded as ADRs in `docs/adr/` using [Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (Context, Decision, Consequences). Per-feature design docs live at `docs/feat/wip/<feature>/` while work is active and move to `docs/feat/done/<feature>/` on completion.

| ADR                                                   | Decision                                                  |
| ----------------------------------------------------- | --------------------------------------------------------- |
| [0001](../adr/0001-profile-detection-model.md)        | Single additive detection axis for all profile types      |
| [0002](../adr/0002-profile-content-organization.md)   | Profile-first layout with index-driven content loading    |
| [0003](../adr/0003-plugin-root-referenced-content.md) | Plugin-root references instead of cross-boundary symlinks |
| [0004](../adr/0004-skill-workflow-ordering.md)        | Instructions before action in every skill workflow        |
| [0005](../adr/0005-codex-hook-enforcement-gap.md)     | Two-layer hook + advisory enforcement for Codex (superseded by 0013) |
| [0013](../adr/0013-codex-file-access-through-hooked-tools.md) | Codex file access is guarded through hooked tools |

## Documentation Site

The docs site uses MkDocs Material with mike for versioned publishing.

**Local preview:**

```bash
make docs-serve    # serves at http://localhost:8000
```

**Build without serving:**

```bash
make docs-build
```

**How publishing works:**

- Push to `master` → deploys as `dev` via mike (unreleased docs)
- Push tag `v0.14.0` → deploys as `0.14` (major.minor) and updates the `latest` alias to point to it
- The bare URL always redirects to `latest` (most recent release)
- GitHub Actions workflow at `.github/workflows/docs.yml` handles both
- Mike pushes to the `gh-pages` branch; GitHub Pages serves from there
- First deploy requires enabling GitHub Pages on the `gh-pages` branch in repo Settings

**Site content.** Published pages live in `docs/`, including the ADRs in `docs/adr/`. `mkdocs.yml` excludes internal feature and review records from the site build. Their source remains available in the repository. The landing page uses `docs/overrides/home.html`.

**Python deps:** Install via `pip install -r requirements.txt` (mkdocs-material, mike, minify, panzoom).

## Repository Structure

```
klaude-plugin/                   # kk plugin — Claude (canonical source of truth)
├── .claude-plugin/plugin.json   # Plugin manifest
├── skills/                      # Workflow and utility skills
├── commands/                    # Claude Code slash commands
├── agents/                      # Sub-agents (code-reviewer, spec-reviewer, design-reviewer, ...)
├── profiles/                    # Per-domain content (languages, IaC DSLs)
├── hooks/hooks.json             # Plugin-root export + permission guard registration
└── scripts/guard/              # Canonical engine, wrapper, declaration and license

kodex-plugin/                    # kk plugin — Codex (GENERATED from klaude-plugin/)
├── .codex-plugin/plugin.json    # Generated plugin manifest
├── skills/                      # Generated skills (transformed SKILL.md files)
└── profiles/                    # Per-domain content (languages, IaC DSLs)

.claude-plugin/marketplace.json  # Claude marketplace catalog
.agents/plugins/marketplace.json # Codex marketplace catalog

CLAUDE.md                        # Claude project instructions (this repo)
AGENTS.md                        # Codex project instructions (this repo)

.claude/                          # Repository preferences, Capy setup and sync compatibility notice
.codex/                           # Repository sandbox, approvals and Capy registrations
install.sh                        # Bootstrap a machine installation
kk/lib/                           # Installation, launchers, upgrades, rollback and migration
kk/baseline/                      # Machine defaults, generated policies and Codex agents
kodex-guard/                      # Standalone Codex guard plugin
.github/                          # Release helpers and workflows for CI, releases and docs

docs/                            # MkDocs site + internal design docs
├── overrides/                   # Template overrides (home.html, main.html)
├── assets/                      # CSS (tokyonight.css, extra.css), JS
├── getting-started/             # Setup guides
├── user-guide/                  # Skills, profiles, MCP, config, sync
├── providers/                   # Claude Code and Codex specifics
├── contributing/                # architecture.md, testing.md, plugin dev
├── about/                       # License, changelog
├── adr/                         # Architecture decision records
└── feat/                        # Feature design docs (excluded from search)
    ├── archive/                 # Feature docs that weren't worked on, but were preserved for discovery purposes
    ├── done/                    # Completed features
    ├── reviews/                 # Reviews reports for features and standalone issues
    └── wip/                     # In-progress features

mkdocs.yml                       # MkDocs Material config
requirements.txt                 # Python deps for docs site

cmd/
├── plugin-graph/                # Plugin dependency graph and validation
├── vendor-profiles/             # Profile vendoring tool
└── generate-kodex/              # Codex plugin generation tool

test/
├── helpers.sh                   # Shared test utilities and assertions
├── test-*.sh                    # Shell test suites
└── fixtures/                    # Test manifests and templates
```

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
