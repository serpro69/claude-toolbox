#!/usr/bin/env bash
# Stage review evals as independent repositories with a real staged Git diff.
# Requires the repository's existing Git and Python 3 tooling (stdlib only).
#
# Usage: ./setup.sh [new-stage-dir]
# The optional destination must not exist, even as an empty directory or link.
# Prints only the absolute stage path on stdout; diagnostics go to stderr.
# Flat test-files/ trees are all-added. Paired before/after trees use HEAD as
# the PR base (also tagged eval-base). Optional history.json has the shape:
# {"snapshots": [{"path": "history/released", "tag": "eval-release"}]}
# History snapshots are complete trees, committed in manifest order before base.
set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for tool in git python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "setup.sh: $tool is required" >&2
    exit 1
  fi
done

exec python3 - "$HARNESS_DIR/.." "$@" <<'PY'
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile


# Do not inherit a caller's repository, templates, signing, hooks or filters.
GIT_ENV = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
GIT_ENV.update(
    GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
    GIT_AUTHOR_NAME="Eval Harness", GIT_AUTHOR_EMAIL="eval-harness@local",
    GIT_COMMITTER_NAME="Eval Harness", GIT_COMMITTER_EMAIL="eval-harness@local",
    GIT_TERMINAL_PROMPT="0",
)


def git(*args, cwd=None):
    return subprocess.run(
        ["git", "-c", "core.hooksPath=" + os.devnull,
         "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false",
         "-c", "core.autocrlf=false", *args],
        cwd=cwd, env=GIT_ENV, check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    ).stdout.strip()


def within(path, root):
    return path == root or root in path.parents


def exists(path):
    return os.path.lexists(path)


def validate_tree(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"snapshot must be a real directory: {root}")
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name
            if name.casefold() in {".git", "eval.json", "oracle"}:
                raise ValueError(f"reserved actor-workspace entry: {path}")
            if path.is_symlink():
                target = Path(os.readlink(path))
                try:
                    resolved = path.resolve(strict=True)
                except FileNotFoundError:
                    resolved = path.resolve()  # Allow contained dangling links.
                if (target.is_absolute() or not within(resolved, root)
                        or any(part.casefold() == ".git" for part in target.parts)):
                    raise ValueError(f"escaping or absolute symlink: {path}")
            elif not path.is_dir() and not path.is_file():
                raise ValueError(f"unsupported snapshot entry: {path}")


def read_fixture(eval_dir):
    fixture = eval_dir / "test-files"
    if eval_dir.is_symlink() or fixture.is_symlink():
        raise ValueError(f"fixture directories cannot be symlinks: {fixture}")
    before, after = fixture / "before", fixture / "after"
    manifest = fixture / "history.json"
    paired = exists(before) or exists(after)
    if not paired:
        if exists(manifest) or exists(fixture / "history"):
            raise ValueError(f"history requires before/after snapshots: {fixture}")
        validate_tree(fixture)
        return eval_dir.name, None, fixture, []

    validate_tree(before)
    validate_tree(after)
    history = []
    if exists(manifest):
        if manifest.is_symlink() or not manifest.is_file():
            raise ValueError(f"history.json must be a regular file: {manifest}")
        data = json.loads(manifest.read_text())
        if (not isinstance(data, dict) or set(data) != {"snapshots"}
                or not isinstance(data["snapshots"], list) or not data["snapshots"]):
            raise ValueError(f"history.json requires a nonempty snapshots array: {manifest}")
        tags, paths = set(), set()
        for entry in data["snapshots"]:
            if not isinstance(entry, dict) or set(entry) != {"path", "tag"}:
                raise ValueError("history entries require exactly path and tag")
            relative, tag = entry["path"], entry["tag"]
            if (not isinstance(relative, str) or "\\" in relative
                    or any(part in {"", ".", ".."} for part in relative.split("/"))
                    or PurePosixPath(relative).parts[0] != "history"
                    or len(PurePosixPath(relative).parts) < 2):
                raise ValueError(f"invalid historical snapshot path: {relative!r}")
            snapshot = fixture / relative
            if any(part.is_symlink() for part in [snapshot, *snapshot.parents]
                   if within(part, fixture)):
                raise ValueError(f"historical path contains a symlink: {snapshot}")
            if (not isinstance(tag, str) or not tag or tag.startswith(("-", "refs/"))
                    or tag.casefold() in {"head", "main", "eval-base"}
                    or tag.casefold().startswith("eval-base/")
                    or tag in tags or relative in paths
                    or any(tag.startswith(old + "/") or old.startswith(tag + "/") for old in tags)):
                raise ValueError(f"duplicate, conflicting or reserved history ref: {tag!r}")
            try:
                git("check-ref-format", "refs/tags/" + tag)
            except subprocess.CalledProcessError as error:
                raise ValueError(f"invalid history tag: {tag!r}") from error
            validate_tree(snapshot)
            tags.add(tag)
            paths.add(relative)
            history.append((snapshot, tag))
    elif exists(fixture / "history"):
        raise ValueError(f"history directory requires history.json: {fixture}")
    return eval_dir.name, before, after, history


