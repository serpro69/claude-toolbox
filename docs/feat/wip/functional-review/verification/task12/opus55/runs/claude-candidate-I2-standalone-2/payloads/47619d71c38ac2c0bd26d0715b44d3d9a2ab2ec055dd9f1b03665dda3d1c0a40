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
            ("note None", {"note": None}, {"note": None, "enabled": True}),
            ("note empty", {"note": ""}, {"note": "", "enabled": True}),
            ("enabled False", {"enabled": False}, {"note": "before", "enabled": False}),
            ("both", {"note": None, "enabled": False}, {"note": None, "enabled": False}),
        ]
        for name, payload, expected in cases:
            with self.subTest(name):
                original = {"note": "before", "enabled": True}
                result = update_preferences(original, payload)
                self.assertEqual(result, expected)
                self.assertEqual(original, {"note": "before", "enabled": True})

    def test_omitted_keys_keep_current_values(self):
        original = {"note": "before", "enabled": False}
        self.assertEqual(update_preferences(original, {}), original)
        self.assertEqual(
            update_preferences(original, {"enabled": True}),
            {"note": "before", "enabled": True},
        )

    def test_clear_note_sets_none(self):
        original = {"note": "before", "enabled": True}
        result = clear_note(original)
        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original, {"note": "before", "enabled": True})

    def test_does_not_mutate_caller_inputs(self):
        current = {"note": "before", "enabled": True}
        patch = {"note": "", "enabled": False}
        result = patch_settings(current, patch)
        self.assertEqual(result, {"note": "", "enabled": False})
        self.assertEqual(current, {"note": "before", "enabled": True})
        self.assertEqual(patch, {"note": "", "enabled": False})
        self.assertIsNot(result, current)
        self.assertIsNot(result, patch)
