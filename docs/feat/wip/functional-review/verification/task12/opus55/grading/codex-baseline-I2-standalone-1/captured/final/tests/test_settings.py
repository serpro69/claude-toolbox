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
        cases = (
            ({"note": None}, {"note": None, "enabled": True}),
            ({"note": ""}, {"note": "", "enabled": True}),
            ({"enabled": False}, {"note": "before", "enabled": False}),
        )
        for update in (patch_settings, update_preferences):
            for patch, expected in cases:
                with self.subTest(update=update.__name__, patch=patch):
                    current = {"note": "before", "enabled": True}
                    original_patch = dict(patch)
                    result = update(current, patch)
                    self.assertEqual(result, expected)
                    self.assertIsNot(result, current)
                    self.assertEqual(current, {"note": "before", "enabled": True})
                    self.assertEqual(patch, original_patch)

    def test_empty_patch_preserves_current_values_and_missing_keys(self):
        for update in (patch_settings, update_preferences):
            for current in ({"note": None, "enabled": False}, {"note": ""}, {}):
                with self.subTest(update=update.__name__, current=current):
                    result = update(current, {})
                    self.assertEqual(result, current)
                    self.assertIsNot(result, current)

    def test_explicit_values_add_missing_keys(self):
        for update in (patch_settings, update_preferences):
            for patch in ({"note": None}, {"note": ""}, {"enabled": False}):
                with self.subTest(update=update.__name__, patch=patch):
                    current = {}
                    original_patch = dict(patch)
                    result = update(current, patch)
                    self.assertEqual(result, original_patch)
                    self.assertIsNot(result, patch)
                    self.assertEqual(current, {})
                    self.assertEqual(patch, original_patch)

    def test_cli_clears_note(self):
        current = {"note": "before", "enabled": True}
        self.assertEqual(clear_note(current), {"note": None, "enabled": True})
        self.assertEqual(current, {"note": "before", "enabled": True})
