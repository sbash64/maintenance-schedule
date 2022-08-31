import re
import datetime

from maintenance_schedule.remind import Schedule, new_schedule, add, Recurrence, Period


def deserialize(file) -> Schedule:
    schedule = new_schedule()
    pattern = re.compile(
        "in ([0-9]+) (month|year)s from ([0-9]{2})/([0-9]{2})/([0-9]{4}) (.*)"
    )
    for line in file:
        matches = pattern.match(line)
        if matches.group(2) == "month":
            period = Period(months=int(matches.group(1)))
        else:
            period = Period(years=int(matches.group(1)))
        add(
            schedule,
            Recurrence(what=matches.group(6), period=period),
            datetime.date(
                int(matches.group(5)), int(matches.group(3)), int(matches.group(4))
            ),
        )
    return schedule


def serialize(schedule: Schedule, file):
    for action in schedule.nextActions:
        if action.recurrence.period.months > 0:
            time = "{} month".format(action.recurrence.period.months)
            if action.recurrence.period.months > 1:
                time += "s"
        else:
            time = "{} year".format(action.recurrence.period.years)
            if action.recurrence.period.years > 1:
                time += "s"
        print(
            "in {} from {:02}/{:02}/{:04} {}".format(
                time,
                action.startDate.month,
                action.startDate.day,
                action.startDate.year,
                action.recurrence.what,
            ),
            file=file,
        )
