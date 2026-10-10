import unittest
from api import update_preferences


class SettingsTests(unittest.TestCase):
    def test_updates_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": "after"})
        self.assertEqual(result, {"note": "after", "enabled": True})
        self.assertEqual(original["note"], "before")

    def test_supplied_none_replaces_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": None})
        self.assertEqual(result, {"note": None, "enabled": True})

    def test_supplied_empty_text_replaces_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": ""})
        self.assertEqual(result, {"note": "", "enabled": True})

    def test_supplied_false_replaces_enabled(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"enabled": False})
        self.assertEqual(result, {"note": "before", "enabled": False})

    def test_omitted_keys_keep_current_values(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {})
        self.assertEqual(result, {"note": "before", "enabled": True})
