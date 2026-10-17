"""Post-capture retention of verified run-local inputs; no actor or setting edits."""
import hashlib
import io
import json
from pathlib import Path
import tarfile

import runner


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    frozen = runner.configure()
    runner.controller.verify_frozen(frozen)
    archive = runner.HERE / "runtime-inputs.tar.gz"
    receipt = runner.HERE / "runtime-inputs.json"
    if archive.exists() or receipt.exists():
        raise FileExistsError("Refuse to overwrite retained runtime inputs")
    names = ["binding-claude", "binding-codex"] + [j.evidence.name for j in runner.jobs_for(frozen)]
    credentials = [v.encode() for v in runner.prior.matrix.codex.secrets()]
    contents = {}
    captures = {}
    for name in names:
        evidence = runner.HERE / (name if name.startswith("binding-") else "runs/" + name)
        seal = json.loads((evidence / "manifest.json").read_text())
        for relative, digest in seal.items():
            if sha((evidence / relative).read_bytes()) != digest:
                raise ValueError("Capture changed: " + name + "/" + relative)
        if runner.prior.matrix.runtime.completion_status(evidence):
            raise ValueError("Capture failed: " + name)
        launch = json.loads((evidence / "launch.json").read_text())
        workspace = Path(launch["workspace"])
        if workspace != runner.WORKSPACES / name or workspace.is_symlink():
            raise ValueError("Unexpected workspace")
        prepared = json.loads((evidence / "prepared.json").read_text())
        files = {**prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}
        for relative, digest in files.items():
            path = workspace / relative
            if path.is_symlink() or not path.resolve().is_relative_to(workspace):
                raise ValueError("Runtime path escaped workspace")
            data = path.read_bytes()
            if sha(data) != digest or any(secret in data for secret in credentials):
                raise ValueError("Runtime input changed or contains configured credential: " + relative)
            contents[name + "/" + relative] = data
        captures[name] = sha((evidence / "manifest.json").read_bytes())
    with tarfile.open(archive, "x:gz") as output:
        for name, data in sorted(contents.items()):
            item = tarfile.TarInfo(name)
            item.size = len(data)
            item.mode = 0o600
            output.addfile(item, io.BytesIO(data))
    with tarfile.open(archive) as retained:
        if set(retained.getnames()) != set(contents):
            raise ValueError("Archive membership differs")
        for name, data in contents.items():
            if retained.extractfile(name).read() != data:
                raise ValueError("Archive bytes differ: " + name)
    runner.seed.write_new_json(receipt, {
        "status": "PASS", "archive": archive.name, "archive_sha256": sha(archive.read_bytes()),
        "files": {name: sha(data) for name, data in contents.items()}, "captures": captures,
        "retention_tool_sha256": sha(Path(__file__).read_bytes()),
        "scope": "Post-capture run-local configurations/roles only; source bundles and returned instruction bytes are separately retained. No personal authentication configuration copied.",
        "scratch": "Owned subject/packet copies retained until Task 13 housekeeping; no deletion or persistent setting mutation."})
    print(json.dumps({"status": "PASS", "captures": len(captures), "files": len(contents)}))


if __name__ == "__main__":
    main()
