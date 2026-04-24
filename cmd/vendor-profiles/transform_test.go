package main

import (
	"strings"
	"testing"
)

func TestTransformAll_Passthrough(t *testing.T) {
	input := []byte("some content\nwith multiple lines\n")
	got := TransformAll(input)
	if string(got) != string(input) {
		t.Errorf("TransformAll modified content: got %q", got)
	}
}

func TestTransformAll_EmptyContent(t *testing.T) {
	got := TransformAll([]byte{})
	if len(got) != 0 {
		t.Errorf("TransformAll on empty input returned %q", got)
	}
}

func TestTransformFromFirstH1_WithFrontmatterAndPersona(t *testing.T) {
	input := []byte(`---
description: A Go security skill
---

You are a Go security expert reviewing code for vulnerabilities.

# Go Security Checklist

## Injection Prevention

Always use parameterized queries.

## Cryptography

Use crypto/rand, not math/rand.
`)
	got, err := TransformFromFirstH1(input)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.HasPrefix(result, "# Go Security Checklist") {
		t.Errorf("expected output to start with H1, got: %q", result[:min(60, len(result))])
	}
	if strings.HasPrefix(result, "---\n") {
		t.Error("output still contains frontmatter delimiters")
	}
	if strings.Contains(result, "You are a Go security expert") {
		t.Error("output still contains persona declaration")
	}
	if !strings.Contains(result, "## Injection Prevention") {
		t.Error("output missing expected H2 section")
	}
	if !strings.Contains(result, "## Cryptography") {
		t.Error("output missing expected H2 section")
	}
}

func TestTransformFromFirstH1_NoH1Error(t *testing.T) {
	input := []byte(`---
description: no heading file
---

## Only H2 headings here

Some content.
`)
	_, err := TransformFromFirstH1(input)
	if err == nil {
		t.Fatal("expected error for content without H1, got nil")
	}
	if !strings.Contains(err.Error(), "no H1 heading found") {
		t.Errorf("error = %q, want containing %q", err, "no H1 heading found")
	}
}

func TestTransformFromFirstH1_EmptyContentError(t *testing.T) {
	_, err := TransformFromFirstH1([]byte{})
	if err == nil {
		t.Fatal("expected error for empty content, got nil")
	}
	if !strings.Contains(err.Error(), "empty content") {
		t.Errorf("error = %q, want containing %q", err, "empty content")
	}
}

func TestTransformFromFirstH1_WhitespaceOnlyError(t *testing.T) {
	_, err := TransformFromFirstH1([]byte("   \n\n  \t\n"))
	if err == nil {
		t.Fatal("expected error for whitespace-only content, got nil")
	}
	if !strings.Contains(err.Error(), "empty content") {
		t.Errorf("error = %q, want containing %q", err, "empty content")
	}
}

func TestTransformFromFirstH1_H1OnFirstLine(t *testing.T) {
	input := []byte("# Heading\n\nContent here.\n")
	got, err := TransformFromFirstH1(input)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if string(got) != string(input) {
		t.Errorf("expected full content returned when H1 is first line, got %q", got)
	}
}

