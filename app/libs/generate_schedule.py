from generate_staff import convert_time, STAFF
from prettytable import PrettyTable

schedule_print = PrettyTable(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"])

monday_template = [
    ["pick-up window", "", "", "", "", "", "",],
    ["floor lead", "", "", "", "", "", "",],
    ["service pt 1", "", "", "", "", "", "",],
    ["service pt 1", "", "", "", "", "", "",],
    ["service pt 2", "", "", "", "", "", "",],
    ["service pt 2", "", "", "", "", "", "",],
]

for d in monday_template:
    schedule_print.add_row(d)

print(schedule_print)
