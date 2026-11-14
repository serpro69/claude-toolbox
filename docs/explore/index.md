---
template: explore.html
title: Explore the toolbox
description: >-
  What claude-toolbox caught while AI was building capy, quoted from capy's own
  records: a design review, three code reviews and a spec review.

# Page content. `explore.html` renders everything below; nothing is generated
# at runtime. Rules for editing:
# - Copy fields: wrap code in backticks.
# - Headlines keep line breaks when written as a `|-` block; `>-` folds them
#   into spaces.
# - Excerpt `text` must be the record's exact text. Mark cuts with `…` and the
#   highlighted phrase with `[[…]]`. `at` is the source line or range
#   ("113-116", joined with spaces); it also builds the GitHub link.
# - A step without `command` prints its `note` as a comment, so it never reads
#   as output of the previous command. `inferred: true` marks a command the
#   record describes but doesn't quote.
explore:
  repos:
    capy: https://github.com/serpro69/capy/blob/master/
    claude-toolbox: https://github.com/serpro69/claude-toolbox/blob/master/

  chapters:
    - id: shortcut
      kicker: What claude-toolbox caught while AI was building capy
      headline: |-
        "I took the shortcut."
        — your LLM
      copy:
        - >-
          Three `/kk:review-code` runs on the same capy diff. Each time, the
          agent read the code first and got to the review checklists late or
          not at all. In the third run it was told to "follow the review
          process exactly". It loaded 28 files and still read the diff first.
          The skill itself said to start with the diff, so the fix was to
          change the order, not to write a sterner prompt.
        - >-
          capy is a local MCP server, written in Go, that keeps large outputs
          out of a coding agent's context window. It was built from start to
          finish with claude-toolbox: skills, sub-agents and config for Claude
          Code and Codex, run as `/kk:` commands from design through review,
          tests and docs. Below is what they caught along the way, quoted from
          capy's own records. Nothing is staged.
      left_behind: >-
        All 16 skills now load their method before they touch your code. From
        `review-code/SKILL.md`: "The standard workflow below is strictly
        sequential."
      footnote: >-
        From the same record: "Enforcement is convention, not mechanism."
      steps:
        - command: /kk:review-code
          note: three runs, same diff
          repo: claude-toolbox
          path: docs/adr/0004-skill-workflow-ordering.md
          lines:
            - at: 15
              text: >-
                - **Run 1.** … When pressed, the agent admitted: "I had the
                full diff visible, recognized the changes as a clean
                source-kind refactor, and decided I could pattern-match a
                review from the diff alone. [[I took the shortcut.]]"
            - at: 17
              text: >-
                - **Run 3.** User explicitly asked the agent to "follow the
                review process exactly." Agent loaded 28 files but still
                diffed first, then circled back to read checklists after
                findings were already forming.
            - at: 21
              text: >-
                This is a workflow-ordering bug, not an agent-discipline bug.
        - note: where the three runs happened
          repo: claude-toolbox
          path: docs/feat/done/kubernetes-support/design.md
          lines:
            - at: 483
              text: >-
                **Flagged by:** Task 7 P0 verification dry-run (2026-04-19) —
                user-led `/kk:review-code` runs in a [[sibling Go project
                (`capy`)]] reproduced the same process-bypass behavior across
                three consecutive invocations.

    - id: one-reader
      kicker: Design
      headline: One reader handled a new line type. The other two silently dropped it.
      copy:
        - >-
          capy's session vault read Claude transcripts with three separate
          readers: one for search, one for `show`, one for the terminal
          viewer. capy's knowledge base had a recurring bug on record: a new
          line type handled in one reader was silently lost from the other
          two. The plan to add Codex sessions cited that record and didn't add
          three more readers. It replaced them with one decoder per format.
        - >-
          Before any of the old reader code changed, Task 1 recorded what
          those readers produced for every session file on the machine, 700
          of them. Every later task had to match that output byte for byte.
          The final `/kk:test` run compared 698 and found 0 mismatches.
      left_behind: >-
        ADR-031: "A new line type is handled once, in the decoder; the "three
        parsers must stay in sync" convention is retired." And
        `TestGolden_CoversEveryLineType`, which "enforces the one-case-per-arm
        rule mechanically".
      steps:
        - command: /kk:design
          inferred: true
          repo: capy
          path: docs/feat/done/codex-vault-sessions/design.md
          lines:
            - at: 19
              text: >-
                There is a second, pre-existing cost this feature exposes: the
                three Claude readers duplicate the same pass-1 logic, and the
                project's knowledge base records the recurring bug shape —
                [[a new line type handled in one reader is silently lost from
                the other two.]] Adding a Codex trio the same way would double
                that surface.
        - note: Task 1, before any reader code changed
          repo: capy
          path: docs/feat/done/codex-vault-sessions/tasks.md
          lines:
            - at: 26
              text: >-
                - [x] 1.6 Produce the baseline on `master` and re-run
                unchanged: 0 mismatches (700 files baselined at
                `$REPO/bench-results/vault-parity-baseline.tsv`, gitignored;
                compare run: 699 compared, 0 mismatches, 1 skipped as a live
                session)
        - command: /kk:test
          note: final verification, 2026-09-16
          repo: capy
          path: docs/feat/done/codex-vault-sessions/tasks.md
          lines:
            - at: 211
              text: >-
                - [x] 14.1 Run `/kk:test` skill to verify all tasks — … [[parity
                canary 698 compared / **0 mismatches**]] / 2 skipped as live
                sessions / 31 new since baseline

    - id: vault-lockout
      kicker: Design review
      headline: This upgrade would have stopped every existing vault from opening.
      copy:
        - >-
          The same plan then went through four separate `/kk:review-design`
          runs before any code existed. Two of them found that a new index ran
          before the migration that creates its column. On any existing vault,
          that fails at open. The same pass found that merging an old vault
          would silently drop about 1 in 11 sessions.
        - >-
          Every claim was re-checked against the code and the real session
          files on the machine before the plan changed. The design was revised
          on 2026-09-13; the code landed two days later.
      left_behind: >-
        An invariant in the implementation plan: "`schemaSQL` may therefore
        reference only columns that exist in every historical schema." And
        `TestMigrate0006_LegacyVaultOpensThroughStore`, which opens a
        pre-migration vault through the store.
      steps:
        - command: /kk:review-design
          note: four independent runs, R1–R4
          repo: capy
          path: docs/feat/done/codex-vault-sessions/design-triage.md
          lines:
            - at: 3
              text: >-
                **Date:** 2026-09-13 · **Inputs:** four independent
                `kk:review-design` runs (R1–R4) · … Nothing below is taken
                from a review on trust.
            - at: 11
              text: >-
                | A | `idx_sessions_parent` in `schemaSQL` breaks legacy vault
                open (R3, R4) | **Confirmed** | P0 | Fix |
            - at: 44
              text: >-
                On a pre-0006 vault `CREATE TABLE IF NOT EXISTS` is a no-op, so
                `CREATE INDEX IF NOT EXISTS idx_sessions_parent ON
                vault_sessions(parent_uuid)` in `schemaSQL` (…) fails with "no
                such column" and [[every existing vault refuses to open.]]
            - at: 60
              text: >-
                … **41/464 (8.8 %)** would return an error. … so merging any
                pre-0006 vault silently drops ~1 in 11 sessions.

    - id: symlink
      kicker: Code review
      headline: A symlinked folder and `..` walked straight past the deny list.
      copy:
        - >-
          capy checks file paths against deny rules, so an agent can't route a
          read of something like `~/.ssh/id_rsa` through it. The first version
          tidied each path before resolving symlinks. Tidying turns
          `dir-link/../secrets` into `secrets`, so the symlinked folder
          vanishes from the check. The OS doesn't tidy: it follows `dir-link`
          first, then `..`, and can end up inside a denied folder.
        - >-
          The isolated review rated it P0. It was fixed in the same task, with
          a regression test, and the finding went into capy's knowledge base,
          where later reviews search it.
      left_behind: >-
        The regression test `physical traversal via symlinked dir caught`, and
        the finding indexed as `kk:review-findings`.
      steps:
        - command: /kk:review-code:isolated
          inferred: true
          repo: capy
          path: docs/feat/done/upstream-sync-v1.0.136/tasks.md
          lines:
            - at: 31
              text: >-
                > **Isolated review (P0, fixed):** The initial implementation
                fed the lexically-`Clean`ed path to `filepath.EvalSymlinks`.
                `Clean` collapses `..` lexically, discarding a symlinked
                directory before symlink resolution (`dir-link/../secrets`
                cleans to `secrets`), [[so a symlink-then-`..` physical escape
                bypassed the realpath candidate.]] … Indexed as
                `kk:review-findings`.
        - note: the regression test
          repo: capy
          path: internal/security/eval_test.go
          lines:
            - at: 209
              text: >-
                t.Run("physical traversal via symlinked dir caught", func(t
                *testing.T) {
            - at: 212
              text: >-
                // (non-existent), but the OS resolves dir-link -> safe-dir
                first, then
            - at: 213
              text: >-
                // ".." -> realTmp, reaching the denied realTmp/secrets/id_rsa.
                Only the
            - at: 214
              text: >-
                // uncleaned EvalSymlinks candidate catches it.

    - id: key-chmod
      kicker: Code review
      headline: The tests could chmod a developer's real key file.
      copy:
        - >-
          A capy change made setup repair the permissions on database key
          files. The full test suite passed. Then a fresh reviewer agent, one
          that hadn't written the code, noticed that the existing setup tests
          read the developer's global config. After this change, running them
          could change the permissions on the developer's real key.
        - >-
          The external model reviewing alongside it reported no issues and
          claimed protections the code didn't have. The record says so and
          doesn't adopt them.
      left_behind: >-
        The tests now isolate global config in `TestMain`. A probe with a
        deliberately loose `0644` key file "left that file at `0644`". The
        non-atomic repair is recorded as a known limit, with the hardening
        steps written down.
      steps:
        - command: /kk:review-code:isolated
          repo: capy
          path: docs/feat/reviews/issue-124-key-file-permissions.md
          lines:
            - at: 26
              text: >-
                `kk:review-code:isolated` used a fresh `code-reviewer` agent and
                two-step PAL `gemini-3.1-pro-preview` review.
            - at: 28
              text: >-
                The code reviewer found **P2: existing setup tests inherited
                global configuration and [[could chmod a developer's real
                absolute key file]]**.
            - at: 30
              text: >-
                PAL reported no issues. Its broad claims of TOCTOU protection
                are not adopted: opened-descriptor validation protects the read
                admission check, but pathname-based setup repair is not atomic.

    - id: default-wait
      kicker: Spec review
      headline: The live tests passed. None of them exercised the default wait.
      copy:
        - >-
          `capy_execute` waits up to 25 seconds, then hands back a "still
          running" receipt so the agent isn't stuck. The live acceptance runs
          on real Claude Code and Codex hosts all passed. But they were short
          commands with the wait raised to 30 seconds, so none of them ever
          hit the default.
        - >-
          The closing spec review caught it. Both hosts were rerun with a
          27-second command at the default wait. Both answered "running"
          before it finished, and the full output was recovered afterwards.
      left_behind: >-
        Live evidence from both hosts, retained with exact inputs: 27,011 ms
        on Codex and 27,012 ms on Claude.
      steps:
        - command: /kk:review-spec:isolated
          inferred: true
          repo: capy
          path: docs/feat/done/routine-command-capture/task17-spec-review.md
          lines:
            - at: 40-42
              text: >-
                The independent closeout review initially identified a P2
                acceptance gap: short commands specifying `wait_ms=30000` [[did
                not exercise the default 25-second attached wait.]]
        - note: the rerun
          repo: capy
          path: docs/feat/done/routine-command-capture/task17-verification.md
          lines:
            - at: 110-111
              text: >-
                `wait_ms=30000` calls completed normally and zero-wait recovery
                worked.
            - at: 113-116
              text: >-
                The final review identified that those short calls did not
                measure default-wait viability. Both trusted hosts were
                therefore resumed for one additional 27-second command with
                `wait_ms=25000` and `timeout=40000`. Both returned a healthy
                `running`/`recording` response before command completion,
                without a host timeout.
            - at: 122
              text: >-
                | Codex | `70ec2b9a-37e3-4dcc-9651-c34fe0c764a5` | 27,011 ms |
                44 |
            - at: 123
              text: >-
                | Claude | `34426298-5d84-42cf-9194-43c9bfe057a4` | 27,012 ms |
                46 |

  closing:
    headline: Each catch left something behind.
    copy:
      - >-
        A rule, an invariant, a test, a recorded limit. Every excerpt above is
        the record's own text, and every line number links to it.
    # Snapshot figures. The docs deploy refreshes `value` per `key` and `as_of`
    # from a capy clone (scripts/mkdocs/capy_stats.py); without one, as here
    # locally, these are shown as written.
    stats:
      as_of: "2026-11-14"
      items:
        - key: commits
          value: "672"
          label: commits since 2026-03-18
        - key: adrs
          value: "37"
          label: ADRs
        - key: features
          value: "27"
          label: finished feature records
    links:
      - label: Get started
        href: getting-started/
        primary: true
      - label: capy's feature records ↗
        href: https://github.com/serpro69/capy/tree/master/docs/feat/done
      - label: claude-toolbox on GitHub ↗
        href: https://github.com/serpro69/claude-toolbox
---

# Explore the toolbox

What claude-toolbox caught while AI was building capy, a Go MCP server built from
start to finish with it: an agent that skipped its own review method, a design
shaped by a recurring bug in capy's knowledge base, an upgrade that would have
locked every existing vault, a deny-list bypass through a symlinked folder,
tests that could chmod a developer's real key file, and live tests that never
exercised the default wait. Each chapter quotes capy's records.
