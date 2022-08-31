from typing import NamedTuple, List
from datetime import date
import bisect

from dateutil.relativedelta import relativedelta


class Period(NamedTuple):
    months: int = 0
    years: int = 0


class Recurrence(NamedTuple):
    what: str
    period: Period


class NextAction(NamedTuple):
    startDate: date
    recurrence: Recurrence

    def date(self):
        return self.startDate + relativedelta(
            years=self.recurrence.period.years, months=self.recurrence.period.months
        )

    def __lt__(self, other):
        return self.date() < other.date()

    def __repr__(self):
        return "{} - {}".format(self.date().strftime("%B %d, %Y"), self.recurrence.what)


class Schedule:
    def __init__(self):
        self.nextActions: List[NextAction] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.nextActions) - 1)).format(*self.nextActions)


def new_schedule() -> Schedule:
    return Schedule()


def add(schedule: Schedule, recurrence: Recurrence, startDate: date):
    bisect.insort(
        schedule.nextActions,
        NextAction(recurrence=recurrence, startDate=startDate),
    )
