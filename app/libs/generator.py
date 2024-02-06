from csv_generators import convert_time, STAFF, TEMPLATE, all_day_locations, all_compare_times
from os.path import dirname, join, realpath
from prettytable import PrettyTable
from random import randint

# Import staff list and schedule templates from CSVs
staff = STAFF.staff_list
template = TEMPLATE.schedule_template

# Function to check if employee works during a specified timeframe
def isavailable(employee, time):
    # Naming the employee's hours/compare time hours for readability
    staff_in, staff_out, compare_in, compare_out = employee[0][0], employee[1][1], int(time[0]), int(time[1])
    # If the employee isn't off, convert the employee hours from a string to integer
    if not str(staff_in) in ["O", "f", "f", "Off"]: staff_in = int(staff_in)
    if not str(staff_out) in ["O", "f", "f", "Off"]: staff_out = int(staff_out)
    # If both the start/end times for the employee are integers...
    if isinstance(staff_in, int) and isinstance(staff_out, int):
        # If the employee's start hour is more than the timeslot's first hour and the employee's end hour is less than the timeslot's last hour...
        if ((staff_in >= compare_in and staff_in < compare_out)
        # Or if the employee's start hour is less than the timeslot's first hour and the employee's end hour is more than the timeslot's last hour...
            or (staff_in < compare_in and staff_out > compare_out)
        # Or if the employee's start hour is less than the timeslot's first hour and the employee's start hour is more than the timeslot's first hour and the employee's end hour is less than or the same as the timeslot's last hour...
            or (staff_in < compare_in and staff_out > compare_in and staff_out <= compare_out)):
            # ...The employee is available during that timeslot
            return True

def isondesk(employee, day, hour):
    y_n = []
    for loc in all_day_locations:
        if day in loc:
            for shift in employee[loc]:
                if shift[0] == hour:
                    y_n.append("y")
                else:
                    y_n.append("n")
    if "y" in y_n:
        return True

print(isondesk(staff[9], "monday", all_compare_times[2][3]))

