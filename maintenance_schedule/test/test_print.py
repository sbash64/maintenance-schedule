import unittest
import datetime

from maintenance_schedule.remind import Recurrence, Period, new_schedule, add


class FileStub:
    def __init__(self):
        self.written = ""

    def write(self, s):
        self.written += s


class PrintTestCase(unittest.TestCase):
    def test_tbd(self):
        schedule = new_schedule()
        startDate = datetime.date(2022, 8, 30)
        add(
            schedule,
            Recurrence(what="replace water filter", period=Period(months=2)),
            startDate,
        )
        add(
            schedule,
            Recurrence(what="change toothbrush", period=Period(months=6)),
            startDate,
        )
        add(schedule, Recurrence(what="change oil", period=Period(months=4)), startDate)
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
