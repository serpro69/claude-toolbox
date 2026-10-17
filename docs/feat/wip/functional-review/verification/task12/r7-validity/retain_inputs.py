"""Archive exact run-local configuration and instruction packets without deletion."""
import hashlib
import json
from pathlib import Path
import tarfile
import tomllib

import runner

HERE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    runner.configure()
    runner.controller.verify_frozen(HERE / "freeze.json")
    archive = HERE / "runtime-inputs.tar.gz"
    if archive.exists() or (HERE / "runtime-inputs.json").exists():
        raise FileExistsError("Refuse to replace retained runtime inputs")
    sources, provenance = {}, []
    captures = [HERE / "binding", *(HERE / "runs").iterdir()]
    if len(captures) != 5:
        raise ValueError("Expected one binding and four measured captures")
    for evidence in sorted(captures):
        seal = json.loads((evidence / "manifest.json").read_text())
        for relative, expected in seal.items():
            if digest((evidence / relative).read_bytes()) != expected:
                raise ValueError("Capture changed: " + str(evidence / relative))
        launch = json.loads((evidence / "launch.json").read_text())
        workspace = Path(launch["workspace"])
        if workspace != runner.WORKSPACES / evidence.name or workspace.is_symlink():
            raise ValueError("Unexpected workspace")
        prepared = json.loads((evidence / "prepared.json").read_text())
        for relative, expected in {
                **prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}.items():
            path = workspace / relative
            if path.is_symlink() or not path.resolve().is_relative_to(workspace) or digest(path.read_bytes()) != expected:
                raise ValueError("Runtime input changed: " + str(path))
            sources["runtime/" + evidence.name + "/" + relative] = path
        helpers = set()
        for line in (evidence / "events.jsonl").read_text().splitlines():
            record = json.loads(line)
            event = record["event"]
            message = event.get("message", {})
            if not isinstance(message, dict):
                continue
            for block in message.get("content", []):
                if (block.get("type") == "tool_use" and block.get("name") == "Bash"
                        and "/prepare_instructions.py " in block.get("input", {}).get("command", "")):
                    helpers.add(block["id"])
                if (block.get("type") != "tool_result" or block.get("tool_use_id") not in helpers
                        or block.get("is_error")):
                    continue
                content = block.get("content")
                if not isinstance(content, str):
                    raise ValueError("Unexpected helper result format")
                # A permitted shell call may list filenames before the helper.
                # The helper emits one trailing JSON object; reject any suffix.
                packet = json.loads(content[content.index("{"):])
                if packet["plugin_root"] != str(workspace / "plugins/kk"):
                    raise ValueError("Packet belongs to another bundle")
                directories = set()
                for item in packet["parts"]:
                    path = Path(item["path"])
                    # macOS exposes its private temporary root through /var.
                    normalized = Path(str(path).replace("/var/folders/", "/private/var/folders/", 1)) if str(path).startswith("/var/folders/") else path
                    if (path.is_symlink() or path.parent.is_symlink() or path.resolve() != normalized
                            or not path.parent.name.startswith("kk-review-instructions-")
                            or digest(path.read_bytes()) != item["sha256"]):
                        raise ValueError("Packet source changed")
                    directories.add(path.parent)
                    sources["packets/" + path.parent.name + "/" + path.name] = path
                for directory in directories:
                    manifest = directory / "manifest.json"
                    if manifest.is_symlink() or json.loads(manifest.read_text()) != packet:
                        raise ValueError("Packet manifest mismatch")
                    sources["packets/" + directory.name + "/manifest.json"] = manifest
                    provenance.append({"run": evidence.name, "event": record["sequence"],
                                       "directory": str(directory), "proof": "successful helper allocation"})
    config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    values = config.get("mcp_servers", {}).get("pal", {}).get("env", {})
    secrets = [str(v).encode() for k, v in values.items()
               if any(part in k for part in ("KEY", "TOKEN", "SECRET")) and v]
    hashes = {}
    for name, path in sources.items():
        data = path.read_bytes()
        if any(secret in data for secret in secrets):
            raise ValueError("Configured credential present; refusing archive")
        hashes[name] = digest(data)
    with tarfile.open(archive, "x:gz") as output:
        for name, path in sorted(sources.items()):
            output.add(path, arcname=name, recursive=False)
    with tarfile.open(archive) as retained:
        if sorted(retained.getnames()) != sorted(hashes):
            raise ValueError("Archive membership differs")
        for name, expected in hashes.items():
            if digest(retained.extractfile(name).read()) != expected:
                raise ValueError("Archive bytes differ")
    result = {"archive": archive.name, "sha256": digest(archive.read_bytes()),
              "files": hashes, "packet_allocations": provenance, "status": "PASS",
              "configured_credential_scan": "no configured PAL credential values found",
              "scratch_policy": "Retained until Task 13 evidence housekeeping; archive is durable and verified. No deletions or persistent settings changes."}
    runner.seed.write_new_json(HERE / "runtime-inputs.json", result)
    print(json.dumps({"status": "PASS", "files": len(hashes),
                      "packet_directories": len(provenance), "sha256": result["sha256"]}))


if __name__ == "__main__":
    main()