def replace_tree(worktree, source):
    # Only called for repositories created by this invocation. Never replace .git.
    for path in worktree.iterdir():
        if path.name == ".git":
            continue
        if path.is_symlink() or not path.is_dir():
            path.unlink()
        else:
            shutil.rmtree(path)
    if source is not None:
        shutil.copytree(source, worktree, dirs_exist_ok=True, symlinks=True)
    # Snapshots are complete: fixture/global ignore rules must not omit files.
    git("add", "--force", "--all", cwd=worktree)


def main():
    if len(sys.argv) > 3:
        raise ValueError("usage: setup.sh [new-stage-dir]")
    evals = Path(sys.argv[1]).resolve()
    fixtures = [read_fixture(path) for path in sorted(evals.iterdir())
                if path.name != "_harness" and path.is_dir()
                and (path / "eval.json").is_file() and (path / "test-files").is_dir()]
    if not fixtures:
        raise ValueError(f"no evals found under {evals}")

    # Validate all inputs before creating anything. mkdir is the ownership check;
    # even an empty existing directory (or dangling symlink) is never accepted.
    if len(sys.argv) == 3:
        requested = Path(sys.argv[2]).absolute()
        if exists(requested):
            raise ValueError(f"destination already exists: {requested}")
        stage = requested.resolve()
        if within(stage, evals):
            raise ValueError("destination must be outside the fixture source tree")
    else:
        stage = Path(tempfile.gettempdir()).resolve()
    if any((parent / "SKILL.md").exists() for parent in [stage, *stage.parents]):
        raise ValueError("destination must be outside any SKILL.md-rooted directory")

    if len(sys.argv) == 3:
        stage.mkdir(parents=True, exist_ok=False)
    else:
        stage = Path(tempfile.mkdtemp(prefix="review-code-evals.")).resolve()
    try:
        for name, before, after, history in fixtures:
            worktree = stage / name
            worktree.mkdir()
            git("init", "--quiet", "--template=", "--initial-branch=main", cwd=worktree)
            for snapshot, tag in history:
                replace_tree(worktree, snapshot)
                git("commit", "--allow-empty", "--quiet", "-m", "fixture history: " + tag, cwd=worktree)
                git("tag", "--", tag, cwd=worktree)
            replace_tree(worktree, before)
            git("commit", "--allow-empty", "--quiet", "-m", "fixture review base", cwd=worktree)
            git("tag", "eval-base", cwd=worktree)
            replace_tree(worktree, after)
    except BaseException:
        # This path became ours only after successful exclusive creation.
        shutil.rmtree(stage)
        raise
    print(stage)


try:
    main()
except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
    detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
    print(f"setup.sh: {detail}", file=sys.stderr)
    sys.exit(1)
PY
