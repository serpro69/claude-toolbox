"""Load the CLI as a package from this release under python3 -I.

This entry point stays parseable by older interpreters, down to the 3.6 that some
distributions still ship as python3, so that it can report the floor instead of
crashing. It therefore avoids `from __future__ import annotations` (3.7+).
"""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

FLOOR = (3, 9)


def require_python() -> None:
    if sys.version_info < FLOOR:
        sys.exit("kk: Python {}.{} or newer is required; {} found".format(
            *FLOOR, ".".join(map(str, sys.version_info[:3]))))


def load_cli(directory: Path, package: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        package, directory / "cli.py", submodule_search_locations=[str(directory)]
    )
    if spec is None or spec.loader is None:
        raise ImportError("cannot load kk from {}".format(directory))
    cli = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = cli
    # Python's stubs omit exec_module from Loader before 3.10; source loaders implement it.
    spec.loader.exec_module(cli)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    return cli


if __name__ == "__main__":
    require_python()
    cli = load_cli(Path(__file__).resolve().parent, "_kk_cli")
    if sys.argv[1:2] == ["--refresh-notice"] and len(sys.argv) == 4:
        cli.notice.refresh(Path(sys.argv[2]), sys.argv[3])
    else:
        sys.exit(cli.main())