func TestTransformHeadings_SingleH2(t *testing.T) {
	input := []byte(`# Main Title

## Section A

Content of section A.

## Section B

Content of section B.
`)
	got, err := TransformHeadings(input, []string{"## Section A"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.Contains(result, "## Section A") {
		t.Error("output missing requested heading")
	}
	if !strings.Contains(result, "Content of section A.") {
		t.Error("output missing section content")
	}
	if strings.Contains(result, "## Section B") {
		t.Error("output contains non-requested section")
	}
	if strings.Contains(result, "# Main Title") {
		t.Error("output contains H1 title")
	}
}

func TestTransformHeadings_MultipleH2s(t *testing.T) {
	input := []byte(`# Title

## Alpha

Alpha content.

## Beta

Beta content.

## Gamma

Gamma content.
`)
	got, err := TransformHeadings(input, []string{"## Alpha", "## Gamma"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.Contains(result, "## Alpha") {
		t.Error("missing Alpha heading")
	}
	if !strings.Contains(result, "Alpha content.") {
		t.Error("missing Alpha content")
	}
	if !strings.Contains(result, "## Gamma") {
		t.Error("missing Gamma heading")
	}
	if !strings.Contains(result, "Gamma content.") {
		t.Error("missing Gamma content")
	}
	if strings.Contains(result, "## Beta") {
		t.Error("output contains non-requested Beta section")
	}
}

func TestTransformHeadings_NestedH3Included(t *testing.T) {
	input := []byte(`# Title

## Injection Prevention

Overview of injection types.

### SQL Injection

Always use parameterized queries.

### Command Injection

Never pass user input to exec.

## Next Section

Other content.
`)
	got, err := TransformHeadings(input, []string{"## Injection Prevention"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.Contains(result, "### SQL Injection") {
		t.Error("output missing nested H3 'SQL Injection'")
	}
	if !strings.Contains(result, "### Command Injection") {
		t.Error("output missing nested H3 'Command Injection'")
	}
	if !strings.Contains(result, "Always use parameterized queries.") {
		t.Error("output missing nested content")
	}
	if strings.Contains(result, "## Next Section") {
		t.Error("output contains content past the H2 boundary")
	}
}

func TestTransformHeadings_HeadingNotFound(t *testing.T) {
	input := []byte(`# Title

## Existing Section

Content.
`)
	_, err := TransformHeadings(input, []string{"## Nonexistent Section"})
	if err == nil {
		t.Fatal("expected error for missing heading, got nil")
	}
	if !strings.Contains(err.Error(), "heading not found") {
		t.Errorf("error = %q, want containing %q", err, "heading not found")
	}
	if !strings.Contains(err.Error(), "Nonexistent Section") {
		t.Errorf("error should name the missing heading, got %q", err)
	}
}

func TestTransformHeadings_LastSectionCapturedToEOF(t *testing.T) {
	input := []byte(`# Title

## Only Section

Content goes all the way to the end.
More content here.
`)
	got, err := TransformHeadings(input, []string{"## Only Section"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.Contains(result, "More content here.") {
		t.Error("last section should capture to EOF")
	}
}

func TestApplyTransform_DispatchAll(t *testing.T) {
	input := []byte("content")
	got, err := ApplyTransform(input, "all")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if string(got) != "content" {
		t.Errorf("got %q, want %q", got, "content")
	}
}

func TestApplyTransform_DispatchFromFirstH1(t *testing.T) {
	input := []byte("preamble\n# Title\nbody\n")
	got, err := ApplyTransform(input, "from_first_h1")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.HasPrefix(string(got), "# Title") {
		t.Errorf("expected output starting with H1, got %q", got)
	}
}

func TestApplyTransform_DispatchHeadings(t *testing.T) {
	input := []byte("# Title\n\n## Target\n\nContent.\n\n## Other\n\nSkipped.\n")
	keep := map[string]any{"headings": []any{"## Target"}}
	got, err := ApplyTransform(input, keep)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	result := string(got)
	if !strings.Contains(result, "## Target") {
		t.Error("missing target heading")
	}
	if strings.Contains(result, "## Other") {
		t.Error("contains non-requested heading")
	}
}

func TestApplyTransform_UnknownKeepMode(t *testing.T) {
	_, err := ApplyTransform([]byte("content"), "bogus")
	if err == nil {
		t.Fatal("expected error for unknown keep mode, got nil")
	}
	if !strings.Contains(err.Error(), "unknown keep mode") {
		t.Errorf("error = %q, want containing %q", err, "unknown keep mode")
	}
}

func TestApplyTransform_UnsupportedType(t *testing.T) {
	_, err := ApplyTransform([]byte("content"), 42)
	if err == nil {
		t.Fatal("expected error for unsupported keep type, got nil")
	}
	if !strings.Contains(err.Error(), "unsupported keep type") {
		t.Errorf("error = %q, want containing %q", err, "unsupported keep type")
	}
}

func TestApplyTransform_HeadingsMissingKey(t *testing.T) {
	keep := map[string]any{"not_headings": []any{"## Foo"}}
	_, err := ApplyTransform([]byte("content"), keep)
	if err == nil {
		t.Fatal("expected error for missing headings key, got nil")
	}
	if !strings.Contains(err.Error(), "missing 'headings' key") {
		t.Errorf("error = %q, want containing %q", err, "missing 'headings' key")
	}
}

func TestApplyTransform_HeadingsNotAList(t *testing.T) {
	keep := map[string]any{"headings": "not a list"}
	_, err := ApplyTransform([]byte("content"), keep)
	if err == nil {
		t.Fatal("expected error for non-list headings, got nil")
	}
	if !strings.Contains(err.Error(), "must be a list of strings") {
		t.Errorf("error = %q, want containing %q", err, "must be a list of strings")
	}
}

func TestApplyTransform_HeadingsNonStringElement(t *testing.T) {
	keep := map[string]any{"headings": []any{"## Valid", 42}}
	_, err := ApplyTransform([]byte("content"), keep)
	if err == nil {
		t.Fatal("expected error for non-string heading element, got nil")
	}
	if !strings.Contains(err.Error(), "heading must be a string") {
		t.Errorf("error = %q, want containing %q", err, "heading must be a string")
	}
}
