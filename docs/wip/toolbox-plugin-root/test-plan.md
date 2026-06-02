# RC validation test plan — `TOOLBOX_PLUGIN_ROOT` & plugin-root resolution

Follow this after cutting a new RC of the `kk` plugin. It validates that every consumer
that references the plugin root resolves it correctly, in **both** Claude Code and Codex.

It is the executable form of the PR's "make an RC and test it" + "test codex" items
(PR #132). Companion: [codex-deferred.md](codex-deferred.md).

---

## 0. The bias rule (read first)

The behavioral tests in §3–§7 use **natural user prompts** — the kind a real user would
type. They deliberately say **nothing** about plugin roots, `TOOLBOX_PLUGIN_ROOT`, paths,
file resolution, sub-agents, or "testing". If a prompt hints at the mechanism, the agent
may "helpfully" work around a real bug and the test passes falsely.

**You validate by observing, never by asking.** Each test states the _observable_ signal
of success (a profile-attributed finding, a file read at the cache path, the absence of an
error). Two artifacts give you everything:

1. **The agent's transcript** — every `Read`/`Bash` tool call and its argument. Watch the
   _paths_ the agent opens.
2. **The skill's structured output** — `/kk:review-code` reports tag each finding with
   `Profile: <name> · Checklist: <file>`. That tag is only producible if the checklist was
   actually read from a resolved path. It is the cleanest non-leading success signal.

Only the **mechanism checks** in §2 (pure infrastructure) use explicit prompts — there is
no agent behavior to bias there.

> **Session caching:** the harness caches skill/plugin content at session start. After
> installing a new RC, **start a brand-new session** for every behavioral test. Re-running
> in the same session tests the old cached copy. When in doubt, start fresh.

---

## 1. Prerequisites

### 1.1 Build, tag, regenerate

```bash
# from the repo
make generate-kodex            # regenerate codex output from source
for t in test/test-*.sh; do echo "== $t"; bash "$t"; done   # all green except the
                                                            # pre-existing template-sync
                                                            # RC-tag failure
go test ./cmd/generate-kodex/
```

Cut the RC tag and publish to your marketplace as usual.

### 1.2 Install the RC

**Claude Code** — in a throwaway project dir:

```bash
claude plugin marketplace add serpro69/claude-toolbox     # or your fork/branch source
claude plugin install kk@claude-toolbox --scope project
claude plugin list                                        # confirm the RC version
```

**Codex** — in the same throwaway project:

```bash
# add the marketplace + install per https://developers.openai.com/codex/plugins
# (repo or personal marketplace pointing at the kk plugin)
codex   # then verify the plugin + its skills are listed
```

### 1.3 Scratch fixtures

Reuse the in-repo review fixtures (no need to invent diffs):

```bash
ls <repo>/klaude-plugin/skills/review-code/evals/
#   go-regression  k8s-helm-chart  k8s-kustomize-only  k8s-monorepo-false-positive  k8s-workload-full
```

For phase tests (design/implement/test/document/review-spec) you'll create a tiny Helm
chart in §3; commands are inline.

---

## 2. Mechanism checks (explicit prompts OK — pure infra)

### M1 — Claude session exports `TOOLBOX_PLUGIN_ROOT` to the right place

Fresh Claude session in the project where the RC is installed. Paste:

```
Run `echo "$TOOLBOX_PLUGIN_ROOT"` and show me the output.
```

- **PASS:** a non-empty absolute path under `~/.claude/plugins/cache/claude-toolbox/kk/<RC-version>/`.
- **FAIL:** empty output → SessionStart hook didn't fire or `cpr.py`/`set-plugin-root.sh`
  failed. A `~/.claude/plugins/marketplaces/...` path → the wrong-path bug is back.

### M2 — `cpr.py` resolves independently of the hook

```
Run `python3 "$TOOLBOX_PLUGIN_ROOT/scripts/cpr.py" kk` and show the output.
```

- **PASS:** the same `cache/claude-toolbox/kk/<RC-version>/` path.
- **FAIL:** error, or a different/marketplace path.

### M3 — the resolved root actually contains the plugin tree

```
Run `ls "$TOOLBOX_PLUGIN_ROOT/profiles"` and show the output.
```

- **PASS:** lists `go java js_ts kotlin python k8s k8s-operator skill-md`.
- **FAIL:** `No such file or directory` → root points one level off (e.g. a repo root whose
  profiles live under `klaude-plugin/`).

### M4 — Codex generated paths are relative and present

Codex resolves nothing in skill prose; it reads `../..`-relative paths from the skill dir.
Confirm the generated copies are correct on disk:

```bash
CODEX_ROOT=~/.codex/plugins/cache/*/kk/*/        # adjust glob to the installed RC
grep -rn '\.\./\.\./profiles' $CODEX_ROOT/skills/_shared/profile-detection.md | head
grep -rlF '${TOOLBOX_PLUGIN_ROOT}' $CODEX_ROOT/skills/   # MUST be empty
ls $CODEX_ROOT/profiles                                  # profiles present at root
```

- **PASS:** `../../profiles/...` present in skills; **no** `${TOOLBOX_PLUGIN_ROOT}` brace
  literals in `skills/`; `profiles/` present at the plugin root so `../..` from
  `skills/<name>/` lands on it.
- **FAIL:** any unresolved brace token, or `profiles/` absent at that depth.

---

## 3. Claude Code — skill invocation + profile resolution (unbiased)

Each test: fresh session, create/stage the fixture, paste the natural prompt, then verify
against the **observe** notes. Do **not** add any other instruction.

### C1 — `/kk:review-code` (standard) activates the **go** profile

Setup:

```bash
mkdir -p ~/rc-test/go-svc && cd ~/rc-test/go-svc && git init -q
cat > cache.go <<'EOF'
package cache

import "os"

// LoadConfig reads the config file and returns its contents.
func LoadConfig(path string) []byte {
	data, _ := os.ReadFile(path)   // error deliberately ignored
	return data
}
EOF
git add -A && git commit -qm "init" && sed -i '' 's/return data/return append(data, 0)/' cache.go
```

Prompt:

```
/kk:review-code
```

(if it needs a nudge to find the diff:)

```
Review my uncommitted changes in this repo.
```

- **Observe:** transcript shows the agent reading files under
  `…/cache/claude-toolbox/kk/<ver>/profiles/go/review-code/…` (e.g. `error-handling.md`
  or `solid-checklist.md`). The report contains a finding tagged
  `Profile: go · Checklist: error-handling.md` (the ignored error).
- **PASS:** a go-checklist-attributed finding appears.
- **FAIL:** the agent reads a literal `${TOOLBOX_PLUGIN_ROOT}/...` path, hits `ENOENT`,
  reads from `marketplaces/`, or the report has only generic findings with no `Profile:`
  attribution.

### C2 — `/kk:review-code:isolated` activates **k8s** and the SUB-AGENT loads checklists ⭐

This is the headline test — it exercises the `## Plugin Root` injection into the Read-only
`code-reviewer` sub-agent.

Setup (reuse the repo fixture):

```bash
mkdir -p ~/rc-test/k8s && cd ~/rc-test/k8s && git init -q
cp -R <repo>/klaude-plugin/skills/review-code/evals/k8s-workload-full/test-files/* .
git add -A && git commit -qm baseline
# introduce a reviewable change so there's a diff:
#   bump an image tag, drop a resource limit, or set privileged: true in a Deployment
git add -A
```

Prompt:

```
/kk:review-code:isolated
```

- **Observe (main agent):** it resolves the plugin root once (a `Bash`/`echo` or a `Read`
  at the cache path), then spawns `kk:code-reviewer` with a prompt that contains a
  `## Plugin Root` section holding that absolute path.
- **Observe (sub-agent):** the `code-reviewer` transcript shows `Read` calls on
  `…/profiles/k8s/review-code/security-checklist.md` (etc.) under the **cache** path that
  was injected — not a literal token, not `marketplaces/`.
- **Observe (report):** findings tagged `Profile: k8s · Checklist: security-checklist.md`
  (or helm/reliability/architecture per the planted issue).
- **PASS:** k8s-checklist-attributed findings from the sub-agent appear.
- **FAIL (the bug this PR fixes):** the sub-agent reports it cannot read a checklist /
  "file not found" / "path unresolved" / "no Plugin Root provided"; or the isolated review
  silently falls back to generic findings; or the run aborts at the "single load-bearing
  checklist gate".

### C3 — `/kk:design` design-phase profile detection (k8s)

Fresh session, any scratch dir. Prompt:

```
/kk:design
I want to add a background worker that drains our image-processing queue. It should run
as its own deployment in our Kubernetes cluster and autoscale on queue depth. Help me turn
this into a proper design.
```

- **Observe:** the agent confirms activating the k8s profile, then reads
  `…/profiles/k8s/design/index.md` (+ `questions.md`/`sections.md`) at the cache path, and
  its refinement questions / proposed sections include k8s-specific concerns (resource
  requests, probes, HPA, RBAC) drawn from that content.
- **PASS:** k8s design content is loaded and visibly shapes the questions/sections.
- **FAIL:** literal-token read, `ENOENT`, or generic design with no k8s-sourced questions
  despite the obvious Kubernetes framing.

### C4 — `/kk:implement` pre-write profile gotchas

Reuse `~/rc-test/k8s`. Create a trivial `docs/wip/<feature>/tasks.md` with one task that
edits a chart template, then:

```
/kk:implement
Work on the first task.
```

- **Observe:** before editing, the agent reads `…/profiles/k8s/implement/index.md` at the
  cache path and applies a gotcha from it.
- **PASS:** implement-phase k8s content loaded from the resolved path pre-write.
- **FAIL:** literal-token read / `ENOENT` / no implement content consulted.

### C5 — `/kk:test`, C6 — `/kk:document`, C7 — `/kk:review-spec`

Run each against `~/rc-test/k8s`. Natural prompts:

```
/kk:test          → "Check the manifests in this repo are sound."
/kk:document      → "Document this chart for the repo."
/kk:review-spec   → "Does the implementation match the design docs?"
```

- **Observe / PASS:** each reads its `…/profiles/k8s/<phase>/index.md` at the cache path and
  applies that phase's content (validators / doc rubric / verification patterns).
- **FAIL:** literal-token read, `ENOENT`, or the phase runs with no profile content.

### C8 — Negative control (no profile, no misbehavior)

Fresh session. Setup a plain-text/markdown-only change (no code, no manifests):

```bash
mkdir -p ~/rc-test/plain && cd ~/rc-test/plain && git init -q
printf '# Notes\nSome prose.\n' > NOTES.md && git add -A && git commit -qm init
printf 'More prose.\n' >> NOTES.md
```

Prompt: `/kk:review-code`

- **PASS:** review completes with generic guidance; **no** profile activated; no errors
  about unresolved paths.
- **FAIL:** spurious profile activation, or an error trying to resolve a path.

---

## 4. Claude Code — sub-agent direct-spawn tests (deterministic)

§3-C2 exercises the sub-agents end-to-end. These spawn them in isolation so the result is
deterministic and the injection contract is tested directly. Run from a fresh session.

First capture a real plugin root and a tiny diff to reuse:

```
Run these and show output:
  echo "$TOOLBOX_PLUGIN_ROOT"
  cd ~/rc-test/k8s && git --no-pager diff
```

### S1 — `code-reviewer` POSITIVE (injection works)

Paste (substitute the real `$TOOLBOX_PLUGIN_ROOT` value and the captured diff):

```
Use the Agent tool to spawn subagent_type "kk:code-reviewer" with this exact prompt:

---
You are reviewing the following code changes. Apply your full review workflow.

## Plugin Root

<PASTE-THE-ABSOLUTE-PATH-FROM-echo-ABOVE>

## Git Diff

<PASTE-THE-DIFF>

## Active Profiles and Resolved Checklists

- profile: k8s, checklist: security-checklist.md, triggered_by: filename — Chart.yaml in parent directory

## Spec Context

No spec context available — review based on code quality alone.

## Rejected Approaches

No rejected approaches to note.

Produce your findings in the output format specified in your agent definition.
---
```

- **PASS:** the sub-agent `Read`s `<plugin-root>/profiles/k8s/review-code/security-checklist.md`
  and returns findings tagged `Profile: k8s · Checklist: security-checklist.md`.
- **FAIL:** `ENOENT`, literal-token read, or no checklist-attributed finding.

### S2 — `code-reviewer` NEGATIVE (must fail loudly without injection)

Same as S1 but **delete the entire `## Plugin Root` section** from the spawned prompt.

- **PASS (correct fail-loud behavior):** the sub-agent stops and surfaces an error that it
  has no plugin-root path / cannot read the checklist — it does **not** invent a path or
  silently produce only generic findings. (Its agent definition says: _"If no `## Plugin
Root` value was provided, stop and surface the error rather than guessing a path."_)
- **FAIL:** it guesses a path, reads from `marketplaces/`, or proceeds silently with
  generic-only output.

### S3 — `profile-resolver` POSITIVE

```
Use the Agent tool to spawn subagent_type "kk:profile-resolver" with this exact prompt:

---
Resolve profiles for the following staged diff. Follow your agent instructions.

## Plugin Root

<PASTE-THE-ABSOLUTE-PATH>

Worktree root: ~/rc-test/k8s

Diff (git diff --cached):
---
<PASTE A STAGED DIFF THAT TOUCHES Chart.yaml / templates/*.yaml>
---
---
```

- **PASS:** the resolver `Read`s `<plugin-root>/skills/_shared/profile-detection.md`, then
  `<plugin-root>/profiles/<name>/DETECTION.md` for each known profile, and returns the
  structured table with `k8s` active and its `review-code` checklists in Loaded/NOT-loaded.
- **FAIL:** `ENOENT`, literal-token reads, or it cannot enumerate profiles.

### S4 — `profile-resolver` NEGATIVE

Same as S3 with the `## Plugin Root` section removed → **PASS** = fails loudly, same as S2.

### S5 — review-code eval harness (drives the resolver + reviewer together)

```
Run the review-code eval harness described in
klaude-plugin/skills/review-code/evals/_harness/HARNESS.md against all evals, and show me
the aggregate pass/fail table.
```

- **PASS:** the orchestrator stages worktrees, injects `## Plugin Root` into both the
  resolver and reviewer prompts, and the grader table shows the routing/finding assertions
  passing (notably the `k8s-*` evals load their checklists; `k8s-monorepo-false-positive`
  and `go-regression` behave per their assertions).
- **FAIL:** resolver/reviewer sub-agents error on unresolved paths, or routing assertions
  regress vs the last recorded harness run.

---

## 5. Codex — skill invocation + profile resolution (unbiased)

Repeat §3 in a fresh **Codex** session with the RC installed. Same fixtures, same natural
prompts (invoke skills the Codex way, e.g. `$kk:review-code` / the skills tool). The
difference is purely in what you **observe**, because Codex reads generated `../..`-relative
paths instead of an env var.

For each of C1–C8, the Codex equivalents:

- **Observe:** the agent opens files at `../../profiles/<name>/<phase>/…` which resolve,
  relative to the skill directory, to `~/.codex/plugins/cache/.../kk/<ver>/profiles/…`.
  There must be **no** literal `${TOOLBOX_PLUGIN_ROOT}` / `${PLUGIN_ROOT}` token in what the
  model reads, and **no** `read_file` failure on a profile/checklist path.
- **PASS:** same profile-attributed findings / phase content as the Claude runs.
- **FAIL (the open risk this plan exists to close):** the model treats `../../profiles/…`
  as relative to the project cwd and gets a "file not found", or reads an unexpanded token.
  If this fails, the fix needs the per-file relative base or a Codex-runtime root export
  (see [codex-deferred.md](codex-deferred.md)).

Run at minimum: **C1 (go, standard)**, **C2 (k8s, isolated — sub-agents)**, **C3 (design)**,
and **C8 (negative control)**. Add C4–C7 if C2 passes.

---

## 6. Codex — sub-agent tests

Codex sub-agents are the generated `.codex/agents/*.toml` (`kk:code-reviewer`,
`kk:profile-resolver`), spawned by Codex's subagent mechanism.

### CX-S1 — isolated review end-to-end (k8s)

Fresh Codex session, `~/rc-test/k8s` staged. Invoke the isolated review
(`$kk:review-code:isolated` or equivalent).

- **Observe:** the Codex orchestrator injects `## Plugin Root` into the spawned
  `kk:code-reviewer` prompt; the sub-agent opens `…/profiles/k8s/review-code/*.md` and
  returns checklist-attributed findings. (The Codex agent file also carries the
  `<kk-plugin-root>` preamble — confirm the agent uses the injected value, not a guess.)
- **PASS / FAIL:** as §3-C2, but in Codex.

### CX-S2 — direct sub-agent spawn (positive + negative)

Repeat S1/S2 and S3/S4 by asking Codex to spawn `kk:code-reviewer` / `kk:profile-resolver`
with the same hand-built prompts (with and without the `## Plugin Root` section).

- **PASS:** positive runs read the injected path and produce attributed output; negative
  runs fail loudly.
- **FAIL:** path-not-found, literal token, or silent generic fallback.

---

## 7. Results template

Copy into a session note (`docs/wip/toolbox-plugin-root/.sessions/rc-<version>-<date>.md`):

```
RC: <version>      Date: <date>      Tester: <name>

Mechanism (Claude):   M1 [ ]  M2 [ ]  M3 [ ]
Mechanism (Codex):    M4 [ ]

Claude behavioral:    C1 [ ]  C2 [ ]  C3 [ ]  C4 [ ]  C5 [ ]  C6 [ ]  C7 [ ]  C8 [ ]
Claude sub-agents:    S1 [ ]  S2 [ ]  S3 [ ]  S4 [ ]  S5 [ ]
Codex behavioral:     C1 [ ]  C2 [ ]  C3 [ ]  C8 [ ]  (C4–C7 [ ] if C2 passed)
Codex sub-agents:     CX-S1 [ ]  CX-S2 [ ]

Failures / notes:
- ...
```

**Merge-ready when:** all Claude tests pass, M4 passes, and at least Codex C1/C2/C3/C8 +
CX-S1 pass. If Codex `../..` resolution fails (§5 FAIL), do **not** merge the Codex claim —
fall back to one of the options in [codex-deferred.md](codex-deferred.md) and re-test.

---

## Appendix — failure signature quick reference

| Symptom in transcript                                                                  | Meaning                                                     |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `Read` arg literally contains `${TOOLBOX_PLUGIN_ROOT}` or `${PLUGIN_ROOT}`             | Token not resolved; agent forwarded it raw                  |
| Path under `~/.claude/plugins/marketplaces/...`                                        | Wrong-path bug (cache vs marketplaces) returned             |
| `ENOENT` / "file not found" on a `profiles/…` path                                     | Root resolved to wrong depth, or codex `../..` mis-anchored |
| Sub-agent: "no Plugin Root provided / cannot read checklist"                           | Spawner didn't inject `## Plugin Root` (regression)         |
| Report has findings but **no** `Profile:`/`Checklist:` tags on a clearly-profiled diff | Checklists never loaded; review fell back to generic        |
| `$TOOLBOX_PLUGIN_ROOT` empty in a Bash call (Claude)                                   | SessionStart hook / `cpr.py` / `set-plugin-root.sh` failed  |
