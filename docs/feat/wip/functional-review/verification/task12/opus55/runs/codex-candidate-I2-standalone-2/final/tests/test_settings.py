import unittest
from api import update_preferences
from cli import clear_note
from settings import patch_settings


class SettingsTests(unittest.TestCase):
    def test_updates_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": "after"})
        self.assertEqual(result, {"note": "after", "enabled": True})
        self.assertEqual(original["note"], "before")

    def test_explicit_values_replace_current_values(self):
        for patch, expected in (
            ({"note": None}, {"note": None, "enabled": True}),
            ({"note": ""}, {"note": "", "enabled": True}),
            ({"enabled": False}, {"note": "before", "enabled": False}),
        ):
            with self.subTest(patch=patch):
                original = {"note": "before", "enabled": True}
                payload = dict(patch)
                result = update_preferences(original, payload)
                self.assertEqual(result, expected)
                self.assertEqual(original, {"note": "before", "enabled": True})
                self.assertEqual(payload, patch)

    def test_empty_patch_returns_unchanged_copy(self):
        original = {"note": "before", "enabled": False}
        patch = {}
        result = patch_settings(original, patch)
        self.assertEqual(result, original)
        self.assertIsNot(result, original)
        self.assertEqual(patch, {})

    def test_patch_adds_explicit_values_without_mutating_inputs(self):
        original = {"other": "keep"}
        patch = {"note": "", "enabled": False, "extra": None}
        result = patch_settings(original, patch)
        self.assertEqual(
            result, {"other": "keep", "note": "", "enabled": False, "extra": None}
        )
        self.assertIsNot(result, original)
        self.assertIsNot(result, patch)
        self.assertEqual(original, {"other": "keep"})
        self.assertEqual(patch, {"note": "", "enabled": False, "extra": None})

    def test_cli_clears_note(self):
        original = {"note": "before", "enabled": True}
        result = clear_note(original)
        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original, {"note": "before", "enabled": True})
