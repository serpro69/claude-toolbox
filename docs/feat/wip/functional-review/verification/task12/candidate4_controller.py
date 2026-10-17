"""Revision selector for candidate 4; all previous controllers remain unchanged."""
from pathlib import Path
import sys

import controller

controller.CANDIDATE = "cde36b8239de1fc1e10e589e969e6613668aa26c"
controller.SNAPSHOTS["candidate"] = Path("/tmp/fr-task12-candidate4-20261010")
controller.HERE = Path(__file__).resolve().parent / "candidate4"
controller.DEPENDENCIES.append(Path(__file__))

if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "grade":
        from prepare_grades import prepare
        prepare(*(Path(p).resolve() for p in sys.argv[2:]))
    else:
        controller.main()
