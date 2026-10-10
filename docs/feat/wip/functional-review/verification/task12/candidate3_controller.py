"""Revision selector for candidate 3; original adapters and evidence stay intact."""
from pathlib import Path
import sys

import controller

controller.CANDIDATE = "f7bbcc81c4760167d38622d9b698c2b2da54e5d9"
controller.SNAPSHOTS["candidate"] = Path("/tmp/fr-task12-candidate3-20261010")
controller.HERE = Path(__file__).resolve().parent / "candidate3"
controller.DEPENDENCIES.append(Path(__file__))

if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "grade":
        from prepare_grades import prepare
        prepare(*(Path(p).resolve() for p in sys.argv[2:]))
    else:
        controller.main()
