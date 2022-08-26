from typing import NamedTuple
import re


class Time(NamedTuple):
    months: int = 0
    years: int = 0


class Item(NamedTuple):
    description: str
    time: Time


def parse(command: str) -> Item:
    pattern = re.compile("in ([0-9]+) (year|month)s? (.*)")
    matches = pattern.match(command)

    if matches.group(2) == "month":
        time = Time(months=int(matches.group(1)))
    else:
        time = Time(years=int(matches.group(1)))
    item = Item(description=matches.group(
        3), time=time)
    return item
