import unittest

from api import list_destinations
from writer import new_destination


class DestinationTests(unittest.TestCase):
    def test_new_write_can_be_listed(self):
        row = new_destination("new", "new@example.test")
        self.assertEqual(list_destinations([row]),
                         [{"id": "new", "address": "new@example.test"}])

    def test_empty_list(self):
        self.assertEqual(list_destinations([]), [])
