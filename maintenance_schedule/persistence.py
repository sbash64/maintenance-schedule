import re
import datetime

from maintenance_schedule.remind import (
    Schedule,
    new_schedule,
    add_to_schedule,
    Maintenance,
    HowOften,
)


def deserialize(file) -> Schedule:
    schedule = new_schedule()
    pattern = re.compile(
        "in ([0-9]+) (day|month|year)s? from ([0-9]{2})/([0-9]{2})/([0-9]{4}) (.*)"
    )
    for line in file:
        matches = pattern.match(line)
        if matches.group(2) == "day":
            how_often = HowOften(days=int(matches.group(1)))
        elif matches.group(2) == "month":
            how_often = HowOften(months=int(matches.group(1)))
        else:
            how_often = HowOften(years=int(matches.group(1)))
        add_to_schedule(
            schedule,
            Maintenance(what=matches.group(6), how_often=how_often),
            datetime.date(
                int(matches.group(5)), int(matches.group(3)), int(matches.group(4))
            ),
        )
    return schedule


def serialize(schedule: Schedule, file):
    for scheduled_maintenance in schedule.scheduled_maintenances:
        if scheduled_maintenance.maintenance.how_often.months > 0:
            time_unit = "month"
            time_quantity = scheduled_maintenance.maintenance.how_often.months
        else:
            time_unit = "year"
            time_quantity = scheduled_maintenance.maintenance.how_often.years
        time = f"{time_quantity} {time_unit}"
        if time_quantity > 1:
            time += "s"
        print(
            f"in {time} from {scheduled_maintenance.from_date.month:02}/{scheduled_maintenance.from_date.day:02}/{scheduled_maintenance.from_date.year:04} {scheduled_maintenance.maintenance.what}",
            file=file,
        )
