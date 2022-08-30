import unittest
import datetime

from remember.these import add, new, Item, Time
from remember.persistence import deserialize, serialize


class FileStub:
    def __init__(self, lines):
        self.lines = lines
        self.written = ""

    def __iter__(self):
        yield from self.lines

    def write(self, s):
        self.written += s


class SerializeTestCase(unittest.TestCase):
    def test_tbd(self):
        file = FileStub(
            [
                "in 2 months from 08/30/2022 change vacuum filter",
                "in 4 months from 08/30/2022 change mower oil",
                "in 2 years from 08/30/2022 get quotes for driveway",
            ]
        )
        reminders = deserialize(file)
        self.assertEqual(reminders.todos[0].description, "change vacuum filter")
        self.assertEqual(reminders.todos[0].time.months, 2)
        self.assertEqual(reminders.todos[0].fromDate, datetime.date(2022, 8, 30))
        self.assertEqual(reminders.todos[1].description, "change mower oil")
        self.assertEqual(reminders.todos[1].time.months, 4)
        self.assertEqual(reminders.todos[1].fromDate, datetime.date(2022, 8, 30))
        self.assertEqual(reminders.todos[2].description, "get quotes for driveway")
        self.assertEqual(reminders.todos[2].time.years, 2)

    def test_tbd2(self):
        reminders = new()
        add(
            reminders,
            Item(description="replace furnace filter", time=Time(months=6)),
            datetime.date(2022, 8, 30),
        )
        add(
            reminders,
            Item(description="clean water bowl", time=Time(months=1)),
            datetime.date(2022, 8, 30),
        )
        add(
            reminders,
            Item(description="service mower blade", time=Time(years=1)),
            datetime.date(2022, 8, 30),
        )
        file = FileStub([])
        serialize(reminders, file)
        self.assertEqual(
            file.written,
            """\
in 1 month from 08/30/2022 clean water bowl
in 6 months from 08/30/2022 replace furnace filter
in 1 year from 08/30/2022 service mower blade
""",
        )
