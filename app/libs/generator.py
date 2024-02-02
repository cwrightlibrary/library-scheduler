from csv_generators import convert_time, STAFF, TEMPLATE, all_day_locations
from os.path import dirname, join, realpath
from prettytable import PrettyTable
from random import randint

staff = STAFF.staff_list
template = TEMPLATE.schedule_template

def create_schedule(date):
    schedule_header_list = [
        ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"],
        ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"],
        ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"]
    ]
    
    day_names = [
        "sunday1", "sunday2", "sunday3", "monday", "tuesday", "wednesday", "thursday", "friday1a", "friday1b", "friday2a", "friday2b", "friday3a", "friday3b", "saturday1a", "saturday1b", "saturday2a", "saturday2b", "saturday3a", "saturday3b"
    ]

    date_day = date[0].lower()
    if day_names.index(date_day) <= 2:
        schedule_header = schedule_header_list[0]
    if day_names.index(date_day) >= 3 and day_names.index(date_day) <= 6:
        schedule_header = schedule_header_list[1]
    if day_names.index(date_day) >= 7:
        schedule_header = schedule_header_list[2]
    
    schedule_print = PrettyTable(schedule_header)
    
    weekday_template = [
        ["PICK-UP WINDOW", "", "", "", "", "", ""],
        ["FLOOR LEAD", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["PROGRAMS", "", "", "", "", "", ""],
        ["PROJECT TIME", "", "", "", "", "", ""]
    ]
    
    location_names = ["PUW", "FL", "SP1a", "SP1b", "SP2a", "SP2b"]
    
    if "sunday" in date_day:
        for i in weekday_template:
            i.pop()
            i.pop()
    
    for loc in range(6):
        for employee in staff:
            pass
        print(date_day + location_names[loc])
    
    for d in range(6):
        if d in [0, 1, 3, 5]:
            schedule_print.add_row(weekday_template[d], divider=True)
        else:
            schedule_print.add_row(weekday_template[d])
    
    return schedule_print

date = ["Monday", "January 29, 2024"]

schedule = create_schedule(date)

print(schedule)