from typing import Dict, Callable
import datetime
import json

from maintenance_schedule.remind import Maintenance, HowOften, Schedule


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


def parse_from_date(
    message: str, default_date: datetime.date = datetime.date.today()
) -> datetime.date:
    decoded = json.loads(message)
    try:
        return datetime.date.fromisoformat(decoded["fromDate"])
    except ValueError:
        return default_date


def parse_what(message: str) -> str:
    decoded = json.loads(message)
    return decoded["what"]


def parse_method(message: str) -> Callable[[str, Schedule], None]:
    decoded = json.loads(message)
    methods = {"add": add_to_schedule_from_message}
    return methods[decoded["method"]]


def add_to_schedule_from_message(message: str, schedule: Schedule):
    pass
