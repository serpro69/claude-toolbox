"""Compute the portable identity of a Codex guard bundle, independently of kk."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


MANIFEST = Path(".codex-plugin/plugin.json")


def with_version(data, version):
    """Replace just the top-level version value, preserving all other UTF-8 bytes."""
    text = data.decode("utf-8")
    manifest = json.loads(text)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("version"), str):
        raise ValueError("guard manifest must contain a version string")

    # A parsed-and-reserialized document would also mask changes to whitespace,
    # key order and escapes. Walk the validated object's top-level members.
    decoder = json.JSONDecoder()
    pos = text.index("{") + 1
    span = None
    while True:
        while text[pos] in " \r\n\t":
            pos += 1
        key, pos = decoder.raw_decode(text, pos)
        pos = text.index(":", pos) + 1
        while text[pos] in " \r\n\t":
            pos += 1
        start = pos
        _, pos = decoder.raw_decode(text, pos)
        if key == "version":
            if span is not None:
                raise ValueError("duplicate guard manifest version")
            span = start, pos
        while text[pos] in " \r\n\t":
            pos += 1
        if text[pos] == "}":
            break
        pos += 1  # comma
    start, end = span
    return (text[:start] + json.dumps(version) + text[end:]).encode("utf-8")


def guard_identity(root: Path) -> str:
    """Hash relative paths, release-archive file modes and content."""
    root = Path(root).resolve(strict=True)
    manifest = root / MANIFEST
    if manifest.parent.is_symlink() or manifest.is_symlink() or not manifest.is_file():
        raise ValueError("missing regular guard manifest: {}".format(manifest))
    result = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        relative = path.relative_to(root)
        if stat.S_ISLNK(mode):
            artifact_mode = stat.S_IFLNK
            target = os.readlink(path)
            if os.path.isabs(target):
                raise ValueError("absolute guard bundle symlink: {}".format(relative))
            try:
                path.resolve(strict=True).relative_to(root)
            except (OSError, ValueError, RuntimeError) as error:
                raise ValueError("broken or escaping guard bundle symlink: {}".format(relative)) from error
            content = hashlib.sha256(os.fsencode(target))
        elif stat.S_ISREG(mode):
            # Match payload.extract: Git/tag archives carry regular or
            # executable files; checkout umask must not restamp a guard.
            artifact_mode = stat.S_IFREG | (0o755 if mode & 0o111 else 0o644)
            content = hashlib.sha256()
            with path.open("rb") as stream:
                if relative == MANIFEST:
                    content.update(with_version(stream.read(), ""))
                else:
                    for block in iter(lambda: stream.read(131072), b""):
                        content.update(block)
        else:
            raise ValueError("unsupported guard bundle entry: {}".format(path))
        result.update(os.fsencode(relative.as_posix()) + b"\0" + artifact_mode.to_bytes(4, "big") + content.digest())
    return result.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    try:
        print(guard_identity(args.bundle))
    except (ValueError, OSError) as error:
        parser.exit(1, "guard identity: {}\n".format(error))
