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

    def test_explicit_falsey_values_replace_current(self):
        cases = [
            ("none note", {"note": None}, {"note": None, "enabled": True}),
            ("empty note", {"note": ""}, {"note": "", "enabled": True}),
            ("disable", {"enabled": False}, {"note": "before", "enabled": False}),
        ]
        for name, patch, expected in cases:
            with self.subTest(name):
                current = {"note": "before", "enabled": True}
                self.assertEqual(patch_settings(current, patch), expected)

    def test_omitted_keys_keep_current_values(self):
        current = {"note": "before", "enabled": True}
        self.assertEqual(patch_settings(current, {}), current)
        self.assertEqual(
            update_preferences(current, {"enabled": False}),
            {"note": "before", "enabled": False},
        )

    def test_does_not_mutate_caller_inputs(self):
        current = {"note": "before", "enabled": True}
        patch = {"note": None, "enabled": False}
        result = patch_settings(current, patch)
        self.assertEqual(current, {"note": "before", "enabled": True})
        self.assertEqual(patch, {"note": None, "enabled": False})
        self.assertIsNot(result, current)

    def test_update_preferences_applies_falsey_payload(self):
        current = {"note": "before", "enabled": True}
        result = update_preferences(current, {"note": "", "enabled": False})
        self.assertEqual(result, {"note": "", "enabled": False})

    def test_clear_note_sets_none(self):
        current = {"note": "before", "enabled": True}
        self.assertEqual(clear_note(current), {"note": None, "enabled": True})
        self.assertEqual(current["note"], "before")
