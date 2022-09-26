import unittest
import datetime


from maintenance_schedule.parse import (
    parse_maintenance,
    parse_from_date,
    parse_what,
    parse_method,
    add_to_schedule_from_message,
    remove_from_schedule_from_message,
    save_schedule,
)


class ParseTestCase(unittest.TestCase):
    def test_maintenance(self):
        maintenance = parse_maintenance(
            '{"method":"add","what":"wash vacuum filters","fromDate":"2022-09-21","howOften":{"days":"","months":"2","years":""}}'
        )
        self.assertEqual(maintenance.what, "wash vacuum filters")
        self.assertEqual(maintenance.how_often.days, 0)
        self.assertEqual(maintenance.how_often.months, 2)
        self.assertEqual(maintenance.how_often.years, 0)

    def test_from_date(self):
        from_date = parse_from_date(
            '{"method":"add","what":"wash vacuum filters","fromDate":"2022-09-21","howOften":{"days":"","months":"2","years":""}}'
        )
        self.assertEqual(from_date, datetime.date(2022, 9, 21))

    def test_from_date_default(self):
        from_date = parse_from_date(
            '{"method":"add","what":"wash vacuum filters","fromDate":"","howOften":{"days":"","months":"2","years":""}}',
            datetime.date(2022, 3, 2),
        )
        self.assertEqual(from_date, datetime.date(2022, 3, 2))

    def test_what(self):
        what = parse_what('{"method":"remove","what":"wash vacuum filters"}')
        self.assertEqual(what, "wash vacuum filters")

    def test_method_add(self):
        method = parse_method(
            '{"method":"add","what":"wash vacuum filters","fromDate":"2022-09-21","howOften":{"days":"","months":"2","years":""}}'
        )
        self.assertEqual(method, add_to_schedule_from_message)

    def test_method_remove(self):
        method = parse_method('{"method":"remove","what":"wash vacuum filters"}')
        self.assertEqual(method, remove_from_schedule_from_message)

    def test_method_save(self):
        method = parse_method('{"method":"save"}')
        self.assertEqual(method, save_schedule)
