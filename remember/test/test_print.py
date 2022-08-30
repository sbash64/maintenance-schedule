import unittest
from remember.these import Item, Time, new, add


class FileStub:
    def __init__(self):
        self.written = ""

    def write(self, s):
        self.written += s


class PrintTestCase(unittest.TestCase):
    def test_tbd(self):
        items = new()
        add(items, Item(description="replace water filter", time=Time(months=2)))
        add(items, Item(description="change toothbrush", time=Time(months=6)))
        add(items, Item(description="change oil", time=Time(months=4)))
        file = FileStub()
        print(items, file=file)
        self.assertEqual(
            file.written,
            """\
in 2 months replace water filter
in 4 months change oil
in 6 months change toothbrush
""",
        )
