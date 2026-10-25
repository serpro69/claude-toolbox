#!/usr/bin/env python3
"""
Tests for klaude-plugin/scripts/guard/guard.py, the kk guard engine.

Run:  python3 -I test/guard/test_guard.py        (or bash test/test-guard.sh)

Most cases call the engine in-process: a check that raises `Denied` refuses
the call, a check that returns allows it. A small set runs `guard.py` as a
real process to pin the stdout/stderr/exit-code contract.

Python floor is 3.8. Verified under: Python 3.10.12 (oldest interpreter on
the authoring machine, 2026-10-25). No 3.8 or 3.9 interpreter was available,
so `test_engine_parses_as_python_3_8` additionally parses the engine with
`ast.parse(feature_version=(3, 8))`, which rejects syntax newer than 3.8
that the parser knows about (`match`, parenthesised context managers). It
is a drift guard, not a full 3.8 run.

Fixtures (test/fixtures/guard/):
  glob-cases.json   pattern/path table for `glob_to_regex`
  corpus.jsonl      one hook payload per line, replayed through `decide`

Corpus row schema: `tool_name`, `tool_input`, optional `cwd` (default: the
project root), optional `project_root` (default: the sandbox root), optional
`project_config` / `user_config` (paths relative to the corpus file, applied
through `KK_GUARD_PROJECT_CONFIG` / `KK_GUARD_USER_CONFIG` for that row
only; rows without them point both at nonexistent files, the plugin-only
condition), optional `pending_task` (skip until that task lands), `expect`
(`allow` or `deny`), optional `category` (the expected deny category), `note`.

String values may use `{root}`, `{home}` and `{tmp}` placeholders. The
runner substitutes a per-run sandbox: `{root}` is a project directory with a
`sub/` child, `{home}` a fake home containing `.ssh/id_rsa`, and `{tmp}` a
scratch directory holding `kk-secret-link` (a symlink to that key) and
`kk-ssh-link` (a symlink to the `.ssh` directory). The sandbox also exposes
`home-link` and `project-link`, symlinks to the home and project directories,
for the tests that give the engine logical (symlinked) roots.
"""

import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
GUARD = os.path.join(REPO, "klaude-plugin", "scripts", "guard", "guard.py")
RULES = os.path.join(REPO, "klaude-plugin", "scripts", "guard", "guard-rules.json")
FIXTURES = os.path.join(REPO, "test", "fixtures", "guard")
GLOB_CASES = os.path.join(FIXTURES, "glob-cases.json")
CORPUS = os.path.join(FIXTURES, "corpus.jsonl")

# Tasks whose corpus rows are still pending. Remove a number here when that
# task lands and its rows must pass.
PENDING_TASKS = {3, 4, 5, 8, 13}


def load_guard():
    spec = importlib.util.spec_from_file_location("guard", GUARD)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load " + GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = load_guard()


def read_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise AssertionError("%s:%d is not valid JSON: %s" % (path, number, exc))
            row["_line"] = number
            rows.append(row)
    return rows


def substitute(value, mapping):
    if isinstance(value, str):
        for key, replacement in mapping.items():
            value = value.replace("{" + key + "}", replacement)
        return value
    if isinstance(value, dict):
        return {k: substitute(v, mapping) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, mapping) for v in value]
    return value


