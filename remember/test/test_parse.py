import unittest
from remember.parse import parse


class ParseTestCase(unittest.TestCase):
    def test_tbd(self):
        item = parse("in 2 months clean vacuum filters")
        self.assertEqual(item.time.months, 2)
        self.assertEqual(item.description, "clean vacuum filters")

    def test_tbd2(self):
        item = parse("in 1 month change contacts")
        self.assertEqual(item.time.months, 1)
        self.assertEqual(item.description, "change contacts")

    def test_tbd3(self):
        item = parse("in 1 year change oil")
        self.assertEqual(item.time.years, 1)
        self.assertEqual(item.description, "change oil")
