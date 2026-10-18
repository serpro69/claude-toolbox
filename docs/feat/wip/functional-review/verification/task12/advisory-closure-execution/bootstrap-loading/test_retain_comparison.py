"""Retention boundary regressions using owned temporary configuration only."""
from pathlib import Path
import tempfile
import unittest

import retain_comparison as retain


class RetentionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fr-retain-comparison-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / ".runner").mkdir()
        (self.root / ".runner/settings.json").write_text('{"safe":true}\n')
        (self.root / ".capy.toml").write_text('vault = false\n')
        self.prepared = {"runtime_files": {".runner/settings.json": retain.s.inputs.sha(self.root / ".runner/settings.json")},
                         "capy_config_sha256": retain.s.inputs.sha(self.root / ".capy.toml")}

    def test_only_prepared_configuration_bytes_are_returned(self):
        (self.root / "personal-auth.json").write_text('private\n')
        result = retain.runtime_contents(self.root, self.prepared, [])
        self.assertEqual(result, {".runner/settings.json": b'{"safe":true}\n', ".capy.toml": b'vault = false\n'})

    def test_changed_bytes_and_configured_credentials_fail(self):
        with self.assertRaisesRegex(ValueError, "Configured credential"):
            retain.runtime_contents(self.root, self.prepared, [b'"safe"'])
        (self.root / ".runner/settings.json").write_text('changed\n')
        with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
            retain.runtime_contents(self.root, self.prepared, [])

    def test_outside_and_nonruntime_paths_fail(self):
        for name in ("../outside", "/etc/passwd"):
            with self.subTest(name=name):
                prepared = {**self.prepared, "runtime_files": {name: "0" * 64}}
                with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                    retain.runtime_contents(self.root, prepared, [])
        (self.root / "personal-auth.json").write_text('private\n')
        prepared = {**self.prepared, "runtime_files": {"personal-auth.json": retain.s.inputs.sha(self.root / "personal-auth.json")}}
        with self.assertRaisesRegex(ValueError, "Unexpected runtime"):
            retain.runtime_contents(self.root, prepared, [])

    def test_linked_configuration_is_not_retained(self):
        (self.root / "settings-copy.json").write_bytes((self.root / ".runner/settings.json").read_bytes())
        (self.root / ".runner/settings.json").unlink()
        (self.root / ".runner/settings.json").symlink_to("../settings-copy.json")
        with self.assertRaisesRegex(ValueError, "Runtime path escaped"):
            retain.runtime_contents(self.root, self.prepared, [])


if __name__ == "__main__":
    unittest.main()
