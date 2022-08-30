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
        add(
            reminders,
            Item(description=matches.group(6), time=Time()),
            datetime.date.fromordinal(1),
        )
    return reminders
