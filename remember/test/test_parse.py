import unittest
from remember.parse import parse


class ParseTestCase(unittest.TestCase):
    def test_tbd(self):
        item = parse("in 2 months clean vacuum filters")
        self.assertEqual(item.time.months, 2)
        self.assertEqual(item.description, "clean vacuum filters")
