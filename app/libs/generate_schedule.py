from generate_staff import convert_time, STAFF
from prettytable import PrettyTable

staff = STAFF.staff_list
compare_time = [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]

def isavailable(employee, day, time):
    staff_in, staff_out, staff_break, compare_in, compare_out = employee[day + "-hours"][0], employee[day + "-hours"][1], employee[day + "-break"][0], time[0], time[1]
    if not isinstance(staff_break, int): staff_break = 0
    if isinstance(staff_in, int) and isinstance(staff_out, int):
        if staff_in >= compare_in and staff_out >= compare_out:
            if (staff_break < compare_in or staff_break > compare_out) or staff_break == 0:
                return True

def staff_to_schedule(schedule, day):
    # REWORK THIS
    occupied_employees = []
    available_employees = []
    
    for shift in compare_time:
        temp_list = []
        for employee in staff:
            if isavailable(employee, day, shift) and not employee["position"] in ["security", "shelver"]:
                temp_list.append(employee)
        available_employees.append(temp_list)
    
    for employee in available_employees[0]:
        print(employee["name"])

schedule_print = PrettyTable(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"])
monday_template = [
    ["pick-up window", "", "", "", "", "", "",],
    ["floor lead", "", "", "", "", "", "",],
    ["service pt 1", "", "", "", "", "", "",],
    ["service pt 1", "", "", "", "", "", "",],
    ["service pt 2", "", "", "", "", "", "",],
    ["service pt 2", "", "", "", "", "", "",]
]

staff_to_schedule(monday_template, "monday")

for d in monday_template:
    schedule_print.add_row(d)

print(schedule_print)
