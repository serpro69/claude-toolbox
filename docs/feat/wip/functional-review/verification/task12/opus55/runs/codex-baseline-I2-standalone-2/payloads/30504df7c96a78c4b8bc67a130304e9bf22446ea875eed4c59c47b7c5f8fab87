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
        for update in (patch_settings, update_preferences):
            for key, value in (("note", None), ("note", ""), ("enabled", False)):
                with self.subTest(update=update.__name__, key=key, value=value):
                    original = {"note": "before", "enabled": True}
                    patch = {key: value}

                    result = update(original, patch)

                    self.assertEqual(result[key], value)
                    omitted_key = "enabled" if key == "note" else "note"
                    self.assertEqual(result[omitted_key], original[omitted_key])
                    self.assertEqual(original, {"note": "before", "enabled": True})
                    self.assertEqual(patch, {key: value})
                    self.assertIsNot(result, original)
                    self.assertIsNot(result, patch)

    def test_empty_patch_preserves_values_and_returns_a_copy(self):
        for update in (patch_settings, update_preferences):
            for note in ("before", "", None):
                with self.subTest(update=update.__name__, note=note):
                    original = {"note": note, "enabled": False}
                    patch = {}

                    result = update(original, patch)

                    self.assertEqual(result, original)
                    self.assertIsNot(result, original)
                    result["note"] = "changed"
                    self.assertEqual(original, {"note": note, "enabled": False})
                    self.assertEqual(patch, {})

    def test_explicit_values_add_missing_keys(self):
        for value in (None, "", False, 0, "new"):
            with self.subTest(value=value):
                original = {}
                patch = {"new_key": value}

                result = patch_settings(original, patch)

                self.assertEqual(result, {"new_key": value})
                self.assertEqual(original, {})
                self.assertEqual(patch, {"new_key": value})

    def test_clear_note_sets_none(self):
        original = {"note": "before", "enabled": True}

        result = clear_note(original)

        self.assertEqual(result, {"note": None, "enabled": True})
        self.assertEqual(original, {"note": "before", "enabled": True})
