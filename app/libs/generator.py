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
    staff_in, staff_out, compare_in, compare_out = employee[0], employee[1], int(time[0]), int(time[1])
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

# Check if the employee is on desk
def isondesk(employee, day, hour):
    # A list that will store "yeses" and "nos"
    y_n = []
    # Loop through all of the locations
    for loc in all_day_locations:
        # If the current day is in the location name...
        if day in loc:
            # ... Loop through the employee's shifts for that location
            for shift in employee[loc]:
                # If the hours match...
                if shift[0] == hour:
                    # ... Add a "yes"...
                    y_n.append("y")
                else:
                    # ... Otherwise, add a "no"
                    y_n.append("n")
    # If there's even one "yes" in the y_n list...
    if "y" in y_n:
        # ... Return true
        return True

# Combine and convert time for schedule adjustments
def parse_leave_programs(adjustments):
    # Create an empty list
    adjustment_employees = []
    # Add all the hours from the adjustments
    for hours in adjustments:
        adjustment_employees.append(hours[1])
    # Remove duplicate hours
    adjustment_employees = list(set(tuple(sub) for sub in adjustment_employees))
    # Change the tuples to a list
    adjustment_employees = [[list(item)] for item in adjustment_employees]
    # Loop through the hours in the list we created
    for hours in adjustment_employees:
        # Loop through the adjustments
        for item in adjustments:
            # If the hours match...
            if item[1] == hours[0]:
                # ... Add names to that list
                hours.append(item[0])
                # If the length of the item is longer than 2 (if it's a program)...
                if len(item) > 2:
                    # ... Add the program name
                    hours.append(item[2])
    # Convert all times in the list
    for hours in adjustment_employees:
        if hours[0][0] != 0 and hours[0][1] != 0:
            hours[0][0] = int(convert_time(hours[0][0], to_24=True))
            hours[0][1] = int(convert_time(hours[0][1], to_24=True))
        else:
            hours[0] = "all day"
    return adjustment_employees

