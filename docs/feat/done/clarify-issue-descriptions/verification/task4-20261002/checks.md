# Task 4 repository checks

Run date: 2026-10-02. Starting revision: `9a501e1108b9083b83adbc6b550a18d0ff7b2b40`.
Only maintained usage and feature-status documentation changed for this task before
these checks. Canonical behavior and evals remain at the final Task 3 revision.

| Command/check | Exit | Evidence |
| --- | --- | --- |
| `make generate-kodex`, initial workspace sandbox attempt | 2 | [Preserved failure](checks/generate-sandbox-attempt.txt): generator tests passed; the sandbox prohibited refreshing `.codex/agents/`. |
| `GOCACHE=/private/tmp/clarify-task4-go-cache make generate-kodex`, approved escalation | 0 | [First generation](checks/generate-first.txt), including generator tests and both structure suites. |
| Same generation command, second run | 0 | [Second generation](checks/generate-second.txt). |
| Generated-file SHA256 comparison | 0 | [Before](checks/generated-before.sha256) and [after](checks/generated-after.sha256) manifests are byte-identical. |
| `git diff --exit-code -- kodex-plugin/ .codex/agents/` | 0 | No intended generated changes or uncommitted drift in Task 4. |
| All nine `bash test/test-*.sh` suites | 0 each | [Per-suite exits](checks/shell-exits.tsv); 303 test cases / 604 passing assertions, no skipped network cases. Individual `checks/test-*.sh.txt` files retain complete ordered output. |
| `GOCACHE=/private/tmp/clarify-task4-go-cache go test ./...` | 0 | [Go output](checks/go-test.txt): all three command packages pass; the two fixture packages have no test files. |
| `GOCACHE=/private/tmp/clarify-task4-go-cache make plugin-graph` | 0 | [Graph output](checks/plugin-graph.txt): no broken edges or orphans; existing cycle warning retained. |
| Operative procedure vs complete preflight candidate | 0 (`cmp`) | Both have 1,297 whitespace-delimited words and identical bytes, within the unchanged 1,297-word ceiling. |
| Scenario metadata and declared-fixture integrity | 0 | [Current scenario manifest](checks/scenario-manifest.json): 24 standalone + five consumer scenarios, 133 assertions; standalone IDs 1–24 are unique, assertion IDs match their scenario IDs, all declared fixture files exist. This is not a behavioral grade. |
| Root issue-cohort seal audit | 0 | [310 files checked](checks/issue-seal-audit.json), with both SHA256 and byte lengths matching. |

The first generation failure was a filesystem permission limit, not a failed test.
The approved rerun permits the required generated-agent refresh. The shell and Go
runs also used approved escalation for temporary Git/network fixtures and local
test HTTP listeners. Each shell suite's exit is recorded independently; a later
success cannot mask an earlier failure.

Command output was initially captured as `.log`; those files were renamed to
`.txt` without changing their bytes because repository ignore rules exclude logs.
The evidence links therefore remain suitable for normal Git tracking.

The first root seal-check command incorrectly compared a digest string with the
entire `{sha256, bytes}` metadata object and exited 1. The corrected check compares
the actual digest and size with their respective fields; all 310 files match.
No evidence bytes, expected hashes or behavioral assertions changed for this fix.

Operative shared-procedure SHA256:
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
Entry-point SHA256:
`1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`.
The entry point remains 616 words. The procedure has no mandatory dependencies to
add to its count. These checks establish structure and packaging; behavioral
acceptance is recorded separately by the fresh scenario runs.
