from customtkinter import *
from os.path import dirname, join, realpath
import csv

class LocationName(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = CTkLabel(self, text="enter the name of your library branch")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        self.entry = CTkEntry(self, placeholder_text="Location Name")
        self.entry.grid(row=1, column=0, padx=10, pady=10, sticky="new")

class LocationHours(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.sunday_label = CTkLabel(self, text="sunday")
        self.sunday_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.sunday_input = CTkEntry(self, placeholder_text="Closed")
        self.sunday_input.grid(row=0, column=1, padx=10, pady=10, sticky="new")
        self.sunday_input2 = CTkEntry(self, placeholder_text="Closed")
        self.sunday_input2.grid(row=0, column=2, padx=10, pady=10, sticky="new")
        
        self.monday_label = CTkLabel(self, text="monday")
        self.monday_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")
        self.monday_input = CTkEntry(self, placeholder_text="9:00am")
        self.monday_input.grid(row=1, column=1, padx=10, pady=10, sticky="new")
        self.monday_input2 = CTkEntry(self, placeholder_text="8:00pm")
        self.monday_input2.grid(row=1, column=2, padx=10, pady=10, sticky="new")
        
        self.tuesday_label = CTkLabel(self, text="tuesday")
        self.tuesday_label.grid(row=2, column=0, padx=10, pady=10, sticky="new")
        self.tuesday_input = CTkEntry(self, placeholder_text="9:00am")
        self.tuesday_input.grid(row=2, column=1, padx=10, pady=10, sticky="new")
        self.tuesday_input2 = CTkEntry(self, placeholder_text="8:00pm")
        self.tuesday_input2.grid(row=2, column=2, padx=10, pady=10, sticky="new")
        
        self.wednesday_label = CTkLabel(self, text="wednesday")
        self.wednesday_label.grid(row=3, column=0, padx=10, pady=10, sticky="new")
        self.wednesday_input = CTkEntry(self, placeholder_text="9:00am")
        self.wednesday_input.grid(row=3, column=1, padx=10, pady=10, sticky="new")
        self.wednesday_input2 = CTkEntry(self, placeholder_text="8:00pm")
        self.wednesday_input2.grid(row=3, column=2, padx=10, pady=10, sticky="new")
        
        self.thursday_label = CTkLabel(self, text="thursday")
        self.thursday_label.grid(row=4, column=0, padx=10, pady=10, sticky="new")
        self.thursday_input = CTkEntry(self, placeholder_text="9:00am")
        self.thursday_input.grid(row=4, column=1, padx=10, pady=10, sticky="new")
        self.thursday_input2 = CTkEntry(self, placeholder_text="8:00pm")
        self.thursday_input2.grid(row=4, column=2, padx=10, pady=10, sticky="new")
        
        self.friday_label = CTkLabel(self, text="friday")
        self.friday_label.grid(row=5, column=0, padx=10, pady=10, sticky="new")
        self.friday_input = CTkEntry(self, placeholder_text="9:00am")
        self.friday_input.grid(row=5, column=1, padx=10, pady=10, sticky="new")
        self.friday_input2 = CTkEntry(self, placeholder_text="6:00pm")
        self.friday_input2.grid(row=5, column=2, padx=10, pady=10, sticky="new")
        
        self.saturday_label = CTkLabel(self, text="saturday")
        self.saturday_label.grid(row=6, column=0, padx=10, pady=10, sticky="new")
        self.saturday_input = CTkEntry(self, placeholder_text="9:00am")
        self.saturday_input.grid(row=6, column=1, padx=10, pady=10, sticky="new")
        self.saturday_input2 = CTkEntry(self, placeholder_text="6:00pm")
        self.saturday_input2.grid(row=6, column=2, padx=10, pady=10, sticky="new")

class FloorLocations(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.puw = CTkCheckBox(self, text="pickup window")
        self.puw.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.puw.toggle()
        
        self.floor_lead = CTkCheckBox(self, text="floor lead")
        self.floor_lead.grid(row=1, column=0, padx=10, pady=10, sticky="new")
        self.floor_lead.toggle()
        
        self.sp1a = CTkCheckBox(self, text="service point 1a")
        self.sp1a.grid(row=2, column=0, padx=10, pady=10, sticky="new")
        self.sp1a.toggle()
        
        self.sp1b = CTkCheckBox(self, text="service point 1b")
        self.sp1b.grid(row=3, column=0, padx=10, pady=10, sticky="new")
        self.sp1b.toggle()
        
        self.sp2a = CTkCheckBox(self, text="service point 2a")
        self.sp2a.grid(row=4, column=0, padx=10, pady=10, sticky="new")
        self.sp2a.toggle()
        
        self.sp2b = CTkCheckBox(self, text="service point 2b")
        self.sp2b.grid(row=5, column=0, padx=10, pady=10, sticky="new")
        self.sp2b.toggle()
        

class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("scheduler")
        self.geometry("650x525")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.location_name_frame = LocationName(self)
        self.location_name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        
        self.location_name_frame.grid_rowconfigure(0, weight=1)
        self.location_name_frame.grid_columnconfigure(0, weight=1)
        
        self.hours_frame = LocationHours(self)
        self.hours_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
        
        self.hours_frame.grid_rowconfigure(0, weight=1)
        self.hours_frame.grid_columnconfigure(0, weight=1)
        
        self.floor_locations = FloorLocations(self)
        self.floor_locations.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.button = CTkButton(self, text="confirm", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        
    def button_callback(self):
        location_name = self.location_name_frame.entry.get().title()
        sunday1, sunday2 = self.hours_frame.sunday_input.get(), self.hours_frame.sunday_input2.get()
        monday1, monday2 = self.hours_frame.monday_input.get(), self.hours_frame.monday_input2.get()
        tuesday1, tuesday2 = self.hours_frame.tuesday_input.get(), self.hours_frame.tuesday_input2.get()
        wednesday1, wednesday2 = self.hours_frame.wednesday_input.get(), self.hours_frame.wednesday_input2.get()
        thursday1, thursday2 = self.hours_frame.thursday_input.get(), self.hours_frame.thursday_input2.get()
        friday1, friday2 = self.hours_frame.friday_input.get(), self.hours_frame.friday_input2.get()
        saturday1, saturday2 = self.hours_frame.saturday_input.get(), self.hours_frame.saturday_input2.get()
        
        sunday1, sunday2 = self.fix_hours(sunday1), self.fix_hours(sunday2)
        monday1, monday2 = self.fix_hours(monday1), self.fix_hours(monday2)
        tuesday1, tuesday2 = self.fix_hours(tuesday1), self.fix_hours(tuesday2)
        wednesday1, wednesday2 = self.fix_hours(wednesday1), self.fix_hours(wednesday2)
        thursday1, thursday2 = self.fix_hours(thursday1), self.fix_hours(thursday2)
        friday1, friday2 = self.fix_hours(friday1), self.fix_hours(friday2)
        saturday1, saturday2 = self.fix_hours(saturday1), self.fix_hours(saturday2)
        
        sunday = sunday1 + "-" + sunday2
        monday = monday1 + "-" + monday2
        tuesday = tuesday1 + "-" + tuesday2
        wednesday = wednesday1 + "-" + wednesday2
        thursday = thursday1 + "-" + thursday2
        friday = friday1 + "-" + friday2
        saturday = saturday1 + "-" + saturday2
        
        floor_locations = ""
        if self.floor_locations.puw.get() == 1:
            floor_locations += "pickup-window "
        if self.floor_locations.floor_lead.get() == 1:
            floor_locations += "floor-lead "
        if self.floor_locations.sp1a.get() == 1:
            floor_locations += "service-pt-1a "
        if self.floor_locations.sp1b.get() == 1:
            floor_locations += "service-pt-1b "
        if self.floor_locations.sp2a.get() == 1:
            floor_locations += "service-pt-2a "
        if self.floor_locations.sp2b.get() == 1:
            floor_locations += "service-pt-2b "
        
        floor_locations = floor_locations.replace(" ", "/")
        if floor_locations[-1] == "/":
            floor_locations = floor_locations[0:-1]
        
        with open(join(dirname(realpath(__file__)), "test_csvs", "location_info.csv"), 'w', newline='') as file:
            writer = csv.writer(file)
            
            field = ["location-name","sunday-hours","monday-hours","tuesday-hours","wednesday-hours","thursday-hours","friday-hours","saturday-hours","floor-locations"]
            writer.writerow(field)
            
            writer.writerow([location_name, sunday, monday, tuesday, wednesday, thursday, friday, saturday, floor_locations])
    def fix_hours(self, input_hour):
        hour = input_hour
        if hour == "2:00" or hour == "2" or hour == 2: hour = "2:00pm"
        hour = hour.replace("2pm", "2:00pm").replace("2:00 pm", "2:00pm")
        if hour == "9:00" or hour == "9" or hour == 9: hour = "9:00am"
        hour = hour.replace("9pm", "9:00pm").replace("9:00 am", "9:00pm")
        if hour == "6:00" or hour == "6" or hour == 6: hour = "6:00pm"
        hour = hour.replace("6pm", "6:00pm").replace("6:00 pm", "6:00pm")
        if hour == "8:00" or hour == "8" or hour == 8: hour = "8:00pm"
        hour = hour.replace("8pm", "8:00pm").replace("8:00 pm", "8:00pm")
        
        return hour

app = App()
app.mainloop()
