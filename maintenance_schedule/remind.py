from typing import NamedTuple, List, Optional
from datetime import date
import bisect

from dateutil.relativedelta import relativedelta


class HowOften(NamedTuple):
    days: int = 0
    months: int = 0
    years: int = 0


class Maintenance(NamedTuple):
    what: str
    how_often: HowOften


class ScheduledMaintenance(NamedTuple):
    from_date: date
    maintenance: Maintenance

    def __lt__(self, other):
        return action_date(self) < action_date(other)

    def __repr__(self):
        when = action_date(self).strftime("%B %d, %Y")
        return f"{when} - {self.maintenance.what}"


def action_date(scheduled_maintenance: ScheduledMaintenance) -> date:
    return scheduled_maintenance.from_date + relativedelta(
        years=scheduled_maintenance.maintenance.how_often.years,
        months=scheduled_maintenance.maintenance.how_often.months,
        days=scheduled_maintenance.maintenance.how_often.days,
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


def add_to_schedule(schedule: Schedule, maintenance: Maintenance, from_date: date):
    bisect.insort(
        schedule.scheduled_maintenances,
        ScheduledMaintenance(maintenance=maintenance, from_date=from_date),
    )


def remove_from_schedule(schedule: Schedule, what: str):
    for i, scheduled_maintenance in enumerate(schedule.scheduled_maintenances):
        if scheduled_maintenance.maintenance.what == what:
            del schedule.scheduled_maintenances[i]


def renew_maintenance(schedule: Schedule, what: str, from_date: date):
    for i, scheduled_maintenance in enumerate(schedule.scheduled_maintenances):
        if scheduled_maintenance.maintenance.what == what:
            schedule.scheduled_maintenances[i] = scheduled_maintenance._replace(
                from_date=from_date
            )
            return


def find_scheduled_maintenance(
    schedule: Schedule, what: str
) -> Optional[ScheduledMaintenance]:
    for scheduled_maintenance in schedule.scheduled_maintenances:
        if scheduled_maintenance.maintenance.what == what:
            return scheduled_maintenance
    return None