# Main function to generate the schedule
def create_schedule(date, adjustments):
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
        info_date_selector = int(date_day[len(date_day) - 1:]) - 1
    elif "friday" in date_day or "saturday" in date_day:
        # If the weekday is Friday or Saturday, set the (a) header to the third element of the schedule_header_list (b) timeslot comparison to the second element of the all_compare_times list (c) the range of timeslots to 1 - 7 (there six timeslots on Fridays and Saturdays)
        schedule_header = schedule_header_list[2]
        compare_time = all_compare_times[1]
        hour_range = [1, 7]
        weekday = "friday" if "friday" in date_day else "saturday"
        info_date_selector_1 = int(date_day[len(date_day) - 2:len(date_day) - 1]) - 1
        info_date_selector_2 = date_day[len(date_day) - 1:]
        if info_date_selector_2 == "a": info_date_selector_2 = 0
        if info_date_selector_2 == "b": info_date_selector_2 = 1
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
    leave_employees = parse_leave_programs(adjustments[0])
    program_employees = parse_leave_programs(adjustments[1])

    # Handle leave by looping through the items in leave_employees
    for item in leave_employees:
        # Loop through the staff
        for employee in staff:
            # If the employee's name is in leave_employees...
            if employee["name"].split()[0].lower() in item[1]:
                # ... If the employee is off all day...
                if item[0] == "all day":
                    # (Define their hours by date)
                    if "sunday" in date_day:
                        emp_hours = employee[weekday + "-hours"][info_date_selector]
                    elif "friday" in date_day or "saturday" in date_day:
                        emp_hours = employee[weekday + "-hours"][info_date_selector_1][info_date_selector_2]
                    else:
                        emp_hours = employee[weekday + "-hours"]
                    # Set both hours to Off
                    emp_hours[0] = "Off"
                    emp_hours[1] = "Off"
                    # Loop through all location names
                    for loc in all_day_locations:
                        # If the weekday is in the name...
                        if weekday in loc:
                            # ... Remove the hours
                            employee[loc] = []
                # If the employee isn't off all day...
                else:
                    # Loop through the employee's dictionary
                    for shift in employee:
                        # If the employee's dictionary is in the location names and the weekday is in the shift name...
                        if shift in all_day_locations and weekday in shift:
                            # ... Loop through all hours for that employee at that location
                            for loc in range(len(employee[shift])):
                                # If the employee's hours fall within the range of the leave hours... 
                                if ((employee[shift][loc][0][0] >= item[0][0] and employee[shift][loc][0][1] <= item[0][1])
                                    or (employee[shift][loc][0][0] < item[0][0] and employee[shift][loc][0][1] >= item[0][1])
                                    or (employee[shift][loc][0][0] < item[0][0] and employee[shift][loc][0][1] >= item[0][0] and employee[shift][loc][0][1] <= item[0][1])):
                                    # ... Set the employee's shift at that location to nothing
                                    employee[shift] = []
                                    # WORKING HERE
                                    # employee["leave"] = 
                                
    
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
    
    off_desk_employees = []
    # Add employees to project time by looping through the times...
    for hour in compare_time:
        # ... Creating a list of all employees off-desk during that hour...
        project_time_employees = []
        # ... Looping through the staff...
        for employee in staff:
            # Create a variable to return the hours for that day depending on the rotation calendar
            if "sunday" in date_day:
                emp_hours = employee[weekday + "-hours"][info_date_selector]
            elif "friday" in date_day or "saturday" in date_day:
                emp_hours = employee[weekday + "-hours"][info_date_selector_1][info_date_selector_2]
            else:
                emp_hours = employee[weekday + "-hours"]
            # ... Checking if the employee works that day and if they're not on desk...
            # print(emp_hours)
            if isavailable(emp_hours, hour) and not isondesk(employee, weekday, hour):
                # ... And if the employee isn't security, part-time, or a shelver...
                if not employee["position"] in ["security", "part-time", "shelver"]:
                    # ... Add them to the list
                    project_time_employees.append(employee["initials"])
        # Add the list to the off desk employees list
        off_desk_employees.append(project_time_employees)
    
    # If a service point is completely empty
    for hour in range(len(off_desk_employees)):
        if weekday_template[2][hour + 1] == "" and weekday_template[3][hour + 1] == "":
            for employee in staff:
                if employee["initials"] == off_desk_employees[hour][-1]:
                    weekday_template[2][hour + 1] = employee["name"].split()[0]
                    off_desk_employees[hour].pop()
    
    for hour in range(len(off_desk_employees)):
        weekday_template[7][hour + 1] = ", ".join(off_desk_employees[hour])
    
    # If a service point's a location is empty but the b location isn't, loop through the hours of that location...
    for hour in range(len(weekday_template[2])):
        # ... If the location is empty but the b location isn't...
        if weekday_template[2][hour] == "" and weekday_template[3][hour] != "":
            # ... Change the a location to b location's value and erase the b value
            weekday_template[2][hour] = weekday_template[3][hour]
            weekday_template[3][hour] = ""
        # ... 
        if weekday_template[4][hour] == "" and weekday_template[5][hour] != "":
            weekday_template[4][hour] = weekday_template[5][hour]
            weekday_template[5][hour] = ""
    # Loop through list of locations to add to the schedule
    for d in range(len(weekday_template)):
        # Add the list element to the PrettyTable with dividing lines for formatting
        schedule_print.add_row(weekday_template[d], divider=True) if d in [0, 1, 3, 5, 6] else schedule_print.add_row(weekday_template[d])
    # Export the schedule
    return schedule_print

# This is the proper date format, ["Sunday1", "January 29, 2024"] and ["Friday2b", "January 29, 2024"] will also work
date = ["Monday", "January 29, 2024"]

# This is the proper adjustments format, leave first, programs second. Group names into a list within each list: [[[NAMES GO HERE], [HOURS GO HERE], MEETING/PROGRAM NAME]]
adjustments = [
    # Leave
    [
        [["lea"], [0, 0]], 
        [["sonaite"], ["1:30pm", "2:15pm"]],
        [["alyssa"], ["11:00am", "1:00pm"]]
    ],
    # Programs/Meetings
    [
        [["steve"], ["9:00am", "10:00am"], "storytime"],
        [["chris", "anthony"], ["4:00pm", "5:00pm"], "stem"]
    ]
]

# Create the PrettyTable schedule using the specified date
schedule = create_schedule(date, adjustments)

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
