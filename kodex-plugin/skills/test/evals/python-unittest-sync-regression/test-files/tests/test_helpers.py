import unittest

from helpers import normalize_label


class LabelTests(unittest.TestCase):
    def test_normalizes_label(self):
        self.assertEqual(normalize_label("  Example  "), "example")

    def test_empty_label(self):
        self.assertEqual(normalize_label("   "), "")
