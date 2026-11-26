#!/usr/bin/env python3
"""Load the adjacent engine without adding its directory to Python's search path.

Importing permits Python's normal, interpreter-specific bytecode cache to avoid
recompiling the engine on every hook. Rules, configuration and decisions are
still evaluated afresh. A missing or unwritable cache falls back to source;
unexpected loader failures propagate to guard.sh's fail-closed boundary.

This launcher stays parseable by older interpreters, down to the 3.6 that some
distributions still ship as python3, so that it can report the floor instead of
crashing. It therefore avoids `from __future__ import annotations` (3.7+).
"""

import importlib.util
import os
import sys

FLOOR = (3, 9)
# guard.sh tries its next interpreter on this status, so an older python3
# earlier in its search order cannot block every call.
TOO_OLD = 3


def main() -> int:
    if sys.version_info < FLOOR:
        sys.stderr.write("kk guard needs Python %d.%d or newer\n" % FLOOR)
        return TOO_OLD
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard.py")
    spec = importlib.util.spec_from_file_location("_kk_guard_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the guard engine")
    engine = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = engine
    # Python's stubs omit exec_module from Loader before 3.10; source loaders implement it.
    spec.loader.exec_module(engine)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    return engine.main()


if __name__ == "__main__":
    sys.exit(main())
