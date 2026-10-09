import unittest
from api import update_preferences
from cli import clear_note


class SettingsTests(unittest.TestCase):
    def test_updates_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": "after"})
        self.assertEqual(result, {"note": "after", "enabled": True})
        self.assertEqual(original["note"], "before")

    def test_explicit_none_replaces_value(self):
        original = {"note": "before", "enabled": True}
        result = clear_note(original)
        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original["note"], "before")

    def test_explicit_false_replaces_value(self):
        original = {"note": "keep", "enabled": True}
        result = update_preferences(original, {"enabled": False})
        self.assertEqual(result, {"note": "keep", "enabled": False})
        self.assertEqual(original["enabled"], True)

    def test_explicit_empty_text_replaces_value(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": ""})
        self.assertEqual(result, {"note": "", "enabled": True})

    def test_omitted_keys_keep_current_values(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {})
        self.assertEqual(result, {"note": "before", "enabled": True})
