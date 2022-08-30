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
    time: Time
    fromDate: date

    def date(self):
        return self.fromDate + relativedelta(
            years=self.time.years, months=self.time.months
        )

    def __lt__(self, other):
        return self.date() < other.date()

    def __repr__(self):
        return "{} - {}".format(self.date().strftime("%B %d, %Y"), self.description)


class Reminders:
    def __init__(self):
        self.todos: List[ToDo] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.todos) - 1)).format(*self.todos)


def new() -> Reminders:
    return Reminders()


def create_todo(item: Item, fromDate: date) -> ToDo:
    return ToDo(description=item.description, time=item.time, fromDate=fromDate)


def add(reminders: Reminders, item: Item, fromDate: date):
    bisect.insort(reminders.todos, create_todo(item, fromDate))
