#!/usr/bin/env python3
"""Prepare a fresh loading probe; never use this workspace for measured runs."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from probe_state import workspace_at


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=("claude", "codex"))
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("marketplace", help="Unique revision/side-bearing marketplace name")
    parser.add_argument("--disable-plugin", action="append", default=["kk@claude-toolbox"],
                        help="Other visible kk plugin ID; repeat for every installed sibling")
    args = parser.parse_args()
    workspace = workspace_at(args.workspace.resolve())
    runner = workspace / ".runner"
    tree = "klaude-plugin" if args.provider == "claude" else "kodex-plugin"
    bundle = workspace / "plugins/kk"
    shutil.copytree(args.snapshot / "retained" / tree, bundle, symlinks=True)
    # Validate the actor copy before constructing a catalog that exposes it.
    subprocess.run([sys.executable, str(Path(__file__).with_name("prepare-bundles.py")), "verify",
                    str(bundle), str(args.snapshot / "retained-manifest.json"), tree], check=True)
    capy_command = shutil.which("capy")
    if not capy_command:
        raise RuntimeError("capy is required")
    capy = {"command": "env", "args": ["-u", "CAPY_VAULT_KEY", "-u", "CAPY_DB_KEY",
            "CAPY_DB_KEY=synthetic-functional-review-probe-key-20261008",
            "CAPY_VAULT_PATH=" + str(runner / "vault"),
            "XDG_CONFIG_HOME=" + str(runner / "xdg"), capy_command,
            "--project-dir", str(workspace), "serve"]}
    if args.provider == "claude":
        (runner / "mcp.json").write_text(json.dumps({"mcpServers": {"capy": capy}}, indent=2) + "\n")
        version = json.loads((bundle / ".claude-plugin/plugin.json").read_text())["version"]
        registry = {"version": 2, "plugins": {"kk@" + args.marketplace: [{"scope": "project",
                    "projectPath": str(workspace), "installPath": str(bundle), "version": version,
                    "installedAt": "2026-10-08T00:00:00Z"}]}}
        (runner / "registry.json").write_text(json.dumps(registry, indent=2) + "\n")
        (runner / "claude-config").mkdir()
        (runner / "settings.json").write_text(json.dumps({"autoMemoryEnabled": False,
            "permissions": {"additionalDirectories": [str(bundle)]}}) + "\n")
    else:
        catalog = workspace / ".agents/plugins"
        catalog.mkdir(parents=True)
        (catalog / "marketplace.json").write_text(json.dumps({"name": args.marketplace,
            "plugins": [{"name": "kk", "source": {"source": "local", "path": "./plugins/kk"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Productivity"}]}, indent=2) + "\n")
        shutil.copytree(args.snapshot / "retained/.codex/agents", workspace / ".codex/agents")
        # No global installation/config is edited by this preparation helper.
        config = ('model = "gpt-6-astra"\nmodel_reasoning_effort = "xhigh"\n'
                  'approval_policy = "never"\nsandbox_mode = "workspace-write"\n'
                  '[plugins.' + json.dumps("kk@" + args.marketplace) + ']\nenabled = true\n'
                  '[mcp_servers.capy]\ncommand = "env"\nargs = ' + json.dumps(capy["args"]) + '\n')
        for plugin in args.disable_plugin:
            if plugin == "kk@" + args.marketplace:
                raise ValueError("Cannot disable selected plugin")
            config += '[plugins.' + json.dumps(plugin) + ']\nenabled = false\n'
        (workspace / ".codex/config.toml").write_text(config)
    print(json.dumps({"provider": args.provider, "workspace": str(workspace), "bundle": str(bundle),
                      "marketplace": args.marketplace, "status": "prepared; runtime unverified"}))


if __name__ == "__main__":
    main()
