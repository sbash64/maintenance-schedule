from typing import NamedTuple
import re


class Time(NamedTuple):
    months: int


class Item(NamedTuple):
    description: str
    time: Time


def parse(command: str) -> Item:
    pattern = re.compile("in ([0-9]+) months (.*)")
    matches = pattern.match(command)
    item = Item(description=matches.group(
        2), time=Time(months=int(matches.group(1))))
    return item
