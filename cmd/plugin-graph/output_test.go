package main

import (
	"flag"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// update regenerates the golden files instead of comparing against them:
//
//	go test ./cmd/plugin-graph/... -run TestOutput -update
var update = flag.Bool("update", false, "update golden files")

// buildFixtureGraph constructs a small graph exercising every node type and
// every edge type, plus an orphan and a broken edge. It also materializes the
// edge targets that must resolve on disk in a temp dir, returning that root so
// ComputeMetrics's broken-edge detection sees exactly one missing target
// (skills/beta/missing.md).
func buildFixtureGraph(t *testing.T) (*Graph, string) {
	t.Helper()

	g := NewGraph()
	nodes := []*Node{
		{Path: "skills/alpha/", Type: NodeSkill, Name: "alpha"},
		{Path: "skills/beta/", Type: NodeSkill, Name: "beta"},
		{Path: "skills/_shared/common.md", Type: NodeShared, Name: "common.md"},
		{Path: "skills/_shared/unused.md", Type: NodeShared, Name: "unused.md"},
		{Path: "agents/reviewer.md", Type: NodeAgent, Name: "reviewer.md"},
		{Path: "profiles/go/", Type: NodeProfile, Name: "go"},
		{Path: "profiles/go/review-code/", Type: NodeProfilePhase, Name: "review-code"},
		{Path: "commands/alpha/", Type: NodeCommand, Name: "alpha"},
		{Path: "docs/guide.md", Type: NodeContent, Name: "guide.md"},
		{Path: "README.md", Type: NodeContent, Name: "README.md"},
	}
	for _, n := range nodes {
		g.AddNode(n)
	}

	// AddEdge normalizes raw endpoints against the nodes added above.
	edges := []Edge{
		{RawSource: "skills/alpha/SKILL.md", RawTarget: "skills/_shared/common.md", Type: EdgeMarkdownLink, Line: 10},
		{RawSource: "skills/beta/shared-common.md", RawTarget: "skills/_shared/common.md", Type: EdgeSymlink, Line: 0},
		{RawSource: "skills/alpha/SKILL.md", RawTarget: "profiles/go/overview.md", Type: EdgeTemplateRef, Line: 20},
		{RawSource: "skills/beta/SKILL.md", RawTarget: "profiles/go/review-code/index.md", Type: EdgeParameterizedNav, Line: 30},
		{RawSource: "skills/alpha/SKILL.md", RawTarget: "agents/reviewer.md", Type: EdgeAgentDelegation, Line: 40},
		{RawSource: "skills/alpha/SKILL.md", RawTarget: "skills/beta/", Type: EdgeSkillInvocation, Line: 50},
		{RawSource: "skills/alpha/SKILL.md", RawTarget: "commands/alpha/isolated.md", Type: EdgeSkillInvocation, Line: 60},
		{RawSource: "skills/beta/SKILL.md", RawTarget: "skills/beta/missing.md", Type: EdgeMarkdownLink, Line: 12},
	}
	for _, e := range edges {
		g.AddEdge(e)
	}

	// Every non-broken edge target must exist on disk so broken-edge detection
	// flags only skills/beta/missing.md.
	root := t.TempDir()
	files := []string{
		"skills/_shared/common.md",
		"profiles/go/overview.md",
		"profiles/go/review-code/index.md",
		"agents/reviewer.md",
		"commands/alpha/isolated.md",
	}
	for _, f := range files {
		writeFixtureFile(t, root, f)
	}
	// skills/beta/ is a skill-invocation target stat'd as a directory.
	if err := os.MkdirAll(filepath.Join(root, "skills/beta"), 0o755); err != nil {
		t.Fatal(err)
	}

	return g, root
}

func writeFixtureFile(t *testing.T, root, rel string) {
	t.Helper()
	full := filepath.Join(root, rel)
	if err := os.MkdirAll(filepath.Dir(full), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(full, nil, 0o644); err != nil {
		t.Fatal(err)
	}
}

func TestOutput(t *testing.T) {
	g, root := buildFixtureGraph(t)
	// Threshold 1 so the alpha/beta pair (2 shared deps) surfaces in coupling.
	m, _ := ComputeMetrics(g, root, 1)
	diagnostics := []string{"example diagnostic: sample warning"}

	cases := []struct {
		format string
		golden string
	}{
		{"json", "fixture.json.golden"},
		{"text", "fixture.text.golden"},
		{"dot", "fixture.dot.golden"},
		{"mermaid", "fixture.mermaid.golden"},
	}

	for _, tc := range cases {
		t.Run(tc.format, func(t *testing.T) {
			got, err := Render(tc.format, g, m, diagnostics)
			if err != nil {
				t.Fatalf("Render(%q): %v", tc.format, err)
			}

			goldenPath := filepath.Join("testdata", tc.golden)
			if *update {
				if err := os.MkdirAll("testdata", 0o755); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(goldenPath, got, 0o644); err != nil {
					t.Fatal(err)
				}
				return
			}

			want, err := os.ReadFile(goldenPath)
			if err != nil {
				t.Fatalf("read golden (run with -update to create): %v", err)
			}
			if string(got) != string(want) {
				t.Errorf("%s output mismatch (run with -update to regenerate)\n--- got ---\n%s\n--- want ---\n%s",
					tc.format, got, want)
			}
		})
	}
}

func TestRenderUnknownFormat(t *testing.T) {
	g, root := buildFixtureGraph(t)
	m, _ := ComputeMetrics(g, root, 1)

	if _, err := Render("yaml", g, m, nil); err == nil {
		t.Error("Render with unknown format = nil error, want error")
	}
}

// TestMermaidIDDistinctForColludingPaths covers the collision-disambiguation
// branch of uniqueMermaidID: two distinct paths that sanitize to the same base
// id must still produce distinct Mermaid ids.
func TestMermaidIDDistinctForColludingPaths(t *testing.T) {
	g := NewGraph()
	// "a/b.md" and "a-b.md" both sanitize to "a_b_md".
	g.AddNode(&Node{Path: "a/b.md", Type: NodeContent, Name: "b.md"})
	g.AddNode(&Node{Path: "a-b.md", Type: NodeContent, Name: "a-b.md"})

	out := string(renderMermaid(g, &GraphMetrics{}, nil))

	if !strings.Contains(out, "a_b_md[") || !strings.Contains(out, "a_b_md_2[") {
		t.Errorf("expected disambiguated ids a_b_md and a_b_md_2 in output:\n%s", out)
	}
}

// TestGraphEdgesSkipsDanglingTarget covers the node-existence filter in
// graphEdges: an edge whose normalized target is not a declared node (e.g. a
// cross-artifact broken link) must not appear in the visual formats.
func TestGraphEdgesSkipsDanglingTarget(t *testing.T) {
	g := NewGraph()
	g.AddNode(&Node{Path: "skills/alpha/", Type: NodeSkill, Name: "alpha"})
	// Target docs/nowhere.md is never added as a node.
	g.AddEdge(Edge{RawSource: "skills/alpha/SKILL.md", RawTarget: "docs/nowhere.md", Type: EdgeMarkdownLink})

	if got := graphEdges(g); len(got) != 0 {
		t.Errorf("graphEdges = %v, want empty (dangling target filtered)", got)
	}
}

// TestGraphEdgesDedupesNormalizedDuplicates covers the dedup branch: two raw
// edges from different files within the same skill to the same shared target
// normalize to one (Source, Target, Type) and must collapse to a single visual
// edge, so the artifact-level graph does not double-count the dependency.
func TestGraphEdgesDedupesNormalizedDuplicates(t *testing.T) {
	g := NewGraph()
	g.AddNode(&Node{Path: "skills/alpha/", Type: NodeSkill, Name: "alpha"})
	g.AddNode(&Node{Path: "skills/_shared/common.md", Type: NodeShared, Name: "common.md"})
	g.AddEdge(Edge{RawSource: "skills/alpha/SKILL.md", RawTarget: "skills/_shared/common.md", Type: EdgeMarkdownLink, Line: 1})
	g.AddEdge(Edge{RawSource: "skills/alpha/process.md", RawTarget: "skills/_shared/common.md", Type: EdgeMarkdownLink, Line: 9})

	got := graphEdges(g)
	if len(got) != 1 {
		t.Fatalf("graphEdges = %d edges, want 1 (normalized duplicates collapsed)", len(got))
	}
	if got[0].Source != "skills/alpha/" || got[0].Target != "skills/_shared/common.md" {
		t.Errorf("edge = %s -> %s, want skills/alpha/ -> skills/_shared/common.md", got[0].Source, got[0].Target)
	}
}

// TestEscapingAdversarialPaths verifies DOT and Mermaid escape the characters
// that are structurally significant in each format when they appear in a
// path-derived label. These characters cannot occur in the current plugin
// corpus (so the golden fixtures stay clean), but will be reachable once Task 6
// analyzes untrusted git-ref roots — escaping must happen in the formatter.
func TestEscapingAdversarialPaths(t *testing.T) {
	g := NewGraph()
	g.AddNode(&Node{Path: `skills/a"b/`, Type: NodeSkill, Name: `a"b`})
	g.AddNode(&Node{Path: "docs/c#d|e.md", Type: NodeContent, Name: "c#d|e.md"})
	g.AddEdge(Edge{RawSource: `skills/a"b/SKILL.md`, RawTarget: "docs/c#d|e.md", Type: EdgeMarkdownLink})

	dot, err := renderDOT(g, &GraphMetrics{}, nil)
	if err != nil {
		t.Fatalf("renderDOT: %v", err)
	}
	// strconv.Quote escapes the embedded double-quote as \" — valid DOT.
	if !strings.Contains(string(dot), `"skills/a\"b/"`) {
		t.Errorf("DOT did not escape embedded quote in node id:\n%s", dot)
	}

	mer := string(renderMermaid(g, &GraphMetrics{}, nil))
	if strings.Contains(mer, `["skills/a"b/"]`) {
		t.Errorf("Mermaid emitted an unescaped quote in a label:\n%s", mer)
	}
	for _, want := range []string{"#quot;", "#35;", "#124;"} {
		if !strings.Contains(mer, want) {
			t.Errorf("Mermaid label missing entity escape %q:\n%s", want, mer)
		}
	}
}
