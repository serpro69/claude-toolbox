import unittest

from app import answer


class AnswerTests(unittest.TestCase):
    def test_answer(self):
        self.assertEqual(answer(), 42)
