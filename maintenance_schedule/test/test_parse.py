import unittest
import datetime


from maintenance_schedule.parse import parse_maintenance, parse_from_date


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
