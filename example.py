import datetime

from maintenance_schedule.remind import (
    Period,
    Maintenance,
    new_schedule,
    add_to_schedule,
)
from maintenance_schedule.persistence import serialize, deserialize

schedule = new_schedule()
add_to_schedule(
    schedule,
    Maintenance(what="clean vacuum filters", period=Period(months=2)),
    datetime.date.today(),
)
add_to_schedule(
    schedule,
    Maintenance(what="change car oil", period=Period(years=1)),
    datetime.date(2022, 4, 20),
)
add_to_schedule(
    schedule,
    Maintenance(what="backup computer", period=Period(months=1)),
    datetime.date(2022, 6, 1),
)
print(schedule)

with open("schedule.txt", "w") as file:
    serialize(schedule, file)

# Later...

with open("schedule.txt") as file:
    schedule = deserialize(file)

print(schedule)
