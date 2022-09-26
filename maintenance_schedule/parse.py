from typing import Dict, Callable, NamedTuple
import datetime
import json

from maintenance_schedule.remind import (
    Maintenance,
    HowOften,
    Schedule,
    add_to_schedule,
    remove_from_schedule,
)
from maintenance_schedule.persistence import serialize


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


class Session(NamedTuple):
    schedule: Schedule
    file_path: str


def parse_method(message: str) -> Callable[[str, Session], None]:
    decoded = json.loads(message)
    methods = {
        "add": add_to_schedule_from_message,
        "remove": remove_from_schedule_from_message,
        "save": save_schedule,
    }
    return methods[decoded["method"]]


def add_to_schedule_from_message(message: str, session: Session):
    add_to_schedule(
        session.schedule,
        parse_maintenance(message),
        parse_from_date(message, datetime.date.today()),
    )


def remove_from_schedule_from_message(message: str, session: Session):
    remove_from_schedule(session.schedule, parse_what(message))


def save_schedule(message: str, session: Session):
    with open(session.file_path, "w", encoding="utf-8") as file:
        serialize(session.schedule, file)
