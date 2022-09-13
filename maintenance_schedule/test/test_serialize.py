import unittest
import datetime

from maintenance_schedule.remind import (
    add_to_schedule,
    new_schedule,
    find_scheduled_maintenance,
    Maintenance,
    HowOften,
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
        vacuum_filter = find_scheduled_maintenance(schedule, "change vacuum filter")
        self.assertEqual(vacuum_filter.maintenance.how_often.months, 2)
        self.assertEqual(vacuum_filter.from_date, datetime.date(2022, 8, 30))
        mower_oil = find_scheduled_maintenance(schedule, "change mower oil")
        self.assertEqual(mower_oil.maintenance.how_often.months, 4)
        self.assertEqual(mower_oil.from_date, datetime.date(2022, 8, 30))
        driveway = find_scheduled_maintenance(schedule, "get quotes for driveway")
        self.assertEqual(driveway.maintenance.how_often.years, 2)
        self.assertEqual(driveway.from_date, datetime.date(2022, 8, 30))
        prescription = find_scheduled_maintenance(schedule, "refill prescription")
        self.assertEqual(prescription.maintenance.how_often.days, 90)
        self.assertEqual(prescription.from_date, datetime.date(2022, 9, 3))

    def test_deserialize_one_month(self):
        file = FileStub(["in 1 month from 08/31/2022 clean toilet"])
        schedule = deserialize(file)
        self.assertEqual(
            schedule.scheduled_maintenances[0].maintenance.how_often.months, 1
        )

    def test_serialize(self):
        schedule = new_schedule()
        add_to_schedule(
            schedule,
            Maintenance(what="replace furnace filter", how_often=HowOften(months=6)),
            datetime.date(2022, 8, 30),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="clean water bowl", how_often=HowOften(months=1)),
            datetime.date(2022, 8, 30),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="service mower blade", how_often=HowOften(years=1)),
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
