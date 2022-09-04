import unittest
import datetime

from maintenance_schedule.remind import (
    add_to_schedule,
    new_schedule,
    Maintenance,
    Period,
)
from maintenance_schedule.persistence import deserialize, serialize


class FileStub:
    def __init__(self, lines):
        self.lines = lines
        self.written = ""

    def __iter__(self):
        yield from self.lines

    def write(self, s):
        self.written += s


class SerializeTestCase(unittest.TestCase):
    def test_deserialize(self):
        file = FileStub(
            [
                "in 2 months from 08/30/2022 change vacuum filter",
                "in 4 months from 08/30/2022 change mower oil",
                "in 2 years from 08/30/2022 get quotes for driveway",
                "in 90 days from 09/03/2022 refill prescription",
            ]
        )
        schedule = deserialize(file)
        self.assertEqual(
            schedule.nextActions[0].maintenance.what, "change vacuum filter"
        )
        self.assertEqual(schedule.nextActions[0].maintenance.when.months, 2)
        self.assertEqual(schedule.nextActions[0].startDate, datetime.date(2022, 8, 30))
        self.assertEqual(schedule.nextActions[2].maintenance.what, "change mower oil")
        self.assertEqual(schedule.nextActions[2].maintenance.when.months, 4)
        self.assertEqual(schedule.nextActions[2].startDate, datetime.date(2022, 8, 30))
        self.assertEqual(
            schedule.nextActions[3].maintenance.what, "get quotes for driveway"
        )
        self.assertEqual(schedule.nextActions[3].maintenance.when.years, 2)
        self.assertEqual(schedule.nextActions[3].startDate, datetime.date(2022, 8, 30))
        self.assertEqual(
            schedule.nextActions[1].maintenance.what, "refill prescription"
        )
        self.assertEqual(schedule.nextActions[1].maintenance.when.days, 90)
        self.assertEqual(schedule.nextActions[1].startDate, datetime.date(2022, 9, 3))

    def test_deserialize_one_month(self):
        file = FileStub(["in 1 month from 08/31/2022 clean toilet"])
        schedule = deserialize(file)
        self.assertEqual(schedule.nextActions[0].maintenance.when.months, 1)

    def test_serialize(self):
        schedule = new_schedule()
        add_to_schedule(
            schedule,
            Maintenance(what="replace furnace filter", when=Period(months=6)),
            datetime.date(2022, 8, 30),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="clean water bowl", when=Period(months=1)),
            datetime.date(2022, 8, 30),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="service mower blade", when=Period(years=1)),
            datetime.date(2022, 8, 30),
        )
        file = FileStub([])
        serialize(schedule, file)
        self.assertEqual(
            file.written,
            """\
in 1 month from 08/30/2022 clean water bowl
in 6 months from 08/30/2022 replace furnace filter
in 1 year from 08/30/2022 service mower blade
""",
        )
