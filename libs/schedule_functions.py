import csv
from random import randint
from collections import defaultdict
from datetime import datetime
from os.path import dirname, join, realpath

all_compare_times = [
        [[1400, 1500], [1500, 1600], [1600, 1700], [1700, 1800]],
        [[900, 1100], [1100, 1200], [1200, 1300], [1300, 1400], [1400, 1600], [1600, 1800]],
        [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]
]
all_day_locations = [
    "sunday1PUW","sunday1FL","sunday1SP1a","sunday1SP1b","sunday1SP2a","sunday1SP2b","sunday2PUW","sunday2FL","sunday2SP1a","sunday2SP1b","sunday2SP2a","sunday2SP2b","sunday3PUW","sunday3FL","sunday3SP1a","sunday3SP1b","sunday3SP2a","sunday3SP2b","mondayPUW","mondayFL","mondaySP1a","mondaySP1b","mondaySP2a","mondaySP2b","tuesdayPUW","tuesdayFL","tuesdaySP1a","tuesdaySP1b","tuesdaySP2a","tuesdaySP2b","wednesdayPUW","wednesdayFL","wednesdaySP1a","wednesdaySP1b","wednesdaySP2a","wednesdaySP2b","thursdayPUW","thursdayFL","thursdaySP1a","thursdaySP1b","thursdaySP2a","thursdaySP2b","friday1aPUW","friday1aFL","friday1aSP1a","friday1aSP1b","friday1aSP2a","friday1aSP2b","friday1bPUW","friday1bFL","friday1bSP1a","friday1bSP1b","friday1bSP2a","friday1bSP2b","friday2aPUW","friday2aFL","friday2aSP1a","friday2aSP1b","friday2aSP2a","friday2aSP2b","friday2bPUW","friday2bFL","friday2bSP1a","friday2bSP1b","friday2bSP2a","friday2bSP2b","friday3aPUW","friday3aFL","friday3aSP1a","friday3aSP1b","friday3aSP2a","friday3aSP2b","friday3bPUW","friday3bFL","friday3bSP1a","friday3bSP1b","friday3bSP2a","friday3bSP2b","saturday1aPUW","saturday1aFL","saturday1aSP1a","saturday1aSP1b","saturday1aSP2a","saturday1aSP2b","saturday1bPUW","saturday1bFL","saturday1bSP1a","saturday1bSP1b","saturday1bSP2a","saturday1bSP2b","saturday2aPUW","saturday2aFL","saturday2aSP1a","saturday2aSP1b","saturday2aSP2a","saturday2aSP2b","saturday2bPUW","saturday2bFL","saturday2bSP1a","saturday2bSP1b","saturday2bSP2a","saturday2bSP2b","saturday3aPUW","saturday3aFL","saturday3aSP1a","saturday3aSP1b","saturday3aSP2a","saturday3aSP2b","saturday3bPUW","saturday3bFL","saturday3bSP1a","saturday3bSP1b","saturday3bSP2a","saturday3bSP2b"
]
schedule_header_list = [
    ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"],
    ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"],
    ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"]
]
master_template = [
    ["PICK-UP WINDOW", "", "", "", "", "", ""],
    ["FLOOR LEAD", "", "", "", "", "", ""],
    ["SERVICE PT 1", "", "", "", "", "", ""],
    ["SERVICE PT 1", "", "", "", "", "", ""],
    ["SERVICE PT 2", "", "", "", "", "", ""],
    ["SERVICE PT 2", "", "", "", "", "", ""],
    ["PROGRAMS", "", "", "", "", "", ""],
    ["PROJECT TIME", "", "", "", "", "", ""]
]
time_at_locations = ["pickup-window-time", "floor-lead-time", "sp1a-time", "sp1b-time", "sp2a-time", "sp2b-time"]
location_names = ["PUW", "FL", "SP1a", "SP1b", "SP2a", "SP2b"]
hour_ranges = [[1, 5], [1, 7]]
loc_range = 6
weekdays = ["sunday", "friday", "saturday"]

