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

    def test_patch_applies_every_supplied_value_without_mutating_inputs(self):
        for value in (None, "", False, 0, [], {}, "after"):
            with self.subTest(value=value):
                original = {"setting": "before", "untouched": "keep"}
                patch = {"setting": value, "added": value}

                result = patch_settings(original, patch)

                self.assertEqual(
                    result,
                    {"setting": value, "added": value, "untouched": "keep"},
                )
                self.assertEqual(original, {"setting": "before", "untouched": "keep"})
                self.assertEqual(patch, {"setting": value, "added": value})
                self.assertIsNot(result, original)
                self.assertIsNot(result, patch)

    def test_empty_patch_returns_unchanged_copy(self):
        original = {"note": None, "enabled": False}
        patch = {}

        result = patch_settings(original, patch)

        self.assertEqual(result, {"note": None, "enabled": False})
        self.assertIsNot(result, original)
        self.assertEqual(patch, {})

    def test_api_preserves_explicit_values_and_omitted_keys(self):
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

    def test_cli_clears_note_without_mutating_input(self):
        original = {"note": "before", "enabled": True}

        result = clear_note(original)

        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original, {"note": "before", "enabled": True})
