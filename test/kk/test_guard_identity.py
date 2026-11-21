import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_install import ROOT


class GuardIdentity(unittest.TestCase):
    def test_standalone_identity_covers_the_bundle_except_the_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            tool = directory / "guard_identity.py"
            shutil.copy2(ROOT / "kk/lib/guard_identity.py", tool)
            bundle = directory / "bundle"
            shutil.copytree(ROOT / "kodex-guard", bundle)

            def identity():
                return subprocess.check_output([sys.executable, "-I", "-B", str(tool), str(bundle)],
                                               cwd=directory, text=True).strip()

            manifest = bundle / ".codex-plugin/plugin.json"
            self.assertEqual(json.loads(manifest.read_text())["name"], "kk-guard")
            baseline = identity()
            self.assertRegex(baseline, "^[0-9a-f]{64}$")
            version = json.loads(manifest.read_text())["version"]
            manifest.write_text(manifest.read_text().replace(json.dumps(version), '"9.9.9+kk.123456789abc"'))
            self.assertEqual(identity(), baseline)
            manifest.write_bytes(manifest.read_bytes() + b" ")
            self.assertNotEqual(identity(), baseline)
            manifest.write_bytes(manifest.read_bytes()[:-1])
            adapter = bundle / "scripts/pretooluse-bash.sh"
            contents = adapter.read_bytes()
            adapter.write_bytes(contents + b"\n")
            self.assertNotEqual(identity(), baseline)
            adapter.write_bytes(contents)
            adapter.chmod(0o600)
            self.assertEqual(identity(), baseline)
            adapter.chmod(0o610)
            self.assertNotEqual(identity(), baseline)
            executable = identity()
            adapter.chmod(0o755)
            self.assertEqual(identity(), executable)
            adapter.chmod(0o644)
            adapter.rename(adapter.with_name("moved.sh"))
            self.assertNotEqual(identity(), baseline)
