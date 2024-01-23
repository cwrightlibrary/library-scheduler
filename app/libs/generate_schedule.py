from csv_generators import convert_time, STAFF, TEMPLATE
from prettytable import PrettyTable
from random import randint

staff = STAFF.staff_list
template = TEMPLATE.schedule_template
compare_time = [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]
location_names = ["pickup-window", "floor-lead", "sp1a", "sp1b", "sp2a", "sp2b"]

def isavailable(employee, day, time):
    staff_in, staff_out, compare_in, compare_out = employee[day + "-hours"][0], employee[day + "-hours"][1], int(time[0]), int(time[1])
    if not staff_in in ["O", "f", "f"]: staff_in = int(staff_in)
    if not staff_out in ["O", "f", "f"]: staff_out = int(staff_out)
    if isinstance(staff_in, int) and isinstance(staff_out, int):
        if ((staff_in >= compare_in and staff_in < compare_out)
            or (staff_in < compare_in and staff_out > compare_out)
            or (staff_in < compare_in and staff_out > compare_in and staff_out <= compare_out)):
            return True

def isatlocation(employee, template, hour):
    y_n = []
    for loc in range(0, len(template)):
        if employee["name"].split()[0].lower() in template[loc][hour].lower():
            y_n.append("n")
        else:
            y_n.append("y")
    if not "n" in y_n:
        return True

