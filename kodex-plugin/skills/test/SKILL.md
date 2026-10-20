---
name: test
description: |
  Guidelines describing how to test the code.
  Use whenever writing new or updating existing code, for example after implementing a new feature or fixing a bug.
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Testing & Quality Assurance Process

## Conventions

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Read verification policy** at [shared-verification-policy.md](shared-verification-policy.md).
- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When an active profile contributes a `test/` subdirectory (e.g., `../../profiles/k8s/test/`), its `index.md` lists validators, check categories, and any binary-presence or auto-detection protocols the skill must apply. See Step 2 of the Workflow.

## Workflow

**Mandatory order — instructions before action.** The flow below is strictly sequential. Load this skill and its shared protocols, then complete profile detection and load all resolved profile content before investigating subject files or running validators/tests. Only bounded inspection to resolve a declared routing predicate may precede profile loading.

1. **Detect active profiles.** Run the `shared-profile-detection.md` procedure against the changed files.
2. **Load profile content.** For each active profile that contributes a `test/` subdirectory, load `../../profiles/<name>/test/index.md` and read its always-load + any matching conditional content. Honor the binary-presence protocols named there BEFORE any validator invocation — a missing pre-check step can crash on a tool that isn't installed.
3. **Apply the test guidelines below.** With instructions loaded, inspect the affected behavior, select proportionate checks and execute applicable profile validators.

## Guidelines

1. Cover intended behavior, affected contracts and consequential boundaries. Reuse existing coverage; add a regression test when it would meaningfully detect recurrence.
2. Investigate failing tests against the requirement and implementation. Correct a flawed test explicitly; never relax a valid assertion just to obtain a pass.
3. Start with relevant checks and honor explicit repository/release requirements. Broaden or repeat only when changed shared behavior, failures or unresolved risks justify it; apply the loaded verification policy to agent evaluations.
4. **Profile-aware validators.** Apply the validators and check categories the active profile's `test/index.md` specifies (loaded in Step 2 of the Workflow); honor the binary-presence protocol documented there — missing binaries should surface install hints, not shell errors.

**Capy search:** Before applying test guidelines, search `kk:test-patterns` for project-specific testing approaches and known edge cases.

Choose techniques that answer the actual verification question; this is not a required checklist:

- Use table-/data-driven tests and test generation
- Benchmark tests and performance regression detection
- Integration testing with test containers
- Mock generation with %LANGUAGE% best practices and well-establised %LANGUAGE% mocking tools
- Property-based testing with %LANGUAGE% best practices and well-establised %LANGUAGE% testing tools
- Propose end-to-end testing strategies if automated e2e testing is not feasible
- Code coverage analysis and reporting

**Capy index:** If a novel testing approach or tricky edge case was discovered during this session, index it as `kk:test-patterns`.
