from typing import NamedTuple, List
from datetime import date
from dateutil.relativedelta import relativedelta
import bisect


class Time(NamedTuple):
    months: int = 0
    years: int = 0


class Item(NamedTuple):
    description: str
    time: Time


class ToDo(NamedTuple):
    description: str
    date: date

    def __lt__(self, other):
        return self.date < other.date

    def __repr__(self):
        return "{} - {}".format(self.date.strftime("%B %d, %Y"), self.description)


class Reminders:
    def __init__(self):
        self.todos: List[ToDo] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.todos) - 1)).format(*self.todos)


def new() -> Reminders:
    return Reminders()


def create_todo(item: Item, fromDate: date) -> ToDo:
    return ToDo(
        description=item.description,
        date=fromDate + relativedelta(years=item.time.years, months=item.time.months),
    )


def add(reminders: Reminders, item: Item, fromDate: date):
    bisect.insort(reminders.todos, create_todo(item, fromDate))
