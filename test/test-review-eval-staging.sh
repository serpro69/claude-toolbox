#!/usr/bin/env bash
# Offline integration tests of the public staging helper, including real seeds.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"
log_test "Review eval staging contract"
if python3 - "$SCRIPT_DIR/.." <<'PY'
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
import unittest

REPO = Path(sys.argv.pop()).resolve()
HELPER = REPO / "klaude-plugin/skills/review-code/evals/_harness/setup.sh"


def tree(root):
    return {str(path.relative_to(root)): ("link", os.readlink(path)) if path.is_symlink()
            else ("file", hashlib.sha256(path.read_bytes()).hexdigest(), bool(path.stat().st_mode & 0o111))
            for path in root.rglob("*") if ".git" not in path.relative_to(root).parts
            and (path.is_symlink() or path.is_file())}


class StagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="test-review-staging.")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.evals = self.root / "evals"
        self.script = self.evals / "_harness/setup.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(HELPER, self.script)
        self.destination = self.root / "stage with spaces"

    def fixture(self, name="case", paired=True):
        path = self.evals / name
        path.mkdir()
        (path / "eval.json").write_text('{"trap": "grader-only"}')
        (path / "oracle").mkdir()
        (path / "oracle/answers.json").write_text('{"secret": true}')
        source = path / "test-files"
        source.mkdir()
        if paired:
            for half in ("before", "after"):
                (source / half).mkdir()
                (source / half / "unchanged.txt").write_text("same\n")
        else:
            (source / "flat.txt").write_text("flat\n")
        return source

    def invoke(self, destination=True, env=None, script=None, extra=()):
        args = ["bash", str(script or self.script)]
        if destination:
            args.append(str(self.destination))
        result = subprocess.run(args + list(extra), capture_output=True, text=True, env=env)
        return result

    def stage(self, **kwargs):
        result = self.invoke(**kwargs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        path = Path(result.stdout.strip())
        self.assertTrue(path.is_absolute())
        self.assertTrue(path.is_dir())
        return path

    def reject(self, **kwargs):
        result = self.invoke(**kwargs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("setup.sh:", result.stderr)
        self.assertFalse(self.destination.exists())

    def git(self, repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()

    def history(self, source, entries=None):
        for name in ("first", "second"):
            snapshot = source / "history" / name
            snapshot.mkdir(parents=True)
            (snapshot / (name + ".txt")).write_text(name + "\n")
        entries = entries if entries is not None else [
            {"path": "history/first", "tag": "release/one"},
            {"path": "history/second", "tag": "eval-release"},
        ]
        (source / "history.json").write_text(json.dumps({"snapshots": entries}))

    def test_flat_legacy_hidden_ignored_and_executable(self):
        source = self.fixture(paired=False)
        (source / ".hidden").write_text("hidden\n")
        (source / ".gitignore").write_text("ignored.txt\n")
        (source / "ignored.txt").write_text("must be staged\n")
        (source / "run.sh").write_text("#!/bin/sh\nexit 0\n")
        (source / "run.sh").chmod(0o755)
        repo = self.stage() / "case"
        self.assertEqual(tree(source), tree(repo))
        self.assertEqual(self.git(repo, "ls-tree", "--name-only", "HEAD"), "")
        self.assertEqual(self.git(repo, "diff", "--cached", "--name-only").splitlines(),
                         [".gitignore", ".hidden", "flat.txt", "ignored.txt", "run.sh"])
        self.assertEqual(set(self.git(repo, "diff", "--cached", "--name-status").split()[::2]), {"A"})

    def test_paired_diff_is_complete_and_base_is_preserved(self):
        source = self.fixture()
        before, after = source / "before", source / "after"
        for half in (before, after):
            (half / ".hidden").write_text("hidden\n")
            (half / "change.txt").write_text(half.name + "\n")
        (before / "deleted.txt").write_text("gone\n")
        (after / "added.txt").write_text("new\n")
        repo = self.stage() / "case"
        self.assertEqual(tree(after), tree(repo))
        self.assertEqual(self.git(repo, "show", "HEAD:change.txt"), "before")
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), self.git(repo, "rev-parse", "eval-base"))
        self.assertEqual(self.git(repo, "diff", "--cached", "--no-renames", "--name-status").splitlines(),
                         ["A\tadded.txt", "M\tchange.txt", "D\tdeleted.txt"])
        self.assertEqual(self.git(repo, "diff"), "")

    def test_history_order_complete_trees_and_release_only_source(self):
        source = self.fixture()
        self.history(source)
        repo = self.stage() / "case"
        self.assertEqual(self.git(repo, "rev-list", "--count", "HEAD"), "3")
        self.assertEqual(self.git(repo, "rev-parse", "HEAD~2"), self.git(repo, "rev-parse", "release/one"))
        self.assertEqual(self.git(repo, "rev-parse", "HEAD~1"), self.git(repo, "rev-parse", "eval-release"))
        self.assertEqual(self.git(repo, "ls-tree", "--name-only", "eval-release"), "second.txt")
        self.assertEqual(self.git(repo, "show", "release/one:first.txt"), "first")
        self.assertEqual(self.git(repo, "ls-tree", "--name-only", "HEAD"), "unchanged.txt")
        self.assertEqual(tree(source / "after"), tree(repo))
        self.assertEqual(self.git(repo, "diff", "--cached"), "")

    def test_internal_symlinks_remain_links(self):
        source = self.fixture(paired=False)
        (source / "sub").mkdir()
        (source / "sub/link").symlink_to("../flat.txt")
        repo = self.stage() / "case"
        self.assertEqual(tree(source), tree(repo))
        self.assertTrue((repo / "sub/link").is_symlink())

    def test_empty_snapshots(self):
        source = self.fixture()
        (source / "before/unchanged.txt").unlink()
        (source / "after/unchanged.txt").unlink()
        self.assertEqual(self.git(self.stage() / "case", "diff", "--cached"), "")

    def test_missing_or_non_directory_halves(self):
        source = self.fixture()
        for half in ("before", "after"):
            with self.subTest(half=half):
                shutil.rmtree(source / half)
                self.reject()
                (source / half).write_text("not a directory")
                self.reject()
                (source / half).unlink()
                (source / half).mkdir()

    def test_embedded_git_metadata_and_oracles_rejected(self):
        source = self.fixture()
        for half in ("before", "after"):
            for name in (".git", ".GIT", "oracle", "eval.json"):
                with self.subTest(half=half, name=name):
                    path = source / half / name
                    path.write_text("do not stage")
                    self.reject()
                    path.unlink()
        (source / "after/nested/.git").mkdir(parents=True)
        self.reject()

    def test_escaping_absolute_cyclic_and_git_symlinks(self):
        source = self.fixture()
        for target in ("../../oracle/answers.json", "/tmp", "link", ".git/config"):
            with self.subTest(target=target):
                link = source / "after/link"
                link.symlink_to(target)
                self.reject()
                link.unlink()
        shutil.rmtree(source / "after")
        (source / "after").symlink_to(source / "before", target_is_directory=True)
        self.reject()

    def test_invalid_history_schema(self):
        source = self.fixture()
        for value in ("{", "null", "[]", "{}", '{"snapshots": []}',
                      '{"snapshots": "bad"}', '{"snapshots": [null]}',
                      '{"snapshots": [{"path": "history/first"}]}'):
            with self.subTest(value=value):
                (source / "history.json").write_text(value)
                self.reject()

    def test_invalid_history_paths_and_refs(self):
        source = self.fixture()
        self.history(source)
        manifest = source / "history.json"
        for path in ("", "../before", "/tmp", "history/../before", "history//first",
                     "history/./first", "before", "history/missing", "history\\first", None):
            with self.subTest(path=path):
                manifest.write_text(json.dumps({"snapshots": [{"path": path, "tag": "valid"}]}))
                self.reject()
        for tag in ("", "HEAD", "main", "eval-base", "refs/heads/main", "-bad", "bad..ref", "bad ref", None):
            with self.subTest(tag=tag):
                manifest.write_text(json.dumps({"snapshots": [{"path": "history/first", "tag": tag}]}))
                self.reject()
        for tags in (("duplicate", "duplicate"), ("release", "release/child")):
            manifest.write_text(json.dumps({"snapshots": [
                {"path": "history/first", "tag": tags[0]},
                {"path": "history/second", "tag": tags[1]}]}))
            self.reject()

    def test_history_links_and_git_entries_rejected(self):
        source = self.fixture()
        self.history(source)
        path = source / "history/first"
        (path / ".git").write_text("gitdir: elsewhere")
        self.reject()
        (path / ".git").unlink()
        (path / "escape").symlink_to("../../before")
        self.reject()
        shutil.rmtree(path)
        path.symlink_to("second", target_is_directory=True)
        self.reject()

    def test_reserved_tag_namespace_rejected_before_git_init(self):
        source = self.fixture()
        self.history(source, [{"path": "history/first", "tag": "eval-base/released"}])
        commands = self.root / "git-commands"
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        wrapper = bin_dir / "git"
        wrapper.write_text('#!/bin/sh\n'
                           f'printf "%s\\n" "$@" >> {shlex.quote(str(commands))}\n'
                           f'exec {shlex.quote(shutil.which("git"))} "$@"\n')
        wrapper.chmod(0o755)
        env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"])
        self.reject(env=env)
        self.assertFalse(commands.exists(), "reserved tags must fail before any Git operation")

    def test_history_requires_manifest_and_pair(self):
        source = self.fixture()
        (source / "history").mkdir()
        self.reject()
        shutil.rmtree(source / "before")
        shutil.rmtree(source / "after")
        self.reject()

    def test_refuses_existing_destination_without_changes(self):
        self.fixture()
        self.destination.mkdir()
        for with_sentinel in (False, True):
            if with_sentinel:
                (self.destination / "keep").write_text("caller data")
            before = tree(self.destination)
            self.assertNotEqual(self.invoke().returncode, 0)
            self.assertEqual(tree(self.destination), before)
        shutil.rmtree(self.destination)
        for target in (self.root / "missing", self.evals):
            self.destination.symlink_to(target, target_is_directory=True)
            self.assertNotEqual(self.invoke().returncode, 0)
            self.assertTrue(self.destination.is_symlink())
            self.destination.unlink()
        self.destination.write_text("caller file")
        self.assertNotEqual(self.invoke().returncode, 0)
        self.assertEqual(self.destination.read_text(), "caller file")

    def test_destination_scope_and_argument_validation(self):
        self.fixture()
        (self.root / "SKILL.md").write_text("skill")
        self.reject()
        (self.root / "SKILL.md").unlink()
        self.destination = self.evals / "new-stage"
        self.reject()
        self.reject(extra=("unexpected",))

    def test_validates_entire_batch_before_creation(self):
        self.fixture("a-valid")
        source = self.fixture("z-invalid")
        shutil.rmtree(source / "after")
        self.reject()

    def test_no_evals_rejected(self):
        self.reject()

    def test_auto_destination_is_fresh(self):
        self.fixture()
        first = self.stage(destination=False)
        self.addCleanup(shutil.rmtree, first)
        second = self.stage(destination=False)
        self.addCleanup(shutil.rmtree, second)
        self.assertNotEqual(first, second)

    def test_git_configuration_and_environment_do_not_change_snapshots(self):
        source = self.fixture(paired=False)
        marker = self.root / "hook-ran"
        hooks = self.root / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_text(f'#!/bin/sh\ntouch "{marker}"\nexit 1\n')
        hook.chmod(0o755)
        config = self.root / "gitconfig"
        config.write_text(f'[commit]\n gpgsign = true\n[tag]\n gpgsign = true\n'
                          f'[core]\n hooksPath = {hooks}\n autocrlf = true\n'
                          '[filter "fail"]\n clean = false\n required = true\n')
        (source / ".gitattributes").write_text("*.txt filter=fail\n")
        env = dict(os.environ, GIT_CONFIG_GLOBAL=str(config), GIT_DIR="/missing/repo",
                   GIT_WORK_TREE="/missing/worktree", GIT_INDEX_FILE="/missing/index",
                   GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="true")
        repo = self.stage(env=env) / "case"
        self.assertFalse(marker.exists())
        self.assertEqual(tree(source), tree(repo))
        self.assertEqual(self.git(repo, "show", ":flat.txt"), "flat")

    def test_real_seed_snapshots_and_legacy_fixtures(self):
        seeds = HELPER.parent.parent
        before_hashes = tree(seeds)
        stage = self.stage(script=HELPER)
        for name in ("functional-cleanup-ownership", "functional-disabled-provider-history"):
            with self.subTest(seed=name):
                source = seeds / name / "test-files"
                repo = stage / name
                self.assertEqual(tree(source / "after"), tree(repo))
                for path in (source / "before").rglob("*"):
                    if path.is_file():
                        content = subprocess.check_output(["git", "-C", str(repo), "show",
                                  "HEAD:" + str(path.relative_to(source / "before"))])
                        self.assertEqual(content, path.read_bytes())
        repo = stage / "functional-disabled-provider-history"
        released = subprocess.check_output(["git", "-C", str(repo), "show", "eval-release:provider/settings.py"])
        self.assertEqual(released, (seeds / "functional-disabled-provider-history/test-files/history/released/provider/settings.py").read_bytes())
        self.assertNotIn("provider/settings.py", self.git(repo, "ls-tree", "-r", "--name-only", "HEAD"))
        self.assertNotIn("provider/settings.py", self.git(repo, "diff", "--cached"))
        self.assertFalse((repo / "provider").exists())
        for name in ("go-regression", "k8s-helm-chart", "k8s-kustomize-only", "k8s-monorepo-false-positive", "k8s-workload-full"):
            self.assertEqual(tree(seeds / name / "test-files"), tree(stage / name))
        self.assertEqual(tree(seeds), before_hashes)


unittest.main(verbosity=2)
PY
then
  log_pass "Staging integration tests passed"
else
  log_fail "Staging integration tests failed"
fi
print_summary
