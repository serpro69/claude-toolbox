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
            ("disabled", {"enabled": False}, {"note": "before", "enabled": False}),
        ]
        for name, payload, expected in cases:
            with self.subTest(name):
                original = {"note": "before", "enabled": True}
                result = update_preferences(original, payload)
                self.assertEqual(result, expected)
                self.assertEqual(original, {"note": "before", "enabled": True})

    def test_omitted_keys_keep_current_values(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {})
        self.assertEqual(result, original)
        self.assertIsNot(result, original)

    def test_clear_note_sets_none(self):
        original = {"note": "before", "enabled": True}
        result = clear_note(original)
        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original["note"], "before")

    def test_patch_settings_does_not_mutate_inputs(self):
        current = {"note": "before", "enabled": True}
        patch = {"enabled": False}
        patch_settings(current, patch)
        self.assertEqual(current, {"note": "before", "enabled": True})
        self.assertEqual(patch, {"enabled": False})


if __name__ == "__main__":
    unittest.main()
