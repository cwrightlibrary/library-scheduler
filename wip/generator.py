from csv_generators import staff, template, location, convert_time
from datetime import *
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from os.path import dirname, join, realpath
from prettytable import PrettyTable

class Schedule:
    def __init__(self, date, adjustments):
        # Get the library branch's name
        self.branch_name = location.location_info["location-name"]
        # Initialize a dictionary for the branch's hours
        self.branch_hours = {}
        # Initialize a list for the branch's floor locations
        self.floor_locations = []
        self.floor_categories = ["workroom", "front desk", "computer desk", "programs & projects"]
        # Set the date to the argument
        self.date = date
        # Get the weekday
        self.weekday = datetime.strptime(self.date, "%B %d, %Y").strftime("%A")
        # Set the schedule adjustments to the argument
        self.adjustments = adjustments
        # Create a table for the schedule information
        self.info_header = [
            "who works today" , "lunch breaks" , "schedule changes" 
        ]
        
        self.get_hours_locations()
        self.create_header_compare()
        self.add_to_schedule()
        self.generate_word_doc()
    
    def get_hours_locations(self):
        # Loop through the imported location csv's info dictionary
        for k, v in location.location_info.items():
            # Ignore the branch name and floor locations
            if "hours" in k and v.lower() != "closed":
                day = k.capitalize()
                day = day.replace("-hours", "")
                # Split the formatted "9:00am-8:00pm" string into ["9:00am", "8:00pm"]
                hours = v.split("-")
                # Convert the time to 24 hour integers
                hours[0] = int(convert_time(hours[0], to_24=True))
                hours[1] = int(convert_time(hours[1], to_24=True))
                # Assign dictionary values for each day
                self.branch_hours[day] = hours
            if k == "floor-locations":
                floor_locations = v.split("/")
                for loc in floor_locations:
                    self.floor_locations.append(loc.replace("-", " "))
        
        # Remove the "workroom" floor category if there's no pickup window
        if not "pickup window" in self.floor_locations:
            self.floor_categories.pop(0)
    
    def create_header_compare(self):
        for k, v in self.branch_hours.items():
            if self.weekday == k:
                # If the hours are 2-6, set the appropriate header/compare_time
                if v == [1400, 1800]:
                    self.template_header = ["", "2 - 3", "3 - 4", "4 - 5", "5 - 6"]
                    self.compare_time = [[1400, 1500], [1500, 1600], [1600, 1700], [1700, 1800]]
                # If the hours are 9-6, set the appropriate header/compare_time
                elif v == [900, 1800]:
                    self.template_header = ["", "9 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 4", "4 - 6"]
                    self.compare_time = [[900, 1100], [1100, 1200], [1200, 1300], [1300, 1400], [1400, 1600], [1600, 1800]]
                # If the hours are 9-8, set the appropriate header/compare_time
                elif v == [900, 2000]:
                    self.template_header = ["", "9 - 11", "11 - 1", "1 - 2", "2 - 4", "4 - 6", "6 - 8"]
                    self.compare_time = [[900, 1100], [1100, 1300], [1300, 1400], [1400, 1600], [1600, 1800], [1800, 2000]]
        
        # Create PrettyTables for the template and information
        self.print_template = PrettyTable(self.template_header)
        self.print_info = PrettyTable(self.info_header)
    
    def add_to_schedule(self):
        # Create list for all available location/hour slots
        self.template = []
        for loc in range(len(self.floor_locations)):
            temp = []
            temp.append(self.floor_locations[loc])
            for hour in range(len(self.template_header) - 1):
                temp.append("")
            self.template.append(temp)
        
        for row in range(len(self.template)):
            self.print_template.add_row(self.template[row], divider = True)
    
    def pretty_print(self):
        # Set the padding width for the PrettyTables
        self.print_info.padding_width = 20
        self.print_template.padding_width = 10
        # Get the width of the info table
        table_width = len(self.print_info.get_string().splitlines()[0])
        # Strings to center the weekday/date over the PrettyTable
        weekday_centered = " " * int((table_width / 2) - int(len(self.weekday) / 2)) + self.weekday
        date_centered = " " * int((table_width / 2) - int(len(self.date.replace(",", "")) / 2)) + self.date
        
        # Print all
        print(weekday_centered)
        print(date_centered)
        print(self.print_info)
        print(self.print_template)
    
    def generate_word_doc(self):
        blue_dark = "#007e9e"
        blue_med = "#378fba"
        blue_light = "#f2f8fa"
        green_dark = "#679a44"
        green_med = "#679a44"
        green_light = "#f6faf2"
        
        self.word_doc = Document()
        
        heading1 = self.word_doc.styles["Heading 1"]
        heading1.font.name = "Aptos Display"
        heading1.font.size = Pt(16)
        
        self.word_doc.add_heading(self.weekday)
        self.word_doc.add_heading(self.date)
    
    def save_doc(self, location):
        self.word_doc.save(location)

date = "February 21, 2024"

adjustments = [
    [
        
    ],
    [
        
    ]
]

daily_schedule = Schedule(date, adjustments)

daily_schedule.pretty_print()

daily_schedule.save_doc(join(dirname(realpath(__file__)), "test.docx"))
