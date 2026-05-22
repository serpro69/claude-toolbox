# plugin-graph — Implementation Plan

> Design: [design.md](design.md) | Tasks: [tasks.md](tasks.md)

## Project Structure

```
cmd/plugin-graph/
  main.go              — CLI entry point, flag parsing, subcommand dispatch
  graph.go             — Graph/Node/Edge types, graph builder
  parse.go             — File walker + six extractors
  parse_test.go        — Extractor unit tests (table-driven, one section per extractor)
  metrics.go           — Metric computation over the graph
  metrics_test.go      — Metric calculation tests
  output.go            — JSON/text/DOT/Mermaid formatters
  output_test.go       — Output format tests (golden file comparisons)
  worktree.go          — Git worktree create/cleanup for --ref
  worktree_test.go     — Worktree lifecycle tests
  main_test.go         — Integration test: full pipeline against fixture directory
  testdata/
    minimal-plugin/    — Fixture mimicking minimal klaude-plugin/ structure
```

Follows the flat `package main` pattern used by `cmd/generate-kodex/` and `cmd/vendor-profiles/`.

## Dependencies

- **`gopkg.in/yaml.v3`** — already in `go.mod`.
- **Goldmark** (`github.com/yuin/goldmark`) — markdown parser for reliable link extraction. Needs validation in Task 0 that it can extract inline link targets (`[text](path.md)`) from AST nodes. Fallback: regex-based extraction if goldmark's AST is awkward for this use case.
- No other new dependencies expected. Symlinks, file walking, regex, JSON encoding, and text formatting are all stdlib.

## Implementation Details

### Core Types (`graph.go`)

**`NodeType`** — string enum: `skill`, `shared`, `agent`, `profile`, `profile-phase`, `content`, `command`.

**`EdgeType`** — string enum: `markdown-link`, `symlink`, `template-ref`, `parameterized-nav`, `agent-delegation`, `skill-invocation`.

**`Node`** — `Path` (relative to plugin root, unique ID), `Type`, `Name` (human label derived from path).

**`Edge`** — `Source` (path), `Target` (path), `Type`, `Line` (source line number for diagnostics).

**`Graph`** — `Nodes` map (path → Node), `Edges` slice. Methods: `AddNode`, `AddEdge`, `NodeByPath`, `OutEdges(path)`, `InEdges(path)`, `Reachable(path, direction)`.

The graph builder walks the plugin root, classifies each file/directory into a node type based on its location in the tree, then runs the extractors on each `.md` file to discover edges.

#### Node Classification Rules

| Path pattern | Node type |
|-------------|-----------|
| `skills/<name>/SKILL.md` present → directory is a `skill` | `skill` |
| `skills/_shared/*.md` | `shared` |
| `agents/*.md` | `agent` |
| `profiles/<name>/` (directory with `DETECTION.md`) | `profile` |
| `profiles/<name>/<phase>/` (directory with `index.md`) | `profile-phase` |
| `commands/<name>/` | `command` |
| Everything else `.md` | `content` |

### Extractors (`parse.go`)

Each extractor is a standalone function: `func(filePath string, content []byte, ctx *ParseContext) []Edge`.

`ParseContext` carries shared state the extractors need:
- `PluginRoot` — absolute path to the plugin directory being analyzed
- `KnownProfiles` — list of profile names (parsed from `skills/_shared/profile-detection.md` §Known profiles at startup)
- `KnownPhases` — `[]string{"review-code", "review-spec", "design", "implement", "test", "document"}`
- `KnownAgents` — list of agent names (derived from `agents/` directory listing at startup)
- `KnownSkills` — list of skill names (derived from `skills/` directory listing at startup)

**Extractor 1 — Markdown links:** Parse with goldmark, walk AST for `ast.Link` nodes, extract `Destination`. Resolve relative paths against the file's directory. Filter: skip external URLs (`://`), anchor-only (`#...`), non-`.md` targets. Each surviving link → `markdown-link` edge with line number from AST position.

**Extractor 2 — Symlinks:** Called before content extraction. `os.Lstat(path)` → if `ModeSymlink`, `os.Readlink(path)` → resolve target relative to symlink's directory → `symlink` edge. Note: the resolved file's content is still processed by other extractors (the walker follows symlinks for content but records the symlink edge separately).

