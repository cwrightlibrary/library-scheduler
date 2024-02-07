from libs.schedule_functions import isavailable, isondesk, compare_hours, create_project_time, sort_adjustments, create_schedule_info, create_schedule_template, apply_leave, add_to_schedule, shift_empty_spa
from prettytable import PrettyTable

def create_schedule(date, adjustments):
    weekday_untrimmed = date[0].lower()
    schedule_header, compare_time, hour_range, weekday, emp_selector, emp_selector_1, emp_selector_2 = create_schedule_info(weekday_untrimmed)
    
    leave_employees = sort_adjustments(adjustments[0])
    program_employees = sort_adjustments(adjustments[1])
    apply_leave(leave_employees, weekday_untrimmed, weekday, emp_selector, emp_selector_1, emp_selector_2)
    
    schedule = PrettyTable(schedule_header)
    template = create_schedule_template(weekday)
    
    add_to_schedule(weekday_untrimmed, hour_range, compare_time, template)
    
    off_desk_employees = create_project_time(compare_time, weekday_untrimmed, weekday, emp_selector, emp_selector_1, emp_selector_2)
    
    shift_empty_spa(template)
    
    for hour in range(len(off_desk_employees)):
        template[7][hour + 1] = ", ".join(off_desk_employees[hour])
    
    for loc in range(len(template)):
        schedule.add_row(template[loc], divider=True) if loc in [0, 1, 3, 5, 6] else schedule.add_row(template[loc])
    
    table_string = schedule.get_string()
    table_width = len(table_string.splitlines()[0])
    weekday_centered = " " * int((table_width / 2) - int(len(weekday) / 2)) + weekday.capitalize()
    date_centered = " " * int((table_width / 2) - int(len(date[1].replace(",", " ")) / 2)) + date[1].title()
    
    full_date = weekday_centered + "\n" + date_centered
    return full_date, schedule

date = ["Monday", "February 6, 2024"]

adjustments = [
    [
        [["lea"], [0, 0]], 
        [["sonaite"], ["1:30pm", "2:15pm"]],
        [["alyssa"], ["11:00am", "1:00pm"]]
    ],
    [
        [["steve"], ["9:00am", "10:00am"], "storytime"],
        [["chris", "anthony"], ["4:00pm", "5:00pm"], "stem"]
    ]
]

full_date, schedule = create_schedule(date, adjustments)

print(full_date)
print(schedule)