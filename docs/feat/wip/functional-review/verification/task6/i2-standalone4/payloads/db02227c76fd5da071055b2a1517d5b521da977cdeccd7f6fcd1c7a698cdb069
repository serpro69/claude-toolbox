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

    def test_none_replaces_value(self):
        result = patch_settings({"note": "keep"}, {"note": None})
        self.assertIsNone(result["note"])

    def test_empty_text_replaces_value(self):
        result = patch_settings({"note": "keep"}, {"note": ""})
        self.assertEqual(result["note"], "")

    def test_false_replaces_value(self):
        result = patch_settings({"enabled": True}, {"enabled": False})
        self.assertIs(result["enabled"], False)

    def test_omitted_keys_keep_current_values(self):
        result = patch_settings({"note": "keep", "enabled": True}, {"note": None})
        self.assertEqual(result["enabled"], True)

    def test_caller_inputs_not_mutated(self):
        current = {"note": "before", "enabled": True}
        patch = {"note": None}
        patch_settings(current, patch)
        self.assertEqual(current, {"note": "before", "enabled": True})
        self.assertEqual(patch, {"note": None})

    def test_clear_note_resets_to_none(self):
        self.assertIsNone(clear_note({"note": "old", "enabled": True})["note"])

    def test_update_preferences_applies_false(self):
        result = update_preferences({"note": "n", "enabled": True}, {"enabled": False})
        self.assertIs(result["enabled"], False)


if __name__ == "__main__":
    unittest.main()
