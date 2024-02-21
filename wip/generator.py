from csv_generators import staff, template, location, convert_time
from prettytable import PrettyTable

# Variables for the csv information
branch = location["location-name"]
branch_hours = []

for k, v in location.items():
    if "hours" in k:
        day = k
        hours = v.split("-")
        hours[0] = convert_time(hours[0], to_24=True)
        hours[1] = convert_time(hours[1], to_24=True)
        branch_hours.append({k: hours})

# Generate template info from branch info
print(branch_hours)
