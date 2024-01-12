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

schedule_print = PrettyTable(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"])
monday_template = [
    ["pick-up window", "", "", "", "", "", ""],
    ["floor lead", "", "", "", "", "", ""],
    ["service pt 1", "", "", "", "", "", ""],
    ["service pt 1", "", "", "", "", "", ""],
    ["service pt 2", "", "", "", "", "", ""],
    ["service pt 2", "", "", "", "", "", ""],
    ["project time", "", "", "", "", "", ""]
]

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
                        pass
            i += 1

fill_template(monday_template, "monday", staff, template)

for d in monday_template:
    schedule_print.add_row(d)

print(schedule_print)
