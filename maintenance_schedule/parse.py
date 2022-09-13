from typing import Dict
import datetime
import json

from maintenance_schedule.remind import Maintenance, HowOften


def to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


def parse_how_often(d: Dict[str, int]) -> HowOften:
    return HowOften(
        days=to_int(d["days"]),
        months=to_int(d["months"]),
        years=to_int(d["years"]),
    )


def parse_maintenance(message: str) -> Maintenance:
    decoded = json.loads(message)
    return Maintenance(
        what=decoded["what"],
        how_often=parse_how_often(decoded["howOften"]),
    )


def parse_from_date(message: str) -> datetime.date:
    decoded = json.loads(message)
    return datetime.date.fromisoformat(decoded["fromDate"])