**Extractor 3 — Template references:** Regex: `` `\$\{CLAUDE_PLUGIN_ROOT\}/([^`]+)` ``. Capture group 1 is the relative path. Create `template-ref` edge. Line number from byte offset.

**Extractor 4 — Parameterized navigation:** Regex: backtick-quoted paths containing `<...>` variables. Match pattern: `` `[^`]*<(plugin_root|name|phase|profile|checklist)>[^`]*` ``. For each match:
1. Replace `<plugin_root>` with empty string (paths are already relative).
2. Identify remaining variables. Expand `<name>` and `<profile>` over `KnownProfiles`, `<phase>` over `KnownPhases`.
3. For each concrete expansion, check if the target exists on disk. If yes → `parameterized-nav` edge.
4. `<checklist>` requires special handling: expand over the files listed in the profile-phase's `index.md` (if the profile-phase is part of the expansion context).

**Extractor 5 — Agent delegation:** Two patterns:
1. Regex for `subagent_type.*kk:([a-z-]+)` → maps to `agents/<name>.md`.
2. Regex for known agent names in prose: scan for each `KnownAgents` entry as a whole word. Create `agent-delegation` edge.

**Extractor 6 — Skill invocation:** Regex: `/kk:([a-z-]+)` not inside a backtick code span that's defining the current skill's own name. Match against `KnownSkills`. Create `skill-invocation` edge.

### Metrics (`metrics.go`)

**`NodeMetrics`** struct: `FanOut`, `FanIn`, `Depth`, `TransitiveClosureSize` (all `int`).

**`GraphMetrics`** struct: `PerNode` map (path → NodeMetrics), `Orphans` ([]path), `BrokenEdges` ([]Edge), `Hotspots` ([]path sorted by fan-in desc), `Coupling` ([]SkillPair with shared dep count).

Computation:
- Fan-in/fan-out: single pass over edges, count per node.
- Depth: DFS from each node, memoized. Cycle detection → report cycle as a diagnostic, depth = -1 for nodes in a cycle.
- Transitive closure: BFS from each node, count reachable set size.
- Coupling: for each pair of `skill` nodes, intersect their forward-reachable sets. Only report pairs with intersection > threshold (default 3).
- Orphans: nodes where fan-in = 0 AND type is `content` or `shared` (skills, agents, profiles, commands are root-level entry points and aren't expected to have incoming edges from other files in all cases).
- Broken edges: edges whose target path doesn't resolve to a file on disk.

### Output (`output.go`)

Four formatter functions, each taking `*Graph` and `*GraphMetrics` and returning `[]byte`.

**JSON:** Direct marshal of a `Report` struct containing nodes, edges, per-node metrics, and global metrics. Pretty-printed with `json.MarshalIndent`.

**Text:** Table formatted with `text/tabwriter`. Header row, one row per skill node sorted by transitive closure size descending. Columns: Name, Fan-out, Fan-in, Depth, Transitive. Followed by sections for orphans, broken edges, hotspots.

**DOT:** Template-based. Nodes get `shape` and `fillcolor` by type. Edges get `style` by type (solid for static, dashed for template/parameterized, dotted for implicit). Subgraph clusters for skills, profiles, agents.

**Mermaid:** Same visual semantics as DOT, rendered as Mermaid flowchart LR syntax. Node IDs are sanitized paths. Edge labels show type.

### Targeted Mode

When positional args are provided:
1. Build the full graph normally.
2. Parse each arg as a path relative to plugin root.
3. Based on `--direction`: compute forward-reachable set (BFS following out-edges), reverse-reachable set (BFS following in-edges), or union of both.
4. Filter graph to only include nodes in the reachable set and edges between them.
5. Compute metrics on the filtered subgraph.

### Git Worktree (`worktree.go`)

```go
func WithWorktree(ref string, fn func(root string) error) error
```

1. Create temp directory via `os.MkdirTemp`.
2. Run `git worktree add --detach <tempdir> <ref>`.
3. Call `fn(tempdir)`.
4. Deferred: `git worktree remove --force <tempdir>` then `os.RemoveAll(tempdir)`.

Error handling: if `git worktree add` fails (invalid ref, not a git repo), return a clear error message. The `--force` on remove handles the case where the worktree has uncommitted changes (shouldn't happen since we're read-only, but defensive).

### Makefile Integration

```makefile
plugin-graph:
	go test ./cmd/plugin-graph/...
	go run ./cmd/plugin-graph validate
```

The `validate` subcommand provides a natural CI hook — broken links and orphans fail the build.

## Testing Strategy

### Unit Tests

**Extractor tests (`parse_test.go`):** Table-driven. Each extractor gets its own test function with cases like:

- Markdown links: inline link, reference link, external URL (skipped), anchor-only (skipped), non-md target (skipped)
- Symlinks: valid symlink, broken symlink
- Template refs: `${CLAUDE_PLUGIN_ROOT}/...` path, bare `$CLAUDE_PLUGIN_ROOT` (skipped — no braces)
- Parameterized nav: single variable, multiple variables, non-existent expansion target (skipped)
- Agent delegation: `subagent_type` reference, prose mention of agent name
- Skill invocation: `/kk:name` reference, self-reference (skipped)

**Metrics tests (`metrics_test.go`):** Construct small graphs programmatically, assert computed metrics. Cases: linear chain (depth), diamond (fan-in/out), isolated node (orphan), missing target (broken edge), cycle (cycle detection).

**Output tests (`output_test.go`):** Golden file comparisons. A fixture graph → each format → compare against `testdata/*.golden`. Update with `-update` flag.

### Integration Test

**`main_test.go`:** Uses `testdata/minimal-plugin/` — a stripped-down plugin structure with:
- 2 skills (one with symlink to shared, one referencing an agent)
- 1 shared instruction
- 1 agent
- 1 profile with 1 phase
- 1 intentional broken link
- 1 orphan file

Runs the full pipeline: walk → parse → build graph → compute metrics → validate. Asserts:
- Expected node count and types
- Expected edge count and types
- Broken edge detected
- Orphan detected
- Metrics are non-zero for connected nodes

### Worktree Test

**`worktree_test.go`:** Tests `WithWorktree` lifecycle. Skipped in environments without git (`testing.Short()` or git-not-found check). Asserts temp directory is created, callback receives valid path, cleanup removes worktree.

## Assumptions

1. **Goldmark can reliably extract markdown link targets.** Validated in Task 0.
2. **Three link categories cover all dependency edges.** Static, template, and parameterized. Variable vocabulary is small and expansion sets are finite.
3. **`git worktree` is available** in CI and local dev.
4. **The graph fits in memory.** Dozens of nodes.
5. **JSON output is sufficient for programmatic consumers.**

## Not Doing

- **Review skill integration** — Follow-up work after the CLI exists.
- **Committed JSON artifact / CI freshness checks** — Easy to layer later.
- **Interactive visualization** — DOT/Mermaid rendered externally.
- **Diff/comparison subcommand** — Users diff JSON from two `--ref` runs.
- **Cross-plugin analysis** — Only `klaude-plugin/`.
- **Semantic analysis of prose** — Only backtick-quoted path patterns.
