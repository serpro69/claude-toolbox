"""Retain only verified run-local preflight inputs; no actor or setting edits."""
import io
from pathlib import Path
import tarfile
import tomllib

import inputs
import runner

HERE = Path(__file__).resolve().parent


def main():
    adapter = runner.Adapter()
    adapter.verify()
    adapter.calibration_ready()
    archive = HERE / "preflight-runtime-inputs.tar.gz"
    receipt = HERE / "preflight-runtime-inputs.json"
    if archive.exists() or receipt.exists():
        raise FileExistsError("Refuse to overwrite retained inputs")
    secrets = [value.encode() for value in adapter.prior.matrix.codex.secrets() if value]
    contents, captures, cleanup = {}, {}, {}
    personal = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    for provider in ("claude", "codex"):
        for side in ("baseline", "candidate"):
            name = f"binding-{provider}-{side}"
            evidence = HERE / name
            runner.checked_files(evidence, inputs.read(evidence / "manifest.json"))
            launch = inputs.read(evidence / "launch.json")
            workspace = Path(launch["workspace"])
            if workspace != runner.WORKSPACES / name or workspace.is_symlink():
                raise ValueError("Unexpected runtime workspace")
            prepared = inputs.read(evidence / "prepared.json")
            records = {**prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}
            for relative, digest in records.items():
                path = workspace / relative
                if path.is_symlink() or not path.resolve().is_relative_to(workspace):
                    raise ValueError("Runtime path escaped workspace")
                value = path.read_bytes()
                if inputs.sha(path) != digest or any(secret in value for secret in secrets):
                    raise ValueError("Changed runtime input or configured credential present")
                contents[name + "/" + relative] = value
            captures[name] = inputs.sha(evidence / "manifest.json")
            if provider == "codex":
                plugin = "kk@" + adapter.prior.matrix.marketplace(side)
                if (personal.get("plugins", {}).get(plugin) is not None
                        or personal.get("projects", {}).get(str(workspace)) is not None):
                    raise ValueError("Owned temporary registration/trust remains")
                admin = HERE / "admin" / name
                seals = {}
                for operation in ("trust", "install", "uninstall", "untrust"):
                    directory = admin / operation
                    runner.checked_files(directory, inputs.read(directory / "manifest.json"))
                    seals[operation] = inputs.sha(directory / "manifest.json")
                prior = inputs.read(admin / "trust/previous-project-entry.json")
                if prior != {"path": str(workspace), "previous": None}:
                    raise ValueError("Temporary trust ownership not established")
                cleanup[name] = {"prior_trust_absent": True, "plugin_absent": True,
                                 "trust_absent": True, "admin_seals": seals}
    for row in inputs.read(HERE / "state-probe/summary.json"):
        workspace = Path(row["workspace"])
        if workspace.parent != runner.WORKSPACES / "state-probes" or workspace.is_symlink():
            raise ValueError("Unexpected state workspace")
        path = workspace / ".capy.toml"
        value = path.read_bytes()
        if any(secret in value for secret in secrets):
            raise ValueError("Credential in state configuration")
        contents[workspace.name + "/.capy.toml"] = value
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
    import hashlib
    inputs.write_new(receipt, {"archive": archive.name, "archive_sha256": inputs.sha(archive),
        "files": {name: hashlib.sha256(value).hexdigest() for name, value in contents.items()},
        "binding_seals": captures, "cleanup": cleanup, "retention_tool_sha256": inputs.sha(Path(__file__)),
        "scope": "Verified per-run configuration/roles only; no personal authentication files or knowledge database copied.",
        "scratch": "Owned probe/packet files retained for later housekeeping; no cleanup of repository/history."})
    print("Verified and retained", len(contents), "runtime files; owned Codex registrations/trust are absent.")


if __name__ == "__main__":
    main()