# Main function to generate the schedule
def create_schedule(date):
    # Time slots for sunday, friday/saturday, weekdays
    schedule_header_list = [
        ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"],
        ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"],
        ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"]
    ]
    # A list of each location name to add to the date's weekday
    location_names = ["PUW", "FL", "SP1a", "SP1b", "SP2a", "SP2b"]
    time_at_locations = ["pickup-window-time", "floor-lead-time", "sp1a-time", "sp1b-time", "sp2a-time", "sp2b-time"]
    date_day = date[0].lower()
    # Select the correct header/time comparison
    if "sunday" in date_day:
        # If the weekday is Sunday, set the (a) header to the first element of the schedule_header_list (b) timeslot comparison to the first element of the all_compare_times list (c) the range of timeslots to 1 - 5 (there are only four timeslots on Sunday)
        schedule_header = schedule_header_list[0]
        compare_time = all_compare_times[0]
        hour_range = [1, 5]
        weekday = "sunday"
    elif "friday" in date_day or "saturday" in date_day:
        # If the weekday is Friday or Saturday, set the (a) header to the third element of the schedule_header_list (b) timeslot comparison to the second element of the all_compare_times list (c) the range of timeslots to 1 - 7 (there six timeslots on Fridays and Saturdays)
        schedule_header = schedule_header_list[2]
        compare_time = all_compare_times[1]
        hour_range = [1, 7]
        weekday = "friday" if "friday" in date_day else "saturday"
    else:
        # If the weekday is Monday, Tuesday, Wednesday, or Thursday, set the (a) header to the second element of the schedule_header_list (b) timeslot comparison to the third element of the all_compare_times list (c) the range of timeslots to 1 - 7 (there six timeslots on weekdays)
        schedule_header = schedule_header_list[1]
        compare_time = all_compare_times[2]
        hour_range = [1, 7]
        weekday = date_day.lower()
    
    # Create the PrettyTable with the header we previously selected
    schedule_print = PrettyTable(schedule_header)
    
    # List of all locations to add to the schedule
    weekday_template = [
        ["PICK-UP WINDOW", "", "", "", "", "", ""],
        ["FLOOR LEAD", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 1", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["SERVICE PT 2", "", "", "", "", "", ""],
        ["PROGRAMS", "", "", "", "", "", ""],
        ["PROJECT TIME", "", "", "", "", "", ""]
    ]
    # We're going to be ignoring PROGRAMS and PROJECT TIME from the weekday_template, we'll only assign employees to location
    loc_range = 6
    # Remove the last two timeslots for each location if the day is Sunday, because there are less hours
    if "sunday" in date_day:
        for i in weekday_template:
            i.pop()
            i.pop()
    # Loop through each location from PUW to SERVICE PT 2
    for loc in range(loc_range):
        # Set the dictionary value for the day/location
        day_loc = date_day + location_names[loc]
        # Loop through each employee
        for employee in staff:
            #If they're at the location...
            if len(employee[day_loc]) != 0:
                # Add 1 to their time at that location
                employee[time_at_locations[loc]] += 1
                # Create the totals for SP1 times...
                employee["sp1-time"] = employee["sp1a-time"] + employee["sp1b-time"]
                # And SP2 times
                employee["sp2-time"] = employee["sp2a-time"] + employee["sp2b-time"]
        # Loop through each timeslot per location
        for hour in range(hour_range[0], hour_range[1]):
            for employee in staff:
                # If the employee's timeslot for the location isn't empty (if they work)...
                if len(employee[day_loc]) != 0:
                    # ...Loop through employee's dictionary keys
                    for k, v in employee.items():
                        # If the key's value is a list and the length of the list is 1 or more (if the employee is at the location more than once that day)...
                        if isinstance(employee[k], list) and len(employee[k]) != 0:
                            # ...Loop through each time the employee is at that location
                            for names in range(len(employee[k])):
                                # If the employee's dictionary key is the same as the day/location we're looking for and the hours fall into the timeslot...
                                if k == day_loc and employee[k][names][0] == compare_time[hour - 1]:
                                    # ...Add the employee's name to the location in the timeslot
                                    weekday_template[loc][hour] += employee[k][names][1]
                        # If the key's value isn't a list (it's a weekday, not an alternating a/b weekend)...
                        else:
                            # ...If the employee's dictionary key is the same as the day/location we're looking for and the hours fall into the timeslot...
                            if k == day_loc and employee[k][0] == compare_time[hour - 1]:
                                # ...Add the employee's name to the location in the timeslot
                                weekday_template[loc][hour] += employee[k][1]
            # Because of formatting the employee's name (if they're not at the specified timeslot for the duration of the entire timeslot)...
            if weekday_template[loc][hour][-3:-1] == "pm":
                # ...Remove any extra new-lines to keep the schedule clean
                weekday_template[loc][hour] = weekday_template[loc][hour][:-1]
    # Add employees to project time by looping through the times...
    for hour in compare_time:
        # ... Creating a list of all employees off-desk during that hour...
        project_time_employees = []
        # ... Looping through the staff...
        for employee in staff:
            # ... Checking if the employee works that day and if they're not on desk...
            if isavailable(employee[weekday + "-hours"], hour) and not isondesk(employee, weekday, hour):
                # ... And if the employee isn't security, part-time, or a shelver...
                if not employee["position"] in ["security", "part-time", "shelver"]:
                    # ... Add them to the list
                    project_time_employees.append(employee["initials"])
        # Add the list to that hour's project time slot
        weekday_template[7][compare_time.index(hour) + 1] = ", ".join(project_time_employees)
    
    # Loop through list of locations to add to the schedule
    for d in range(len(weekday_template)):
        # Add the list element to the PrettyTable with dividing lines for formatting
        schedule_print.add_row(weekday_template[d], divider=True) if d in [0, 1, 3, 5, 6] else schedule_print.add_row(weekday_template[d])
    # Export the schedule
    return schedule_print

# This is the proper date format, ["Sunday1", "January 29, 2024"] and ["Friday2b", "January 29, 2024"] will also work
date = ["Sunday1", "January 29, 2024"]

# Create the PrettyTable schedule using the specified date
schedule = create_schedule(date)

# Set a string to the weekday (if it's a weekend/friday, remove the 1a, 2b, etc.)
if "sunday" in date[0].lower():
    weekday = "Sunday"
elif "friday" in date[0].lower():
    weekday = "Friday"
elif "saturday" in date[0].lower():
    weekday = "Saturday"
else:
    weekday = date[0]

# Generate a string from the table
table_string = schedule.get_string()
# Get the amount of characters in the first line of the table (the width of the table)
table_width = len(table_string.splitlines()[0])

# Create a string to center the weekday by adding one space for the width of the table divided by two minus the length of the weekday divided by two and add the string, this will center the string
weekday_centered = " " * int((table_width / 2) - int(len(weekday) / 2)) + weekday
# Do the same thing for the date
date_centered = " " * int((table_width / 2) - int(len(date[1].replace(",", " ")) / 2)) + date[1]
# Print both the centered weekday...
print(weekday_centered)
# ...And date
print(date_centered)

# Print the PrettyTable to the terminal
print(schedule)