class Sandbox(object):
    """Per-run directories the corpus placeholders point at."""

    def __init__(self):
        self.base = tempfile.mkdtemp(prefix="kk-guard-test-")
        self.root = os.path.join(self.base, "project")
        self.home = os.path.join(self.base, "home")
        self.tmp = os.path.join(self.base, "tmp")
        os.makedirs(os.path.join(self.root, "sub"))
        os.makedirs(os.path.join(self.home, ".ssh"))
        os.makedirs(self.tmp)
        key = os.path.join(self.home, ".ssh", "id_rsa")
        with open(key, "w") as handle:
            handle.write("not a real key\n")
        os.symlink(key, os.path.join(self.tmp, "kk-secret-link"))
        os.symlink(os.path.join(self.home, ".ssh"), os.path.join(self.tmp, "kk-ssh-link"))
        # Logical aliases of HOME and the project root, the macOS /tmp and
        # /var/folders condition reproduced on any host.
        self.home_link = os.path.join(self.base, "home-link")
        self.root_link = os.path.join(self.base, "project-link")
        os.symlink(self.home, self.home_link)
        os.symlink(self.root, self.root_link)
        self.mapping = {"root": self.root, "home": self.home, "tmp": self.tmp}

    def env(self, project_root=None, project_config=None, user_config=None, home=None):
        return {
            "HOME": home or self.home,
            "CLAUDE_PROJECT_DIR": project_root or self.root,
            "KK_GUARD_RULES": RULES,
            "KK_GUARD_PROJECT_CONFIG": project_config or os.path.join(self.base, "nonexistent-project.json"),
            "KK_GUARD_USER_CONFIG": user_config or os.path.join(self.base, "nonexistent-user.json"),
        }


def outcome(fn, *args, **kwargs):
    """('allow', None) or ('deny', Denied)."""
    try:
        fn(*args, **kwargs)
    except guard.Denied as denied:
        return "deny", denied
    return "allow", None


class GlobMatcherTests(unittest.TestCase):
    def setUp(self):
        self.root = "/work/project"
        self.parent = "/work"
        self.home = "/users/me"
        self.mapping = {"root": self.root, "parent": self.parent, "home": self.home}

    def test_fixture_table(self):
        cases = read_json(GLOB_CASES)["cases"]
        self.assertGreater(len(cases), 20)
        for case in cases:
            with self.subTest(pattern=case["pattern"], path=case["path"]):
                if case["expect"] == "reject":
                    with self.assertRaises(ValueError, msg=case.get("note", "")):
                        guard.glob_to_regex(case["pattern"], self.root, self.home)
                    continue
                regex = guard.glob_to_regex(case["pattern"], self.root, self.home)
                path = substitute(case["path"], self.mapping)
                matched = regex.match(path) is not None
                self.assertEqual(
                    matched, case["expect"] == "match",
                    "%s against %s: expected %s (%s); regex %s"
                    % (case["pattern"], path, case["expect"], case.get("note", ""), regex.pattern),
                )

    def test_every_baseline_glob_compiles_and_has_an_accepted_shape(self):
        rules = read_json(RULES)
        shape = re.compile(r"^(\./\*\*/|~/|//)")
        for glob in rules["secrets"]:
            with self.subTest(glob=glob):
                self.assertRegex(glob, shape)
                guard.glob_to_regex(glob, self.root, self.home)

    def test_empty_pattern_is_rejected(self):
        with self.assertRaises(ValueError):
            guard.glob_to_regex("", self.root, self.home)


