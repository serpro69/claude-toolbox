# plugin-graph — Design

## Problem Statement

How might we give plugin maintainers, contributors, and AI assistants visibility into the dependency web between skills, shared instructions, profiles, and agents — so they can assess impact before making changes, catch broken links before they ship, and objectively measure skill complexity?

The klaude-plugin has a rich link taxonomy (markdown links, symlinks, `${CLAUDE_PLUGIN_ROOT}` template references, parameterized navigation instructions, implicit agent delegations, skill invocations) but no unified view of it. Impact analysis is manual, and complexity is felt but not measured.

## Target Users

1. **Plugin maintainer** — needs impact analysis, validation, and complexity visibility across the skill web.
2. **Contributors** — need to understand the dependency structure before making changes.
3. **AI assistants** — skills like `/kk:review-code` and `/kk:review-design` need programmatic access to complexity data to flag "this skill has unusually high coupling" with evidence.

## Success Metric

Quantified complexity metrics (fan-in/out, depth, coupling, transitive closure) are available to review skills and humans, with data-backed findings. Validation and impact analysis are supporting capabilities.

## Design

### Graph Model

A directed graph where nodes represent plugin artifacts and edges represent dependency relationships.

#### Node Types

Each node has a `type` discriminator and a `path` (relative to `klaude-plugin/`) as its unique identifier.

| Type | Description | Example |
|------|-------------|---------|
| `skill` | Skill directory containing `SKILL.md` | `skills/review-code/` |
| `shared` | File under `skills/_shared/` | `skills/_shared/profile-detection.md` |
| `agent` | Agent definition under `agents/` | `agents/code-reviewer.md` |
| `profile` | Profile directory under `profiles/` | `profiles/go/` |
| `profile-phase` | Phase subdirectory within a profile | `profiles/go/review-code/` |
| `content` | Any other `.md` file (process files, checklists, indexes, evals) | `skills/review-code/review-process.md` |
| `command` | Command directory under `commands/` | `commands/chain-of-verification/` |

#### Edge Types

Edges fall into three categories based on how they're discovered.

**Static edges** — directly parseable from the filesystem:

| Type | Source | Discovery |
|------|--------|-----------|
| `markdown-link` | `[text](target.md)` in file content | Markdown parser or regex |
| `symlink` | Filesystem symlink | `os.Readlink` |

**Template edges** — require variable substitution:

| Type | Source | Discovery |
|------|--------|-----------|
| `template-ref` | `` `${CLAUDE_PLUGIN_ROOT}/concrete/path` `` in prose | Regex + prefix substitution |

**Parameterized edges** — require variable expansion over known sets:

| Type | Source | Discovery |
|------|--------|-----------|
| `parameterized-nav` | Backtick-quoted paths with `<name>`, `<phase>` etc. | Regex + expansion over Known Profiles / phases |
| `agent-delegation` | Skill references sub-agent type name | Match against `agents/` directory listing |
| `skill-invocation` | `/kk:<name>` in prose | Regex + match against `skills/` directory listing |

Each edge records: `source` (path), `target` (path), `type`, and `line` number.

### Link Parsing Pipeline

Files are processed in a single pass. Six extractors run in sequence, each independent and composable. Signature: `func(path string, content []byte) []RawEdge`.

**Extractor 1 — Markdown links:** Uses goldmark (or regex fallback) to find `[text](target.md)`. Resolves relative targets against the file's directory. Ignores external URLs, anchor-only refs, and non-`.md` targets.

**Extractor 2 — Symlinks:** `os.Lstat` before reading content. If symlink, `os.Readlink` captures target. Creates `symlink` edge. The resolved file is also processed for its own outgoing links.

**Extractor 3 — Template references:** Regex for backtick-delimited `${CLAUDE_PLUGIN_ROOT}/...` paths (brace form). Strips the prefix, remainder is a concrete relative path → `template-ref` edge.

**Extractor 4 — Parameterized navigation:** Regex for backtick-quoted paths containing angle-bracket variables (`<plugin_root>`, `<name>`, `<phase>`, `<profile>`, `<checklist>`). Substitutes `<plugin_root>` → empty. Expands `<name>`/`<profile>` over the Known Profiles list (8 profiles) and `<phase>` over the six known phase names. Each expansion becomes a `parameterized-nav` edge — only if the target exists on disk.

**Extractor 5 — Agent delegation:** Regex for `subagent_type` references and prose mentions of known agent names (matched against `agents/` listing). Creates `agent-delegation` edges.

