"""Revision selector for candidate 2; retains the original Task 12 controller."""
from pathlib import Path
import sys

import controller

controller.CANDIDATE = "174cbb3ff5fb5b0647082705b9bba7ef07986bee"
controller.SNAPSHOTS["candidate"] = Path("/tmp/fr-task12-candidate2-20261010")
controller.HERE = Path(__file__).resolve().parent / "candidate2"
controller.DEPENDENCIES.append(Path(__file__))

if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "grade":
        from prepare_grades import prepare
        prepare(*(Path(p).resolve() for p in sys.argv[2:]))
    else:
        controller.main()
