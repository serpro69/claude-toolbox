"""Retain verified configuration after the measured batch; never alter captures."""
import hashlib
import io
from pathlib import Path
import tarfile
import tomllib

import listing_guard

s = listing_guard.successor
HERE = s.HERE


def runtime_contents(workspace, prepared, secrets):
    records = {**prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}
    s.runner.checked_files(workspace, records)
    contents = {}
    for relative in records:
        rel = Path(relative)
        if rel.parts[0] not in {".runner", ".codex", ".agents", ".capy.toml"}:
            raise ValueError("Unexpected runtime retention path")
        path = workspace / relative
        if path.is_symlink() or not path.resolve().is_relative_to(workspace):
            raise ValueError("Runtime path escaped workspace")
        value = path.read_bytes()
        if any(secret in value for secret in secrets):
            raise ValueError("Configured credential in runtime input")
        contents[relative] = value
    return contents


def main():
    adapter = listing_guard.Adapter()
    adapter.preflight()
    jobs = adapter.jobs()
    if len(jobs) != 64 or len({j.evidence.name for j in jobs}) != 64:
        raise ValueError("Expected the complete declared comparison")
    archive = HERE / "comparison-runtime-inputs.tar.gz"
    receipt = HERE / "comparison-runtime-inputs.json"
    if archive.exists() or receipt.exists():
        raise FileExistsError("Refuse to overwrite retained inputs")
    secrets = [value.encode() for value in adapter.prior.matrix.codex.secrets() if value]
    personal = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    contents, captures, cleanup = {}, {}, {}
    for job in jobs:
        name = job.evidence.name
        s.runner.checked_files(job.evidence, s.inputs.read(job.evidence / "manifest.json"))
        if adapter.prior.matrix.runtime.completion_status(job.evidence):
            raise ValueError("Incomplete/failed capture: " + name)
        launch = s.inputs.read(job.evidence / "launch.json")
        if (launch["workspace"] != str(job.workspace) or job.workspace.is_symlink()
                or job.workspace != s.host.WORKSPACES / name
                or launch["fixture_manifest_sha256"] != s.inputs.sha(s.host.FROZEN)):
            raise ValueError("Unexpected owned runtime workspace/identity")
        prepared = s.inputs.read(job.evidence / "prepared.json")
        for relative, value in runtime_contents(job.workspace, prepared, secrets).items():
            contents[name + "/" + relative] = value
        captures[name] = s.inputs.sha(job.evidence / "manifest.json")
        if job.provider == "codex":
            plugin = "kk@" + adapter.prior.matrix.marketplace(job.side)
            if (personal.get("plugins", {}).get(plugin) is not None
                    or personal.get("projects", {}).get(str(job.workspace)) is not None):
                raise ValueError("Owned temporary registration/trust remains")
            admin = HERE / "admin" / name
            seals = {}
            for operation in ("trust", "install", "uninstall", "untrust"):
                directory = admin / operation
                s.runner.checked_files(directory, s.inputs.read(directory / "manifest.json"))
                seals[operation] = s.inputs.sha(directory / "manifest.json")
            if s.inputs.read(admin / "trust/previous-project-entry.json") != {
                    "path": str(job.workspace), "previous": None}:
                raise ValueError("Temporary trust ownership not established")
            cleanup[name] = {"prior_trust_absent": True, "plugin_absent": True,
                             "trust_absent": True, "admin_seals": seals}
    with tarfile.open(archive, "x:gz") as output:
        for name, value in sorted(contents.items()):
            item = tarfile.TarInfo(name)
            item.size, item.mode = len(value), 0o600
            output.addfile(item, io.BytesIO(value))
    with tarfile.open(archive) as retained:
        if set(retained.getnames()) != set(contents):
            raise ValueError("Archive member mismatch")
        for name, value in contents.items():
            if retained.extractfile(name).read() != value:
                raise ValueError("Archive bytes changed")
    s.inputs.write_new(receipt, {"archive": archive.name, "archive_sha256": s.inputs.sha(archive),
        "files": {name: hashlib.sha256(value).hexdigest() for name, value in contents.items()},
        "capture_seals": captures, "cleanup": cleanup,
        "retention_tool_sha256": s.inputs.sha(Path(__file__)),
        "scope": "Verified configuration/roles only; no personal authentication files or knowledge stores copied.",
        "identity": "post-capture retention only; execution, grading and source identities unchanged"})
    print("Retained", len(contents), "runtime files for", len(captures), "captures; owned Codex entries absent.")


if __name__ == "__main__":
    main()
