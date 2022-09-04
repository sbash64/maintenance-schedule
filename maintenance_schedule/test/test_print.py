import unittest
import datetime

from maintenance_schedule.remind import (
    Maintenance,
    Period,
    new_schedule,
    add_to_schedule,
)


class FileStub:
    def __init__(self):
        self.written = ""

    def write(self, s):
        self.written += s


class PrintTestCase(unittest.TestCase):
    def test_print(self):
        schedule = new_schedule()
        startDate = datetime.date(2022, 8, 30)
        add_to_schedule(
            schedule,
            Maintenance(what="replace water filter", when=Period(months=2)),
            startDate,
        )
        add_to_schedule(
            schedule,
            Maintenance(what="change toothbrush", when=Period(months=6)),
            startDate,
        )
        add_to_schedule(
            schedule, Maintenance(what="change oil", when=Period(months=4)), startDate
        )
        file = FileStub()
        print(schedule, file=file)
        self.assertEqual(
            file.written,
            """\
October 30, 2022 - replace water filter
December 30, 2022 - change oil
February 28, 2023 - change toothbrush
""",
        )