**Extractor 6 — Skill invocation:** Regex for `/kk:<name>` patterns. Maps to `skills/<name>/` directories. Creates `skill-invocation` edges.

### Metrics

#### Per-Node Metrics

| Metric | Definition | Signal |
|--------|-----------|--------|
| Fan-out | Out-degree (direct dependencies) | High = pulls in many files |
| Fan-in | In-degree (direct dependents) | High = high-impact change target |
| Depth | Longest dependency chain to a leaf | Deep = many instruction layers |
| Transitive closure | Total reachable nodes | "True weight" of a skill |

#### Global Metrics

| Metric | Definition | Signal |
|--------|-----------|--------|
| Orphans | Nodes with zero fan-in | Potential dead content |
| Broken edges | Edges whose target doesn't exist on disk | Build-breaking errors |
| Hotspots | Nodes ranked by fan-in | Highest-impact change targets |
| Coupling | Shared dependency count between skill pairs | Over-sharing between unrelated skills |

### CLI Interface

Lives at `cmd/plugin-graph/`. Single binary, subcommand-based.

```
plugin-graph [flags] [subcommand] [target...]
```

#### Subcommands

- `graph` — emit the dependency graph in the chosen format (default subcommand)
- `metrics` — compute and emit complexity metrics
- `validate` — check for broken edges and orphans; exit code 1 if any found

#### Flags

- `--root <path>` — plugin root directory (default: `klaude-plugin/`)
- `--ref <git-ref>` — build graph from a git ref via temporary worktree (default: working tree)
- `--format json|text|dot|mermaid` — output format (default: `text`)
- `--direction forward|reverse|both` — for targeted mode: follow outgoing deps, incoming deps, or both (default: `forward`)

#### Targeted Mode

When positional arguments are provided, the tool builds the full graph internally but filters output to the subgraph reachable from those starting nodes. Multiple targets are unioned.

```
plugin-graph metrics skills/review-code/SKILL.md
plugin-graph graph --direction both skills/_shared/profile-detection.md
```

#### Git Ref Support

When `--ref` is provided:
1. `git worktree add --detach <tempdir> <ref>`
2. Effective root becomes `<tempdir>/klaude-plugin/`
3. Run normally
4. `git worktree remove <tempdir>` on cleanup (deferred)

### Output Formats

- **`json`** — full graph + metrics as structured JSON. Nodes array, edges array, per-node metrics, global metrics. The canonical programmatic output.
- **`text`** — human-readable summary table. Per-skill metrics sorted by transitive closure size. Warnings for orphans/broken edges.
- **`dot`** — GraphViz DOT format. Nodes colored by type, edges styled by type.
- **`mermaid`** — Mermaid flowchart syntax. Same visual semantics as DOT.

## Assumptions

1. **Goldmark (or equivalent) can reliably extract markdown link targets.** Will be validated as a prerequisite task before implementation.
2. **Three link categories cover all dependency edges.** Static (markdown links, symlinks), template paths (`${CLAUDE_PLUGIN_ROOT}/...` with concrete suffixes), and parameterized navigation instructions (backtick-quoted paths with variables expanding over known sets). The variable vocabulary is small and the expansion sets are finite (8 profiles, 6 phases).
3. **`git worktree` is available** in environments where the tool runs (CI, local dev).
4. **The graph fits in memory.** ~11 skills, 5 agents, 8 profiles, ~4 shared instructions — dozens of nodes, not thousands.
5. **JSON output is sufficient for programmatic consumers.**

## Not Doing

- **Review skill integration** — Teaching `/kk:review-code` or `/kk:review-design` to invoke the tool and interpret results. The CLI needs to exist first; integration is follow-up work.
- **Committed JSON artifact / CI freshness checks** — A `make plugin-graph` target that generates and checks in a JSON artifact. Easy to layer later, orthogonal to the CLI.
- **Interactive visualization** — No web UI, no `--serve` mode. DOT/Mermaid output can be rendered by external tools.
- **Diff/comparison subcommand** — Users can diff JSON output from two `--ref` runs themselves. A dedicated `diff` subcommand is future work.
- **Cross-plugin analysis** — Only `klaude-plugin/` is in scope. Analyzing `kodex-plugin/` or downstream consumer plugins is out of scope.
- **Semantic analysis of prose** — The tool parses backtick-quoted path patterns, not free-text descriptions of what files to read.
