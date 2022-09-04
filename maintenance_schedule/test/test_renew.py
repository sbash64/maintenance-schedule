import unittest
import datetime

from maintenance_schedule.remind import (
    new_schedule,
    renew_maintenance,
    add_to_schedule,
    Maintenance,
    HowOften,
)


class RenewTestCase(unittest.TestCase):
    def test_tbd(self):
        schedule = new_schedule()
        add_to_schedule(
            schedule,
            Maintenance(what="refill prescription", howOften=HowOften(days=90)),
            datetime.date(2022, 7, 4),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="wash vacuum filters", howOften=HowOften(months=2)),
            datetime.date(2022, 8, 20),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="change oil", howOften=HowOften(months=4)),
            datetime.date(2022, 2, 5),
        )
        renew_maintenance(schedule, "wash vacuum filters", datetime.date(2022, 10, 31))
        self.assertEqual(schedule.nextActions[2].startDate, datetime.date(2022, 10, 31))
