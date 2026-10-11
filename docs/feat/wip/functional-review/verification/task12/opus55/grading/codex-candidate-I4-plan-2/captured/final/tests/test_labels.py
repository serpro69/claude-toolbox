import unittest

from api import list_labels


class LabelTests(unittest.TestCase):
    def test_object_labels(self):
        self.assertEqual(list_labels([{"id": "current-b", "label": {"text": "Beta"}}]), ["Beta"])

    def test_empty_list(self):
        self.assertEqual(list_labels([]), [])
