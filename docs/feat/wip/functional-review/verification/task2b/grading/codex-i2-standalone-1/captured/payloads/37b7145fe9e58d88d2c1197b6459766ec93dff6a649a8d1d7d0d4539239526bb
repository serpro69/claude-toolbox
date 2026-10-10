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
        for value in (None, "", False, 0, [], {}, "after"):
            with self.subTest(value=value):
                original = {"note": "before", "enabled": True}
                patch = {"note": value}

                result = patch_settings(original, patch)

                self.assertEqual(result, {"note": value, "enabled": True})
                self.assertIs(result["note"], value)
                self.assertEqual(original, {"note": "before", "enabled": True})
                self.assertEqual(patch, {"note": value})
                self.assertIsNot(result, original)
                self.assertIsNot(result, patch)

    def test_empty_patch_preserves_all_current_values(self):
        original = {"note": None, "enabled": False, "label": ""}
        patch = {}

        result = patch_settings(original, patch)

        self.assertEqual(result, {"note": None, "enabled": False, "label": ""})
        self.assertIsNot(result, original)
        self.assertEqual(patch, {})

    def test_patch_adds_new_keys_with_falsey_values(self):
        original = {}
        patch = {"note": None, "enabled": False, "label": ""}

        result = patch_settings(original, patch)

        self.assertEqual(result, {"note": None, "enabled": False, "label": ""})
        self.assertEqual(original, {})
        self.assertEqual(patch, {"note": None, "enabled": False, "label": ""})

    def test_api_accepts_explicit_empty_values(self):
        cases = (
            ({"note": None}, {"note": None, "enabled": True}),
            ({"note": ""}, {"note": "", "enabled": True}),
            ({"enabled": False}, {"note": "before", "enabled": False}),
        )
        for payload, expected in cases:
            with self.subTest(payload=payload):
                original = {"note": "before", "enabled": True}
                payload_before = dict(payload)

                result = update_preferences(original, payload)

                self.assertEqual(result, expected)
                self.assertEqual(original, {"note": "before", "enabled": True})
                self.assertEqual(payload, payload_before)

    def test_cli_clears_note(self):
        original = {"note": "before", "enabled": True}

        result = clear_note(original)

        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original, {"note": "before", "enabled": True})
