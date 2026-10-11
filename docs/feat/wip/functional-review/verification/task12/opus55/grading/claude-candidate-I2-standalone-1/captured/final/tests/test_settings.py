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
        cases = {
            "none note": ({"note": None}, {"note": None, "enabled": True}),
            "empty note": ({"note": ""}, {"note": "", "enabled": True}),
            "disabled": ({"enabled": False}, {"note": "before", "enabled": False}),
        }
        for name, (patch, expected) in cases.items():
            with self.subTest(name):
                current = {"note": "before", "enabled": True}
                self.assertEqual(patch_settings(current, patch), expected)

    def test_omitted_keys_keep_current_values(self):
        current = {"note": "before", "enabled": True}
        self.assertEqual(patch_settings(current, {}), current)

    def test_does_not_mutate_inputs(self):
        current = {"note": "before", "enabled": True}
        patch = {"note": None, "enabled": False}
        result = patch_settings(current, patch)
        self.assertIsNot(result, current)
        self.assertEqual(current, {"note": "before", "enabled": True})
        self.assertEqual(patch, {"note": None, "enabled": False})

    def test_update_preferences_applies_falsey_payload(self):
        original = {"note": "before", "enabled": True}
        payload = {"note": "", "enabled": False, "ignored": "x"}
        result = update_preferences(original, payload)
        self.assertEqual(result, {"note": "", "enabled": False})
        self.assertEqual(original, {"note": "before", "enabled": True})

    def test_clear_note_sets_none(self):
        original = {"note": "before", "enabled": True}
        self.assertEqual(clear_note(original), {"note": None, "enabled": True})
        self.assertEqual(original["note"], "before")