class DeclarationTests(unittest.TestCase):
    def test_baseline_loads(self):
        rules = guard.load_rules(RULES)
        self.assertEqual(rules["version"], 1)
        for category in ("filesystem", "git", "infra", "privilege"):
            self.assertIn(category, rules["destructive"])
        self.assertIn("$TMPDIR", rules["tmp_roots"])
        self.assertIn(".claude/settings.json", rules["selfmod"])

    def test_destructive_rules_use_only_the_frozen_vocabulary(self):
        allowed = {"program", "subcommand", "flags_any", "flags_all", "flags_none", "exempt", "reason", "codex"}
        rules = guard.load_rules(RULES)
        for category, entries in rules["destructive"].items():
            for rule in entries:
                with self.subTest(category=category, rule=rule.get("program")):
                    self.assertTrue(set(rule) <= allowed, "unknown fields: %s" % (set(rule) - allowed))
                    self.assertIsInstance(rule["program"], str)
                    self.assertIsInstance(rule["reason"], str)
                    sub = rule.get("subcommand")
                    self.assertTrue(sub is None or isinstance(sub, str) or isinstance(sub, list))
                    for key in ("flags_any", "flags_all", "flags_none"):
                        for pattern in rule.get(key, []):
                            re.compile(pattern)
                            if re.match(r"^\^-[a-zA-Z]\$$", pattern):
                                self.fail("%s %s: short flag %s must use the cluster form" % (category, key, pattern))

    def test_codex_records_only_on_the_five_unconditional_literals(self):
        rules = guard.load_rules(RULES)
        with_records = set()
        for category, entries in rules["destructive"].items():
            for rule in entries:
                for record in rule.get("codex", []):
                    with_records.add(rule["program"])
                    self.assertEqual(set(record), {"pattern", "match", "not_match"})
                    self.assertEqual(record["pattern"][0], rule["program"])
                    self.assertTrue(record["match"] and record["not_match"])
                    for example in record["match"]:
                        self.assertEqual(example.split()[0], rule["program"], example)
                    for example in record["not_match"]:
                        self.assertNotEqual(example.split()[0], rule["program"], example)
        self.assertEqual(with_records, {"rm", "shred", "sudo", "su", "doas"})

    def test_specific_predicates_the_design_names(self):
        rules = guard.load_rules(RULES)
        git = {(r["program"], json.dumps(r.get("subcommand"))): r for r in rules["destructive"]["git"]}
        self.assertIn("flags_none", git[("git", '"restore"')])
        branch_rules = [r for r in rules["destructive"]["git"] if r.get("subcommand") == "branch"]
        self.assertTrue(any("flags_all" in r for r in branch_rules))
        self.assertTrue(any("flags_any" in r for r in branch_rules))
        self.assertIn(("git", '["stash", "drop"]'), git)
        self.assertEqual(rules["destructive"]["filesystem"][0]["exempt"], "targets_under_tmp")

    def test_unknown_version_fails_closed(self):
        # `True == 1` and `1.0 == 1` in Python; only the integer 1 may pass.
        for version in (99, True, 1.0, "1", None):
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
                json.dump({"version": version, "secrets": [], "destructive": {}, "tmp_roots": [], "selfmod": []}, handle)
            self.addCleanup(os.unlink, handle.name)
            with self.subTest(version=version):
                kind, denied = outcome(guard.load_rules, handle.name)
                self.assertEqual(kind, "deny")
                self.assertEqual(denied.category, "failure")
                self.assertIn("version", denied.reason())

    def test_missing_and_invalid_files_fail_closed(self):
        kind, denied = outcome(guard.load_rules, "/nonexistent/guard-rules.json")
        self.assertEqual((kind, denied.category), ("deny", "failure"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write("{not json")
        self.addCleanup(os.unlink, handle.name)
        kind, denied = outcome(guard.load_rules, handle.name)
        self.assertEqual((kind, denied.category), ("deny", "failure"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write("")
        self.addCleanup(os.unlink, handle.name)
        kind, denied = outcome(guard.load_rules, handle.name)
        self.assertEqual((kind, denied.category), ("deny", "failure"))


class PayloadTests(unittest.TestCase):
    def test_project_root_precedence(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "x"}, "cwd": "/cwd"})
        ctx = guard.parse_payload(payload, {"KK_GUARD_PROJECT_ROOT": "/adapter", "CLAUDE_PROJECT_DIR": "/claude"})
        self.assertEqual((ctx.project_root, ctx.exec_dir), ("/adapter", "/cwd"))
        ctx = guard.parse_payload(payload, {"CLAUDE_PROJECT_DIR": "/claude"})
        self.assertEqual((ctx.project_root, ctx.exec_dir), ("/claude", "/cwd"))
        ctx = guard.parse_payload(payload, {})
        self.assertEqual((ctx.project_root, ctx.exec_dir), ("/cwd", "/cwd"))

    def test_home_must_be_absolute(self):
        # A missing, empty or relative HOME must yield the password-database
        # home (absolute) or fail closed; it must never yield a relative anchor.
        for bad in ({}, {"HOME": ""}, {"HOME": "relative/home"}):
            with self.subTest(env=bad):
                try:
                    home = guard.home_dir(bad)
                except guard.Denied as denied:
                    self.assertEqual(denied.category, "failure")
                else:
                    self.assertTrue(os.path.isabs(home), home)
        self.assertEqual(guard.home_dir({"HOME": "/users/me"}), "/users/me")

    def test_missing_cwd_uses_the_fallback(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "x"}})
        ctx = guard.parse_payload(payload, {}, fallback_cwd="/fallback")
        self.assertEqual(ctx.exec_dir, "/fallback")

    def test_permission_mode_is_carried(self):
        payload = json.dumps({"tool_name": "Bash", "tool_input": {}, "cwd": "/c", "permission_mode": "bypassPermissions"})
        self.assertEqual(guard.parse_payload(payload, {}).permission_mode, "bypassPermissions")

    def test_bad_payloads_fail_closed(self):
        for raw in ("", "   ", "{not json", "[1,2]", json.dumps({"tool_input": {}}), json.dumps({"tool_name": "Read", "tool_input": "x"})):
            with self.subTest(raw=raw):
                kind, denied = outcome(guard.parse_payload, raw, {})
                self.assertEqual((kind, denied.category), ("deny", "failure"))

    def test_relative_roots_fail_closed(self):
        # A relative anchor could never match an absolute file_path, which
        # would silently allow every secret; refuse instead.
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "/x/.env"}, "cwd": "relative/dir"})
        kind, denied = outcome(guard.parse_payload, payload, {})
        self.assertEqual((kind, denied.category), ("deny", "failure"))
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "/x/.env"}, "cwd": "/abs"})
        kind, denied = outcome(guard.parse_payload, payload, {"CLAUDE_PROJECT_DIR": "rel"})
        self.assertEqual((kind, denied.category), ("deny", "failure"))


