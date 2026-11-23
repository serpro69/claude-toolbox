"""Read release sources into a private staging directory before activation."""

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile
from urllib.request import urlopen
from uuid import uuid4


UPSTREAM = "serpro69/agentstakk"
FORMER_UPSTREAMS = ("serpro69/claude-toolbox", "serpro69/claude-starter-kit")
TAG = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")
LAYOUT = Path(__file__).resolve().parents[1] / "payload.json"


def read_json(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def layout_at(path):
    manifest = read_json(path)
    if (not isinstance(manifest, dict) or type(manifest.get("layout_version")) is not int
            or manifest["layout_version"] != 1):
        raise ValueError("unsupported release payload layout")
    names = manifest.get("required_directories")
    if (not isinstance(names, list) or not names or
            not all(isinstance(name, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", name) for name in names)
            or len(set(names)) != len(names)):
        raise ValueError("payload directories must be distinct top-level names")
    return manifest


GUARD_CACHE = Path("klaude-plugin/scripts/guard/__pycache__")
GUARD_BYTECODE = re.compile(r"guard\.[\w-]+(?:\.opt-[0-9]+)?\.pyc(?:\.[0-9]+)?")


def fingerprint(root, *, legacy=False):
    """Bind all shipped files and link targets. Task 3 journals also hashed bytecode."""
    digest = hashlib.sha256()
    cache = root / GUARD_CACHE
    for path in sorted(root.rglob("*")):
        if not legacy and not path.is_symlink():
            if path == cache and path.is_dir():
                continue
            # CPython publishes its cache by renaming a .pyc.<number>
            # temporary file. Either name can appear or disappear mid-walk.
            if path.parent == cache and GUARD_BYTECODE.fullmatch(path.name) and (path.is_file() or not path.exists()):
                continue
        if path.is_symlink():
            identity = ["link", os.readlink(path)]
        elif path.is_dir():
            identity = ["dir"]
        elif path.is_file():
            contents = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(131072), b""):
                    contents.update(chunk)
            identity = ["file", path.stat().st_mode & 0o111, contents.hexdigest()]
        else:
            raise ValueError("unexpected file type in candidate: {}".format(path))
        digest.update(json.dumps([path.relative_to(root).as_posix(), identity]).encode() + b"\n")
    return digest.hexdigest()


def verify_saved(root, saved):
    if not root.is_dir() or root.is_symlink():
        raise ValueError("journaled payload is missing: {}".format(root))
    if "digest_format" in saved:
        if type(saved["digest_format"]) is not int or saved["digest_format"] != 2:
            raise ValueError("unsupported release digest format")
    if not saved.get("digest") and ("digest_format" in saved or "source" in saved):
        raise ValueError("missing journaled release digest")
    if saved.get("digest") and fingerprint(root, legacy="digest_format" not in saved) != saved["digest"]:
        raise ValueError("journaled payload changed: {}".format(root))
    # Re-derive executable cache bytes from the verified source before
    # exercising the registered handler; an open interpreter can recreate them.
    cache = root / GUARD_CACHE
    if cache.is_dir() and cache.resolve() == cache:
        for path in cache.glob("*.pyc"):
            if GUARD_BYTECODE.fullmatch(path.name) and not path.is_symlink() and path.is_file():
                path.unlink(missing_ok=True)
    validate_layout(root, root.name)


def tag_name(value):
    if not isinstance(value, str) or not TAG.fullmatch(value):
        raise ValueError("expected a release tag such as v1.2.3")
    return value


def release_id(value):
    if isinstance(value, str) and re.fullmatch(r"local-[0-9a-f]{32}", value):
        return value
    return tag_name(value)


def api_root(repo):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or any(
            part in (".", "..") for part in repo.split("/")):
        raise ValueError("KK_REPOSITORY must be a GitHub owner/repository")
    return "https://api.github.com/repos/" + repo


def latest_tag(repo):
    with urlopen(api_root(repo) + "/releases/latest", timeout=30) as response:
        return tag_name(json.load(response)["tag_name"])


def canonical_repository(repo):
    if not isinstance(repo, str):
        raise ValueError("KK_REPOSITORY must be a GitHub owner/repository")
    if repo.lower() in (*FORMER_UPSTREAMS, UPSTREAM):
        return UPSTREAM
    return repo


def canonical_source(source):
    if source and "repository" in source:
        return dict(source, repository=canonical_repository(source["repository"]))
    return source


def upgrade_repository():
    return canonical_repository(os.environ.get("KK_REPOSITORY", UPSTREAM))


def check_links(root):
    for directory, directories, files in os.walk(root):
        for name in directories + files:
            path = Path(directory) / name
            if path.is_symlink():
                if os.path.isabs(os.readlink(path)):
                    raise ValueError("absolute payload symlink: {}".format(path))
                try:
                    path.resolve(strict=True).relative_to(root)
                except (ValueError, OSError, RuntimeError) as exc:
                    raise ValueError("broken or escaping payload symlink: {}".format(path)) from exc


def extract(archive, target, required):
    """Read GitHub's single-root tar. Create symlinks only after regular writes."""
    prefix = None
    links = []
    with tarfile.open(fileobj=archive, mode="r|*") as tar:
        for item in tar:
            name = PurePosixPath(item.name)
            if name.is_absolute() or ".." in name.parts or not name.parts:
                raise ValueError("unsafe archive member: {}".format(item.name))
            if prefix is None:
                prefix = name.parts[0]
            if name.parts[0] != prefix:
                raise ValueError("multiple roots in release archive")
            if len(name.parts) < 2 or name.parts[1] not in required:
                continue
            path = target.joinpath(*name.parts[1:])
            if item.isdir():
                path.mkdir(parents=True, exist_ok=True)
            elif item.isreg():
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(item) as source, path.open("xb") as output:
                    shutil.copyfileobj(source, output)
                path.chmod(0o755 if item.mode & 0o111 else 0o644)
            elif item.issym():
                if os.path.isabs(item.linkname):
                    raise ValueError("absolute link in release archive: {}".format(name))
                links.append((path, item.linkname))
            else:
                raise ValueError("unsupported member in release archive: {}".format(name))
    for path, _ in links:
        path.parent.mkdir(parents=True, exist_ok=True)
    # Every member's ancestors now exist as real directories. A link trying
    # to replace one of those directories will fail with FileExistsError.
    for path, link in links:
        path.symlink_to(link)
    check_links(target)


def stage(target, local=None, tag=None, archive_file=None, repo=None):
    layout = layout_at(LAYOUT)
    required = layout["required_directories"]
    if local is not None:
        version = "local-" + uuid4().hex
        for name in required:
            source = local / name
            if source.is_symlink() or not source.is_dir():
                raise ValueError("missing payload directory: {}".format(source))
            if source.resolve() in target.parents:
                raise ValueError("staging directory is inside the source payload: {}".format(source))
            shutil.copytree(source, target / name, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
        check_links(target)
    else:
        version = tag_name(tag) if tag else latest_tag(repo)
        if archive_file is not None:
            with archive_file.open("rb") as stream:
                extract(stream, target, required)
        else:
            with urlopen(api_root(repo) + "/tarball/" + version, timeout=60) as stream:
                extract(stream, target, required)
    validate_layout(target, version)
    return version


def validate_layout(root, version):
    layout = layout_at(LAYOUT)
    if layout_at(root / "kk/payload.json") != layout:
        raise ValueError("unsupported or incomplete release payload layout")
    for name in layout["required_directories"]:
        directory = root / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError("missing payload directory: {}".format(name))
    for name in ("bin/kk", "lib/run.py", "lib/cli.py", "lib/state.py", "lib/claude.py",
                 "lib/payload.py", "lib/validation.py", "lib/guard_identity.py", "selftest/guard-cases.json",
                 "baseline/codex/kk.rules", "lib/claude_launch.py", "baseline/claude.json", "baseline/claude/deny.json",
                 "lib/codex_launch.py", "lib/codex_profile.py", "baseline/codex.json", "baseline/codex/bootstrap.md"):
        if not (root / "kk" / name).is_file():
            raise ValueError("missing release file: kk/{}".format(name))
    versions = []
    for manifest in ("klaude-plugin/.claude-plugin/plugin.json", "kodex-plugin/.codex-plugin/plugin.json"):
        plugin = read_json(root / manifest)
        if plugin.get("name") != "kk" or not isinstance(plugin.get("version"), str):
            raise ValueError("invalid release manifest: {}".format(manifest))
        versions.append(tag_name("v" + plugin["version"]))
    if versions[0] != versions[1] or (TAG.fullmatch(version) and versions[0] != version):
        raise ValueError("release tag and plugin manifest versions disagree")
    guard = read_json(root / "kodex-guard/.codex-plugin/plugin.json")
    if not isinstance(guard, dict) or guard.get("name") != "kk-guard" or not isinstance(guard.get("version"), str):
        raise ValueError("invalid Codex guard manifest")
    tag_name("v" + guard["version"])  # The guard version is independent of the skills release.
    if not (root / "kodex-guard/hooks/hooks.json").is_file():
        raise ValueError("missing release file: kodex-guard/hooks/hooks.json")
