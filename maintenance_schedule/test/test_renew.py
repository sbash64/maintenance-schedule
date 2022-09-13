import unittest
import datetime

from maintenance_schedule.remind import (
    new_schedule,
    renew_maintenance,
    add_to_schedule,
    find_scheduled_maintenance,
    Maintenance,
    HowOften,
)


class RenewTestCase(unittest.TestCase):
    def test_tbd(self):
        schedule = new_schedule()
        add_to_schedule(
            schedule,
            Maintenance(what="refill prescription", how_often=HowOften(days=90)),
            datetime.date(2022, 7, 4),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="wash vacuum filters", how_often=HowOften(months=2)),
            datetime.date(2022, 8, 20),
        )
        add_to_schedule(
            schedule,
            Maintenance(what="change oil", how_often=HowOften(months=4)),
            datetime.date(2022, 2, 5),
        )
        renew_maintenance(schedule, "wash vacuum filters", datetime.date(2022, 10, 31))
        self.assertEqual(
            find_scheduled_maintenance(schedule, "wash vacuum filters").from_date,
            datetime.date(2022, 10, 31),
        )
