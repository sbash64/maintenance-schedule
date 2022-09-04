from typing import NamedTuple, List
from datetime import date
import bisect

from dateutil.relativedelta import relativedelta


class Period(NamedTuple):
    days: int = 0
    months: int = 0
    years: int = 0


class Maintenance(NamedTuple):
    what: str
    when: Period


class NextAction(NamedTuple):
    startDate: date
    maintenance: Maintenance

    def __lt__(self, other):
        return action_date(self) < action_date(other)

    def __repr__(self):
        return "{} - {}".format(
            action_date(self).strftime("%B %d, %Y"), self.maintenance.what
        )


def action_date(nextAction: NextAction) -> date:
    return nextAction.startDate + relativedelta(
        years=nextAction.maintenance.when.years,
        months=nextAction.maintenance.when.months,
        days=nextAction.maintenance.when.days,
    )


class Schedule:
    def __init__(self):
        self.nextActions: List[NextAction] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.nextActions) - 1)).format(*self.nextActions)


def new_schedule() -> Schedule:
    return Schedule()


def add_to_schedule(schedule: Schedule, maintenance: Maintenance, startDate: date):
    bisect.insort(
        schedule.nextActions,
        NextAction(maintenance=maintenance, startDate=startDate),
    )
