import unittest

import datetime

from maintenance_schedule.remind import (
    new_schedule,
    add_to_schedule,
    remove_from_schedule,
    find_scheduled_maintenance,
    Maintenance,
    HowOften,
)


class AddRemoveTestCase(unittest.TestCase):
    def test_add(self):
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
        prescription = find_scheduled_maintenance(schedule, "refill prescription")
        self.assertEqual(prescription.maintenance.how_often.days, 90)
        self.assertEqual(prescription.from_date, datetime.date(2022, 7, 4))
        vacuum = find_scheduled_maintenance(schedule, "wash vacuum filters")
        self.assertEqual(vacuum.maintenance.how_often.months, 2)
        self.assertEqual(vacuum.from_date, datetime.date(2022, 8, 20))
        oil = find_scheduled_maintenance(schedule, "change oil")
        self.assertEqual(oil.maintenance.how_often.months, 4)
        self.assertEqual(oil.from_date, datetime.date(2022, 2, 5))

    def test_remove(self):
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
        remove_from_schedule(schedule, "wash vacuum filters")
        self.assertIsNone(find_scheduled_maintenance(schedule, "wash vacuum filters"))
