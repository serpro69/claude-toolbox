import json
from pathlib import Path
import unittest
from unittest.mock import patch

from test_install import InstallFixture, ROOT, cli


launcher = cli.codex_launch
toml = cli.codex_profile.toml_value
BASELINE = json.loads((ROOT / "kk/baseline/codex.json").read_text())
PROFILE = BASELINE["profile"]
MODEL_GROUP = {"model", "model_reasoning_effort", "model_context_window", "model_auto_compact_token_limit"}
OPT_INS = {name: True for name in BASELINE["optIn"]}


class LaunchArguments(unittest.TestCase):
    def test_options_report_the_arguments_that_shape_a_launch(self):
        here = Path.cwd().resolve()
        plain = launcher.launch_options(["hello"])
        self.assertEqual(plain, (here, None, False, [], here, False, False, False, False))
        # Codex selects the workspace of a resumed session, but it still starts in a directory.
        resumed = launcher.launch_options(["-C", "/", "resume"])
        self.assertEqual((resumed.workspace, resumed.directory), (None, Path("/")))
        flags = launcher.launch_options(["-cmodel=x", "--enable", "a", "exec", "--config=b=1", "--disable=c", "-c", "d=2"])
        self.assertEqual(flags.config_flags, ["-c", "model=x", "--enable", "a", "--config", "b=1", "--disable", "c",
                                              "-c", "d=2"])
        for name, spellings in {
                "model": (["-m", "x"], ["-mx"], ["--model", "x"], ["--model=x"], ["--oss"], ["exec", "-m", "x"]),
                "permissions": (["-s", "read-only"], ["-sread-only"], ["--sandbox=read-only"], ["-a", "never"],
                                ["--ask-for-approval", "never"], ["--approve-for-me"],
                                ["--dangerously-bypass-approvals-and-sandbox"], ["--yolo"]),
                "ignore_user_config": (["exec", "--ignore-user-config"],),
                "trust": (["exec", "--trust"],)}.items():
            for args in spellings:
                with self.subTest(args=args):
                    noted = launcher.launch_options(args)._asdict()
                    self.assertEqual([key for key in ("model", "permissions", "ignore_user_config", "trust")
                                      if noted[key]], [name])
        # An option's value and anything after -- are not options.
        for args in (["-i", "--oss"], ["--", "--oss", "--trust", "-s", "x"]):
            with self.subTest(args=args):
                self.assertEqual(launcher.launch_options(args)[5:], (False, False, False, False))

    def test_composing_the_profile_leaves_the_saved_settings_alone(self):
        settings = {"defaults": {"tui": False}, "settings": {"tui": {"model_availability_nux": {"example": 1}}}}
        saved = json.loads(json.dumps(settings))
        cli.codex_profile.compose(ROOT, settings)
        self.assertEqual(settings, saved)
        self.assertIn((("tui", "model_availability_nux", "example"), 1), cli.codex_profile.launch_inputs(ROOT, settings)[1])

    def test_an_unexpected_origin_is_a_failed_lookup(self):
        for origin in (None, "user", {"name": "user"}, {"name": {"type": None}}):
            with self.subTest(origin=origin), patch.object(launcher.codex_app, "origins",
                                                           return_value=({"model": origin}, {})):
                with self.assertRaisesRegex(ValueError, "unexpected origin for model"):
                    launcher.read_origins(Path("/home"), Path("/work"), [], "codex")


