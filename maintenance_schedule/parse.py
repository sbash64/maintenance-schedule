import json

from maintenance_schedule.remind import Maintenance, HowOften


def to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


def parse_maintenance(message: str) -> Maintenance:
    decoded = json.loads(message)
    return Maintenance(
        what=decoded["what"],
        how_often=HowOften(
            days=to_int(decoded["howOften"]["days"]),
            months=to_int(decoded["howOften"]["months"]),
            years=to_int(decoded["howOften"]["years"]),
        ),
    )
