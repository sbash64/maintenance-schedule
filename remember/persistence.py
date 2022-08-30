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
