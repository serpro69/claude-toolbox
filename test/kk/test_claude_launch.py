import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

from test_install import ROOT, cli


class ClaudeLaunch(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.home = self.root / "user home"
        self.toolbox = self.home / "toolbox"
        version = "v1.2.3"
        self.release = self.toolbox / "releases" / version
        self.release.parent.mkdir(parents=True)
        self.release.symlink_to(ROOT, target_is_directory=True)
        record = cli.state.load(self.toolbox)
        cli.state.promote(record, version)
        cli.state.write_json(self.toolbox / "state.json", record)
        self.user = self.root / "vendor/settings.json"
        self.project = self.workspace / ".claude/settings.json"
        self.local = self.workspace / ".claude/settings.local.json"
        self.config = self.root / "config/kk/config.json"
        self.env = dict(os.environ, HOME=str(self.home), KK_HOME=str(self.toolbox),
                        CLAUDE_CONFIG_DIR=str(self.user.parent), XDG_CONFIG_HOME=str(self.root / "config"),
                        PATH=str(ROOT / "test/kk") + os.pathsep + os.environ["PATH"])
        self.denies = json.loads((ROOT / "kk/baseline/claude/deny.json").read_text())

    def run_kk(self, *args, ok=True):
        result = subprocess.run([str(ROOT / "kk/bin/kk"), "claude", *map(str, args)],
                                cwd=self.workspace, env=self.env, text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def layer(self, *args):
        return json.loads(self.run_kk("--print-layer", *args).stdout)

    def test_baseline_and_release_paths(self):
        layer = self.layer()
        self.assertEqual(layer["effortLevel"], "high")
        self.assertNotIn("model", layer)
        self.assertEqual(layer["env"], json.loads((ROOT / "kk/baseline/claude.json").read_text())["preferences"]["env"])
        self.assertEqual(layer["permissions"]["allow"], ["Skill(kk:*)", "Read(/{}/**)".format(self.release)])
        self.assertEqual(layer["permissions"]["deny"], self.denies)
        self.assertNotIn("enabledPlugins", layer)
        self.assertEqual(shlex.split(layer["statusLine"]["command"]),
                         ["bash", str(self.release / "klaude-plugin/statusline/statusline_enhanced.sh")])

    def test_lower_layers_yield_per_key_and_variable(self):
        cli.state.write_json(self.user, {"effortLevel": "medium", "env": {"MAX_MCP_OUTPUT_TOKENS": ""}})
        cli.state.write_json(self.project, {"env": {"CLAUDE_STATUSLINE_THEME": "light"},
                                            "enabledPlugins": {"kk@claude-toolbox": True}})
        cli.state.write_json(self.local, {"statusLine": {"type": "command", "command": "true"},
                                          "env": {"CLAUDE_STATUSLINE_MODE": "auto"}})
        layer = self.layer()
        self.assertNotIn("effortLevel", layer)
        self.assertNotIn("statusLine", layer)
        self.assertEqual(layer["env"], {"CLAUDE_CODE_MAX_OUTPUT_TOKENS": "64000"})
        self.assertEqual(layer["enabledPlugins"], {"kk@claude-toolbox": False})
        explicit = self.layer("--settings", '{"enabledPlugins":{"kk@claude-toolbox":true}}')
        self.assertTrue(explicit["enabledPlugins"]["kk@claude-toolbox"])

    def test_nested_session_reads_shared_local_settings(self):
        subprocess.run(["git", "init", "-q", str(self.workspace)], check=True, env=self.env)
        cli.state.write_json(self.local, {"effortLevel": "low"})
        cli.state.write_json(self.project, {"env": {"CLAUDE_STATUSLINE_MODE": "root-only"}})
        self.workspace = self.workspace / "nested"
        self.workspace.mkdir()
        layer = self.layer()
        self.assertNotIn("effortLevel", layer)
        self.assertIn("CLAUDE_STATUSLINE_MODE", layer["env"])

    def test_baseline_respects_per_model_effort(self):
        model = "claude-opus-5-5"
        cli.state.write_json(self.user, {"modelSettings": {model: {"effortLevel": "low", "other": 7}}})
        layer = self.layer()
        self.assertEqual(layer["effortLevel"], "high")
        self.assertEqual(layer["modelSettings"], {model: {"effortLevel": "low"}})
        overridden = self.layer("--settings", '{"effortLevel":"medium"}')
        self.assertNotIn("effortLevel", overridden.get("modelSettings", {}).get(model, {}))

    def test_launcher_masks_enabled_public_and_pilot_copies(self):
        copies = {"kk@agentstakk": True, "kk@claude-toolbox": True, "kk@toolbox": True}
        cli.state.write_json(self.project, {"enabledPlugins": dict(copies, unrelated=True)})
        self.assertEqual(self.layer()["enabledPlugins"], dict.fromkeys(copies, False))
        self.assertTrue(json.loads(self.project.read_text())["enabledPlugins"]["kk@toolbox"])

    def test_explicit_setting_sources(self):
        cli.state.write_json(self.user, {"effortLevel": "low"})
        cli.state.write_json(self.project, {"enabledPlugins": {"kk@claude-toolbox": True}})
        self.local.write_text("{invalid")
        layer = self.layer("--setting-sources", "project")
        self.assertEqual(layer["effortLevel"], "high")
        self.assertFalse(layer["enabledPlugins"]["kk@claude-toolbox"])
        self.assertNotIn("enabledPlugins", self.layer("--setting-sources=user"))
        self.assertIn("effortLevel", self.layer("--restricted"))

    def test_switches_and_opt_ins(self):
        cli.state.write_json(self.config, {"claude": {
            "instructions": False, "defaults": dict.fromkeys(("skills", "readRelease", "statusLine", "effortLevel", "env"), False),
            "optIn": {"mkdir": True, "webSearch": True}}, "launchNotice": False})
        self.assertEqual(self.layer(), {"permissions": {"allow": ["Bash(mkdir:*)", "WebSearch"], "deny": self.denies}})
        cli.state.write_json(self.config, {"claude": {"defaults": {"skills": False}}})
        self.assertEqual(self.layer()["permissions"]["allow"], ["Read(/{}/**)".format(self.release)])

    def test_override_named_file_and_cli_composition(self):
        cli.state.write_json(self.config, {"claude": {"settingsFile": "personal.json", "settings": {
            "model": "one", "effortLevel": "low", "env": {"CUSTOM": "one"},
            "permissions": {"ask": ["Bash"], "allow": ["WebSearch"], "deny": ["Read(first)"]}}}})
        cli.state.write_json(self.config.parent / "personal.json", {"model": "two", "env": {"NAMED": "yes"},
            "permissions": {"allow": ["WebSearch"], "deny": ["Read(/private/**)"]}})
        self.assertEqual(self.layer()["model"], "two")
        extra = {"model": "three", "env": {"CUSTOM": "three"}, "permissions": {"allow": [],
                 "ask": ["Edit"], "deny": [], "defaultMode": "plan"}}
        cli.state.write_json(self.workspace / "extra.json", extra)
        layer = self.layer("--settings", "extra.json")
        self.assertEqual(layer, self.layer("--settings=" + json.dumps(extra)))
        self.assertEqual(layer["model"], "three")
        self.assertEqual(layer["effortLevel"], "low")
        self.assertEqual(layer["env"]["CUSTOM"], "three")
        self.assertEqual(layer["env"]["NAMED"], "yes")
        self.assertEqual(layer["permissions"]["ask"], ["Bash", "Edit"])
        self.assertEqual(layer["permissions"]["allow"].count("WebSearch"), 1)
        self.assertEqual(layer["permissions"]["defaultMode"], "plan")
        self.assertEqual(layer["permissions"]["deny"],
                         ["Read(first)", "Read(/{}/private/**)".format(self.config.parent)] + self.denies)

    def test_one_private_file_and_forwarded_arguments(self):
        # Both the validator (in its scratch cwd) and the session must select this binary.
        (self.workspace / "bin").symlink_to(ROOT / "test/kk", target_is_directory=True)
        self.env["PATH"] = "bin" + os.pathsep + os.environ["PATH"]
        cli.state.write_json(self.config, {"claude": {"settings": {"permissions": {"deny": []}}}})
        result = self.run_kk("--settings", '{"effortLevel":"low"}', "-p", "--settings={}", "--", "--settings", "prompt")
        args = json.loads(result.stdout)
        self.assertEqual(args[0], "--settings")
        self.assertEqual(args[2:], ["-p", "--", "--settings", "prompt"])
        path = Path(args[1])
        self.assertIn(self.toolbox, path.parents)
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        before = json.loads(path.read_text())
        self.assertEqual(before["effortLevel"], "low")
        self.assertEqual(before["permissions"]["deny"], self.denies)
        # A second, still-running session has its own immutable settings.
        live = path.with_name("{}-{}.json".format(os.getpid(), "a" * 32))
        live.write_bytes(path.read_bytes())
        self.run_kk("--settings", '{"effortLevel":"high"}', "-p")
        self.assertFalse(path.exists())
        self.assertEqual(json.loads(live.read_text()), before)

    def test_child_hooks_keep_launcher_homes_after_chdir(self):
        vendor = self.workspace / "bin" / "claude"
        vendor.parent.mkdir()
        vendor.write_text('#!/bin/sh\ncd /\nprintf "%s\\n" "$KK_HOME" "$XDG_CONFIG_HOME" "$CODEX_HOME"\n')
        vendor.chmod(0o755)
        self.env.update(PATH=str(vendor.parent) + os.pathsep + self.env["PATH"],
                        KK_HOME=os.path.relpath(self.toolbox, self.workspace),
                        XDG_CONFIG_HOME="../config", CODEX_HOME="../codex")
        homes = self.run_kk("-p").stdout.splitlines()
        self.assertTrue(all(os.path.isabs(path) for path in homes), homes)
        self.assertEqual([Path(path).resolve() for path in homes],
                         [self.toolbox, self.root / "config", self.root / "codex"])

    def test_invalid_inputs_stop_before_exec(self):
        for value, diagnostic in (([], "object"), ({"claude": {"instructions": None}}, "boolean"),
                                  ({"claude": {"optIn": {"mkdir": "yes"}}}, "boolean"),
                                  ({"claude": {"default": {}}}, "unknown"),
                                  ({"claude": {"settings": {"permissions": {"deny": None}}}}, "array"),
                                  ({"claude": {"settingsFile": "missing.json"}}, "missing.json")):
            with self.subTest(value=value):
                cli.state.write_json(self.config, value)
                self.assertIn(diagnostic, self.run_kk(ok=False).stderr)
        self.config.write_text("{broken")
        self.assertIn(str(self.config), self.run_kk(ok=False).stderr)
        self.config.unlink()
        for argv in (("--settings",), ("--settings=missing",), ("--settings", "{broken"),
                     ("--settings", '{"permissions":false}')):
            with self.subTest(argv=argv):
                self.assertTrue(self.run_kk(*argv, ok=False).stderr.strip())
        self.assertFalse((self.home / "calls").exists())

    def test_schema_invalid_preference_stops_launch_from_every_override_source(self):
        bad = {"effortLevel": "low", "statusLine": 42}
        named = self.root / "settings.json"
        cli.state.write_json(named, bad)
        for config, args in (({"settings": bad}, []), ({"settingsFile": str(named)}, []),
                             ({}, ["--settings", json.dumps(bad)])):
            with self.subTest(config=config, args=args):
                cli.state.write_json(self.config, {"claude": config})
                self.assertIn("statusLine", self.run_kk(*args, ok=False).stderr)
        self.assertFalse((self.home / "calls").exists())
        self.assertEqual(list((self.toolbox / "claude-layers").iterdir()), [])