class ResolveTests(unittest.TestCase):
    def test_tilde_relative_and_symlink(self):
        sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, sandbox.base)
        requested, resolved = guard.resolve("~/.ssh/id_rsa", sandbox.root, sandbox.home)
        self.assertEqual(requested, os.path.join(sandbox.home, ".ssh", "id_rsa"))
        requested, resolved = guard.resolve("../.env", os.path.join(sandbox.root, "sub"), sandbox.home)
        self.assertEqual(requested, os.path.join(sandbox.root, ".env"))
        link = os.path.join(sandbox.tmp, "kk-secret-link")
        requested, resolved = guard.resolve(link, sandbox.root, sandbox.home)
        self.assertEqual(requested, os.path.normpath(link))
        self.assertEqual(resolved, os.path.realpath(os.path.join(sandbox.home, ".ssh", "id_rsa")))

    def test_parent_of_a_symlink_is_resolved_physically(self):
        # /tmp/kk-ssh-link -> HOME/.ssh, so link/../.netrc is HOME/.netrc to
        # the kernel; a lexical collapse would say /tmp/.netrc instead.
        sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, sandbox.base)
        path = os.path.join(sandbox.tmp, "kk-ssh-link", "..", ".netrc")
        requested, resolved = guard.resolve(path, sandbox.root, sandbox.home)
        self.assertEqual(requested, os.path.join(sandbox.tmp, ".netrc"))
        self.assertEqual(resolved, os.path.realpath(os.path.join(sandbox.home, ".netrc")))


class FileToolTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)
        self.ctx = guard.Context("Read", {}, self.sandbox.root, self.sandbox.root, self.sandbox.home)
        self.policy = guard.compile_policy(guard.load_rules(RULES), self.ctx)

    def test_read_without_a_path_fails_closed(self):
        kind, denied = outcome(guard.check_file_tool, "Read", {}, self.ctx, self.policy)
        self.assertEqual((kind, denied.category), ("deny", "failure"))

    def test_grep_without_a_path_is_allowed(self):
        self.assertEqual(outcome(guard.check_file_tool, "Grep", {"pattern": "x"}, self.ctx, self.policy)[0], "allow")

    def test_deny_names_the_tool_the_path_and_the_glob(self):
        kind, denied = outcome(guard.check_file_tool, "Read", {"file_path": ".env"}, self.ctx, self.policy)
        self.assertEqual(kind, "deny")
        reason = denied.reason()
        self.assertTrue(reason.startswith("kk guard: secrets — Read of .env matches ./**/.env. Way through: "), reason)
        self.assertIn("redacted copy", reason)

    def test_symlinked_home_and_project_root_still_deny(self):
        # HOME and the project root given through symlinks (the macOS /tmp
        # and /var/folders layout): both the logical and the physical spelling
        # of a secret must be denied, and ordinary files still allowed.
        ctx = guard.Context("Read", {}, self.sandbox.root_link, self.sandbox.root_link, self.sandbox.home_link)
        policy = guard.compile_policy(guard.load_rules(RULES), ctx)
        cases = [
            (os.path.join(self.sandbox.root, ".env"), "deny"),               # physical project path
            (os.path.join(self.sandbox.root_link, ".env"), "deny"),          # logical project path
            (os.path.join(self.sandbox.home, ".ssh", "id_rsa"), "deny"),     # physical home path
            (os.path.join(self.sandbox.home_link, ".netrc"), "deny"),        # logical home path
            (os.path.join(self.sandbox.tmp, "kk-secret-link"), "deny"),      # symlink resolving into physical home
            (os.path.join(self.sandbox.tmp, "kk-ssh-link", "..", ".netrc"), "deny"),  # parent of a symlink
            (os.path.join(self.sandbox.root, "README.md"), "allow"),
            (os.path.join(self.sandbox.root_link, "src", "main.go"), "allow"),
            (os.path.join(self.sandbox.tmp, "kk-ssh-link", "..", "notes.txt"), "allow"),
        ]
        for path, expect in cases:
            with self.subTest(path=path):
                kind, denied = outcome(guard.check_file_tool, "Read", {"file_path": path}, ctx, policy)
                self.assertEqual(kind, expect, denied.reason() if denied else "")

    def test_newline_inside_a_guarded_directory_is_still_matched(self):
        path = os.path.join(self.sandbox.home, ".aws", "cred\nentials")
        kind, denied = outcome(guard.check_file_tool, "Read", {"file_path": path}, self.ctx, self.policy)
        self.assertEqual(kind, "deny")


class CorpusTests(unittest.TestCase):
    def test_replay(self):
        sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, sandbox.base)
        rows = read_jsonl(CORPUS)
        self.assertGreater(len(rows), 10)
        replayed = 0
        for row in rows:
            label = "line %d: %s" % (row["_line"], row.get("note", ""))
            with self.subTest(case=label):
                self.assertIn(row.get("expect"), ("allow", "deny"), label)
                if row.get("expect") == "deny":
                    self.assertIn("category", row, label)
                if row.get("pending_task") in PENDING_TASKS:
                    continue
                row = substitute(row, sandbox.mapping)
                project_root = row.get("project_root") or sandbox.root
                env = sandbox.env(
                    project_root=project_root,
                    project_config=os.path.join(FIXTURES, row["project_config"]) if row.get("project_config") else None,
                    user_config=os.path.join(FIXTURES, row["user_config"]) if row.get("user_config") else None,
                )
                payload = {
                    "tool_name": row["tool_name"],
                    "tool_input": row["tool_input"],
                    "cwd": row.get("cwd") or project_root,
                }
                kind, denied = outcome(guard.decide, json.dumps(payload), env)
                reason = denied.reason() if denied else ""
                self.assertEqual(kind, row["expect"], "%s\n%s" % (label, reason))
                if kind == "deny":
                    self.assertEqual(denied.category, row["category"], "%s\n%s" % (label, reason))
                replayed += 1
        self.assertGreater(replayed, 10)


