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
            employee["sp2a-time"] = 0
            employee["sp2b-time"] = 0
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

STAFF = Staff(join(dirname(realpath(__file__)), "staff_info.csv"))

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

TEMPLATE = Template(join(dirname(realpath(__file__)), "template_info.csv"))
