"""Run the public sync entry points against local tagged upstreams."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(".claude/toolbox/scripts")
SYNC = SCRIPTS / "template-sync.sh"
MANIFEST = Path(".github/template-state.json")
SETTINGS = Path(".claude/settings.json")
CONFIG = Path(".codex/config.toml")
HOOKS = Path(".codex/hooks.json")
WORKFLOW = Path(".github/workflows/template-sync.yml")
GUARD = Path(".codex/scripts/guard.sh")
EXCLUDED = Path(".codex/rules/keep.rules")
EXTRA = Path(".claude/CLAUDE.team.md")
TOOL = "bash .codex/scripts/guard.sh"
AUDIT = '{ "type" : "command", "command" : "audit  .codex/scripts/guard.sh" }'
CAPY = '{ "type" : "command", "command" : "capy codex-launch" }'
CUSTOM_TABLE = b"\n[mcp_servers.capy]\ncommand  =  'capy' # from setup\nargs = ['serve']\n"


def put(root, path, data):
    target = root / path
    target.parent.mkdir(exist_ok=True, parents=True)
    if isinstance(data, dict):
        data = json.dumps(data, indent=2) + "\n"
    target.write_bytes(data if isinstance(data, bytes) else data.encode())


def snapshot(repo):
    return {p.relative_to(repo): (p.read_bytes(), p.stat().st_mode & 0o777)
            for p in repo.rglob("*") if ".git" not in p.parts and p.is_file()}


class Retirement(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp = Path(temp.name)
        self.up = self.tmp / "upstream"
        self.up.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_COUNT="1", GIT_CONFIG_VALUE_0="https://github.com/test/fixture.git",
                        GIT_CONFIG_KEY_0="url.{}.insteadOf".format(self.up.as_uri()))
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "fixture")
        put(self.up, SYNC, (ROOT / SYNC).read_bytes())
        put(self.up, SCRIPTS / "semver-compare.sh", (ROOT / SCRIPTS / "semver-compare.sh").read_bytes())
        put(self.up, WORKFLOW, "name: sync\n")
        put(self.up, GUARD, "fixture guard\n")
        put(self.up, EXCLUDED, "template\n")
        put(self.up, ".claude/CLAUDE.extra.md", "template instructions\n")
        put(self.up, SETTINGS, {"permissions": {"deny": ["old"]}})
        put(self.up, CONFIG, 'model = "base"\nold_key = 1\n')
        put(self.up, HOOKS, {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "bash .codex/scripts/old.sh"}]}]}})
        self.tag("v1.0.0")
        put(self.up, SETTINGS, {"permissions": {"deny": ["current"]},
                                "enabledPlugins": {"kk@claude-toolbox": True},
                                "statusLine": {"type": "command", "command": "bash .claude/toolbox/scripts/statusline_enhanced.sh"}})
        put(self.up, CONFIG, 'model = "base"\nowned = 2\nsandbox_mode = "read-only"\napprovals_reviewer = "user"\n')
        put(self.up, HOOKS, {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": TOOL}]}]}})
        self.tag("v3.0.0")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.up, env=self.env, check=True, capture_output=True)

    def tag(self, version):
        self.git("add", "-f", ".")
        self.git("commit", "-qm", version)
        self.git("tag", version)

    def project(self, name, behind=False):
        repo = self.tmp / name
        version = "v1.0.0" if behind else "v3.0.0"
        put(repo, MANIFEST, {"upstream_repo": "test/fixture", "template_version": version,
                             "schema_version": "1", "plugin_migrated": True,
                             "variables": {"PROJECT_NAME": "fixture", "LANGUAGES": "python", "CC_MODEL": "sonnet",
                                           "CODEX_MODEL": "project-model", "CC_EFFORT_LEVEL": "low",
                                           "CC_PERMISSION_MODE": "plan", "CC_STATUSLINE": "basic"},
                             "sync_exclusions": [str(EXCLUDED)]})
        put(repo, GUARD, "edited guard\n")
        put(repo, EXCLUDED, "my rule\n")
        (repo / EXCLUDED).chmod(0o640)
        put(repo, EXTRA, "local instructions\n")
        put(repo, "CLAUDE.md", b"@other\r\n@.claude/CLAUDE.extra.md\r\n@.claude/toolbox/CLAUDE.md\r\n keep")
        deny = "old" if behind else "current"
        put(repo, SETTINGS, '{"permissions":{"deny":["' + deny + '","private"],"allow":["mine"]},'
            '"env":{ "ADOPTER" : "literal  value" }}')
        put(repo, CONFIG, ('model = "project-model"\nsandbox_mode = "read-only"\n'
                           "approval_policy  =  'untrusted' # keep spacing\n"
                           'approvals_reviewer = "user"\n' + ('old_key = 1\n' if behind else 'owned = 2\n')
                           + "personal  =  '''two\nlines'''\n").encode() + CUSTOM_TABLE)
        tool = "bash .codex/scripts/old.sh" if behind else TOOL
        put(repo, HOOKS, '{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[' +
            json.dumps({"type": "command", "command": tool}) + "," + AUDIT + "," + CAPY + "]}]}}")
        subprocess.run(["git", "init", "-q"], cwd=repo, env=self.env, check=True)
        return repo

    def sync(self, repo, *args, migrate=False, script=None, ok=True, env=None):
        env = dict(self.env, **(env or {}))
        if migrate:
            env.update(TEMPLATE_SYNC_NO_HANDOFF="1", TEMPLATE_SYNC_MERGE_DENY="1")
        result = subprocess.run(["bash", script or ROOT / SYNC, *args], cwd=repo, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=75)
        self.assertEqual(result.returncode == 0, ok, result.stdout)
        return result.stdout

    def test_two_step_migration(self):
        final = []
        for name, behind in [("current", False), ("behind", True)]:
            repo = self.project(name, behind)
            args = ["--version", "v3.0.0"]
            outputs = self.tmp / (name + "-outputs")
            preview = self.sync(repo, "--dry-run", "--ci", *args, migrate=True, env={"GITHUB_OUTPUT": str(outputs)})
            self.assertEqual(outputs.read_text().splitlines()[0], "has_changes=true")
            self.assertIn("-edited guard", preview)
            self.assertEqual((repo / GUARD).read_text(), "edited guard\n")
            self.sync(repo, "--local", *args, migrate=True)
            self.assertEqual((repo / GUARD).read_bytes(), (self.up / GUARD).read_bytes())
            settings = json.loads((repo / SETTINGS).read_bytes())
            self.assertEqual(set(settings["permissions"]["deny"]), {"private", "current"})
            self.assertIn(TOOL, (repo / HOOKS).read_text())
            synced = snapshot(repo)
            report = self.sync(repo, "--retire", "--dry-run", *args)
            self.assertEqual(synced, snapshot(repo))
            for required in (str(EXCLUDED), str(EXTRA), "AGENTS.md", "untrusted", "sonnet", "project-model",
                             "without kk", "unwrapped Claude", "account-wide", "basic"):
                self.assertIn(required, report)
            self.sync(repo, "--retire", *args)
            result = snapshot(repo)
            self.assertIn(GUARD, result)  # The retained audit hook takes this script as input.
            for removed in (WORKFLOW, MANIFEST, SYNC):
                self.assertNotIn(removed, result)
            self.assertEqual(result[EXCLUDED], (b"my rule\n", 0o640))
            self.assertEqual(result[Path("CLAUDE.md")][0], b"@other\r\n keep")
            self.assertIn(EXTRA, result)
            self.assertEqual(json.loads(result[SETTINGS][0]), {
                "permissions": {"deny": ["private"], "allow": ["mine"], "defaultMode": "plan"},
                "env": {"ADOPTER": "literal  value"}, "model": "sonnet", "effortLevel": "low"})
            self.assertIn(b'{ "ADOPTER" : "literal  value" }', result[SETTINGS][0])
            for handler in (AUDIT, CAPY):
                self.assertIn(handler.encode(), result[HOOKS][0])
            self.assertEqual(json.loads(result[HOOKS][0])["hooks"]["PreToolUse"],
                             [{"matcher": "Bash", "hooks": [json.loads(AUDIT), json.loads(CAPY)]}])
            for data in (CUSTOM_TABLE, b"approval_policy  =  'untrusted' # keep spacing",
                         b"personal  =  '''two\nlines'''", b'sandbox_mode = "read-only"'):
                self.assertIn(data, result[CONFIG][0])
            self.assertNotIn(b"owned =", result[CONFIG][0])
            final.append(result)
        self.assertEqual(final[0], final[1])

    def test_ordinary_sync_and_direct_retirement(self):
        repo = self.project("local")
        report = self.sync(repo, "--local", "--version", "v3.0.0")
        self.assertEqual(report.count("kk migrate"), 1)
        self.assertEqual(json.loads((repo / SETTINGS).read_bytes())["permissions"]["deny"], ["current"])
        self.assertTrue((repo / GUARD).is_file())
        staged = self.tmp / "stage"
        self.sync(repo, "--ci", "--output-dir", staged, "--version", "v3.0.0")
        self.sync(repo, "--apply", "--output-dir", staged, "--version", "v3.0.0")
        self.assertIn(TOOL, (repo / HOOKS).read_text())
        before = snapshot(repo)
        self.sync(repo, "--retire", "--version", "v9.9.9", ok=False)
        self.assertEqual(snapshot(repo), before)
        put(repo, HOOKS, (self.up / HOOKS).read_bytes())
        self.sync(repo, "--retire", "--version", "v3.0.0")
        self.assertFalse((repo / GUARD).exists())
        self.assertNotIn(TOOL, (repo / HOOKS).read_text() if (repo / HOOKS).exists() else "")
        direct = self.project("unsynced")
        report = self.sync(direct, "--retire", "--version", "v3.0.0")
        self.assertIn("Keep changed file: " + str(GUARD), report)
        self.assertEqual((direct / GUARD).read_text(), "edited guard\n")

    def test_migration_sync_reports_no_changes_with_project_only_files(self):
        repo = self.project("retry")
        args = ["--version", "v3.0.0"]
        self.sync(repo, "--local", *args, migrate=True)
        report = self.tmp / "outputs"
        before = snapshot(repo)
        self.sync(repo, "--dry-run", "--ci", *args, migrate=True, env={"GITHUB_OUTPUT": str(report)})
        self.assertEqual(report.read_text().splitlines()[0], "has_changes=false")
        self.assertEqual(before, snapshot(repo))
        self.assertIn(EXTRA, before)

    def test_mixed_entries_exclusions_and_missing_base(self):
        repo = self.project("mixed", behind=True)
        manifest = json.loads((repo / MANIFEST).read_bytes())
        manifest.update(plugin_migrated=False, template_version="v0.0.1")
        manifest["sync_exclusions"] += [".claude/skills/personal", "docs/feat/wip/kept.md"]
        put(repo, MANIFEST, manifest)
        legacy = "bash $CLAUDE_PROJECT_DIR/.claude/scripts/validate-bash.sh"
        settings = json.loads((repo / SETTINGS).read_text())
        settings["hooks"] = {"PreToolUse": [{"hooks": [{"command": legacy}]},
                                            {"hooks": [{"command": legacy}, json.loads(AUDIT)]}]}
        settings["statusLine"] = {"type": "command", "command": 'bash "$CLAUDE_PROJECT_DIR/.claude/toolbox/scripts/statusline.sh" extra'}
        put(repo, SETTINGS, json.dumps(settings).replace(json.dumps(json.loads(AUDIT)), AUDIT))
        keep = Path(".claude/skills/personal/note")
        put(repo, keep, "keep\n")
        put(repo, "docs/wip/kept.md", "keep in place\n")
        put(self.up, keep, "upstream\n")
        put(self.up, "klaude-plugin/.claude-plugin/plugin.json", "{}")
        with (self.up / CONFIG).open("ab") as output:
            output.write(b"\n[tui]\nwhimsy = false\nanimations = false\n")
        (repo / CONFIG).write_bytes(b"tui = { animations = false, whimsy   =   true }\n" +
                                    (repo / CONFIG).read_bytes())
        self.tag("v3.0.1")
        args = ["--version", "v3.0.1"]
        before = snapshot(repo)
        self.sync(repo, "--dry-run", *args, migrate=True)
        self.assertEqual(before, snapshot(repo))
        prep = self.sync(repo, "--local", *args, migrate=True)
        self.assertIn("No Codex base fetched", prep)
        self.assertTrue((repo / "docs/wip/kept.md").is_file())
        self.assertFalse((repo / "docs/feat/wip/kept.md").exists())
        self.assertEqual(json.loads((repo / SETTINGS).read_bytes())["hooks"],
                         {"PreToolUse": [{"hooks": [json.loads(AUDIT)]}]})
        self.assertIn(AUDIT, (repo / SETTINGS).read_text())
        other = '{"type":"command", "command":"audit  .codex/scripts/guard.sh"}'
        hooks = (repo / HOOKS).read_text()
        put(repo, HOOKS, hooks.replace('"PreToolUse":', '"Stop":[{"hooks":[' + other +
                                       ',{"command":' + json.dumps(TOOL) + '}]}],"PreToolUse":', 1))
        report = self.sync(repo, "--retire", *args)
        self.assertIn('Keep Claude deny "old"', report)
        self.assertIn("Keep Codex hooks.Stop", report)
        self.assertNotIn("statusLine", json.loads((repo / SETTINGS).read_bytes()))
        self.assertEqual((repo / keep).read_bytes(), b"keep\n")
        self.assertIn(b"whimsy   =   true", (repo / CONFIG).read_bytes())
        self.assertNotIn(b"animations", (repo / CONFIG).read_bytes())
        self.assertIn(other, (repo / HOOKS).read_text())
        self.assertIn(AUDIT, (repo / HOOKS).read_text())

    def test_keeps_excluded_configuration_and_aborts_on_parse_error(self):
        repo = self.project("excluded")
        manifest = json.loads((repo / MANIFEST).read_bytes())
        manifest["sync_exclusions"] += [str(HOOKS), str(SETTINGS), "CLAUDE.md", str(MANIFEST)]
        put(repo, MANIFEST, manifest)
        before = snapshot(repo)
        self.sync(repo, "--local", "--version", "v3.0.0", migrate=True)
        put(repo, CONFIG, "invalid toml = [")
        broken = snapshot(repo)
        self.sync(repo, "--retire", "--version", "v3.0.0", ok=False)
        self.assertEqual(broken, snapshot(repo))
        put(repo, CONFIG, before[CONFIG][0])
        self.sync(repo, "--retire", "--version", "v3.0.0")
        after = snapshot(repo)
        for path in (SETTINGS, HOOKS, MANIFEST, Path("CLAUDE.md")):
            self.assertEqual(before[path], after[path])
        self.assertIn(GUARD, after)

    def test_migration_sync_does_not_create_an_excluded_provider_root(self):
        repo = self.project("claude-only", behind=True)
        (repo / ".codex").rename(self.tmp / "unused")
        manifest = json.loads((repo / MANIFEST).read_bytes())
        manifest["sync_exclusions"] = [".codex"]
        put(repo, MANIFEST, manifest)
        self.sync(repo, "--local", "--version", "v3.0.0", migrate=True)
        self.assertFalse((repo / ".codex").exists())
        self.assertEqual(json.loads((repo / MANIFEST).read_bytes())["template_version"], "v3.0.0")

    def test_latest_sync_selects_stable_and_explicit_tag_selects_candidate(self):
        put(self.up, ".claude/README.md", "candidate")
        self.tag("v4.0.0-rc.1")
        repo = self.project("stable-only", behind=True)
        self.sync(repo, "--local", "--version", "latest", migrate=True)
        self.assertEqual(json.loads((repo / MANIFEST).read_bytes())["template_version"], "v3.0.0")
        self.sync(repo, "--local", "--version", "v4.0.0-rc.1", migrate=True)
        self.assertEqual(json.loads((repo / MANIFEST).read_bytes())["template_version"], "v4.0.0-rc.1")

    def test_links_and_comment_only_config(self):
        repo = self.project("links")
        personal = repo / "my-settings.json"
        (repo / SETTINGS).rename(personal)
        (repo / SETTINGS).symlink_to(personal)
        original = personal.read_bytes()
        self.sync(repo, "--local", "--version", "v3.0.0", migrate=True)
        self.assertEqual(personal.read_bytes(), original)
        put(repo, CONFIG, b"# adopter notes only\r\n")
        self.sync(repo, "--retire", "--version", "v3.0.0")
        self.assertEqual((repo / CONFIG).read_bytes(), b"# adopter notes only\r\n")
        self.assertTrue((repo / SETTINGS).is_symlink())
        self.assertEqual(personal.read_bytes(), original)

    def test_retained_import_targets(self):
        repo = self.project("kept-import")
        filename = ".claude/CLAUDE.extra.md"
        manifest = json.loads((repo / MANIFEST).read_bytes())
        manifest["sync_exclusions"].append(filename)
        put(repo, MANIFEST, manifest)
        put(repo, filename, "adopter guidance\n")
        other = ".claude/toolbox/CLAUDE.md"
        put(repo, other, "edited instructions\n")
        put(self.up, other, "template instructions\n")
        self.tag("v3.0.1")
        original = (repo / "CLAUDE.md").read_bytes()
        preview = self.sync(repo, "--retire", "--dry-run", "--version", "v3.0.1")
        report = self.sync(repo, "--retire", "--version", "v3.0.1")
        for target in (filename, other):
            self.assertIn("Keep @" + target, preview)
            self.assertIn("Keep @" + target, report)
        self.assertIn("AGENTS.md contains @" + filename, report)
        self.assertEqual((repo / filename).read_text(), "adopter guidance\n")
        self.assertEqual((repo / other).read_text(), "edited instructions\n")
        self.assertEqual((repo / "CLAUDE.md").read_bytes(), original)

        links = self.project("unresolvable-imports")
        put(links, GUARD, (self.up / GUARD).read_bytes())
        put(links, HOOKS, (self.up / HOOKS).read_bytes())
        (links / filename).symlink_to("missing-file")
        (links / other).parent.mkdir(exist_ok=True)
        (links / other).symlink_to(links / GUARD)
        self.sync(links, "--retire", "--version", "v3.0.1")
        self.assertFalse((links / GUARD).exists())
        self.assertEqual((links / "CLAUDE.md").read_bytes(), b"@other\r\n keep")

    def test_predecessor_handoff(self):
        old = subprocess.run(["git", "show", "v0.25.4:" + str(SYNC)], cwd=ROOT, capture_output=True)
        old_script = self.tmp / "previous/template-sync.sh"
        # Shallow development checkouts still exercise both handoff entry points.
        if old.returncode:
            self.addCleanup(print, "v0.25.4 unavailable locally; handoff exercised with the checkout client")
            put(self.tmp, old_script, (ROOT / SYNC).read_bytes())
            helper = (ROOT / SCRIPTS / "semver-compare.sh").read_bytes()
        else:
            put(self.tmp, old_script, old.stdout)
            helper = subprocess.check_output(["git", "show", "v0.25.4:" + str(SCRIPTS / "semver-compare.sh")], cwd=ROOT)
        put(self.tmp, old_script.with_name("semver-compare.sh"), helper)
        tombstone = ROOT / "test/fixtures/template-sync-tombstone.sh"
        shutil.copy(tombstone, self.up / SYNC)
        self.tag("v4.0.0")
        repo = self.project("handoff")
        original = snapshot(repo)
        self.assertIn("kk migrate", self.sync(repo, "--local", "--version", "v4.0.0", script=old_script))
        actual = snapshot(repo)
        manifest = json.loads(actual.pop(MANIFEST)[0])
        baseline = json.loads(original.pop(MANIFEST)[0])
        baseline["variables"].update(CODEX_APPROVAL_POLICY="on-request", SKIP_CAPY="false")
        self.assertEqual(manifest, baseline)
        self.assertEqual(actual, original)
        stage = self.tmp / "ci-stage"
        put(stage / "substituted", Path("claude/toolbox/scripts/template-sync.sh"), tombstone.read_bytes())
        out = self.tmp / "github-output"
        before = snapshot(repo)
        self.sync(repo, "--apply", "--ci", "--version", "v4.0.0", "--output-dir", stage,
                  script=old_script, env={"GITHUB_OUTPUT": str(out)})
        self.assertEqual(out.read_text(), "has_changes=false\n")
        self.assertEqual(snapshot(repo), before)


if __name__ == "__main__":
    unittest.main()
