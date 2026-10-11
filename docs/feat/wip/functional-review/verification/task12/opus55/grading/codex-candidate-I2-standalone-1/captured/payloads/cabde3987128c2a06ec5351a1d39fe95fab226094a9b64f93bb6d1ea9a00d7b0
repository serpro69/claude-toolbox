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
        for value in (None, "", False, 0):
            with self.subTest(value=value):
                current = {"setting": "before", "untouched": "keep"}
                patch = {"setting": value}
                result = patch_settings(current, patch)
                self.assertIs(result["setting"], value)
                self.assertEqual(result["untouched"], "keep")
                self.assertEqual(current, {"setting": "before", "untouched": "keep"})
                self.assertEqual(patch, {"setting": value})
                self.assertIsNot(result, current)
                self.assertIsNot(result, patch)

    def test_empty_patch_returns_unchanged_copy(self):
        current = {"note": None, "enabled": False}
        result = patch_settings(current, {})
        self.assertEqual(result, current)
        self.assertIsNot(result, current)

    def test_patch_adds_new_keys(self):
        patch = {"note": "", "enabled": False}
        self.assertEqual(patch_settings({}, patch), patch)

    def test_preferences_preserve_omitted_values(self):
        current = {"note": "before", "enabled": True}
        cases = (
            ({}, {"note": "before", "enabled": True}),
            ({"note": None}, {"note": None, "enabled": True}),
            ({"note": ""}, {"note": "", "enabled": True}),
            ({"enabled": False}, {"note": "before", "enabled": False}),
            ({"note": None, "enabled": False}, {"note": None, "enabled": False}),
        )
        for payload, expected in cases:
            with self.subTest(payload=payload):
                original_payload = dict(payload)
                self.assertEqual(update_preferences(current, payload), expected)
                self.assertEqual(current, {"note": "before", "enabled": True})
                self.assertEqual(payload, original_payload)

    def test_clear_note_preserves_other_settings_and_input(self):
        current = {"note": "before", "enabled": True}
        self.assertEqual(clear_note(current), {"note": None, "enabled": True})
        self.assertEqual(current, {"note": "before", "enabled": True})
