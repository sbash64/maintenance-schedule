from typing import NamedTuple, List
from datetime import date
import bisect

from dateutil.relativedelta import relativedelta


class Period(NamedTuple):
    days: int = 0
    months: int = 0
    years: int = 0


class Recurrence(NamedTuple):
    what: str
    period: Period


class NextAction(NamedTuple):
    startDate: date
    recurrence: Recurrence

    def __lt__(self, other):
        return action_date(self) < action_date(other)

    def __repr__(self):
        return "{} - {}".format(
            action_date(self).strftime("%B %d, %Y"), self.recurrence.what
        )


def action_date(nextAction: NextAction) -> date:
    return nextAction.startDate + relativedelta(
        years=nextAction.recurrence.period.years,
        months=nextAction.recurrence.period.months,
        days=nextAction.recurrence.period.days,
    )


class Schedule:
    def __init__(self):
        self.nextActions: List[NextAction] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.nextActions) - 1)).format(*self.nextActions)


def new_schedule() -> Schedule:
    return Schedule()


def add_to_schedule(schedule: Schedule, recurrence: Recurrence, startDate: date):
    bisect.insort(
        schedule.nextActions,
        NextAction(recurrence=recurrence, startDate=startDate),
    )
