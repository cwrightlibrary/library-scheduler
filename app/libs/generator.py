from csv_generators import convert_time, STAFF, TEMPLATE, all_day_locations, all_compare_times
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
    
    dict_avoids = [
        "name","position","sunday-hours","monday-hours","tuesday-hours","wednesday-hours","thursday-hours","friday-hours","saturday-hours","sunday-break","monday-break","tuesday-break","wednesday-break","thursday-break","friday-break","saturday-break", "pickup-window-time", "floor-lead-time", "sp1a-time", "sp1b-time", "sp1-time", "sp2a-time", "sp2b-time", "sp2-time", "initials", "rank"
    ]

    loc_range = 6
    date_day = date[0].lower()
    if "sunday" in date_day:
        schedule_header = schedule_header_list[0]
        compare_time = all_compare_times[0]
        hour_range = [1, 5]
    elif "friday" in date_day or "saturday" in date_day:
        schedule_header = schedule_header_list[2]
        compare_time = all_compare_times[1]
        hour_range = [1, 7]
    else:
        schedule_header = schedule_header_list[1]
        compare_time = all_compare_times[2]
        hour_range = [1, 7]
    
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
    print(len(compare_time))
    for loc in range(loc_range):
        day_loc = date_day + location_names[loc]
        for hour in range(hour_range[0], hour_range[1]):
            for employee in staff:
                if len(employee[day_loc]) != 0:
                    for k, v in employee.items():
                        if k == day_loc and employee[k][0] == compare_time[hour - 1]:
                            weekday_template[loc][hour] += employee[k][1]
            if weekday_template[loc][hour][-3:-1] == "pm":
                weekday_template[loc][hour] = weekday_template[loc][hour][:-1]

    for d in range(len(weekday_template)):
        if d in [0, 1, 3, 5, 6]:
            schedule_print.add_row(weekday_template[d], divider=True)
        else:
            schedule_print.add_row(weekday_template[d])
    
    return schedule_print

# some weekends/fridays don't work
date = ["Sunday3", "January 29, 2024"]

schedule = create_schedule(date)

print(schedule)
