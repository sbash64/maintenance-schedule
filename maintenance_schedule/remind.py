from typing import NamedTuple, List
from datetime import date
import bisect

from dateutil.relativedelta import relativedelta


class HowOften(NamedTuple):
    days: int = 0
    months: int = 0
    years: int = 0


class Maintenance(NamedTuple):
    what: str
    howOften: HowOften


class ScheduledMaintenance(NamedTuple):
    startDate: date
    maintenance: Maintenance

    def __lt__(self, other):
        return action_date(self) < action_date(other)

    def __repr__(self):
        return "{} - {}".format(
            action_date(self).strftime("%B %d, %Y"), self.maintenance.what
        )


def action_date(scheduled_maintenance: ScheduledMaintenance) -> date:
    return scheduled_maintenance.startDate + relativedelta(
        years=scheduled_maintenance.maintenance.howOften.years,
        months=scheduled_maintenance.maintenance.howOften.months,
        days=scheduled_maintenance.maintenance.howOften.days,
    )


class Schedule:
    def __init__(self):
        self.scheduled_maintenances: List[ScheduledMaintenance] = []

    def __str__(self):
        return ("{}" + "\n{}" * (len(self.scheduled_maintenances) - 1)).format(
            *self.scheduled_maintenances
        )


def new_schedule() -> Schedule:
    return Schedule()


def add_to_schedule(schedule: Schedule, maintenance: Maintenance, startDate: date):
    bisect.insort(
        schedule.scheduled_maintenances,
        ScheduledMaintenance(maintenance=maintenance, startDate=startDate),
    )


def renew_maintenance(schedule: Schedule, what: str, startDate: date):
    for i, action in enumerate(schedule.scheduled_maintenances):
        if action.maintenance.what == what:
            schedule.scheduled_maintenances[i] = action._replace(startDate=startDate)
            return
