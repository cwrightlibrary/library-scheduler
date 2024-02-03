import csv
from collections import defaultdict
from datetime import datetime
from os.path import dirname, join, realpath

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

all_compare_times = [
        [[1400, 1500], [1500, 1600], [1600, 1700], [1700, 1800]],
        [[900, 1100], [1100, 1200], [1200, 1300], [1300, 1400], [1400, 1600], [1600, 1800]],
        [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]
]

all_day_locations = [
    "sunday1PUW","sunday1FL","sunday1SP1a","sunday1SP1b","sunday1SP2a","sunday1SP2b","sunday2PUW","sunday2FL","sunday2SP1a","sunday2SP1b","sunday2SP2a","sunday2SP2b","sunday3PUW","sunday3FL","sunday3SP1a","sunday3SP1b","sunday3SP2a","sunday3SP2b","mondayPUW","mondayFL","mondaySP1a","mondaySP1b","mondaySP2a","mondaySP2b","tuesdayPUW","tuesdayFL","tuesdaySP1a","tuesdaySP1b","tuesdaySP2a","tuesdaySP2b","wednesdayPUW","wednesdayFL","wednesdaySP1a","wednesdaySP1b","wednesdaySP2a","wednesdaySP2b","thursdayPUW","thursdayFL","thursdaySP1a","thursdaySP1b","thursdaySP2a","thursdaySP2b","friday1aPUW","friday1aFL","friday1aSP1a","friday1aSP1b","friday1aSP2a","friday1aSP2b","friday1bPUW","friday1bFL","friday1bSP1a","friday1bSP1b","friday1bSP2a","friday1bSP2b","friday2aPUW","friday2aFL","friday2aSP1a","friday2aSP1b","friday2aSP2a","friday2aSP2b","friday2bPUW","friday2bFL","friday2bSP1a","friday2bSP1b","friday2bSP2a","friday2bSP2b","friday3aPUW","friday3aFL","friday3aSP1a","friday3aSP1b","friday3aSP2a","friday3aSP2b","friday3bPUW","friday3bFL","friday3bSP1a","friday3bSP1b","friday3bSP2a","friday3bSP2b","saturday1aPUW","saturday1aFL","saturday1aSP1a","saturday1aSP1b","saturday1aSP2a","saturday1aSP2b","saturday1bPUW","saturday1bFL","saturday1bSP1a","saturday1bSP1b","saturday1bSP2a","saturday1bSP2b","saturday2aPUW","saturday2aFL","saturday2aSP1a","saturday2aSP1b","saturday2aSP2a","saturday2aSP2b","saturday2bPUW","saturday2bFL","saturday2bSP1a","saturday2bSP1b","saturday2bSP2a","saturday2bSP2b","saturday3aPUW","saturday3aFL","saturday3aSP1a","saturday3aSP1b","saturday3aSP2a","saturday3aSP2b","saturday3bPUW","saturday3bFL","saturday3bSP1a","saturday3bSP1b","saturday3bSP2a","saturday3bSP2b"
]
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
