import unittest


from maintenance_schedule.parse import parse_maintenance


class ParseTestCase(unittest.TestCase):
    def test_tbd(self):
        maintenance = parse_maintenance(
            '{"method":"add","what":"wash vacuum filters","months":"2","years":""}'
        )
        self.assertEqual(maintenance.what, "wash vacuum filters")
