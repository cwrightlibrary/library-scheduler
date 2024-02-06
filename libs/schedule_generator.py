from csv_generators import convert_time, STAFF, TEMPLATE, all_compare_times, all_day_locations, schedule_header_list, master_template, time_at_locations, location_names, hour_ranges, loc_range, weekdays
from os.path import dirname, join, realpath
from prettytable import PrettyTable
from random import randint

staff = STAFF.staff_list
template = TEMPLATE.schedule_template

def isavailable(emp_hours, comp_hours):
    emp_in, emp_out, comp_in, comp_out = emp_hours[0], emp_hours[1], int(comp_hours[0]), int(comp_hours[1])
    if not str(emp_in) in ["O", "f", "Off"]: emp_in = int(emp_in)
    if not str(emp_out) in ["O", "f", "Off"]: emp_out = int(emp_out)
    if isinstance(emp_in, int) and isinstance(emp_out, int):
        if ((emp_in >= comp_in and emp_in < comp_out)
        or (emp_in < comp_in and emp_out > comp_out)
        or (emp_in < comp_in and emp_out > comp_in and emp_out <= comp_out)):
            return True

def isondesk(emp, weekday, hour):
    y_n = []
    for loc in all_day_locations:
        if weekday in loc:
            for shift in emp[loc]:
                if shift[0] == hour:
                    y_n.append("y")
                else:
                    y_n.append("n")
    if "y" in y_n:
        return True

def sort_adjustments(adjustments):
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

def create_schedule_info(weekday_untrimmed):
    schedule_header, compare_time, hour_range, weekday, emp_selector, emp_selector_1, emp_selector_2 = [], [], [], "", 0, 0, ""
    if weekdays[0] in weekday_untrimmed:
        schedule_header = schedule_header_list[0]
        compare_time = all_compare_times[0]
        hour_range = hour_ranges[0]
        weekday = weekdays[0]
        emp_selector = int(weekday_untrimmed[len(weekday_untrimmed) - 1:]) - 1
    elif "friday" in weekday_untrimmed or "saturday" in weekday_untrimmed:
        schedule_header = schedule_header_list[1]
        compare_time = all_compare_times[1]
        hour_range = hour_ranges[1]
        weekday = weekdays[1] if "friday" in weekday_untrimmed else weekdays[2]
        emp_selector_1 = int(weekday_untrimmed[len(weekday_untrimmed) - 2:len(weekday_untrimmed) - 1]) - 1
        emp_selector_2 = weekday_untrimmed[len(weekday_untrimmed) - 1:]
        emp_selector_2 = 0 if emp_selector_2 == "a" else 1
    else:
        schedule_header = schedule_header_list[2]
        compare_time = all_compare_times[2]
        hour_range = hour_ranges[1]
        weekday = weekday_untrimmed.lower()
    return schedule_header, compare_time, hour_range, weekday, emp_selector, emp_selector_1, emp_selector_2

def create_schedule_template(weekday):
    template = master_template
    if "sunday" in weekday:
        for hour in template:
            hour.pop()
            hour.pop()
    return template

def create_schedule(date, adjustments):
    weekday_untrimmed = date[0].lower()
    schedule_header, compare_time, hour_range, weekday, emp_selector, emp_selector_1, emp_selector_2 = create_schedule_info(weekday_untrimmed)
    
    leave_employees = sort_adjustments(adjustments[0])
    program_employees = sort_adjustments(adjustments[1])
    
    schedule = PrettyTable(schedule_header)
    template = create_schedule_template(weekday)
    
    for loc in range(len(template)):
        schedule.add_row(template[loc], divider=True) if loc in [0, 1, 3, 5, 6] else schedule.add_row(template[loc])
    
    table_string = schedule.get_string()
    table_width = len(table_string.splitlines()[0])
    weekday_centered = " " * int((table_width / 2) - int(len(weekday) / 2)) + weekday.capitalize()
    date_centered = " " * int((table_width / 2) - int(len(date[1].replace(",", " ")) / 2)) + date[1].title()
    
    full_date = weekday_centered + "\n" + date_centered
    return schedule, full_date

date = ["Tuesday", "February 6, 2024"]
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
test, full_date = create_schedule(date, adjustments)
print(full_date)
print(test)