class Staff:
    def __init__(self, employee_csv):
        # Import the CSV with employee information
        with open(employee_csv, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            self.staff_list = [row for row in reader]
            for employee in self.staff_list:
                for data in employee:
                    if "hours" in data or "break" in data: employee[data] = self.format_time(employee[data])
        for employee in self.staff_list:
            employee["pickup-window-time"] = 0
            employee["floor-lead-time"] = 0
            employee["sp1a-time"] = 0
            employee["sp1b-time"] = 0
            employee["sp1-time"] = 0
            employee["sp2a-time"] = 0
            employee["sp2b-time"] = 0
            employee["sp2-time"] = 0
            employee["initials"] = self.create_initials(employee)
            employee["leave"] = []
            employee["program"] = []
        for employee in range(len(self.staff_list)):
            self.staff_list[employee]["rank"] = employee
    
    def format_time(self, input_time):
        output_time = input_time
        if "(" in output_time:
            output_time = output_time.split(")/(")
            for h1 in range(len(output_time)):
                output_time[h1] = output_time[h1].replace("(", "").replace(")", "")
                if "/" in output_time[h1]: output_time[h1] = output_time[h1].split("/")
        if "/" in output_time: output_time = output_time.split("/")
        if isinstance(output_time, list):
            for h1 in range(len(output_time)):
                if isinstance(output_time[h1], list):
                    for h2 in range(len(output_time[h1])):
                        if "am" in output_time[h1][h2].lower() or "pm" in output_time[h1][h2].lower():
                            if not "Off" in output_time[h1][h2] or not "None" in output_time[h1][h2]:
                                output_time[h1][h2] = output_time[h1][h2].split("-")
                                if isinstance(output_time[h1][h2], list):
                                    for h3 in range(len(output_time[h1][h2])):
                                        if "am" in output_time[h1][h2][h3] or "pm" in output_time[h1][h2][h3]: output_time[h1][h2][h3] = convert_time(output_time[h1][h2][h3], to_24=True)
                                else:
                                    if "am" in output_time[h1][h2] or "pm" in output_time[h1][h2]: output_time[h1][h2] = convert_time(output_time[h1][h2], to_24=True)
                else:
                    if "am" in output_time[h1].lower() or "pm" in output_time[h1].lower():
                        if not "Off" in output_time[h1] or not "None" in output_time[h1]:
                            output_time[h1] = output_time[h1].split("-")
                            for h2 in range(len(output_time[h1])):
                                if "am" in output_time[h1][h2] or "pm" in output_time[h1][h2]:
                                    output_time[h1][h2] = convert_time(output_time[h1][h2], to_24=True)
        else:
            if "am" in output_time.lower() or "pm" in output_time.lower():
                output_time = output_time.split("-")
                if isinstance(output_time, list):
                    for h1 in range(len(output_time)):
                        if "am" in output_time[h1].lower() or "pm" in output_time[h1].lower():
                            output_time[h1] = convert_time(output_time[h1], to_24=True)
                else:
                    if "am" in output_time.lower() or "pm" in output_time.lower():
                        output_time = convert_time(output_time, to_24=True)
        return output_time

    def create_initials(self, employee):
        employee_name_split = employee["name"].replace("-", " ").split()
        employee_initials = ""
        for i in employee_name_split:
            employee_initials += i[0]
        return employee_initials

def convert_time(input_time, to_24):
    output_time = input_time
    if to_24:
        if not ":" in output_time: output_time = output_time[:-2] + ":00" + output_time[-2:]
        output_time = datetime.strptime(output_time.upper(), "%I:%M%p").strftime("%H%M")
    else:
        output_time = datetime.strptime(str(output_time), "%H%M").strftime("%I:%M%p")
        if output_time[0] == "0": output_time = output_time[1:]
        output_time = output_time.replace(":00", "")
        output_time = output_time.replace("AM", "").replace("PM", "")
    return output_time

class Template:
    def __init__(self, template_csv):
        with open(template_csv, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            temp_list = [row for row in reader]
        self.schedule_template = defaultdict(list)
        for d in (temp_list[0], temp_list[1], temp_list[2], temp_list[3], temp_list[4], temp_list[5]):
            for key, value in d.items():
                self.schedule_template[key].append(value)
        for i in self.schedule_template:
            if "DEL" in self.schedule_template[i]:
                self.schedule_template[i].pop()
                self.schedule_template[i].pop()

STAFF = Staff(join(dirname(realpath(__file__)), "staff_info.csv"))

TEMPLATE = Template(join(dirname(realpath(__file__)), "template_info.csv"))

for employee in STAFF.staff_list:
    for day in all_day_locations:
        employee[day] = []

for employee in STAFF.staff_list:
    for day in TEMPLATE.schedule_template:
        names = []
        if "sunday" in day:
            compare_time = all_compare_times[0]
        elif "friday" in day or "saturday" in day:
            compare_time = all_compare_times[1]
        else:
            compare_time = all_compare_times[2]
        for hour in range(len(TEMPLATE.schedule_template[day])):
            if employee["name"].split()[0].lower() in TEMPLATE.schedule_template[day][hour]:
                if "*" in TEMPLATE.schedule_template[day][hour]:
                    dividing_index = TEMPLATE.schedule_template[day][hour].index("*")
                    dividing_hour = ""
                    for char in range(dividing_index, len(TEMPLATE.schedule_template[day][hour])):
                        if TEMPLATE.schedule_template[day][hour][char].isdigit() or TEMPLATE.schedule_template[day][hour][char] == ":":
                            dividing_hour += TEMPLATE.schedule_template[day][hour][char]
                    if dividing_hour[0] == "9" or dividing_hour[0:2] in ["10", "11"]:
                        dividing_hour += "am"
                    else:
                        dividing_hour += "pm"
                    if TEMPLATE.schedule_template[day][hour].index(employee["name"].split()[0].lower()) < dividing_index:
                        names.append([compare_time[hour], employee["name"].split()[0] + " 'til " + dividing_hour + "\n"])
                    else:
                        names.append([compare_time[hour], employee["name"].split()[0] + " at " + dividing_hour])
                else:
                    names.append([compare_time[hour], employee["name"].split()[0]])
            employee[day] = names

# This needs work
class LOCATION:
    def __init__(self, location_csv):
        with open(location_csv, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            data_list = list(reader)
        # print(data_list)

loc = LOCATION(join(dirname(realpath(__file__)), "location_info.csv"))

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

def compare_hours(emp1, emp2, hour1, hour2):
    if ((emp1 >= hour1 and emp2 <= hour2)
    or (emp1 < hour1 and emp2 >= hour2)
    or (emp1 < hour1 and emp2 >= hour1 and emp2 <= hour2)):
        return True

def create_project_time(compare_time, weekday_untrimmed, weekday, emp_selector, emp_selector_1, emp_selector_2):
    off_desk_employees = []
    for hour in compare_time:
        project_time_employees = []
        for employee in staff:
            if "sunday" in weekday:
                emp_hours = employee[weekday + "-hours"][emp_selector]
            elif "friday" in weekday or "saturday" in weekday:
                emp_hours = employee[weekday + "-hours"][emp_selector_1][emp_selector_2]
            else:
                emp_hours = employee[weekday_untrimmed + "-hours"]
            if isavailable(emp_hours, hour) and not isondesk(employee, weekday_untrimmed, hour):
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
    return off_desk_employees

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

def apply_leave(leave_employees, weekday_untrimmed, weekday, emp_selector, emp_selector_1, emp_selector_2):
    for item in leave_employees:
        for employee in staff:
            if employee["name"].split()[0].lower() in item[1]:
                if item[0] == "all day":
                    if "sunday" in weekday_untrimmed:
                        employee[weekday + "-hours"][emp_selector] = "Off"
                        employee[weekday + "-hours"][emp_selector] = "Off"
                    elif "friday" in weekday_untrimmed or "saturday" in weekday_untrimmed:
                        employee[weekday + "-hours"][emp_selector_1][emp_selector_2] = "Off"
                        employee[weekday + "-hours"][emp_selector_1][emp_selector_2] = "Off"
                    else:
                        employee[weekday + "-hours"] = "Off"
                        employee[weekday + "-hours"] = "Off"
                    for loc in all_day_locations:
                        if weekday in loc:
                            employee[loc] = []
                else:
                    for shift in employee:
                        if shift in all_day_locations and weekday in shift:
                            for loc in range(len(employee[shift])):
                                if len(employee[shift]) > 0:
                                    if compare_hours(employee[shift][loc][0][0], employee[shift][loc][0][1], item[0][0], item[0][1]):
                                        employee[shift] = []
                                        employee["leave"] = item[0]

def add_to_schedule(weekday_untrimmed, hour_range, compare_time, template):
    for loc in range(loc_range):
        day_loc = weekday_untrimmed + location_names[loc]
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
                                    template[loc][hour] += employee[k][names][1]
                        else:
                            if k == day_loc and employee[k][0] == compare_time[hour - 1]:
                                template[loc][hour] += employee[k][1]
            if template[loc][hour][-3:-1] == "pm":
                template[loc][hour] = template[loc][hour][:-1]

def shift_empty_spa(template):
    for hour in range(len(template[2])):
        if template[2][hour] == "" and template[3][hour] != "":
            template[2][hour] = template[3][hour]
            template[3][hour] = ""
        if template[4][hour] == "" and template[5][hour] != "":
            template[4][hour] = template[5][hour]
            template[5][hour] = ""
        if template[2][hour] == "" and template[3][hour] == "" and template[4][hour] != "" and template[5][hour] != "":
            template[2][hour] = template[5][hour]
            template[5][hour] = ""
        if template[2][hour] == "" and template[3][hour] == "" and template[1][hour] != "":
            template[2][hour] = template[1][hour]
            template[1][hour] = ""

def testing_function(weekday_untrimmed, weekday, emp_selector, emp_selector_1, emp_selector_2, template, off_desk_employees):
    available = off_desk_employees
    for hour in range(1, len(template[2])):
        if template[2][hour] == "" and template[3][hour] == "":
            if len(off_desk_employees[hour - 1]) > 1:
                available[hour - 1].pop(0)
                # WORKING HERE