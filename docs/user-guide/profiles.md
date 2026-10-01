# Profiles

The kk plugin ships per-domain profiles that make every workflow skill language-aware. Profiles provide:

- **Review checklists** — language-specific code review items
- **Implementation gotchas** — common pitfalls and idioms
- **Design prompts** — architecture patterns relevant to the language
- **Test validators** — testing conventions and frameworks
- **Documentation rubrics** — what to document and how

## Supported Profiles

| Profile | Covers | Detection |
|---------|--------|-----------|
| **Go** | Go modules, packages, concurrency patterns | `*.go`, `go.mod`, `go.sum` |
| **Java** | Maven/Gradle projects, Spring, JVM patterns | `*.java`, `pom.xml`, `build.gradle` |
| **JS/TS** | Node.js, TypeScript, React, frontend tooling | `*.ts`, `*.tsx`, `*.js`, `package.json` |
| **Kotlin** | Kotlin/JVM, Android, Gradle | `*.kt`, `*.kts`, `build.gradle.kts` |
| **Kubernetes** | Helm charts, Kustomize, YAML manifests | `Chart.yaml`, `kustomization.yaml`, K8s resource kinds |
| **K8s Operator** | kubebuilder, operator-sdk, controller-runtime | `PROJECT`, `config/crd/`, `controller-gen` in Makefile |
| **Python** | Python implementation, testing, and review guidance | `*.py`, `*.pyi` |
| **Skill MD** | Agent skill authoring (Claude Code, Codex) | `SKILL.md`, files under a `SKILL.md`-rooted ancestor |

<!-- TODO: Reconcile the other language rows and detection examples below with their DETECTION.md files. Several metadata filenames are listed as triggers despite extension-only detection. This broader documentation audit is outside the Python implementation-phase addition. -->

## How Detection Works

Profiles activate automatically based on the files in your diff or working directory. Detection uses three signal types in cost order:

1. **Path signals** — file extension globs (fast pre-filter, not authoritative alone)
2. **Filename signals** — literal filenames like `go.mod`, `Chart.yaml` (authoritative)
3. **Content signals** — anchors and patterns inside files (authoritative)

Multiple profiles can activate simultaneously — a Helm chart that generates Python scripts would trigger both `k8s` and `python`.

## What Profiles Provide

Each profile populates phase-specific content for the skills that consume it:

| Phase | Consuming Skill | Content |
|-------|----------------|---------|
| `review-code/` | /kk:review-code | Language-specific review checklists, gotchas |
| `design/` | /kk:design | Architecture patterns, design considerations |
| `implement/` | /kk:implement | Implementation gotchas, idioms |
| `test/` | /kk:test | Testing frameworks, conventions, validators |
| `document/` | /kk:document | Documentation rubrics |
| `review-spec/` | /kk:review-spec | Spec conformance rules |

## Python Implementation Guidance

For Python tasks, `/kk:implement` loads guidance on project compatibility, idioms, typing, exceptions, and resource ownership before editing. Async guidance is conditional on concrete async constructs or async-runtime imports in target files or planned edits; mentions in comments or strings do not trigger it.

The guidance applies to new `.py` files and `.pyi` stub changes as well as existing Python code. It follows the project's supported Python versions and existing tools. Packaging metadata alone does not activate the Python profile.

## Python Testing Guidance

For Python tasks, `/kk:test` loads behavioral testing guidance and a validator protocol before running checks. It follows the owning project's test command, environment, discovery settings, and configured quality gates. Pytest, unittest, and framework-specific entry points retain their existing role; the profile does not introduce a new toolchain.

Async testing guidance loads for concrete async code or explicit async-test configuration. Missing environments, unavailable tools, skipped async tests, and zero executed tests are reported as verification gaps. Stub changes use the project's available type/stub checks and relevant runtime tests.

## Vendored Content

Some profiles vendor content from external upstream repositories. The Go profile, for example, vendors from [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang) via a manifest-driven pipeline. See the [Contributing Guide](../contributing/plugin-development.md) for details on the vendoring workflow.
