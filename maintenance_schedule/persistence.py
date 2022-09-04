import re
import datetime

from maintenance_schedule.remind import (
    Schedule,
    new_schedule,
    add_to_schedule,
    Maintenance,
    Period,
)


def deserialize(file) -> Schedule:
    schedule = new_schedule()
    pattern = re.compile(
        "in ([0-9]+) (day|month|year)s? from ([0-9]{2})/([0-9]{2})/([0-9]{4}) (.*)"
    )
    for line in file:
        matches = pattern.match(line)
        if matches.group(2) == "day":
            when = Period(days=int(matches.group(1)))
        elif matches.group(2) == "month":
            when = Period(months=int(matches.group(1)))
        else:
            when = Period(years=int(matches.group(1)))
        add_to_schedule(
            schedule,
            Maintenance(what=matches.group(6), when=when),
            datetime.date(
                int(matches.group(5)), int(matches.group(3)), int(matches.group(4))
            ),
        )
    return schedule


def serialize(schedule: Schedule, file):
    for action in schedule.nextActions:
        if action.maintenance.when.months > 0:
            time_unit = "month"
            time_quantity = action.maintenance.when.months
        else:
            time_unit = "year"
            time_quantity = action.maintenance.when.years
        time = "{} {}".format(time_quantity, time_unit)
        if time_quantity > 1:
            time += "s"
        print(
            "in {} from {:02}/{:02}/{:04} {}".format(
                time,
                action.startDate.month,
                action.startDate.day,
                action.startDate.year,
                action.maintenance.what,
            ),
            file=file,
        )
