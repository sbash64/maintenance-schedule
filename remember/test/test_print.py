import unittest
import datetime

from remember.these import Item, Time, new, add


class FileStub:
    def __init__(self):
        self.written = ""

    def write(self, s):
        self.written += s


class PrintTestCase(unittest.TestCase):
    def test_tbd(self):
        items = new()
        fromDate = datetime.date(2022, 8, 30)
        add(
            items,
            Item(description="replace water filter", time=Time(months=2)),
            fromDate,
        )
        add(items, Item(description="change toothbrush", time=Time(months=6)), fromDate)
        add(items, Item(description="change oil", time=Time(months=4)), fromDate)
        file = FileStub()
        print(items, file=file)
        self.assertEqual(
            file.written,
            """\
October 30, 2022 - replace water filter
December 30, 2022 - change oil
February 28, 2023 - change toothbrush
""",
        )
