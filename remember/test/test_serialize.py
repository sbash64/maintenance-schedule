import unittest
import datetime

from remember.persistence import deserialize


class FileStub:
    def __init__(self, lines):
        self.lines = lines

    def __iter__(self):
        yield from self.lines


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
