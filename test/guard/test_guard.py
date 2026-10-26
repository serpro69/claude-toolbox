#!/usr/bin/env python3
"""
Tests for klaude-plugin/scripts/guard/guard.py, the kk guard engine.

Run:  python3 -I test/guard/test_guard.py        (or bash test/test-guard.sh)

Most cases call the engine in-process: a check that raises `Denied` refuses
the call, a check that returns allows it. A small set runs `guard.py` as a
real process to pin the stdout/stderr/exit-code contract.

Python floor is 3.8. Verified under Python 3.9.6 on macOS (2026-10-26) and
Python 3.10.12 on Linux (2026-10-25). No 3.8 interpreter was available,
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
PENDING_TASKS = set()


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
        # macOS may return /var/... while realpath resolves /private/var/....
        # Keep fixture roots physical; explicit *-link fixtures cover aliases.
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="kk-guard-test-"))
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
        git = {(r["program"], json.dumps(r.get("subcommand"))) for r in rules["destructive"]["git"]}
        restore_rules = [r for r in rules["destructive"]["git"] if r.get("subcommand") == "restore"]
        self.assertTrue(any("flags_none" in r for r in restore_rules))
        branch_rules = [r for r in rules["destructive"]["git"] if r.get("subcommand") == "branch"]
        self.assertTrue(any("flags_all" in r for r in branch_rules))
        self.assertTrue(any("flags_any" in r for r in branch_rules))
        self.assertIn(("git", '["stash", "drop"]'), git)
        self.assertEqual(rules["destructive"]["filesystem"][0]["exempt"], "targets_under_tmp")

    def test_equivalent_destructive_spellings_are_declared(self):
        # Accepted 2026-10-25: spellings with the same data-losing effect as a
        # baseline rule. This pins the declaration's regexes and subcommands;
        # the corpus also exercises them through the complete matcher.
        rules = guard.load_rules(RULES)["destructive"]

        def find(category, program, subcommand, key):
            for rule in rules[category]:
                if rule["program"] == program and rule.get("subcommand") == subcommand and key in rule:
                    return [re.compile(p) for p in rule[key]]
            self.fail("no %s rule for %s %r with %s" % (category, program, subcommand, key))

        def any_hit(regexes, token):
            return any(r.search(token) for r in regexes)

        push = find("git", "git", "push", "flags_any")
        for token in ("-d", "-fd", "--delete", "--force", "-f", "+main", "+refs/heads/x:refs/heads/x", ":old-branch"):
            self.assertTrue(any_hit(push, token), token)
        for token in ("origin", "main", "main:main", "-u", "-n", "--dry-run", "--tags"):
            self.assertFalse(any_hit(push, token), token)

        delete_re, force_re = find("git", "git", "branch", "flags_all")
        for args in (["-d", "-f", "x"], ["-df", "x"], ["--delete", "--force", "x"], ["-fd", "x"]):
            self.assertTrue(any(delete_re.search(a) for a in args) and any(force_re.search(a) for a in args), args)
        for args in (["-d", "x"], ["--delete", "x"], ["-f", "new", "start"]):
            self.assertFalse(any(delete_re.search(a) for a in args) and any(force_re.search(a) for a in args), args)

        restore = find("git", "git", "restore", "flags_any")
        for token in ("--worktree", "-W", "-SW", "-WS"):
            self.assertTrue(any_hit(restore, token), token)
        for token in ("--staged", "-S", "-p", "file.txt"):
            self.assertFalse(any_hit(restore, token), token)

        rsync = find("filesystem", "rsync", None, "flags_any")
        for token in ("--del", "--delete", "--delete-after", "--delete-excluded"):
            self.assertTrue(any_hit(rsync, token), token)
        for token in ("--delay-updates", "-a", "--dry-run"):
            self.assertFalse(any_hit(rsync, token), token)

        destroy = find("infra", "terraform", "apply", "flags_any")
        for token in ("-destroy", "--destroy", "-destroy=true"):
            self.assertTrue(any_hit(destroy, token), token)
        for token in ("-auto-approve", "-target=x", "plan.tfplan"):
            self.assertFalse(any_hit(destroy, token), token)

        docker = {json.dumps(r.get("subcommand")) for r in rules["infra"] if r["program"] == "docker"}
        self.assertIn('["container", "rm"]', docker)
        self.assertIn('["image", "rm"]', docker)

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


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)
        self.ctx = guard.Context("Bash", {}, self.sandbox.root, self.sandbox.root, self.sandbox.home)
        self.policy = guard.compile_policy(guard.load_rules(RULES), self.ctx)

    def check(self, command, category=None):
        command = substitute(command, self.sandbox.mapping)
        kind, denied = outcome(guard.check_command, command, self.ctx, self.policy)
        self.assertEqual(kind, "deny" if category else "allow", command + ": " + (denied.reason() if denied else "allowed"))
        if category:
            self.assertEqual(denied.category, category, denied.reason())

    def test_extraction_preserves_original_bodies_and_quoted_operands(self):
        for command, body in [("sh -c 'rm -rf x'", "rm -rf x"), ('echo "$(rm x)"', "rm x"),
                              ("cat <(rm x)", "rm x"), ("cat >('rm' x)", "'rm' x"),
                              ("echo `rm x`", "rm x")]:
            with self.subTest(command=command):
                self.assertIn(body, [b.text for b in guard.extract_bodies(command)])
        tokens, _, _ = guard._shell_scan('cat "/repo with spaces/.env"')
        self.assertEqual(guard.command_words(tokens), ["cat", "/repo with spaces/.env"])
        self.assertEqual(guard.defang('git commit -m "clean up"'), "git commit -m Q")
        self.assertEqual(guard.defang("r'm' -rf x"), "rm -rf x")

    def test_separators_and_wrapper_option_values(self):
        for separator in ("&&", "||", ";", "|", "|&", "&", "\n"):
            with self.subTest(separator=separator):
                self.check("true " + separator + " cat .env", "secrets")
        for wrapper in ("A=1", "env A=1", "env -u NAME", "nohup", "timeout -s TERM 5",
                        "nice -n 10", "sudo -u user", "xargs -I ITEM", "env --"):
            with self.subTest(wrapper=wrapper):
                # The privilege rule now denies sudo before inspecting its
                # shell body; other wrappers still reach the secret check.
                self.check(wrapper + " sh -c 'cat .env'", "destructive" if wrapper.startswith("sudo ") else "secrets")
                self.assertEqual(list(guard.command_position_tokens(wrapper + " /bin/cat README.md")), ["cat"])

    def test_shell_secret_reads(self):
        for command in ("cat .env", "/bin/cat ./.env", "c'at' .env", "cat .en\\v",
                        'cat "{root}/folder with spaces/.env"', "cat ~/.ssh/id_rsa",
                        "cat {tmp}/kk-secret-link", "cat {tmp}/kk-ssh-link/../.netrc",
                        "sh -c 'cat .env'", 'echo "$(cat .env)"', "echo `cat .env`",
                        "cat <(cat .env)", "cat >(cat .env)", "cat < .env",
                        'sh -c \'echo "$(cat .env)"\''):
            with self.subTest(command=command):
                self.check(command, "secrets")

    def test_benign_commands_and_literal_prose(self):
        for command in ("cat .env.example", 'echo "see .env.example"', "find . -not -path './.git/*'",
                        "cat .claude/settings.json", "cat build/out.txt", "cat app.log",
                        "echo x 2>/dev/null", "echo x >&2", "echo '$(cat .env)'",
                        'echo "literal ; cat .env"', "echo ok # cat .env", "git commit -m 'clean up build/ and dist/'"):
            with self.subTest(command=command):
                self.check(command)

    def test_subdirectory_root_is_not_reanchored(self):
        self.ctx.exec_dir = os.path.join(self.sandbox.root, "sub")
        self.check("cat ../.env", "secrets")
        self.check("cat ../README.md")
        self.check("echo x > ../.claude/settings.json", "selfmod")

    def test_literal_and_expandable_heredocs(self):
        self.check('git commit -m "$(cat <<\'EOF\'\nrm -rf x\n$(cat .env)\n`cat .env`\nbuild/ dist/\nEOF\n)"')
        for delimiter in ("'EOF'", '"EOF"', "E'O'F", r"\EOF"):
            with self.subTest(delimiter=delimiter):
                self.check("cat <<" + delimiter + "\n$(cat .env)\nEOF\n")
        self.check("cat <<- 'EOF'\n\t$(cat .env)\n\tEOF\n")
        self.check("cat <<EOF\n$(cat .env)\nEOF\n", "secrets")
        self.check("cat <<EOF\n'$(cat .env)'\nEOF\n", "secrets")
        self.check("cat <<EOF\n`cat .env`\nEOF\n", "secrets")
        self.check("cat <<EOF\n\\$(cat .env)\nEOF\n")
        self.check("cat <<'ONE' <<TWO\n$(cat .env)\nONE\n$(cat .env)\nTWO\n", "secrets")
        self.check("cat <<'EOF' > .claude/settings.json\nordinary data\nEOF\n", "selfmod")
        self.check("echo 'cat <<EOF'")

    def test_shell_and_unknown_heredoc_consumers_keep_scripts(self):
        for consumer in ("bash", "./scripts/import.sh", "cat | ./scripts/import.sh"):
            with self.subTest(consumer=consumer):
                self.check(consumer + " <<'EOF'\ncat .env\nEOF\n", "secrets")
        self.check("cat <<'EOF' | ./scripts/import.sh\ncat .env\nEOF\n", "secrets")
        for consumer in ("bash", "./scripts/import.sh"):
            bodies = guard.extract_bodies(consumer + " <<'EOF'\nrm -rf x\nEOF\n")
            self.assertIn("rm -rf x\n", [b.text for b in bodies])

    def test_mutation_targets_and_read_controls(self):
        for command in ("echo x > .claude/settings.json", 'echo x >>".claude/settings.json"',
                        "echo x 2>.claude/settings.json", "echo x &>.claude/settings.json",
                        "tee .claude/kk-guard.json", "sed -i 's/a/b/' ~/.claude/kk-guard.json",
                        "dd if=README.md of=.codex/hooks.json", "cp x .claude/settings.json",
                        "install -m 600 x .claude/settings.json", "mv .codex/hooks.json /tmp/saved.json",
                        "mv .codex /tmp/", "ln -s x .claude/settings.json", "ln -sf .codex/hooks.json /tmp/x",
                        "cp -t .codex/scripts x", "mv --target-directory=/tmp .codex"):
            with self.subTest(command=command):
                self.check(command, "selfmod")
        for command in ("mv src/a.go src/b.go", "cp .claude/settings.json /tmp/copy.json",
                        "cat .claude/settings.json", "sed 's/a/b/' .claude/settings.json",
                        "echo x > .claude/settings.json.bak", "tee .codex-other/hooks.json"):
            with self.subTest(command=command):
                self.check(command)
        for command in ("echo x > .env", "tee .env", "dd of=.env"):
            with self.subTest(command=command):
                self.check(command, "secrets")

    def test_selfmod_aliases_and_file_tools(self):
        os.makedirs(os.path.join(self.sandbox.root, ".codex"))
        link = os.path.join(self.sandbox.tmp, "codex-link")
        os.symlink(os.path.join(self.sandbox.root, ".codex"), link)
        self.check("tee " + link + "/hooks.json", "selfmod")
        self.check("mv " + link + " /tmp/saved", "selfmod")
        for tool, key in (("Edit", "file_path"), ("Write", "file_path"), ("NotebookEdit", "notebook_path")):
            for path in (".claude/settings.json", ".codex", ".codex/scripts/new.py", "~/.claude/plugins/cache/a"):
                with self.subTest(tool=tool, path=path):
                    kind, denied = outcome(guard.check_file_tool, tool, {key: path}, self.ctx, self.policy)
                    self.assertEqual((kind, denied.category), ("deny", "selfmod"))
        ctx = guard.Context("Edit", {}, self.sandbox.root_link, self.sandbox.root_link, self.sandbox.home_link)
        policy = guard.compile_policy(guard.load_rules(RULES), ctx)
        kind, denied = outcome(guard.check_file_tool, "Edit", {"file_path": self.sandbox.root + "/.codex/hooks.json"}, ctx, policy)
        self.assertEqual((kind, denied.category), ("deny", "selfmod"))

    def test_inline_interpreter_mutations(self):
        for code in ("open('.claude/settings.json','w')", "open('.claude/settings.json', mode='a')",
                     "open('.claude/settings.json','r+')", "Path('.claude/settings.json').write_text('x')",
                     "shutil.copy('x', '.claude/settings.json')", "shutil.move('.codex', '/tmp/x')",
                     "os.rename('.codex/hooks.json', '/tmp/x')", "os.remove('.claude/settings.json')"):
            with self.subTest(code=code):
                self.check('python3 -c "' + code + '"', "selfmod")
        for code in ("fs.writeFileSync('.claude/settings.json', x)", "fs.renameSync('.codex', '/tmp/x')",
                     "fs.rmSync('.codex/hooks.json')"):
            with self.subTest(code=code):
                self.check('node -e "' + code + '"', "selfmod")
        self.check('python3 -c "open(\'.env\').read()"', "secrets")
        self.check('python3 -c "open(\'.claude/settings.json\').read()"')
        self.check('python3 -c "shutil.copy(\'.claude/settings.json\', \'/tmp/x\')"')
        self.check("python3 - <<'PY'\nopen('.claude/settings.json', 'w')\nPY\n", "selfmod")
        self.check("python3 - <<'PY'\nopen('.claude/settings.json').read()\nPY\n")

    def test_malformed_structure_fails_closed(self):
        for command in ("cat 'unterminated", "echo $(cat README.md", "cat <<EOF\ndata", "cat \\"):
            with self.subTest(command=command):
                self.check(command, "failure")

    def test_literal_shell_spellings_and_option_clusters(self):
        for command in ("cat $'.env'", r"cat $'\x2eenv'", 'cat $".env"', "dd if=.env of=/tmp/out"):
            with self.subTest(command=command):
                self.check(command, "secrets")
        for command in ("echo x > $'.claude/settings.json'", "sed -Ei 's/a/b/' .claude/settings.json",
                        "cp -t.codex/scripts payload.py", "cp -ft.codex/scripts payload.py",
                        'python3 -c"open(\'.claude/settings.json\',\'w\')"',
                        'python3 -Ic "open(\'.claude/settings.json\',\'w\')"',
                        'python3 -Bc "open(\'.claude/settings.json\',\'w\')"',
                        'python3 - <<<"open(\'.claude/settings.json\',\'w\')"'):
            with self.subTest(command=command):
                self.check(command, "selfmod")
        for command in ("sed -i '' 's/a/b/' src/file.txt", "sed -Ei '' 's/a/b/' src/file.txt",
                        "sed -eiscript .claude/settings.json", "cp -t{tmp} payload.py",
                        "cat $'.env.example'", "cat <<<'$(cat .env)'", "cat file\u00a0name.txt",
                        "cat file\vname.txt", "cat file\fname.txt", "echo $'$(cat .env)'"):
            with self.subTest(command=command):
                self.check(command)

    def test_interpreter_keyword_argument_order(self):
        for code in ("open(mode='w', file='.claude/settings.json')",
                     "shutil.copy(dst='.claude/settings.json', src='x')",
                     "shutil.move(dst='/tmp/x', src='.codex')", "os.remove(path='.claude/settings.json')"):
            with self.subTest(code=code):
                self.check('python3 -c "' + code + '"', "selfmod")
        self.check('python3 -c "open(mode=\'r\', file=\'.claude/settings.json\')"')

    def test_here_string_pipeline_consumers(self):
        self.check('cat <<<\'open(".claude/settings.json","w")\' | python3', "selfmod")
        self.check("cat <<<'cat .env' | bash", "secrets")
        self.check('cat <<<\'open(".claude/settings.json").read()\' | python3')
        self.check("cat <<<'cat README.md' | bash")


class DestructiveTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)
        # Static analysis needs no actual checkout here. The filesystem sandbox
        # is under /tmp and would deliberately qualify for temporary cleanup.
        self.ctx = guard.Context("Bash", {}, "/work/project", "/work/project", "/users/guard-test")
        self.policy = guard.compile_policy(guard.load_rules(RULES), self.ctx, {})

    def check(self, command, category=None):
        kind, denied = outcome(guard.check_command, command, self.ctx, self.policy)
        self.assertEqual(kind, "deny" if category else "allow", command + ": " + (denied.reason() if denied else "allowed"))
        if category:
            self.assertEqual(denied.category, category, denied.reason())
        return denied

    def test_predicates_and_global_options(self):
        denied = ("git restore f", "git branch -D x", "git branch -rfD x",
                  "git branch --delete --force x", "git stash drop", "docker volume rm v",
                  "git -C /work/other -c advice.statusHints=false --git-dir=/work/git clean -fd",
                  "git -C/work/other -cfoo=bar reset --hard", "docker --context remote volume rm v",
                  "kubectl --context dev -n testing delete pod x", "helm --kube-context dev uninstall x",
                  "terraform -chdir=/work/infra destroy", 'git "clean" -fd', "g'it' cl'ean' -fd")
        allowed = ("git restore --staged f", "git restore -S f", "git branch --delete x",
                   "git branch -d x", "git stash list", "docker volume ls", "git -C /work/other status",
                   "git -c alias.clean=status status", "docker --context remote ps",
                   'git commit -m "git clean -fd"', "echo 'rm -rf x'", "printf '%s' 'sudo rm x'")
        for command in denied:
            with self.subTest(command=command):
                self.check(command, "destructive")
        for command in allowed:
            with self.subTest(command=command):
                self.check(command)

    def test_wrappers_and_executable_bodies(self):
        for command in ("/bin/rm x", "r'm' x", r"r\m x", "'rm' x", "$'rm' x",
                        '"/tools with spaces/rm" x', "sh -c 'rm -rf x'", 'echo "$(rm x)"',
                        "echo `rm x`", "cat <(rm x)", "cat >(rm x)", "xargs rm", "xargs -I ITEM rm ITEM",
                        "env -u NAME A=1 /bin/rm x", "timeout -s TERM 5 rm x", "nohup rm x",
                        "nice -n 10 env rm x", "sudo -u user ls", "env sudo ls", "command sudo ls",
                        "timeout -vs TERM 5 rm x", "xargs -rn 1 rm x",
                        "env -S 'rm -rf x'", "env --split-string='rm -rf x'",
                        "cat <<EOF\n$(rm -rf x)\nEOF\n", "bash <<'EOF'\nrm -rf x\nEOF\n",
                        "cat <<<'rm x' | bash", "cat <<'EOF' | ./import.sh\nrm -rf x\nEOF\n"):
            with self.subTest(command=command):
                self.check(command, "destructive")
        for separator in ("&&", "||", ";", "|", "|&", "&", "\n"):
            self.check("echo ok " + separator + " rm x", "destructive")
        self.check("cat <<'EOF'\n$(rm x)\nEOF\n")

    def test_temporary_cleanup_boundaries(self):
        for command in ("rm -rf /tmp/kk-test", "rm /tmp/a /tmp/b", 'rm "/tmp/path with spaces/x"',
                        "rm -- /tmp/-f", "cd /tmp/kk-test && rm -rf ./x",
                        'cd "$D" && rm -rf /tmp/x', "cd ../other && rm /tmp/x",
                        "env -C /work/project rm /tmp/x", "sh -c 'rm /tmp/x'",
                        "cd /tmp/kk-test && sh -c 'rm x'", 'cd /tmp/kk-test && echo "$(rm x)"',
                        "cd /tmp/kk-test && bash <<'EOF'\nrm x\nEOF\n"):
            with self.subTest(command=command):
                self.check(command)
        for command in ('rm -rf "$T"', "rm -rf /tmp/*", "rm /tmp/?.txt", "rm /tmp/[ab]",
                        "rm /tmp/a /work/b", "rm /tmp/../etc", "rm /tmp-other/x", "rm -f", "xargs rm /tmp/a",
                        "cd /tmp/kk-test || rm ./x", "cd /tmp/kk-test; rm ./x",
                        "(cd /tmp/kk-test) && rm ./x", "cd /tmp/kk-test | rm ./x",
                        "cd /tmp/kk-test && false || rm ./x", "rm /tmp/{a,../../work/x}"):
            with self.subTest(command=command):
                self.check(command, "destructive")
        for command in ("rm -rf /", "rm -rf ~", "rm -rf ."):
            self.check(command, "selfmod")

    def test_directory_changes_do_not_inherit_a_temporary_payload_cwd(self):
        self.ctx.exec_dir = self.sandbox.tmp
        for command in ("cd /work/project && rm -rf ./work", "env -C /work/project rm -rf ./work",
                        "env -C/work/project rm -rf ./work", "env --chdir=/work/project rm -rf ./work",
                        'cd "$D" && rm ./x', "pushd /work/project && rm ./x", "popd && rm ./x",
                        "cd .. && rm ./x", 'rm "$(printf /work/x)"',
                        "cd /work/project && sh -c 'rm x'", 'cd /work/project && echo "$(rm x)"',
                        "env -C /work/project sh -c 'rm x'"):
            with self.subTest(command=command):
                self.check(command, "destructive")
        self.check("sh -c 'cd /work/project && true' && rm ./x")
        self.check("cd /work/project && cat .env", "secrets")

    def test_tmpdir_comes_from_the_engine_environment_and_is_canonical(self):
        rules = guard.load_rules(RULES)
        rules["tmp_roots"] = ["$TMPDIR"]
        link = os.path.join(self.sandbox.base, "tmp-link")
        os.symlink(self.sandbox.tmp, link)
        self.policy = guard.compile_policy(rules, self.ctx, {"TMPDIR": link})
        self.check("rm " + self.sandbox.tmp + "/ordinary")
        self.check("rm " + link + "/ordinary")
        os.symlink("/work/outside", os.path.join(self.sandbox.tmp, "escape"))
        self.check("rm " + self.sandbox.tmp + "/escape/file", "destructive")
        self.check("rm " + self.sandbox.tmp + "/escape/../file", "destructive")
        self.check("rm " + self.sandbox.tmp + "-sibling/file", "destructive")
        self.policy = guard.compile_policy(rules, self.ctx, {})
        self.check("TMPDIR=/work env rm /work/x", "destructive")
        self.check("rm " + self.sandbox.tmp + "/ordinary", "destructive")

    def test_conditional_and_pipeline_cd_cannot_grant_an_exemption(self):
        for command in ("true || cd /tmp/kk-safe && rm work", "printf x | cd /tmp/kk-safe && rm work",
                        "! cd /tmp/kk-safe && rm work", "env cd /tmp/kk-safe && rm work",
                        "cd /tmp/$(printf ../work/project) && rm valuable"):
            with self.subTest(command=command):
                self.check(command, "destructive")
        self.check("true && cd /tmp/kk-safe && rm work")
        self.check("true || cd /tmp/kk-safe && rm /tmp/work")

    def test_uncertain_cd_keeps_known_secret_and_mutation_locations(self):
        for prefix in ("cd /tmp/kk-safe && cd /work/project; ", "cd /tmp/kk-safe && cd /work/project || ",
                       "cd /tmp/kk-safe && cd /work/project\n"):
            with self.subTest(prefix=prefix):
                self.check(prefix + "cat .env", "secrets")
                self.check(prefix + "printf x > .claude/settings.json", "selfmod")
                self.check(prefix + "cat README.md")
        self.check("cd /tmp/kk-safe && cd /work/project/sub; cat ../.env", "secrets")
        self.check("cd /tmp && env -C ../work/project cat .env", "secrets")
        self.check("cd /tmp && env -C ../work/project sh -c 'printf x > .claude/settings.json'", "selfmod")
        self.check("cd /tmp && env -C ../work/project cat README.md")

    def test_env_split_string_preserves_tail_arguments_and_options(self):
        for command in ("env -S 'rm /tmp/kk-safe' /work/valuable",
                        "env --split-string='rm /tmp/kk-safe' /work/valuable",
                        "env -S '-C /work/project rm' valuable",
                        "env -iS 'rm /tmp/kk-safe' /work/valuable"):
            with self.subTest(command=command):
                self.check(command, "destructive")
        self.check("env -S 'rm /tmp/kk-safe' /tmp/another")
        self.check("env git log -S 'rm -rf x'")
        self.ctx.exec_dir = self.sandbox.tmp
        self.check("env -iC /work/project rm valuable", "destructive")
        self.check("env -iC /work/project printf ok")
        self.check("env -iC/work/project sh -c 'rm valuable'", "destructive")
        self.check("env -S 'rm /tmp/kk-safe' $(printf /work/valuable)", "destructive")
        self.check("env -S 'rm /tmp/kk-safe' \"/tmp/path with spaces\"")
        self.check("printf /work/valuable | xargs env -S 'rm /tmp/kk-safe'", "destructive")
        self.check("printf ok | xargs env -S 'printf %s'")

    def test_temp_exemption_never_overrides_secrets_or_selfmod(self):
        self.ctx = guard.Context("Bash", {}, self.sandbox.root, self.sandbox.root, self.sandbox.home)
        self.policy = guard.compile_policy(guard.load_rules(RULES), self.ctx, {})
        self.check("rm .env", "secrets")
        self.check("rm -rf .", "selfmod")
        self.check("rm .claude/settings.json", "selfmod")
        self.check("rm -rf .codex", "selfmod")
        self.check("rm " + self.sandbox.tmp + "/kk-secret-link", "secrets")
        self.check("rm ordinary-build-output")

    def test_reason_names_the_rule_category_and_remedy(self):
        denied = self.check("git clean -fd", "destructive")
        self.assertEqual(denied.detail, "git")
        reason = denied.reason()
        self.assertIn(guard.load_rules(RULES)["destructive"]["git"][0]["reason"], reason)
        self.assertIn("`git` category", reason)
        self.assertIn("! <command>", reason)
        self.assertIn("~/.claude/kk-guard.json", reason)

    def test_invalid_rule_predicates_fail_closed(self):
        for update in ({"flags_any": ["["]}, {"flags_all": "--force"}, {"subcommand": 3},
                       {"unknown": "ignored?"}, {"exempt": "typo"}):
            rules = guard.load_rules(RULES)
            rules["destructive"]["git"][0].update(update)
            with self.subTest(update=update):
                kind, denied = outcome(guard.compile_policy, rules, self.ctx, {})
                self.assertEqual((kind, denied.category), ("deny", "failure"))


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)
        self.env = self.sandbox.env(project_root="/work/ops/cluster-a")

    def fixture(self, layer, name):
        self.env["KK_GUARD_%s_CONFIG" % layer.upper()] = os.path.join(FIXTURES, layer + "-config", name + ".json")

    def config(self, layer, value):
        path = os.path.join(self.sandbox.base, layer + ".json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(value, handle)
        self.env["KK_GUARD_%s_CONFIG" % layer.upper()] = path

    def check(self, command, category=None, tool="Bash", cwd=None):
        payload = {"tool_name": tool, "cwd": cwd or self.env["CLAUDE_PROJECT_DIR"],
                   "tool_input": {"command" if tool == "Bash" else "file_path": command}}
        try:
            messages = guard.decide(json.dumps(payload), self.env)
        except guard.Denied as denied:
            self.assertEqual(denied.category, category, denied.reason())
            return denied.messages
        self.assertIsNone(category, "unexpected allow: " + command)
        return messages

    def test_project_additions_preserve_baseline_and_support_new_categories(self):
        self.fixture("project", "additions")
        for path in ("private.txt", ".env"):
            self.assertEqual(self.check(path, "secrets", tool="Read"), [])
        for command in ("git fetch", "git clean -fd", "deploy prod"):
            self.check(command, "destructive")
        for path in ("policy.json", ".claude/settings.json"):
            self.check(path, "selfmod", tool="Edit")
        self.check("README.md", tool="Read")

    def test_project_unknown_keys_warn_without_loosening_or_dropping_additions(self):
        self.fixture("project", "unknown-keys")
        for command, category, tool in (("git clean -fd", "destructive", "Bash"),
                                        ("rm ./work", "destructive", "Bash"),
                                        ("private.txt", "secrets", "Read"),
                                        (".claude/settings.json", "selfmod", "Edit")):
            warnings = "\n".join(self.check(command, category, tool))
            for key in ("disable_categories", "disable_selfmod", "allow_patterns", "tmp_roots"):
                self.assertIn(key, warnings)

    def test_invalid_project_discards_all_additions_and_reports_problem(self):
        cases = [[], {"version": True}, {"version": 1.0}, {"version": 99},
                 {"version": 1, "secrets": ["./**/private.txt", "*.token"]},
                 {"version": 1, "secrets": ["./**/[a]"]},
                 {"version": 1, "secrets": ["//etc/passwd"]},
                 {"version": 1, "secrets": ["./**/private.txt"], "selfmod": [42]},
                 {"version": 1, "destructive": []},
                 {"version": 1, "destructive": {"git": [{"program": "git", "reason": "bad", "flags_any": ["["]}]}},
                 {"version": 1, "destructive": {"git": [{"program": "git", "reason": "bad", "typo": True}]}}]
        for value in cases:
            with self.subTest(config=value):
                self.config("project", value)
                self.assertTrue(self.check(".env", "secrets", tool="Read"))
                self.assertTrue(self.check("private.txt", tool="Read"))
                self.check("git clean -fd", "destructive")
        self.fixture("project", "invalid")
        self.assertTrue(self.check("cat .env", "secrets"))

    def test_global_and_longest_prefix_union_is_component_scoped(self):
        self.fixture("user", "scoped")
        for command in ("sudo ls", "kubectl delete pod x", "git clean -nd", "git fetch"):
            self.check(command)
        for command in ("git clean -fd", "shred file"):
            self.check(command, "destructive")  # /work contributes nothing
        self.check(".claude/settings.json", "selfmod", tool="Edit")
        for root in ("/work/app", "/work/ops-extra", "/work/op"):
            self.env["CLAUDE_PROJECT_DIR"] = root
            self.check("kubectl delete pod x", "destructive")
        self.env["CLAUDE_PROJECT_DIR"] = "/work/ops"
        self.check("kubectl delete pod x")

    def test_project_root_not_execution_directory_selects_user_entry(self):
        self.fixture("user", "scoped")
        self.check("kubectl delete pod x", cwd="/work/app")
        self.env["CLAUDE_PROJECT_DIR"] = "/work/app"
        self.check("kubectl delete pod x", "destructive", cwd="/work/ops")

    def test_user_prefix_uses_real_project_root_and_root_prefix(self):
        self.config("user", {"version": 1, "projects": {
            "/": {"disable_categories": ["privilege"]},
            self.sandbox.root: {"disable_categories": ["infra"]}}})
        self.env["CLAUDE_PROJECT_DIR"] = self.sandbox.root_link
        self.check("kubectl delete pod x")
        self.check("sudo ls", "destructive")  # only the longest prefix
        self.env["CLAUDE_PROJECT_DIR"] = "/unrelated"
        self.check("sudo ls")
        self.check("kubectl delete pod x", "destructive")

    def test_allow_patterns_are_local_to_commands_and_extracted_bodies(self):
        self.fixture("user", "scoped")
        for command in ("git clean -nd", "env FOO=x timeout 5 /usr/bin/git clean -nd",
                        "sh -c 'git clean -nd'", 'echo "$(git clean -nd)"'):
            self.check(command)
        for command in ("git clean -fd", "git clean -nd; rm -rf ./work",
                        "git clean -nd && git clean -fd", "git clean -nd | shred file",
                        'git clean -nd "$(rm ./work)"', "git clean -nd `rm ./work`",
                        "sh -c 'git clean -nd; rm ./work'", "sudo rm ./work"):
            self.check(command, "destructive")
        self.config("user", {"version": 1, "projects": {"*": {"allow_patterns": ["^sh ", "^env "]}}})
        self.check("sh -c 'rm ./work'", "destructive")
        self.check("env rm ./work", "destructive")

    def test_allow_patterns_never_disable_secrets_or_selfmod(self):
        self.fixture("project", "additions")
        self.fixture("user", "allow-all")
        self.check("git clean -fd; rm ./work")
        self.check("deploy prod")
        for command in ("cat .env", "cat ./private.txt", "git clean -fd .env"):
            self.check(command, "secrets")
        for command in ("echo x > .claude/settings.json", "mv policy.json /work/saved",
                        'python3 -c "open(\'.claude/settings.json\',\'w\')"'):
            self.check(command, "selfmod")

    def test_disable_selfmod_is_union_scoped_and_never_disables_secrets(self):
        for entries in ({"*": {"disable_selfmod": True}, "/work/ops": {"disable_selfmod": False}},
                        {"*": {"disable_selfmod": False}, "/work/ops": {"disable_selfmod": True}}):
            self.config("user", {"version": 1, "projects": entries})
            self.fixture("project", "additions")
            self.check(".claude/settings.json", tool="Edit")
            self.check("policy.json", tool="Edit")
            self.check("echo x > .claude/settings.json")
            self.check(".env", "secrets", tool="Edit")
            self.check("private.txt", "secrets", tool="Edit")
        self.env["CLAUDE_PROJECT_DIR"] = "/work/app"
        self.check(".claude/settings.json", "selfmod", tool="Edit")

    def test_category_disable_covers_project_additions_and_new_categories(self):
        self.fixture("project", "additions")
        self.config("user", {"version": 1, "projects": {"*": {"disable_categories": ["git", "release", "secrets", "selfmod"]}}})
        self.check("git clean -fd")
        self.check("git fetch")
        self.check("deploy prod")
        self.check("private.txt", "secrets", tool="Read")
        self.check("policy.json", "selfmod", tool="Edit")

    def test_invalid_user_discards_all_loosening_keeps_project_additions(self):
        self.fixture("project", "additions")
        for entry in ({"disable_categories": "git"}, {"disable_selfmod": "true"},
                      {"disable_categories": ["git"], "allow_patterns": ["["]},
                      {"disable_categories": ["git", None]}, {"allow_patterns": [42]}):
            self.config("user", {"version": 1, "projects": {"*": entry}})
            self.assertTrue(self.check("git clean -fd", "destructive"))
            self.check("private.txt", "secrets", tool="Read")
            self.check(".claude/settings.json", "selfmod", tool="Edit")
        for value in ({"version": True, "projects": {}}, {"version": 1, "projects": []},
                      {"version": 1, "projects": {"relative": {"disable_selfmod": True}}}):
            self.config("user", value)
            self.assertTrue(self.check(".claude/settings.json", "selfmod", tool="Edit"))

    def test_invalid_project_does_not_disable_valid_user_config(self):
        self.fixture("project", "invalid")
        self.fixture("user", "scoped")
        self.assertTrue(self.check("kubectl delete pod x"))
        self.assertTrue(self.check("cat .env", "secrets"))

    def test_default_locations_and_fresh_reload(self):
        self.env = self.sandbox.env()
        for layer, base in (("project", self.sandbox.root), ("user", self.sandbox.home)):
            self.env.pop("KK_GUARD_%s_CONFIG" % layer.upper())
            os.makedirs(os.path.join(base, ".claude"))
        project = os.path.join(self.sandbox.root, ".claude", "kk-guard.json")
        user = os.path.join(self.sandbox.home, ".claude", "kk-guard.json")
        with open(project, "w") as handle:
            json.dump(read_json(os.path.join(FIXTURES, "project-config", "additions.json")), handle)
        with open(user, "w") as handle:
            json.dump({"version": 1, "projects": {"*": {"disable_categories": ["git"]}}}, handle)
        self.check("../private.txt", "secrets", tool="Read", cwd=os.path.join(self.sandbox.root, "sub"))
        self.check("git clean -fd")
        with open(user, "w") as handle:
            handle.write("{")
        self.assertTrue(self.check("git clean -fd", "destructive"))


class PatchTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)

    def check(self, patch, cwd=None, env=None):
        return outcome(guard.decide, json.dumps({
            "tool_name": "apply_patch", "tool_input": {"command": patch},
            "cwd": cwd or self.sandbox.root,
        }), env or self.sandbox.env())

    def test_headers_and_multiple_files(self):
        for header in ("Add File", "Update File", "Delete File", "Move to"):
            with self.subTest(header=header):
                patch = "*** Begin Patch\n*** Update File: src/a.py\n*** %s: ../.env\n@@\n-a\n+b\n*** End Patch" % header
                kind, denied = self.check(patch, os.path.join(self.sandbox.root, "sub"))
                self.assertEqual(kind, "deny")
                self.assertEqual(denied.category, "secrets")
        for path in (".codex/hooks.json", ".claude/settings.json", ".codex"):
            with self.subTest(path=path):
                kind, denied = self.check("*** Begin Patch\n*** Update File: %s\n@@\n-a\n+b\n*** End Patch" % path)
                self.assertEqual(kind, "deny")
                self.assertEqual(denied.category, "selfmod")

    def test_context_and_added_text_are_not_headers(self):
        patch = ("*** Begin Patch\n*** Update File: src/main.py\n@@\n"
                 " *** Delete File: .env\n-*** Update File: .env\n"
                 "+*** Move to: .codex/hooks.json\n+rm -rf /\n*** End Patch")
        self.assertEqual(self.check(patch)[0], "allow")

    def test_header_whitespace_matches_codex(self):
        patch = "  *** Begin Patch\r\n\t*** Add File: .env  \r\n+x\r\n *** End Patch\r\n"
        self.assertEqual(self.check(patch)[1].category, "secrets")
        # The extra space after the marker belongs to the literal filename.
        patch = "*** Begin Patch\n*** Add File:  .env\n+x\n*** End Patch"
        self.assertEqual(self.check(patch)[0], "allow")

    def test_paths_are_literal_and_follow_symlinks(self):
        patch = "*** Begin Patch\n*** Add File: ~/.ssh/ordinary.txt\n+x\n*** End Patch"
        self.assertEqual(self.check(patch)[0], "allow")
        patch = "*** Begin Patch\n*** Update File: %s\n@@\n-a\n+b\n*** End Patch" % os.path.join(self.sandbox.tmp, "kk-secret-link")
        self.assertEqual(self.check(patch)[1].category, "secrets")

    def test_delete_policy_and_overrides(self):
        patch = "*** Begin Patch\n*** Delete File: src/old.py\n*** End Patch"
        self.assertEqual(self.check(patch, "/work/guard-project")[1].category, "destructive")
        self.assertEqual(self.check(patch, self.sandbox.tmp)[0], "allow")
        for filename in ("a[1]", "a$literal", "-file", "two words"):
            with self.subTest(filename=filename):
                literal_patch = "*** Begin Patch\n*** Delete File: %s\n*** End Patch" % filename
                self.assertEqual(self.check(literal_patch, self.sandbox.tmp)[0], "allow")
                self.assertEqual(self.check(literal_patch, "/work/guard-project")[1].category, "destructive")
        config = os.path.join(self.sandbox.base, "user.json")
        with open(config, "w") as handle:
            json.dump({"version": 1, "projects": {"*": {"disable_categories": ["filesystem"]}}}, handle)
        self.assertEqual(self.check(patch, "/work/guard-project", self.sandbox.env(user_config=config))[0], "allow")
        # A temporary path still receives secrets/selfmod checks first.
        patch = "*** Begin Patch\n*** Delete File: .codex/hooks.json\n*** End Patch"
        self.assertEqual(self.check(patch)[1].category, "selfmod")

    def test_patch_normalizes_dotdot_before_following_symlinks(self):
        os.makedirs(os.path.join(self.sandbox.tmp, "inside"))
        os.symlink(os.path.join(self.sandbox.tmp, "inside"), os.path.join(self.sandbox.root, "link"))
        os.symlink(os.path.join(self.sandbox.home, ".ssh", "id_rsa"), os.path.join(self.sandbox.root, "alias"))
        patch = "*** Begin Patch\n*** Update File: link/../alias\n@@\n-a\n+b\n*** End Patch"
        kind, denied = self.check(patch)
        self.assertEqual(kind, "deny")
        self.assertEqual(denied.category, "secrets")

        ctx = guard.context_from_payload({
            "tool_name": "apply_patch", "cwd": self.sandbox.root,
            "tool_input": {"command": "*** Begin Patch\n*** Delete File: link/../victim\n*** End Patch"},
        }, self.sandbox.env())
        policy = guard.compile_policy(read_json(RULES), ctx)
        # Isolate the temp exemption even though the entire test sandbox is
        # physically under /tmp. The project victim is not inside this root.
        policy.tmp_roots = [self.sandbox.tmp]
        kind, denied = outcome(guard.evaluate, ctx, policy)
        self.assertEqual(kind, "deny")
        self.assertEqual(denied.category, "destructive")

        os.symlink(self.sandbox.root, os.path.join(self.sandbox.tmp, "link"))
        ctx.exec_dir = self.sandbox.tmp
        self.assertEqual(outcome(guard.evaluate, ctx, policy)[0], "allow")

    def test_bad_payload_and_empty_patch(self):
        for patch in (None, [], "", "not a patch", "*** Begin Patch\n\0\n*** End Patch"):
            with self.subTest(patch=patch):
                self.assertEqual(self.check(patch)[1].category, "failure")
        self.assertEqual(self.check("*** Begin Patch\n*** End Patch")[0], "allow")


class CapyTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox()
        self.addCleanup(__import__("shutil").rmtree, self.sandbox.base)
        self.env = self.sandbox.env()

    def check(self, tool, tool_input, category=None, payload_cwd=None):
        payload = {"tool_name": tool, "tool_input": tool_input,
                   "cwd": payload_cwd or self.sandbox.tmp}
        kind, denied = outcome(guard.decide, json.dumps(payload), self.env)
        self.assertEqual(kind, "deny" if category else "allow", denied.reason() if denied else payload)
        if category:
            self.assertEqual(denied.category, category, denied.reason())

    def test_exact_suffix_with_arbitrary_server_names(self):
        for server in ("capy", "work_tools", "plugin__capy"):
            self.check("mcp__%s__capy_execute" % server,
                       {"language": "shell", "code": "cat .env"}, "secrets")
        for tool in ("FutureTool", "mcp__capy__capy_runs", "mcp__capy__capy_execute_extra",
                     "mcp__capy__other_execute", "capy_execute", "mcp__capy_execute"):
            self.check(tool, {"language": "shell", "code": "cat .env"})

    def test_shell_and_non_shell_checks(self):
        tool = "mcp__capy__capy_execute"
        for language, code, category in (
            ("shell", "go test ./...", None),
            ("shell", "sh -c 'cat .env'", "secrets"),
            ("shell", "git clean -fd", "destructive"),
            ("python", "print(1)", None),
            ("python", "open('.env').read()", "secrets"),
            ("javascript", "fs.readFileSync('.env')", "secrets"),
            ("javascript", "fs.writeFileSync('.claude/settings.json', 'x')", "selfmod"),
            ("typescript", "fs.writeFileSync('.codex/hooks.json', 'x')", "selfmod"),
            ("go", 'os.ReadFile(".env")', "secrets"),
        ):
            with self.subTest(language=language, code=code):
                self.check(tool, {"language": language, "code": code}, category)

    def test_cwd_defaults_to_project_and_relative_override_ignores_payload_cwd(self):
        tool = "mcp__capy__capy_execute"
        self.check(tool, {"language": "shell", "code": "cat .env"}, "secrets")
        self.check(tool, {"language": "shell", "code": "cat ../.env", "cwd": "sub"}, "secrets")
        self.check(tool, {"language": "shell", "code": "cat ../README.md", "cwd": "sub"})
        self.check(tool, {"language": "shell", "code": "cat .env", "cwd": self.sandbox.tmp})
        self.check(tool, {"language": "python", "code": "open('../.env').read()", "cwd": "sub"}, "secrets")

    def test_cwd_symlinks_resolve_before_parent_components(self):
        tool = "mcp__capy__capy_execute"
        alias = os.path.join(self.sandbox.tmp, "kk-ssh-link")
        self.check(tool, {"language": "shell", "code": "cat id_rsa", "cwd": alias}, "secrets")
        self.check(tool, {"language": "shell", "code": "cat .netrc", "cwd": alias + "/.."}, "secrets")

    def test_execute_file_input_and_processing_code_have_separate_anchors(self):
        tool = "mcp__capy__capy_execute_file"
        self.check(tool, {"path": ".env", "language": "python", "code": "print(1)",
                          "cwd": self.sandbox.tmp}, "secrets")
        self.check(tool, {"path": "README.md", "language": "python", "code": "print(1)",
                          "cwd": os.path.join(self.sandbox.home, ".ssh")})
        self.check(tool, {"path": "README.md", "language": "shell", "code": "cat ../.env", "cwd": "sub"}, "secrets")
        self.check(tool, {"path": "README.md", "language": "shell", "code": "git clean -fd"}, "destructive")
        self.check(tool, {"path": "README.md", "language": "javascript",
                          "code": "fs.writeFileSync('.claude/settings.json', 'x')"}, "selfmod")
        self.check(tool, {"path": os.path.join(self.sandbox.tmp, "kk-secret-link"),
                          "language": "python", "code": "print(1)"}, "secrets")

    def test_capy_path_parameters_are_literal_not_shell_expansions(self):
        tool = "mcp__capy__capy_execute"
        for directory in ("~", "$HOME"):
            os.makedirs(os.path.join(self.sandbox.root, directory))
            ctx = guard.context_from_payload({"tool_name": tool,
                "tool_input": {"language": "shell", "code": "pwd", "cwd": directory}}, self.env)
            self.assertEqual(ctx.exec_dir, os.path.join(self.sandbox.root, directory))
        path = os.path.join(self.sandbox.root, "~", ".netrc")
        with open(path, "w") as handle:
            handle.write("ordinary project fixture")
        self.check("mcp__capy__capy_execute_file", {"path": "~/.netrc", "language": "python", "code": "print(1)"})

    def test_batch_checks_every_child_without_carrying_directory_changes(self):
        tool = "mcp__alternate__capy_batch_execute"
        self.env = self.sandbox.env(project_root="/work/project")
        self.check(tool, {"commands": [{"label": "one", "command": "go test ./..."},
                                       {"label": "two", "command": "git status"}]})
        for command, category in (("rm -rf ./work", "destructive"), ("rm -rf .", "selfmod"), ("cat .env", "secrets"),
                                  ("echo x > .claude/settings.json", "selfmod")):
            self.check(tool, {"commands": [{"label": "safe", "command": "ls"},
                                           {"label": "unsafe", "command": command}]}, category)
        self.check(tool, {"commands": [{"command": "cd /tmp && ls"},
                                       {"command": "rm -rf ./work"}]}, "destructive")
        self.check(tool, {"cwd": "/work/project/sub", "commands": [{"command": "cat ../.env"}]}, "secrets")
        self.check(tool, {"cwd": self.sandbox.tmp, "commands": [{"command": "cat .env"}]})

    def test_batch_accepts_backend_compatibility_forms_without_skipping_children(self):
        tool = "mcp__capy__capy_batch_execute"
        self.env = self.sandbox.env(project_root="/work/project")
        for commands, category in (
            (["go test ./...", {"label": "safe", "command": "ls"}], None),
            ([{"label": "safe", "command": "ls"}], None),
            (["ls", "cat .env"], "secrets"),
            (["ls", {"label": "unsafe", "command": "rm ./work"}], "destructive"),
            (["ls", 42], "failure"),
            (["ls", ""], "failure"),
        ):
            for value in (commands, json.dumps(commands)):
                with self.subTest(commands=value):
                    self.check(tool, {"commands": value}, category)
        self.check(tool, {"commands": json.dumps({"command": "ls"})}, "failure")

    def test_malformed_supported_payloads_fail_closed(self):
        tool = "mcp__capy__capy_execute"
        for key, value in (("language", None), ("language", "bash"), ("language", []),
                           ("code", None), ("code", []), ("code", ""), ("code", "ls\0"),
                           ("cwd", None), ("cwd", ""), ("cwd", 3), ("cwd", "bad\0path")):
            payload = {"language": "shell", "code": "ls"}
            payload[key] = value
            with self.subTest(key=key, value=value):
                self.check(tool, payload, "failure")
        for path in (None, "", [], "bad\0path"):
            self.check("mcp__capy__capy_execute_file", {"path": path, "language": "shell", "code": "ls"}, "failure")
        for commands in (None, [], "ls", [None], [{}], [{"command": 3}], [{"command": ""}]):
            self.check("mcp__capy__capy_batch_execute", {"commands": commands}, "failure")

    def test_capy_exceptions_keep_project_policy_and_command_boundaries(self):
        self.env = self.sandbox.env(project_root="/work/ops",
            project_config=os.path.join(FIXTURES, "project-config", "additions.json"),
            user_config=os.path.join(FIXTURES, "user-config", "scoped.json"))
        tool = "mcp__capy__capy_execute"
        self.check(tool, {"language": "shell", "code": "kubectl delete pod x", "cwd": self.sandbox.tmp})
        self.check(tool, {"language": "shell", "code": "git clean -nd; rm ./work"}, "destructive")
        self.check(tool, {"language": "shell", "code": "cat ./private.txt"}, "secrets")
        self.check("mcp__capy__capy_execute_file", {"path": "private.txt", "language": "python", "code": "print(1)",
                                                 "cwd": self.sandbox.tmp}, "secrets")


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

    def test_config_warnings_on_allow_and_deny(self):
        overrides = {"KK_GUARD_PROJECT_CONFIG": os.path.join(FIXTURES, "project-config", "invalid.json"),
                     "KK_GUARD_USER_CONFIG": os.path.join(FIXTURES, "user-config", "invalid.json")}
        for path, expected_code in (("README.md", 0), (".env", 2)):
            code, out, err = self.run_engine(self.payload("Read", {"file_path": path}), overrides)
            self.assertEqual(code, expected_code)
            result = json.loads(out)
            for config in overrides.values():
                self.assertIn(config, result["systemMessage"])
            if code == 0:
                self.assertEqual(set(result), {"systemMessage"})
                self.assertEqual(err, "")
            else:
                self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
                self.assertIn("secrets", err)

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
