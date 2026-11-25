import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from test_install import ROOT, cli


FAKE = str(ROOT / "test/kk/codex")
trust = cli.codex_trust
app = trust.codex_app


class AppServer(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / "codex"
        self.work = self.root / "work"
        self.work.mkdir()
        hooks = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "true"}]}]}}
        guard = self.home / "plugins/cache/agentstakk-local/kk-guard/1/hooks/hooks.json"
        guard.parent.mkdir(parents=True)
        guard.write_text(json.dumps(hooks))

    def fixture(self, name, data):
        (self.home / name).write_text(json.dumps(data))

    def origins(self, *flags):
        found, config = app.origins(self.home, self.work, list(flags), FAKE, 5)
        return {path: origin["name"]["type"] for path, origin in found.items()}, config

    def stub(self, text):
        path = self.root / "stub"
        path.write_text(text)
        path.chmod(0o755)
        return str(path)

    def test_trust_read_applies_flags_like_the_vendor(self):
        table = "features={shell_snapshot=true}"
        for flags, listed in (
                ([], 1),
                (["-c", "features.hooks=false"], 0),
                (["-cfeatures.hooks=false"], 0),
                (["-c=features.hooks=false"], 0),
                (["--config", "features.hooks=false"], 0),
                (["--config=features.hooks=false"], 0),
                (["--disable", "hooks"], 0),
                (["--disable=hooks"], 0),
                (["-c", "features={ \"hooks\" = false }"], 0),
                # A later inline table replaces an earlier leaf under the same key.
                (["-c", "features.hooks=false", "-c", table], 1),
                (["-c", table, "-c", "features.hooks=false"], 0),
                # Codex 0.172 applies feature toggles after every -c flag.
                (["--disable", "hooks", "-c", table], 0),
                (["--enable", "hooks", "-c", "features.hooks=false"], 1)):
            with self.subTest(flags=flags):
                self.assertEqual(len(trust.hooks(self.home, self.work, flags, FAKE)), listed)

    def test_origins_name_the_layer_that_set_each_leaf(self):
        self.fixture("fixture-origins.json", {"model": "user", "approval_policy": "project", "tui.status_line.0": "user"})
        self.fixture("fixture-config.json", {"model": "from-user", "tui": {"status_line": ["model"]}})
        origins, config = self.origins(
            "-c", "model_reasoning_effort=low",
            "-c", 'tui={ "terminal_title" = ["project", "status"], notifications = [], effects = { starfield = false } }',
            "-c", 'docs={ "docs.internal" = { depth = 2, ratio = 1e-05 } }')
        self.assertEqual(origins, {
            "model": "user", "approval_policy": "project", "tui.status_line.0": "user",
            "model_reasoning_effort": "sessionFlags", "tui.terminal_title.0": "sessionFlags",
            "tui.terminal_title.1": "sessionFlags", "tui.effects.starfield": "sessionFlags",
            "docs.docs.internal.depth": "sessionFlags", "docs.docs.internal.ratio": "sessionFlags"})
        self.assertEqual(config["model"], "from-user")
        self.assertEqual(config["model_reasoning_effort"], "low")
        self.assertEqual(config["tui"], {"status_line": ["model"], "terminal_title": ["project", "status"],
                                         "notifications": [], "effects": {"starfield": False}})
        self.assertEqual(config["docs"], {"docs.internal": {"depth": 2, "ratio": 1e-05}})
        self.assertIsNone(config["agents"])

    def test_empty_values_have_no_origin(self):
        origins, config = self.origins("-c", "tui.status_line=[]", "-c", "agents={}")
        self.assertEqual(origins, {})
        self.assertEqual((config["tui"], config["agents"]), ({"status_line": []}, {}))

    def test_a_later_flag_wins_and_sets_a_session_origin_over_other_layers(self):
        self.fixture("fixture-origins.json", {"model": "project"})
        self.fixture("fixture-config.json", {"model": "from-project"})
        origins, config = self.origins("-c", "model=first", "--config=model=gpt-6.2-astra")
        self.assertEqual(origins, {"model": "sessionFlags"})
        self.assertEqual(config["model"], "gpt-6.2-astra")

    def test_aliases_report_the_canonical_name(self):
        self.fixture("fixture-aliases.json", {"agents.max_threads": "agents.max_concurrent_threads_per_session"})
        origins, config = self.origins("-c", "agents={ max_threads = 6, max_depth = 1 }")
        self.assertEqual(origins, {"agents.max_concurrent_threads_per_session": "sessionFlags",
                                   "agents.max_depth": "sessionFlags"})
        self.assertEqual(config["agents"], {"max_concurrent_threads_per_session": 6, "max_depth": 1})

    def test_lookup_asks_for_the_directory_and_rejects_other_shapes(self):
        answer = {"origins": {}, "config": {}}
        with patch.object(app, "session", return_value=[answer]) as session:
            self.assertEqual(app.origins(self.home, self.work, ["-c", "model=x"], FAKE, 5), ({}, {}))
        session.assert_called_once_with(self.home, self.work, ["-c", "model=x"], FAKE,
                                        [("config/read", {"cwd": str(self.work), "includeLayers": False})], 5)
        for result in (None, {"origins": {}}, {"origins": [], "config": {}}, {"origins": {}, "config": None}):
            with self.subTest(result=result), patch.object(app, "session", return_value=[result]):
                with self.assertRaisesRegex(ValueError, "unexpected result"):
                    app.origins(self.home, self.work, [], FAKE, 5)

    def test_one_session_answers_requests_in_order(self):
        (self.home / "fixture-reviewed").write_text("1")
        listed, read = app.session(self.home, self.work, ["-c", "model=x"], FAKE, [
            ("hooks/list", {"cwds": [str(self.work)]}),
            ("config/read", {"cwd": str(self.work), "includeLayers": False})], 5)
        self.assertEqual(listed["data"][0]["hooks"][0]["trustStatus"], "trusted")
        self.assertEqual(read["config"]["model"], "x")

    def test_missing_method_is_distinct_from_other_failures(self):
        (self.home / "fixture-no-config-read").touch()
        with self.assertRaisesRegex(app.NoMethod, "config/read"):
            self.origins()
        self.assertEqual(len(trust.hooks(self.home, self.work, [], FAKE)), 1)
        (self.home / "fixture-no-method").touch()
        with self.assertRaises(trust.NoTrustMethod):
            trust.hooks(self.home, self.work, [], FAKE)
        # A vendor that rejects the handshake must not reach the acknowledgement path.
        rejecting = self.stub("#!" + sys.executable + "\nimport json, sys\nfor line in sys.stdin:\n"
                              "    reply = {'id': json.loads(line).get('id'), 'error': {'code': -32601}}\n"
                              "    print(json.dumps(reply), flush=True)\n")
        with self.assertRaisesRegex(ValueError, "Codex initialize failed"):
            trust.hooks(self.home, self.work, [], rejecting)

    def test_malformed_replies_are_vendor_errors(self):
        for reply, message in (("{'id': request['id']}", "initialize returned no result"),
                               ("{'id': request['id'], 'error': 'broken'}", "initialize failed: broken")):
            malformed = self.stub("#!" + sys.executable + "\nimport json, sys\nfor line in sys.stdin:\n"
                                  "    request = json.loads(line)\n    print('[]', flush=True)\n"
                                  "    print(json.dumps(" + reply + "), flush=True)\n")
            with self.subTest(reply=reply), self.assertRaisesRegex(ValueError, message):
                app.origins(self.home, self.work, [], malformed, 5)

    def test_stopped_and_silent_vendors_fail_within_the_timeout(self):
        with self.assertRaisesRegex(ValueError, "stopped or timed out during initialize"):
            app.origins(self.home, self.work, [], self.stub("#!/bin/sh\nread request\nexit 3\n"), 5)
        started = time.monotonic()
        with self.assertRaisesRegex(ValueError, "stopped or timed out during initialize"):
            app.origins(self.home, self.work, [], self.stub("#!/bin/sh\nexec sleep 60\n"), 0.2)
        self.assertLess(time.monotonic() - started, 30)
