import datetime

from maintenance_schedule.remind import (
    HowOften,
    Maintenance,
    new_schedule,
    add_to_schedule,
)
from maintenance_schedule.persistence import serialize, deserialize

schedule = new_schedule()
add_to_schedule(
    schedule,
    Maintenance(what="clean vacuum filters", how_often=HowOften(months=2)),
    datetime.date.today(),
)
add_to_schedule(
    schedule,
    Maintenance(what="change car oil", how_often=HowOften(years=1)),
    datetime.date(2022, 4, 20),
)
add_to_schedule(
    schedule,
    Maintenance(what="backup computer", how_often=HowOften(months=1)),
    datetime.date(2022, 6, 1),
)
print(schedule)

with open("schedule.txt", "w", encoding="utf-8") as file:
    serialize(schedule, file)

# Later...

with open("schedule.txt", encoding="utf-8") as file:
    schedule = deserialize(file)

print(schedule)
