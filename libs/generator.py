from csv_generators import convert_time, STAFF, TEMPLATE, all_day_locations, all_compare_times
from os.path import dirname, join, realpath
from prettytable import PrettyTable
from random import randint

staff = STAFF.staff_list
template = TEMPLATE.schedule_template

def isavailable(employee, time):
    staff_in, staff_out, compare_in, compare_out = employee[0], employee[1], int(time[0]), int(time[1])
    if not str(staff_in) in ["O", "f", "f", "Off"]: staff_in = int(staff_in)
    if not str(staff_out) in ["O", "f", "f", "Off"]: staff_out = int(staff_out)
    if isinstance(staff_in, int) and isinstance(staff_out, int):
        if ((staff_in >= compare_in and staff_in < compare_out)
            or (staff_in < compare_in and staff_out > compare_out)
            or (staff_in < compare_in and staff_out > compare_in and staff_out <= compare_out)):
            return True

def isondesk(employee, day, hour):
    y_n = []
    for loc in all_day_locations:
        if day in loc:
            for shift in employee[loc]:
                if shift[0] == hour:
                    y_n.append("y")
                else:
                    y_n.append("n")
    if "y" in y_n:
        return True

def parse_leave_programs(adjustments):
    adjustment_employees = []
    for hours in adjustments:
        adjustment_employees.append(hours[1])
    adjustment_employees = list(set(tuple(sub) for sub in adjustment_employees))
    adjustment_employees = [[list(item)] for item in adjustment_employees]
    for hours in adjustment_employees:
        for item in adjustments:
            if item[1] == hours[0]:
                hours.append(item[0])
                if len(item) > 2:
                    hours.append(item[2])
    for hours in adjustment_employees:
        if hours[0][0] != 0 and hours[0][1] != 0:
            hours[0][0] = int(convert_time(hours[0][0], to_24=True))
            hours[0][1] = int(convert_time(hours[0][1], to_24=True))
        else:
            hours[0] = "all day"
    return adjustment_employees

