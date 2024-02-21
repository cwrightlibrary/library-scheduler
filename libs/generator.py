from schedule_functions import STAFF, TEMPLATE, LOCATION, convert_time

# Variables for the csv information
branch = LOCATION.location_info["location-name"]
branch_hours = []
employees = STAFF.staff_list
template = TEMPLATE.schedule_template

for k, v in LOCATION.location_info.items():
    if "hours" in k:
        day = k
        hours = v.split("-")
        hours[0] = convert_time(hours[0], to_24=True)
        hours[1] = convert_time(hours[1], to_24=True)
        branch_hours.append({k: hours})

# Generate template info from branch info
scheduler_header_list = []
