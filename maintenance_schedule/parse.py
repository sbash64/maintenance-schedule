import json

from maintenance_schedule.remind import Maintenance, HowOften


def parse_maintenance(message: str) -> Maintenance:
    decoded = json.loads(message)
    return Maintenance(what=decoded["what"], how_often=HowOften())
