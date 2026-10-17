"""Recover verified preparation inputs without touching actor or user state."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
PREPARATION = HERE.parent / "advisory-closure"
PREPARATION_SHA = "2850e0416ef0277109849e206e11851f10d92fdcfd6954d8ecf5d68127e95bea"
DEFAULT_ROOT = Path("/tmp/fr-advisory-execution-inputs-20261017")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def verify_preparation():
    if sha(PREPARATION / "freeze.json") != PREPARATION_SHA:
        raise ValueError("Preparation freeze changed")
    frozen = read(PREPARATION / "freeze.json")
    for name, digest in frozen["files"].items():
        if sha(PREPARATION / name) != digest:
            raise ValueError("Preparation input changed: " + name)
    return frozen


def extract(archive, destination):
    """Only called on hash-verified controller archives; retain regular modes."""
    with tarfile.open(archive, "r:gz") as stream:
        members = stream.getmembers()
        for member in members:
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Unsafe archived path")
            if not (member.isdir() or member.isfile() or member.issym()):
                raise ValueError("Unsupported archived entry")
        stream.extractall(destination, filter="data")
        for member in members:
            if member.isfile():
                (destination / member.name).chmod(member.mode)


def restore(root=DEFAULT_ROOT):
    verify_preparation()
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=False)
    repository = root / "repository"
    repository.mkdir()
    for name in ("controller", "evaluation"):
        extract(PREPARATION / (name + "-inputs.tar.gz"), repository)
    for side in ("baseline", "candidate"):
        target = root / side
        target.mkdir()
        extract(PREPARATION / (side + "-retained.tar.gz"), target)
        (target / "source.tar").write_bytes(gzip.decompress(
            (PREPARATION / (side + "-source.tar.gz")).read_bytes()))
        for name in ("identity.json", "retained-manifest.json", "source-manifest.json", "exclusions.json"):
            shutil.copyfile(PREPARATION / (side + "-" + name), target / name)
    verify_restored(root)
    return root


def verify_restored(root=DEFAULT_ROOT):
    verify_preparation()
    root = Path(root).resolve(strict=True)
    expected = {}
    for name in ("controller", "evaluation"):
        expected.update(read(PREPARATION / (name + "-inputs.json")))
    paths = list((root / "repository").rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("Unexpected restored repository link")
    actual = {p.relative_to(root / "repository").as_posix(): sha(p) for p in paths if p.is_file()}
    if actual != expected:
        raise ValueError("Restored controller/fixture inputs differ")
    for side in ("baseline", "candidate"):
        target = root / side
        for name in ("identity.json", "retained-manifest.json", "source-manifest.json", "exclusions.json"):
            if sha(target / name) != sha(PREPARATION / (side + "-" + name)):
                raise ValueError("Restored snapshot metadata changed")
        if sha(target / "source.tar") != read(target / "identity.json")["archive_sha256"]:
            raise ValueError("Restored source changed")
        expected_paths = set()
        for tree, rows in read(target / "retained-manifest.json").items():
            boundary = target / "retained" / tree
            for record in rows:
                path = boundary / record["path"]
                expected_paths.add(path.relative_to(target / "retained").as_posix())
                if record["kind"] == "symlink":
                    if (not path.is_symlink() or str(path.readlink()) != record["target"]
                            or not path.resolve().is_relative_to(boundary)):
                        raise ValueError("Restored link changed")
                elif path.is_symlink() or oct(path.stat().st_mode & 0o777) != record["mode"]:
                    raise ValueError("Restored file mode/type changed")
                if sha(path) != record["sha256"]:
                    raise ValueError("Restored instruction changed")
        actual_paths = {p.relative_to(target / "retained").as_posix()
                        for p in (target / "retained").rglob("*") if p.is_file() or p.is_symlink()}
        if actual_paths != expected_paths:
            raise ValueError("Unexpected retained input")
    return root
