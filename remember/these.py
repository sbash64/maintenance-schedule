from typing import NamedTuple, List
import bisect


class Time(NamedTuple):
    months: int = 0
    years: int = 0


class Item(NamedTuple):
    description: str
    time: Time

    def __repr__(self):
        return "in {} months {}".format(self.time.months, self.description)

    def __lt__(self, other):
        return self.time.months < other.time.months


class Items:
    def __init__(self):
        self.items: List[Item] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.items) - 1)).format(*self.items)


def new() -> Items:
    return Items()


def add(items: Items, item: Item):
    bisect.insort(items.items, item)
