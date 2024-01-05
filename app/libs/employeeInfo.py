import csv
from datetime import datetime
from os.path import dirname, join, realpath

# Import the CSV with employee information
def import_employee_csv(file):
    with open(file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
    return data

# To convert time between 12/24 hours
def convert_time(input_time, to_24):
    # Split the string into a list
    output_time = input_time.split("-")
    # Reformat the time for processing (if time is "9am", change to "9:00AM")
    for t in range(len(output_time)):
        if not ":" in output_time[t]:
            output_time[t] = output_time[t][:-2] + ":00" + output_time[t][-2:]
        # Change time to 24 hours
        if to_24:
            output_time[t] = datetime.strptime(output_time[t].upper(), "%I:%M%p").strftime("%H%M")
        # Change time to 12 hours
        else:
            output_time[t] = datetime.strptime(output_time[t].upper(), "%H%M").strftime("%I:%M%p")
    return output_time

def split_hours(input_time):
    if "(" in input_time:
        output_time = input_time.split(")/(")
        for shift in range(len(output_time)):
            output_time[shift] = output_time[shift].replace("(", "").replace(")", "")
            output_time[shift] = output_time[shift].split("/")
            if "Off" in output_time[shift]:
                output_time[shift] = "Off"
        return output_time

employee_csv = import_employee_csv(join(dirname(realpath(__file__)), "employeeInformation.csv"))

yami_monday_hours = employee_csv[5]["monday-hours"]
print(yami_monday_hours)
yami_monday_hours = split_hours(yami_monday_hours)

print(yami_monday_hours)

if isinstance(yami_monday_hours, list):
    for shift in range(len(yami_monday_hours)):
        if isinstance(yami_monday_hours[shift], list):
            for hour in range(len(yami_monday_hours[shift])):
                yami_monday_hours[shift][hour] = convert_time(yami_monday_hours[shift][hour], to_24=True)
        else:
            if not "Off" in yami_monday_hours[shift]:
                yami_monday_hours[shift] = convert_time(yami_monday_hours[shift], to_24=True)
else:
    if "-" in yami_monday_hours:
        yami_monday_hours = convert_time(yami_monday_hours, to_24=True)

print(yami_monday_hours)

# for employee in employee_csv:
#     for data in employee:
#         if ":" in employee[data]:
#             employee[data] = split_multiple_hours(employee[data])
#             print(employee[data])