def create_schedule(date, adjustments):
    schedule_header_list = [
        ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"],
        ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"],
        ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"]
    ]
    location_names = ["PUW", "FL", "SP1a", "SP1b", "SP2a", "SP2b"]
    time_at_locations = ["pickup-window-time", "floor-lead-time", "sp1a-time", "sp1b-time", "sp2a-time", "sp2b-time"]
    date_day = date[0].lower()
    if "sunday" in date_day:
        schedule_header = schedule_header_list[0]
        compare_time = all_compare_times[0]
        hour_range = [1, 5]
        weekday = "sunday"
        info_date_selector = int(date_day[len(date_day) - 1:]) - 1
    elif "friday" in date_day or "saturday" in date_day:
        schedule_header = schedule_header_list[2]
        compare_time = all_compare_times[1]
        hour_range = [1, 7]
        weekday = "friday" if "friday" in date_day else "saturday"
        info_date_selector_1 = int(date_day[len(date_day) - 2:len(date_day) - 1]) - 1
        info_date_selector_2 = date_day[len(date_day) - 1:]
        if info_date_selector_2 == "a": info_date_selector_2 = 0
        if info_date_selector_2 == "b": info_date_selector_2 = 1
    else:
        schedule_header = schedule_header_list[1]
        compare_time = all_compare_times[2]
        hour_range = [1, 7]
        weekday = date_day.lower()
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
    leave_employees = parse_leave_programs(adjustments[0])
    program_employees = parse_leave_programs(adjustments[1])
    for item in leave_employees:
        for employee in staff:
            if employee["name"].split()[0].lower() in item[1]:
                if item[0] == "all day":
                    if "sunday" in date_day:
                        emp_hours = employee[weekday + "-hours"][info_date_selector]
                    elif "friday" in date_day or "saturday" in date_day:
                        emp_hours = employee[weekday + "-hours"][info_date_selector_1][info_date_selector_2]
                    else:
                        emp_hours = employee[weekday + "-hours"]
                    emp_hours[0] = "Off"
                    emp_hours[1] = "Off"
                    for loc in all_day_locations:
                        if weekday in loc:
                            employee[loc] = []
                else:
                    for shift in employee:
                        if shift in all_day_locations and weekday in shift:
                            for loc in range(len(employee[shift])):
                                if ((employee[shift][loc][0][0] >= item[0][0] and employee[shift][loc][0][1] <= item[0][1])
                                    or (employee[shift][loc][0][0] < item[0][0] and employee[shift][loc][0][1] >= item[0][1])
                                    or (employee[shift][loc][0][0] < item[0][0] and employee[shift][loc][0][1] >= item[0][0] and employee[shift][loc][0][1] <= item[0][1])):
                                    employee[shift] = []
                                    employee["leave"] = item[0]
    loc_range = 6
    if "sunday" in date_day:
        for i in weekday_template:
            i.pop()
            i.pop()
    for loc in range(loc_range):
        day_loc = date_day + location_names[loc]
        for employee in staff:
            if len(employee[day_loc]) != 0:
                employee[time_at_locations[loc]] += 1
                employee["sp1-time"] = employee["sp1a-time"] + employee["sp1b-time"]
                employee["sp2-time"] = employee["sp2a-time"] + employee["sp2b-time"]
        for hour in range(hour_range[0], hour_range[1]):
            for employee in staff:
                if len(employee[day_loc]) != 0:
                    for k, v in employee.items():
                        if isinstance(employee[k], list) and len(employee[k]) != 0:
                            for names in range(len(employee[k])):
                                if k == day_loc and employee[k][names][0] == compare_time[hour - 1]:
                                    weekday_template[loc][hour] += employee[k][names][1]
                        else:
                            if k == day_loc and employee[k][0] == compare_time[hour - 1]:
                                weekday_template[loc][hour] += employee[k][1]
            if weekday_template[loc][hour][-3:-1] == "pm":
                weekday_template[loc][hour] = weekday_template[loc][hour][:-1]
    off_desk_employees = []
    for hour in compare_time:
        project_time_employees = []
        for employee in staff:
            if "sunday" in date_day:
                emp_hours = employee[weekday + "-hours"][info_date_selector]
            elif "friday" in date_day or "saturday" in date_day:
                emp_hours = employee[weekday + "-hours"][info_date_selector_1][info_date_selector_2]
            else:
                emp_hours = employee[weekday + "-hours"]
            if isavailable(emp_hours, hour) and not isondesk(employee, weekday, hour):
                if len(employee["leave"]) > 0:
                    leave1, leave2, hour1, hour2 = employee["leave"][0], employee["leave"][1], hour[0], hour[1]
                    if not ((leave1 >= hour1 and leave2 <= hour2)
                        or (leave1 < hour1 and leave2 > hour2)
                        or (leave1 < hour1 and leave2 > hour1 and leave2 <= hour2)):
                            if not employee["position"] in ["security", "part-time", "shelver"]:
                                project_time_employees.append(employee["initials"])
                else:
                    if not employee["position"] in ["security", "part-time", "shelver"]:
                        project_time_employees.append(employee["initials"])
        off_desk_employees.append(project_time_employees)
    for hour in range(len(off_desk_employees)):
        if weekday_template[2][hour + 1] == "" and weekday_template[3][hour + 1] == "":
            for employee in staff:
                if employee["initials"] == off_desk_employees[hour][-1]:
                    weekday_template[2][hour + 1] = employee["name"].split()[0]
                    off_desk_employees[hour].pop()
    for hour in range(len(off_desk_employees)):
        weekday_template[7][hour + 1] = ", ".join(off_desk_employees[hour])
    for hour in range(len(weekday_template[2])):
        if weekday_template[2][hour] == "" and weekday_template[3][hour] != "":
            weekday_template[2][hour] = weekday_template[3][hour]
            weekday_template[3][hour] = ""
        if weekday_template[4][hour] == "" and weekday_template[5][hour] != "":
            weekday_template[4][hour] = weekday_template[5][hour]
            weekday_template[5][hour] = ""
    for d in range(len(weekday_template)):
        schedule_print.add_row(weekday_template[d], divider=True) if d in [0, 1, 3, 5, 6] else schedule_print.add_row(weekday_template[d])
    return schedule_print

date = ["Friday1a", "January 29, 2024"]
adjustments = [
    [
        [["lea"], [0, 0]], 
        [["sonaite"], ["1:30pm", "2:15pm"]],
        [["alyssa"], ["11:00am", "1:00pm"]]
    ],
    [
        [["steve"], ["9:00am", "10:00am"], "storytime"],
        [["chris", "anthony"], ["4:00pm", "5:00pm"], "stem"]
    ]
]

schedule = create_schedule(date, adjustments)

if "sunday" in date[0].lower():
    weekday = "Sunday"
elif "friday" in date[0].lower():
    weekday = "Friday"
elif "saturday" in date[0].lower():
    weekday = "Saturday"
else:
    weekday = date[0]

table_string = schedule.get_string()
table_width = len(table_string.splitlines()[0])
weekday_centered = " " * int((table_width / 2) - int(len(weekday) / 2)) + weekday
date_centered = " " * int((table_width / 2) - int(len(date[1].replace(",", " ")) / 2)) + date[1]

print(weekday_centered)
print(date_centered)
print(schedule)
