# Resolution of the design review

Responds to [review-design.md](review-design.md). Checked 2026-11-18 against repository revision `9c6bd133`. Each finding was corroborated independently before any document changed. All 16 are valid. None was rejected; three were fixed differently from the review's suggestion, and one turned out to be wider than reported. Those are marked **Differs** and **Wider**.

A ticked box means the named document now says it. A second read on the same day found defects in some of these fixes; they are listed under [Corrections after a second read](#corrections-after-a-second-read) and the checklists below describe the corrected state. Nothing here is implemented; these are changes to [design.md](design.md), [implementation.md](implementation.md) and [tasks.md](tasks.md).

Two product decisions were the maintainer's and were confirmed on 2026-11-18: Codex native forbids are opt-in and off by default, and the Codex profile leaves approval and sandbox keys out by default.

## P0

### 1. Ordinary sync can retire a repository — valid, **Wider**

Corroborated in `.claude/toolbox/scripts/template-sync.sh`: `--local` sets `APPLY_MODE=true` and calls `apply_changes` (line 2665); the workflow's second job calls `--apply`, which reaches the same function (line 2554); the local path hands off to the fetched script before comparing (line 2588). A migration gated on a marker and `APPLY_MODE` runs from both.

Wider than reported: the exposure does not end at the retirement tag. Once Task 16 deletes the script, an older script syncing to any later tag finds no script to hand off to and continues against the shrunken tree. Its settings merge then assigns the deny list from upstream (line 1603) and its hook merge drops every downstream toolbox handler that upstream no longer has (line 1739). That strips the deny list and the legacy Codex guard registrations with no readiness check. Deployed scripts cannot be changed, but since v0.21.0 they hand off to the target version's script before touching anything, and the downstream workflow fetches it first. A tombstone at the script's path therefore stops them.

- [x] design: retirement is a separate mode that only `kk migrate` invokes; ordinary sync against the retirement release syncs as usual and prints a notice
- [x] design: later releases keep a tombstone at the script's path; the script is not deleted
- [x] implementation: `--retire` mode replaces the `needs_*` / `run_*` migration; tombstone specified
- [x] tasks: Task 13 exercises `--local`, staged `--apply` and `--retire` on one fixture, and an older script against the tombstone; Task 16 installs the tombstone instead of deleting

### 2. A promoted release controls its own rollback — valid, **Differs**

Corroborated in the design text: `rollback` ran "from the last release that reached ready", which after promotion is the release being rolled back from, and the ready step lets that release replace the entry point. The first install has no ready release to resume from.

The review asked for a separate recovery path. The fix adds no new component: rollback runs from the code of the release being restored, which already activated itself on this machine once, and every release carries its own copy of the entry point for the case where the stable one is broken.

- [x] design: dispatch rule per command, including rollback of an interrupted upgrade; per-release entry point as the recovery path; an additive, versioned state format, because older code now reads a file newer code wrote
- [x] design: the installer is the recovery path for an interrupted first install
- [x] design: demonstration 4, rollback after promotion with the promoted CLI unavailable
- [x] implementation and tasks: Tasks 3, 4 and 10 cover the dispatch, the re-runnable installer and demonstration 4

## P1

### 3. Recorded readiness can outlive hook trust — valid

Corroborated: the launcher and `kk migrate` both read recorded state; `docs/providers/codex.md` already notes that Codex exposes enablement and trust as separate properties of a hook; assumption 7's fallback let an acknowledgement produce *ready*.

- [x] design: trust and enablement are re-read before non-interactive launches and in `kk migrate`
- [x] design: new *unverified* state, distinct from *ready*; `kk migrate` also requires the live check, run in a scratch workspace
- [x] implementation and tasks: probe records whether the read reflects a disabled hook, its workspace scope and its cost (Task 1); Tasks 9, 10, 11 and 14 use it

### 4. Migration can remove the guard an open session loaded — valid

Corroborated: the legacy registrations in `.codex/hooks.json` run `bash "$(git rev-parse --show-toplevel)/.codex/scripts/pretooluse-*.sh"` on every call. A session started before `kk` was installed has only those. The Codex source read recorded for this design says a hook that fails with any status other than 2 does not block the call, so a deleted script leaves that session unguarded. Not probed.

- [x] design: `kk migrate` tells the adopter to close such sessions and asks, default no; continuity claim scoped to sessions started after `kk` became ready
- [x] design: assumption 12 and the protection guarantee state it
- [x] implementation and tasks: probe added to Task 1; demonstration 3 includes a session opened before installation (Task 14)

### 5. Two writers — valid

Corroborated: the design explicitly supports a scheduler line running `kk upgrade`, and nothing serialises it against a manual rollback. Atomic renames protect each file, not the set.

- [x] design: one writer lock for upgrade, rollback and resumption
- [x] design: one machine-wide active release, per-tool verification state, and a defined rollback target that skips a release never verified for every tool and falls back to the previously active release when none qualifies; retention keeps every release that state needs
- [x] implementation and tasks: one overlap test (Task 3) and one mixed-tool recovery case (Task 10)

### 6. The settings merger cannot do a lossless retirement — valid

Corroborated: line 1603 assigns `permissions.deny` from upstream after the merge; lines 1629–1651 re-apply manifest-controlled keys afterwards. With an empty upstream the adopter's own denies are erased and the manifest keys are written back. The design's sentence that the merge "removes exactly what the template added once the upstream side is empty" was false. `docs/user-guide/template-sync.md` calls manifest variables "your explicit choices".

- [x] design: migration syncs to the retirement release first, then removes with a removal-only comparison against that release's template; the removal step does not call the three-way merge
- [x] design: downstream-only denies, manifest-selected values and `sync_exclusions` are kept; the sync step merges the deny list three-way so the adopter's entries reach the removal step
- [x] implementation and tasks: rules in the Migration section; fixtures for a downstream-only deny, manifest-selected values, an excluded file and a repository several releases behind (Task 13)

### 7. A reserved-looking filename is not ownership — valid

Corroborated in the design text: sub-agent files were pruned by prefix, and nothing checked `~/.local/bin/kk`, `kk.config.toml` or `kk.rules` before the first write.

- [x] design: ownership is a record of exact installed paths; collisions stop the upgrade before activation; pruning uses the record
- [x] implementation and tasks: collision preflight and record-based pruning, with a pre-existing file and an unrelated prefixed agent (Task 9)

### 8. A guard version does not identify its bytes — valid

Corroborated: a local checkout keeps the published manifest version while its guard changes, so "re-add only when the version differs" skips it; comparing each release candidate with the previous stable tag gives identical bytes two versions on the way to stable.

- [x] design: guard identity is a content digest; it drives reinstall, confirmation and rollback
- [x] design: version changes only against the nearest earlier tag of any kind; a local checkout's guard version is set from its identity; a tagged candidate with the same version and different content fails staging
- [x] implementation and tasks: identity function (Task 7), activation (Task 10), release rule for pre-releases too (Task 12), version-string probe (Task 1)

### 9. The parity ledger understates the Codex policy change — valid, decided by the maintainer

Corroborated: `.codex/rules/default.rules` forbids `rm` outright; `docs/providers/codex.md` documents excluding the rules file as the per-repository control; the profile outranks `~/.codex/config.toml`.

- [x] design: native forbids are opt-in, off by default, with the account-wide effect stated
- [x] design: `approval_policy`, `approvals_reviewer` and `sandbox_mode` leave the baseline and become opt-in; open question 5 closed
- [x] design: parity ledger and protection guarantee updated
- [x] implementation and tasks: Tasks 9 and 15

### 10. The Claude pass-through drops a protection — valid, **Differs**

Corroborated in the design text: the pass-through started Claude with no toolbox layer, while the protection guarantee promised denies in every wrapped session; overrides "applied last" could replace the deny list.

The review offered composing or labelling the launch unmanaged. Composing is the only option consistent with the constraint that secrets stay non-loosenable, and the launcher already reads JSON settings files. The pass-through is removed.

- [x] design: the adopter's `--settings` is composed into the layer; no override or settings file removes a generated deny
- [x] implementation and tasks: Task 6, with an effective-deny check on a real machine with hooks disabled

### 11. The preflight can pass without exercising what it installs — valid

Corroborated in the design text: the rules check ran over the combined set only, and the self-test called the engine directly. The first half is unlikely in practice but costs one extra command to close.

- [x] design: the candidate rules file is checked alone, then the combined set for compatibility
- [x] design: an event goes through each guard handler as the staged plugin registers it
- [x] implementation and tasks: Tasks 3, 9 and 10

## P2

### Claude's baseline uses the maintainer's settings — valid

Corroborated: `.claude/settings.json` pins `claude-opus-5-5` and `xhigh`; `.github/scripts/template-cleanup.sh` defaults to removing the model key and effort `high`.

- [x] design, implementation, tasks: baseline takes the template's adopter defaults; the real-machine check uses effort level, because the baseline pins no model (Task 6)

### PAL's review evidence has no grant — valid

Corroborated: `review-isolated.md` writes the diff with `mktemp`; `docs/user-guide/mcp-servers.md` already documents a scoped temp-directory grant in PAL's client entry. Routing the client through `kk` grants the release directory only.

- [x] design: parity row says the client entry runs `kk claude` and keeps the scoped temp-directory grant
- [x] implementation and tasks: Task 15 documents it and verifies a review reads both criteria and diff

### The pinned migration script has unpinned prerequisites — valid

Corroborated: the script requires `curl` and `yq` outside apply mode (lines 291–303) and fetches `semver-compare.sh` from `master` when it is missing (line 75).

- [x] design: `kk migrate` fetches the script and its helper from the retirement tag; migration dependencies are named separately from the launcher's
- [x] implementation and tasks: Tasks 13 and 14

### Pruning dates the grace period from activation — valid, and more serious than P2

Corroborated in the design text. The consequence is not cosmetic: the pruned directory holds the hooks of a live Claude session, so that session loses its guard.

- [x] design: the 14 days run from when a release stopped being active; supported session lifetime stated
- [x] implementation and tasks: Task 4, with the month-old-release case

### Cloud and fresh CI runners have no local hook — valid

Corroborated in the design text. Migration also removes the committed plugin enablement that reaches such hosts today.

- [x] design: Not Doing, protection guarantee, parity ledger and the team-wide effect statement scoped to hosts where the plugin is installed, enabled and loaded

## Framing and verification order

### One command per release starts after migration — valid

- [x] design: success measure 1 and legacy coexistence say that committed project settings keep outranking machine defaults until a repository migrates

### Pilot before retirement — valid

Task 17's parity observation came after the irreversible Task 16.

- [x] design: a pilot of the tagged payload gates retirement
- [x] implementation: new "Pilot the tagged release" section
- [x] tasks: new Task 18, which Task 16 depends on. It is numbered 18 so the task references in the review stay valid.

## Corrections after a second read

A fresh read of the three documents on 2026-11-18, checked again against the sync script, the workflows and the guard rules, found seven defects in the fixes above. All are corrected in the documents.

1. **The migration live check could not work (finding 3).** It was specified to run from the repository being migrated. There the legacy and plugin guards both fire with the same denial text, and a decoy outside the workspace does not match the guard's workspace-anchored secret patterns. It now runs in a scratch workspace, with the trust read asked for the repository.
2. **Some adopters had no rollback target (finding 5).** Requiring every installed tool to be verified left nothing to roll back to for an adopter who has Codex installed and never reviews its hooks. The target now falls back to the previously active release.
3. **Rollback dispatch was inconsistent (finding 2).** Rolling back an interrupted upgrade must run the active release's code, not the rollback target's. Older code reading a newer state file also needed a wider guarantee than three frozen fields; the state format is now versioned and additive.
4. **Task 16 would have broken releases.** `release.yml` and `pre-release.yml` call `semver-compare.sh` under `.claude/toolbox/scripts/`. The file moves to `.github/scripts/` first.
5. **Migration dropped the repository's Codex sandbox and approval settings without saying so,** a consequence of taking those keys out of the baseline. The team-wide effect statement and the report now name it, and the adopter can decline that part.
6. **Task order.** The trust re-read in `kk codex` needed the trust reader from a later task. It moved to Task 10.
7. **Guard version stamping contradicted byte verification (finding 8).** A local checkout's staged guard version is now set from its identity, so an unchanged guard stays byte-identical to the installed one.

Smaller corrections: four kinds of evidence, not three; the hand-off happens after the older script may have rewritten its own manifest; installed paths are recorded before they are written; a probe for re-adding an earlier guard version was added to Task 1 as assumption 14.

One design decision changed at the maintainer's direction: removal no longer compares against the template at each repository's recorded version. `kk migrate` first syncs the repository to the retirement release and removes against that one template. Two consequences are stated in the design: the sync step overwrites edits to synced files as any sync does, and it needs a switch that merges the deny list three-way so that a deny the adopter added survives to the removal step.

Still open, and not addressed by these changes:

- An override change to the Codex profile, including either new opt-in, takes effect only when the profile is next written at upgrade. The design names no way to re-apply it sooner.
- Open questions 1 to 4 in the design are unconfirmed. Names and locations block Task 3; the per-repository instruction extras affect Tasks 7 and 9.
- Tasks 3 and 9 are larger than the task convention allows for a single task and should be split before they start.
- Whether migration should keep the repository's Codex sandbox and approval settings by default, instead of removing them unless declined, is a choice the maintainer has not made.

## Not changed

- The review's links and task numbers were left as they are. `review-design.md` is unedited.
- Profile detection for this pass matched the Go profile on the word "Go", which appears in the design only as a rejected alternative. It was not activated.
