"""Load the CLI as a package from this release under python3 -I."""

import importlib.util
from pathlib import Path
import sys


def load_cli(directory, package):
    spec = importlib.util.spec_from_file_location(
        package, directory / "cli.py", submodule_search_locations=[str(directory)]
    )
    cli = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = cli
    spec.loader.exec_module(cli)
    return cli


if __name__ == "__main__":
    sys.exit(load_cli(Path(__file__).resolve().parent, "_kk_cli").main())
