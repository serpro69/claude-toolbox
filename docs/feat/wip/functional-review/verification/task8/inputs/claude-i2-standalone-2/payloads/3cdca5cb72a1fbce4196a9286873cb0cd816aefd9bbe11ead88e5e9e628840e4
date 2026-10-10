import unittest
from api import update_preferences
from settings import patch_settings


class SettingsTests(unittest.TestCase):
    def test_updates_note(self):
        original = {"note": "before", "enabled": True}
        result = update_preferences(original, {"note": "after"})
        self.assertEqual(result, {"note": "after", "enabled": True})
        self.assertEqual(original["note"], "before")


class PatchSettingsTests(unittest.TestCase):
    def test_omitted_keys_keep_current_values(self):
        current = {"note": "keep", "enabled": True}
        result = patch_settings(current, {"enabled": False})
        self.assertEqual(result, {"note": "keep", "enabled": False})

    def test_falsey_values_replace_current(self):
        current = {"note": "before", "count": 5, "enabled": True, "label": "x"}
        for key, value in (
            ("note", None),
            ("label", ""),
            ("enabled", False),
            ("count", 0),
        ):
            with self.subTest(key=key, value=value):
                result = patch_settings(current, {key: value})
                self.assertEqual(result[key], value)

    def test_adds_new_key(self):
        result = patch_settings({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_does_not_mutate_caller_inputs(self):
        current = {"note": "before"}
        patch = {"note": None}
        patch_settings(current, patch)
        self.assertEqual(current, {"note": "before"})
        self.assertEqual(patch, {"note": None})
