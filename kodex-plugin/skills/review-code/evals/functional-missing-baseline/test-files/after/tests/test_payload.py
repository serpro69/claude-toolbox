import unittest

from payload import build_payload


class PayloadTests(unittest.TestCase):
    def test_trim_surrounding_spaces(self):
        self.assertEqual(build_payload("  Ada  "), {"display_name": "Ada"})

    def test_preserve_internal_space(self):
        self.assertEqual(build_payload("Ada Lovelace"), {"display_name": "Ada Lovelace"})
