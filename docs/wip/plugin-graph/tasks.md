# plugin-graph — Tasks

> **Feature:** plugin-graph
> **Design:** [design.md](design.md) | **Implementation:** [implementation.md](implementation.md)
> **Status:** pending
> **Not Doing:** Review skill integration, committed JSON artifact, interactive visualization, diff subcommand, cross-plugin analysis, semantic prose analysis.

---

## Task 0: Validate goldmark dependency

**Status:** pending
**Size:** S
**Dependencies:** —
**Can run in parallel with:** —
**Slicing strategy:** Risk-First (validates the riskiest assumption before building on it)

> Ref: [implementation.md §Dependencies](implementation.md#dependencies)

Validate that goldmark (`github.com/yuin/goldmark`) can extract inline markdown link targets from AST nodes before committing to it as a dependency.

- [ ] Create `cmd/plugin-graph/` directory and `go` file with a spike test: parse a markdown snippet containing inline links (`[text](path.md)`), reference-style links, and non-link backtick content; walk the AST for `ast.Link` nodes; assert `Destination` fields are correct
- [ ] Verify goldmark preserves source position info (line numbers) on link nodes — needed for edge diagnostics
- [ ] If goldmark's AST is awkward for this use case, document findings and switch to regex-based extraction before proceeding
- [ ] Add `github.com/yuin/goldmark` to `go.mod` / `go.sum`

**Verify:** `go test ./cmd/plugin-graph/... -run TestGoldmarkSpike` passes and link targets + line numbers are correctly extracted.

---

## Task 1: Core graph types and builder

**Status:** pending
**Size:** S
**Dependencies:** Task 0
**Can run in parallel with:** —

> Ref: [implementation.md §Core Types](implementation.md#core-types-graphgo)

Implement the graph data model and builder in `cmd/plugin-graph/graph.go`.

- [ ] Define `NodeType` and `EdgeType` string enums with all values from design
- [ ] Define `Node` struct: `Path`, `Type`, `Name`
- [ ] Define `Edge` struct: `Source`, `Target`, `Type`, `Line`
- [ ] Define `Graph` struct with `Nodes` map and `Edges` slice
- [ ] Implement `AddNode`, `AddEdge`, `NodeByPath` methods
- [ ] Implement `OutEdges(path)` and `InEdges(path)` query methods
- [ ] Implement `Reachable(path, direction)` — BFS following out-edges, in-edges, or both; returns set of reachable node paths
- [ ] Implement node classification: given a file path relative to plugin root, return the correct `NodeType` based on the path pattern rules (skill directory with SKILL.md, `_shared/*.md`, `agents/*.md`, etc.)
- [ ] Write table-driven tests for node classification covering all 7 node types plus edge cases (files outside known directories → `content`)

**Verify:** `go test ./cmd/plugin-graph/... -run TestGraph` passes. Node classification correctly maps all path patterns. Reachable returns correct sets for a small hand-built graph.

---

## Task 2: File walker and extractors

**Status:** pending
**Size:** M
**Dependencies:** Task 1
**Can run in parallel with:** —

> Ref: [implementation.md §Extractors](implementation.md#extractors-parsego)

Implement the file walker and all six extractors in `cmd/plugin-graph/parse.go`.

- [ ] Define `ParseContext` struct: `PluginRoot`, `KnownProfiles`, `KnownPhases`, `KnownAgents`, `KnownSkills`
- [ ] Implement `ParseContext` initialization: derive `KnownProfiles` by parsing §Known profiles from `skills/_shared/profile-detection.md`, derive `KnownAgents` and `KnownSkills` from directory listings, hardcode `KnownPhases`
- [ ] Implement Extractor 1 (markdown links): goldmark AST walk for `ast.Link` nodes, resolve relative paths, filter external/anchor/non-md
- [ ] Implement Extractor 2 (symlinks): `os.Lstat` + `os.Readlink`, resolve relative target
- [ ] Implement Extractor 3 (template references): regex for `` `\$\{CLAUDE_PLUGIN_ROOT\}/([^`]+)` ``, strip prefix → relative path
- [ ] Implement Extractor 4 (parameterized navigation): regex for backtick paths with `<variable>` patterns, substitute `<plugin_root>`, expand `<name>`/`<profile>` over `KnownProfiles`, `<phase>` over `KnownPhases`, check target existence
- [ ] Implement Extractor 5 (agent delegation): regex for `subagent_type` patterns + whole-word match of `KnownAgents` in prose
- [ ] Implement Extractor 6 (skill invocation): regex for `/kk:([a-z-]+)`, match against `KnownSkills`
- [ ] Implement file walker: `filepath.WalkDir` over plugin root, skip non-`.md` files (except for symlink detection), classify each file into a node, run extractors, accumulate into `Graph`
- [ ] Write table-driven unit tests for each extractor in `parse_test.go` covering: valid cases, skip cases (external URLs, anchors, non-md for extractor 1; bare `$CLAUDE_PLUGIN_ROOT` for extractor 3; non-existent expansion targets for extractor 4; self-references for extractor 6)

**Verify:** `go test ./cmd/plugin-graph/... -run TestExtract` passes. Each extractor produces correct edges for its test cases.

---

## Task 3: Metrics computation

**Status:** pending
**Size:** S
**Dependencies:** Task 1
**Can run in parallel with:** Task 2

> Ref: [implementation.md §Metrics](implementation.md#metrics-metricsgo)

Implement metric computation in `cmd/plugin-graph/metrics.go`.

- [ ] Define `NodeMetrics` struct: `FanOut`, `FanIn`, `Depth`, `TransitiveClosureSize`
- [ ] Define `GraphMetrics` struct: `PerNode` map, `Orphans`, `BrokenEdges`, `Hotspots`, `Coupling`
- [ ] Define `SkillPair` struct for coupling output
- [ ] Implement fan-in/fan-out: single pass over edges, count per node
- [ ] Implement depth: DFS from each node with memoization; detect cycles → depth = -1 for cyclic nodes, report cycle as diagnostic
- [ ] Implement transitive closure: BFS from each node, count reachable set
- [ ] Implement coupling: for each skill-node pair, intersect forward-reachable sets; report pairs above threshold (default 3)
- [ ] Implement orphan detection: fan-in = 0 AND type is `content` or `shared`
- [ ] Implement broken edge detection: edges whose target path not in `Nodes` map
- [ ] Implement hotspot ranking: nodes sorted by fan-in descending
- [ ] Write tests in `metrics_test.go`: linear chain (depth = N), diamond (fan-in 2), star (fan-out N), isolated node (orphan), missing target (broken edge), cycle (depth -1)

**Verify:** `go test ./cmd/plugin-graph/... -run TestMetrics` passes. All metric cases produce expected values.

---

## Task 4: Output formatters

**Status:** pending
**Size:** M
**Dependencies:** Task 1, Task 3
**Can run in parallel with:** Task 2

> Ref: [implementation.md §Output](implementation.md#output-outputgo)

Implement the four output formatters in `cmd/plugin-graph/output.go`.

- [ ] Implement JSON formatter: `Report` struct containing nodes, edges, per-node metrics, global metrics. `json.MarshalIndent` for pretty output
- [ ] Implement text formatter: `text/tabwriter` table with columns Name, Fan-out, Fan-in, Depth, Transitive. Sort by transitive closure desc. Sections for orphans, broken edges, hotspots
- [ ] Implement DOT formatter: template-based. Nodes get `shape`/`fillcolor` by type. Edges get `style` by type (solid=static, dashed=template/parameterized, dotted=implicit). Subgraph clusters for skills, profiles, agents
- [ ] Implement Mermaid formatter: flowchart LR syntax. Sanitized node IDs from paths. Edge labels with type
- [ ] Create `testdata/` golden files for a small fixture graph (manually constructed in test setup) × 4 formats
- [ ] Write golden file comparison tests in `output_test.go` with `-update` flag support via `go test -update`

**Verify:** `go test ./cmd/plugin-graph/... -run TestOutput` passes. Golden files match expected output. Manual inspection: render a DOT golden file with `dot -Tpng` or paste Mermaid golden into mermaid.live.

---

## Task 5: CLI entry point and targeted mode

**Status:** pending
**Size:** S
**Dependencies:** Task 2, Task 3, Task 4
**Can run in parallel with:** —

> Ref: [implementation.md §CLI Interface](implementation.md) and [implementation.md §Targeted Mode](implementation.md#targeted-mode)

Wire everything together in `cmd/plugin-graph/main.go`.

- [ ] Implement flag parsing: `--root`, `--ref`, `--format`, `--direction`
- [ ] Implement subcommand dispatch: `graph` (default), `metrics`, `validate`
- [ ] Implement targeted mode: when positional args provided, build full graph, compute reachable set per `--direction`, filter graph to subgraph, then run the selected subcommand on the filtered result
- [ ] Implement `validate` exit code: exit 1 if broken edges or orphans found
- [ ] Add basic integration test in `main_test.go`: run `graph`, `metrics`, `validate` subcommands against a fixture and assert non-empty output / correct exit codes

**Verify:** `go run ./cmd/plugin-graph validate --root klaude-plugin/` exits cleanly against the real plugin. `go run ./cmd/plugin-graph metrics --root klaude-plugin/ --format json` produces valid JSON with all skills present.

---

## Task 6: Git worktree support

**Status:** pending
**Size:** S
**Dependencies:** Task 5
**Can run in parallel with:** —

> Ref: [implementation.md §Git Worktree](implementation.md#git-worktree-worktreego)

Implement `--ref` flag support via git worktrees in `cmd/plugin-graph/worktree.go`.

- [ ] Implement `WithWorktree(ref string, fn func(root string) error) error`: create temp dir, `git worktree add --detach`, call fn, deferred cleanup via `git worktree remove --force` + `os.RemoveAll`
- [ ] Wire into `main.go`: when `--ref` is set, wrap the build step in `WithWorktree`
- [ ] Handle error cases: invalid ref, not a git repo, worktree add failure → clear error message
- [ ] Write test in `worktree_test.go`: skip if git not available (`exec.LookPath`), create a test repo with two commits, verify worktree at older ref sees the older state, verify cleanup removes worktree

**Verify:** `go run ./cmd/plugin-graph metrics --root klaude-plugin/ --ref HEAD~1 --format text` produces output reflecting the state at the previous commit. `git worktree list` shows no leftover worktrees after the command completes.

---

## Task 7: Integration test fixture and Makefile

**Status:** pending
**Size:** S
**Dependencies:** Task 5, Task 6
**Can run in parallel with:** —

> Ref: [implementation.md §Integration Test](implementation.md#integration-test) and [implementation.md §Makefile Integration](implementation.md#makefile-integration)

Create the integration test fixture and wire up Makefile/CI.

- [ ] Create `cmd/plugin-graph/testdata/minimal-plugin/` with: 2 skills (one with symlink to shared, one referencing an agent via `${CLAUDE_PLUGIN_ROOT}`), 1 shared instruction, 1 agent, 1 profile with 1 phase and index.md, 1 intentional broken markdown link, 1 orphan `.md` file
- [ ] Write full-pipeline integration test in `main_test.go`: walk → parse → build → metrics → validate. Assert expected node count/types, edge count/types, broken edge detected, orphan detected, non-zero metrics for connected nodes
- [ ] Add `plugin-graph` target to `Makefile`: `go test ./cmd/plugin-graph/...` then `go run ./cmd/plugin-graph validate --root klaude-plugin/`
- [ ] Run `make plugin-graph` against the real `klaude-plugin/` and fix any validation findings (broken links, orphans) that surface — these are real bugs in the plugin, not test failures

**Verify:** `make plugin-graph` passes. Integration test passes. `go run ./cmd/plugin-graph metrics --root klaude-plugin/ --format text` produces a readable table with all 11 skills.

---

## Task 8: Final verification

**Status:** pending
**Size:** S
**Dependencies:** Task 7
**Can run in parallel with:** —

End-to-end verification of the complete feature.

- [ ] Run `/kk:test` — full test suite including `make plugin-graph` and `test/test-plugin-structure.sh`
- [ ] Run `/kk:document` — update any relevant docs (README mention of the new tool, CLAUDE.md if conventions change)
- [ ] Run `/kk:review-code` — review all changes for the feature
- [ ] Run `/kk:review-spec` — verify implementation matches design.md and implementation.md

**Verify:** All four skills pass without blocking findings.

---

## Dependency Graph

```
Task 0 (goldmark validation)
  │
  v
Task 1 (graph types) ──────────────────┐
  │                                     │
  ├──> Task 2 (walker + extractors)     ├──> Task 4 (output formatters)
  │                                     │
  └──> Task 3 (metrics) ───────────────┘
                                        │
         Task 2 ────────────────────────┤
                                        v
                                  Task 5 (CLI + targeted mode)
                                        │
                                        v
                                  Task 6 (worktree)
                                        │
                                        v
                                  Task 7 (integration fixture + Makefile)
                                        │
                                        v
                                  Task 8 (final verification)
```
