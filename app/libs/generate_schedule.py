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
    header_list = [
        ["", "2-3", "3-4", "4-5", "5-6"],
        ["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"],
        ["", "9-11", "11-12", "12-1", "1-2", "2-4", "4-6"]
    ]
    day_names = ["sunday1", "sunday2", "sunday3", "monday", "tuesday", "wednesday", "thursday", "friday1a", "friday1b", "friday2a", "friday2b", "friday3a", "friday3b", "saturday1a", "saturday1b", "saturday2a", "saturday2b", "saturday3a", "saturday3b"]
    
    date_day = date[0].lower()
    if day_names.index(date_day) <= 2:
        header = header_list[0]
    if day_names.index(date_day) >= 3 and day_names.index(date_day) <= 6:
        header = header_list[1]
    if day_names.index(date_day) >= 7:
        header = header_list[2]
    
    info_print = PrettyTable()
    
    schedule_print = PrettyTable(header)
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
                            for employee in staff:
                                if split_employees[0] == employee["name"].split()[0].lower():
                                    assign_employee += employee["name"].split()[0]
                                if split_employees[1] == employee["name"].split()[0].lower():
                                    assign_employee += " 'til " + convert_time(employee[weekday + "-hours"][0], to_24=False) + "\n" + employee["name"].split()[0] + " @ " + convert_time(employee[weekday + "-hours"][0], to_24=False)
                            schedule[i][hour + 1] = assign_employee
                        elif "*" in template[day][hour]:
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
    return (info_print, schedule_print)

monday_schedule = create_schedule(["Sunday1", "January 15, 2024"])

print(monday_schedule)
