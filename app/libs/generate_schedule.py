from csv_generators import convert_time, STAFF, TEMPLATE
from prettytable import PrettyTable
from random import randint

staff = STAFF.staff_list
template = TEMPLATE.schedule_template
compare_time = [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]
location_names = ["pickup-window", "floor-lead", "sp1a", "sp1b", "sp2a", "sp2b"]

def isavailable(employee, day, time):
    staff_in, staff_out, staff_break, compare_in, compare_out = employee[day + "-hours"][0], employee[day + "-hours"][1], employee[day + "-break"][0], time[0], time[1]
    if not isinstance(staff_break, int): staff_break = 0
    if isinstance(staff_in, int) and isinstance(staff_out, int):
        if ((staff_in >= compare_in and staff_in < compare_out)
            or (staff_in < compare_in and staff_out > compare_out)
            or (staff_in < compare_in and staff_out > compare_in and staff_out <= compare_out)):
            return True

def create_schedule(date):
    info_print = PrettyTable(["who's working", "lunch breaks", "schedule changes"])
    info_working, info_lunch, info_changes = "", "", ""
    
    info_date = date[0].lower()
    if "sunday" in info_date:
        info_date_selector = int(info_date[len(info_date) - 1:]) - 1
        info_date = info_date[0:len(info_date) - 1]
    if "friday" in info_date:
        info_date_selector_1 = int(info_date[len(info_date) - 2:len(info_date) - 1]) - 1
        info_date_selector_2 = info_date[len(info_date) - 1:]
        if info_date_selector_2 == "a":info_date_selector_2 = 0
        if info_date_selector_2 == "b": info_date_selector_2 = 1
        info_date = info_date[0:len(info_date) - 2]
    if "saturday" in info_date:
        info_date_selector_1 = int(info_date[len(info_date) - 2:len(info_date) - 1]) - 1
        info_date_selector_2 = info_date[len(info_date) - 1:]
        if info_date_selector_2 == "a": info_date_selector_2 = 0
        if info_date_selector_2 == "b": info_date_selector_2 = 1
        info_date = info_date[0:len(info_date) - 2]
    
    def fill_info_working(info_date):
        info_working = ""
        is_sunday = True if info_date == "sunday" else False
        is_friday_saturday = True if info_date == "friday" or info_date == "saturday" else False
        is_weekday = True if not is_sunday and not is_friday_saturday else False

        a_workers = []
        b_workers = []
        c_workers = []
        
        for employee in staff:
            employee_name = employee["name"].split()[0]
            if is_sunday:
                employee_hours = employee[info_date + "-hours"][info_date_selector]
                if not "Off" in employee_hours:
                    a_workers.append(employee_name)
            elif is_friday_saturday:
                employee_hours = employee[info_date + "-hours"][info_date_selector_1][info_date_selector_2]
                if not "Off" in employee_hours:
                    if employee_hours[0] == "0900" and employee_hours[1] == "1800":
                        a_workers.append(employee_name)
                    else:
                        employee_float = convert_time(employee_hours[0], to_24=False) + "-" + convert_time(employee_hours[1], to_24=False) + ": " + employee_name
                        b_workers.append(employee_float)
            elif is_weekday:
                employee_hours = employee[info_date + "-hours"]
                if not "Off" in employee_hours:
                    if employee_hours[0] == "0900" and employee_hours[1] == "1730":
                        a_workers.append(employee_name)
                    elif employee_hours[0] == "1400" and employee_hours[1] == "2000":
                        b_workers.append(employee_name)
                    else:
                        employee_float = convert_time(employee_hours[0], to_24=False) + "-" + convert_time(employee_hours[1], to_24=False) + ": " + employee_name
                        c_workers.append(employee_float)
        
        if is_sunday:
            info_working += "2-6:\n" + ",\n".join(a_workers)
        elif is_friday_saturday:
            info_working += "9-6:\n" + ",\n".join(a_workers)
            info_working += "\n\n"
            info_working += "\n".join(b_workers)
        elif is_weekday:
            info_working += "9-5:30:\n" + ",\n".join(a_workers)
            info_working += "\n\n"
            info_working += "2-8:\n" + ",\n".join(b_workers)
            info_working += "\n\n"
            info_working += "\n".join(c_workers)
        
        return info_working

    info_working = fill_info_working(info_date)
    
    info_header_list = [[info_working, info_lunch, info_changes]]
    
    for d in info_header_list:
        info_print.add_row(d)
    
    schedule_header_list = [
        ["", "2-3", "3-4", "4-5", "5-6"],
        ["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"],
        ["", "9-11", "11-12", "12-1", "1-2", "2-4", "4-6"]
    ]
    day_names = ["sunday1", "sunday2", "sunday3", "monday", "tuesday", "wednesday", "thursday", "friday1a", "friday1b", "friday2a", "friday2b", "friday3a", "friday3b", "saturday1a", "saturday1b", "saturday2a", "saturday2b", "saturday3a", "saturday3b"]
    
    date_day = date[0].lower()
    if day_names.index(date_day) <= 2:
        schedule_header = schedule_header_list[0]
    if day_names.index(date_day) >= 3 and day_names.index(date_day) <= 6:
        schedule_header = schedule_header_list[1]
    if day_names.index(date_day) >= 7:
        schedule_header = schedule_header_list[2]
    
    schedule_print = PrettyTable(schedule_header)
    weekday_template = [
        ["pick-up window", "", "", "", "", "", ""],
        ["floor lead", "", "", "", "", "", ""],
        ["service pt 1", "", "", "", "", "", ""],
        ["service pt 1", "", "", "", "", "", ""],
        ["service pt 2", "", "", "", "", "", ""],
        ["service pt 2", "", "", "", "", "", ""],
        ["project time", "", "", "", "", "", ""]
    ]
    if "sunday" in date_day:
        for i in weekday_template:
            i.pop()
            i.pop()

    def fill_template(schedule, weekday, staff, template):
        i = 0
        for day in template:
            if weekday in day:
                for hour in range(len(template[day])):
                    if not "none" == template[day][hour]:
                        if not "/" in template[day][hour] and not "*" in template[day][hour]:
                            for employee in staff:
                                if template[day][hour] == employee["name"].split()[0].lower():
                                    assign_employee = employee["name"].split()[0]
                            schedule[i][hour + 1] = assign_employee
                        elif "/" in template[day][hour]:
                            split_employees = template[day][hour].split("/")
                            assign_employee = ""
                            if "*" in template[day][hour]:
                                split_idx = split_employees[0].index("*")
                                split_hour = split_employees[0][split_idx + 1:]
                                split_employees[0] = split_employees[0][0:split_idx]
                            if "friday" in weekday or "saturday" in weekday:
                                weekday_hours = weekday[0:len(weekday) - 2]
                            elif "sunday" in weekday:
                                weekday_hours = weekday[0:len(weekday) - 1]
                            else:
                                weekday_hours = weekday
                            if "*" in template[day][hour]:
                                for employee in staff:
                                    if split_employees[0] == employee["name"].split()[0].lower():
                                        assign_employee += employee["name"].split()[0] + " 'til " + split_hour + "\n"
                                for employee in staff:
                                    if split_employees[1] == employee["name"].split()[0].lower():
                                        assign_employee += employee["name"].split()[0] + " @ " + split_hour
                            else:
                                for employee in staff:
                                    if not "Off" in employee[weekday_hours + "-hours"][0]:
                                        if split_employees[0] == employee["name"].split()[0].lower():
                                            assign_employee += employee["name"].split()[0]
                                        if split_employees[1] == employee["name"].split()[0].lower():
                                            assign_employee += " 'til " + convert_time(employee[weekday_hours + "-hours"][0], to_24=False) + "\n" + employee["name"].split()[0] + " @ " + convert_time(employee[weekday_hours + "-hours"][0], to_24=False)
                            schedule[i][hour + 1] = assign_employee
                        elif "*" in template[day][hour] and not "/" in template[day][hour]:
                            split_employee = template[day][hour].split("*")
                            assign_employee = ""
                            for employee in staff:
                                if split_employee[0] == employee["name"].split()[0].lower():
                                    assign_employee += employee["name"].split()[0] + " 'til " + split_employee[1]
                            schedule[i][hour + 1] = assign_employee
                i += 1

    fill_template(weekday_template, date_day, staff, template)

    for d in weekday_template:
        schedule_print.add_row(d)
    return info_print, schedule_print

weekday_names = ["sunday1", "sunday2", "sunday3", "monday", "tuesday", "wednesday", "thursday", "friday1a", "friday1b", "friday2a", "friday2b", "friday3a", "friday3b", "saturday1a", "saturday1b", "saturday2a", "saturday2b", "saturday3a", "saturday3b"]

date = ["Friday1a", "January 26, 2024"]
monday_info, monday_schedule = create_schedule(date)

weekday = date[0]

if "sunday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 1]
if "friday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 2]
if "saturday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 2]

print(weekday + "\n" + date[1])
print(monday_info)
# print(monday_schedule)
