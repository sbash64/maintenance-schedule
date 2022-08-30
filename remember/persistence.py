import re
import datetime

from remember.these import Reminders, new, add, Item, Time


def deserialize(file) -> Reminders:
    reminders = new()
    pattern = re.compile(
        "in ([0-9]+) (month|year)s from ([0-9]{2})/([0-9]{2})/([0-9]{4}) (.*)"
    )
    for line in file:
        matches = pattern.match(line)
        if matches.group(2) == "month":
            time = Time(months=int(matches.group(1)))
        else:
            time = Time(years=int(matches.group(1)))
        add(
            reminders,
            Item(description=matches.group(6), time=time),
            datetime.date(
                int(matches.group(5)), int(matches.group(3)), int(matches.group(4))
            ),
        )
    return reminders


def serialize(reminders: Reminders, file):
    for todo in reminders.todos:
        if todo.time.months > 0:
            time = "{} month".format(todo.time.months)
            if todo.time.months > 1:
                time += "s"
        else:
            time = "{} year".format(todo.time.years)
            if todo.time.years > 1:
                time += "s"
        print(
            "in {} from {:02}/{:02}/{:04} {}".format(
                time,
                todo.fromDate.month,
                todo.fromDate.day,
                todo.fromDate.year,
                todo.description,
            ),
            file=file,
        )