class CodexLaunchFlags(InstallFixture):
    def setUp(self):
        super().setUp()
        self.codex = Path(self.env["CODEX_HOME"])
        self.install()

    def apply(self, settings):
        cli.state.write_json(Path(self.env["XDG_CONFIG_HOME"]) / "kk/config.json", {"codex": settings})
        self.invoke(self.link, "apply")

    def layers(self, origins=None, config=None):
        """Say what config.toml and repositories set, the way the fake reports config/read."""
        (self.codex / "fixture-origins.json").write_text(json.dumps(origins or {}))
        (self.codex / "fixture-config.json").write_text(json.dumps(config or {}))

    def launch(self, *args):
        """Return kk's flags as {top-level key: TOML text} and what the launcher printed."""
        run = self.invoke(self.link, "codex", *args)
        argv = json.loads(run.stdout)
        own = argv[:len(argv) - len(args)]
        self.assertEqual(argv[len(own):], list(args))
        self.assertEqual(own[::2], ["-c"] * (len(own) // 2))
        pairs = [flag.partition("=")[::2] for flag in own[1::2]]
        flags = dict(pairs)
        self.assertEqual(len(flags), len(pairs), "one flag for each top-level key")
        return flags, run.stderr

    def instructions(self):
        return (self.toolbox / "codex-instructions.md").read_text()

    def test_every_value_is_passed_once_when_no_other_layer_sets_it(self):
        self.apply({"optIn": OPT_INS, "settings": {"tui": {"animations": True, "notifications": False},
                                                   "docs": {"docs.internal": {"depth": 2}}}})
        flags, printed = self.launch("hello")
        expected = dict(PROFILE, **BASELINE["optIn"])
        # A setting replaces the default at its path and joins the same table as the other defaults.
        expected["tui"] = dict(PROFILE["tui"], animations=True, notifications=False)
        expected["docs"] = {"docs.internal": {"depth": 2}}
        expected["developer_instructions"] = self.instructions()
        self.assertEqual(flags, {key: toml(value) for key, value in expected.items()})
        # Codex splits a dotted flag key, so a table name with a dot stays one quoted key.
        self.assertEqual(flags["docs"], '{ "docs.internal" = { "depth" = 2 } }')
        self.assertEqual(printed, "")

    def test_values_yield_to_the_layer_that_set_them(self):
        self.apply({"optIn": {"approval_policy": True}})
        everything = set(PROFILE) | {"approval_policy", "developer_instructions"}

        def missing(origins=None, config=None):
            self.layers(origins, config)
            return everything - self.launch("hello")[0].keys()

        self.assertEqual(missing({"model": "user"}), MODEL_GROUP)
        self.assertEqual(missing({"model_reasoning_effort": "user"}), {"model_reasoning_effort"})
        self.assertEqual(missing({"model": "packagedDefaults"}), set())
        # Explicit values keep the old profile's place: above config.toml, below a repository.
        self.assertEqual(missing({"approval_policy": "user", "developer_instructions": "user"}), set())
        self.assertEqual(missing({"approval_policy": "project", "developer_instructions": "project"}),
                         {"approval_policy", "developer_instructions"})
        without_status_line = toml({key: value for key, value in PROFILE["tui"].items() if key != "status_line"})
        self.layers({"tui.status_line.0": "user", "tui.status_line.1": "user"})
        self.assertEqual(self.launch("hello")[0]["tui"], without_status_line)
        # The lookup asks about the directory Codex starts in, also when Codex selects the session workspace.
        self.layers()
        repository = self.root / "repository"
        repository.mkdir()
        (repository / "fixture-origins.json").write_text(json.dumps({"approval_policy": "project"}))
        self.assertIn("approval_policy", self.launch("resume")[0])
        self.assertNotIn("approval_policy", self.launch("-C", "repository", "resume")[0])
        # An emptied array has no origin. Codex fills some tables with {} by itself, which sets nothing.
        self.layers(config={"tui": {"status_line": [], "terminal_title": None, "effects": {}, "presets": {}}})
        self.assertEqual(self.launch("hello")[0]["tui"], without_status_line)

    def test_caller_arguments_replace_the_values_they_cover(self):
        self.apply({"optIn": OPT_INS})
        everything = set(PROFILE) | set(OPT_INS) | {"developer_instructions"}
        for args, omitted in ((["-m", "other"], MODEL_GROUP), (["--oss"], MODEL_GROUP),
                              (["-c", "model=other"], MODEL_GROUP),
                              (["-s", "read-only"], set(OPT_INS)), (["--approve-for-me"], set(OPT_INS))):
            with self.subTest(args=args):
                flags, _ = self.launch(*args, "hello")
                self.assertEqual(everything - flags.keys(), omitted)
        # The lookup sees the caller's own flags, so kk's table leaves that value to the caller.
        flags, _ = self.launch("--config=tui.animations=true", "hello")
        self.assertEqual(flags["tui"], toml({key: value for key, value in PROFILE["tui"].items() if key != "animations"}))

    def test_defaults_can_be_switched_off_and_a_chosen_model_drops_kk_sizing(self):
        self.apply({"defaults": {"tui": False}})
        self.assertEqual(set(PROFILE) - self.launch("hello")[0].keys(), {"tui"})
        self.apply({"defaults": {"model": False}})
        self.assertEqual(set(PROFILE) - self.launch("hello")[0].keys(), MODEL_GROUP)
        self.apply({"settings": {"model": "other", "model_context_window": 5}})
        flags, _ = self.launch("hello")
        self.assertEqual(set(PROFILE) - flags.keys(), {"model_reasoning_effort", "model_auto_compact_token_limit"})
        self.assertEqual((flags["model"], flags["model_context_window"]), ('"other"', "5"))
        config = Path(self.env["XDG_CONFIG_HOME"]) / "kk/config.json"
        for defaults, message in (({"whimsy": False}, "unknown codex.defaults key: whimsy"),
                                  ({"tui": "off"}, "codex.defaults.tui must be a boolean")):
            cli.state.write_json(config, {"codex": {"defaults": defaults}})
            self.assertIn(message, self.invoke(self.link, "apply", ok=False).stderr)

    def test_failed_lookup_and_repository_instructions_keep_approved_imports(self):
        self.apply({"optIn": OPT_INS})
        (self.root / "AGENTS.md").write_text("@notes.md\n")
        (self.root / "notes.md").write_text("imported text")
        (self.codex / "fixture-no-config-read").touch()
        run = self.invoke(self.link, "codex", "hello")
        self.assertEqual(json.loads(run.stdout), ["hello"])
        self.assertEqual(run.stderr.count("could not read Codex configuration origins"), 1)
        self.assertIn("without kk defaults, opt-ins and instructions so", run.stderr)
        self.assertIn("no config/read method", run.stderr)
        cli.state.write_json(launcher.import_record(self.toolbox, self.root), {"paths": ["notes.md"], "approved": True})
        flags, printed = self.launch("hello")
        self.assertEqual(list(flags), ["developer_instructions"])
        self.assertIn("imported text", flags["developer_instructions"])
        self.assertEqual(len(printed.splitlines()), 1)
        self.assertIn("without kk defaults and opt-ins so", printed)
        (self.codex / "fixture-no-config-read").unlink()
        self.layers({"developer_instructions": "project"})
        flags, printed = self.launch("hello")
        self.assertEqual(flags.keys(), set(PROFILE) | set(OPT_INS) | {"developer_instructions"})
        self.assertIn("imported text", flags["developer_instructions"])
        self.assertEqual(printed, "")