def create_schedule(date):
    info_print = PrettyTable(["    WHO'S WORKING    ", "     LUNCH BREAKS     ", "   SCHEDULE CHANGES   "])
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
        
        all_employee_hours_list = []
        grouped_employees_by_hours = []
        
        for employee in staff:
            if is_sunday:
                employee_hours = employee[info_date + "-hours"][info_date_selector]
            elif is_friday_saturday:
                employee_hours = employee[info_date + "-hours"][info_date_selector_1][info_date_selector_2]
            else:
                employee_hours = employee[info_date + "-hours"]
            if not "Off" in employee_hours:
                all_employee_hours_list.append([employee_hours[0], employee_hours[1]])
        
        all_employee_hours_list = list(set(tuple(sorted(sub)) for sub in all_employee_hours_list))
        
        for hours in all_employee_hours_list:
            hour_1 = convert_time(hours[0], to_24=False)
            hour_2 = convert_time(hours[1], to_24=False)
            temp_employees = []
            for employee in staff:
                employee_name = employee["name"].split()[0]
                if is_sunday:
                    employee_hours = employee[info_date + "-hours"][info_date_selector]
                elif is_friday_saturday:
                    employee_hours = employee[info_date + "-hours"][info_date_selector_1][info_date_selector_2]
                else:
                    employee_hours = employee[info_date + "-hours"]
                if employee_hours[0] == hours[0] and employee_hours[1] == hours[1]:
                    temp_employees.append(employee_name)
            grouped_employees_by_hours.append([[hour_1, hour_2], temp_employees])
        
        for slot in grouped_employees_by_hours:
            info_working += "-".join(slot[0]) + ":\n" + ",\n".join(slot[1]) + "\n" + "\n"
        
        return info_working

    def fill_info_lunch(info_date):
        info_lunch = ""
        is_sunday = True if info_date == "sunday" else False
        is_friday_saturday = True if info_date == "friday" or info_date == "saturday" else False
        
        all_lunch_hours_list = []
        grouped_employees_by_lunch = []
        
        for employee in staff:
            if is_sunday:
                employee_lunch = employee[info_date + "-break"][info_date_selector]
            elif is_friday_saturday:
                employee_lunch = employee[info_date + "-break"][info_date_selector_1][info_date_selector_2]
            else:
                employee_lunch = employee[info_date + "-break"]
            if not "None" in employee_lunch:
                all_lunch_hours_list.append(employee_lunch[0])
        
        all_lunch_hours_list = list(set(all_lunch_hours_list))
        
        for lunch in all_lunch_hours_list:
            hour = convert_time(lunch, to_24=False)
            temp_employees = []
            for employee in staff:
                employee_name = employee["name"].split()[0]
                if is_sunday:
                    employee_lunch = employee[info_date + "-break"][info_date_selector]
                elif is_friday_saturday:
                    employee_lunch = employee[info_date + "-break"][info_date_selector_1][info_date_selector_2]
                else:
                    employee_lunch = employee[info_date + "-break"]
                if employee_lunch[0] == lunch:
                    temp_employees.append(employee_name)
            grouped_employees_by_lunch.append([hour, temp_employees])
        
        for slot in grouped_employees_by_lunch:
            lunch_start = slot[0]
            if ":30" in lunch_start:
                lunch_end = lunch_start.replace(":30", "")
                lunch_end = int(lunch_end) + 1
            else:
                lunch_end = int(slot[0]) + 1
            if lunch_end > 12:
                lunch_end -= 12
            if ":30" in lunch_start:
                lunch_end = str(lunch_end) + ":30"
            lunch_end = str(lunch_end)
            hours_string = lunch_start + "-" + lunch_end + ":\n"
            info_lunch += hours_string + ",\n".join(slot[1]) + "\n" + "\n"
        
        return info_lunch

    info_working = fill_info_working(info_date)
    info_lunch = fill_info_lunch(info_date)
    
    info_header_list = [[info_working, info_lunch, info_changes]]
    
    for d in info_header_list:
        info_print.add_row(d)
    
    schedule_header_list = [
        ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"],
        ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"],
        ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"]
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
        ["PICK-UP WINDOW", "", "", "", "", "", ""],
        ["FLOOR LEAD", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["PROJECT TIME", "", "", "", "", "", ""]
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
                                        assign_employee += employee["name"].split()[0] + " at " + split_hour
                            else:
                                for employee in staff:
                                    if not "Off" in employee[weekday_hours + "-hours"][0]:
                                        if split_employees[0] == employee["name"].split()[0].lower():
                                            assign_employee += employee["name"].split()[0]
                                        if split_employees[1] == employee["name"].split()[0].lower():
                                            assign_employee += " 'til " + convert_time(employee[weekday_hours + "-hours"][0], to_24=False) + "\n" + employee["name"].split()[0] + " at " + convert_time(employee[weekday_hours + "-hours"][0], to_24=False)
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
    
    # WORKING ON THIS
    for hour in range(1, len(weekday_template[0])):
        project_time_employees = []
        for employee in staff:
            if isatlocation(employee, weekday_template, hour):
                if isavailable(employee, info_date, compare_time[hour - 1]):
                    if employee["position"] != "security" and employee["position"] != "shelver":
                        project_time_employees.append(employee["initials"])
        weekday_template[6][hour] = ",\n".join(project_time_employees)

    for d in weekday_template:
        idx = weekday_template.index(d)
        if idx in [0, 1, 3, 5]:
            schedule_print.add_row(d, divider=True)
        else:
            schedule_print.add_row(d)
    return info_print, schedule_print

weekday_names = ["sunday1", "sunday2", "sunday3", "monday", "tuesday", "wednesday", "thursday", "friday1a", "friday1b", "friday2a", "friday2b", "friday3a", "friday3b", "saturday1a", "saturday1b", "saturday2a", "saturday2b", "saturday3a", "saturday3b"]

date = ["Tuesday", "January 23, 2024"]
monday_info, monday_schedule = create_schedule(date)

weekday = date[0]

if "sunday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 1]
if "friday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 2]
if "saturday" in weekday.lower():
    weekday = weekday[0:len(weekday) - 2]

info_width = 75

weekday_centered = " " * int((info_width / 2) - int(len(weekday) / 2)) + weekday
date_centered = " " * int((info_width / 2) - int(len(date[1].replace(",", " ")) / 2)) + date[1]

print(weekday_centered + "\n" + date_centered)
print(monday_info)
print(monday_schedule)