class ProcessContractTests(unittest.TestCase):
    """Run the engine as a process: stdout JSON + stderr + exit 2 on deny,
    silence + exit 0 on allow, fail closed on bad input."""

    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)

    def run_engine(self, stdin, env_extra=None):
        env = dict(self.sandbox.env())
        env["PATH"] = os.environ.get("PATH", "")
        env.update(env_extra or {})
        proc = subprocess.run(
            [sys.executable, "-I", GUARD], input=stdin.encode("utf-8"),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=self.sandbox.root,
        )
        return proc.returncode, proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")

    def payload(self, tool_name, tool_input):
        return json.dumps({"tool_name": tool_name, "tool_input": tool_input, "cwd": self.sandbox.root})

    def test_allow_is_silent(self):
        code, out, err = self.run_engine(self.payload("Read", {"file_path": "README.md"}))
        self.assertEqual((code, out, err), (0, "", ""))

    def test_deny_uses_both_channels(self):
        code, out, err = self.run_engine(self.payload("Read", {"file_path": ".env"}))
        self.assertEqual(code, 2)
        decision = json.loads(out)
        self.assertEqual(set(decision), {"hookSpecificOutput"})
        inner = decision["hookSpecificOutput"]
        self.assertEqual(inner["hookEventName"], "PreToolUse")
        self.assertEqual(inner["permissionDecision"], "deny")
        self.assertTrue(inner["permissionDecisionReason"].startswith("kk guard: secrets — "))
        self.assertEqual(err.strip(), inner["permissionDecisionReason"])

    def test_invalid_json_fails_closed(self):
        code, out, err = self.run_engine("{not json")
        self.assertEqual(code, 2)
        self.assertIn("kk guard: failure", json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIn("nothing was executed", err)

    def test_empty_rules_file_fails_closed(self):
        code, out, err = self.run_engine(self.payload("Read", {"file_path": "README.md"}), {"KK_GUARD_RULES": os.devnull})
        self.assertEqual(code, 2)
        self.assertIn("kk guard: failure", err)

    def test_wrong_version_fails_closed(self):
        path = os.path.join(self.sandbox.base, "rules-v99.json")
        with open(path, "w") as handle:
            json.dump({"version": 99, "secrets": [], "destructive": {}, "tmp_roots": [], "selfmod": []}, handle)
        code, out, err = self.run_engine(self.payload("Read", {"file_path": "README.md"}), {"KK_GUARD_RULES": path})
        self.assertEqual(code, 2)
        self.assertIn("version", err)

    def test_relative_path_from_a_subdirectory_cwd(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "../.env"}, "cwd": os.path.join(self.sandbox.root, "sub")})
        code, out, err = self.run_engine(payload)
        self.assertEqual(code, 2, err)

    def test_physical_path_denied_when_roots_are_symlinks(self):
        env = {"HOME": self.sandbox.home_link, "CLAUDE_PROJECT_DIR": self.sandbox.root_link}
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": os.path.join(self.sandbox.root, ".env")}, "cwd": self.sandbox.root_link})
        code, out, err = self.run_engine(payload, env)
        self.assertEqual(code, 2, err)
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": os.path.join(self.sandbox.tmp, "kk-secret-link")}, "cwd": self.sandbox.root_link})
        code, out, err = self.run_engine(payload, env)
        self.assertEqual(code, 2, err)


class PythonFloorTests(unittest.TestCase):
    def test_engine_parses_as_python_3_8(self):
        with open(GUARD, "r", encoding="utf-8") as handle:
            source = handle.read()
        ast.parse(source, GUARD, feature_version=(3, 8))
        self.assertNotIn("removeprefix", source)
        self.assertNotIn("removesuffix", source)


if __name__ == "__main__":
    unittest.main(verbosity=1)
