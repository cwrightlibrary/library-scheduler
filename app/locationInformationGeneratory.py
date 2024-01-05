import csv
from customtkinter import *
from os.path import dirname, join, realpath

class App(CTk):
	def __init__(self):
		super().__init__()
		self.title = "Location Information"
		self.geometry("445x454")
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.locationNameFrame = CTkFrame(self)
		self.locationNameFrame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
		self.locationNameTitle = CTkLabel(self.locationNameFrame, text="Location Name", fg_color="gray30", corner_radius=6)
		self.locationNameTitle.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
		self.locationNameEntry = CTkEntry(self.locationNameFrame, placeholder_text="Enter location name...")
		self.locationNameEntry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

		self.locationHoursFrame = CTkFrame(self)
		self.locationHoursFrame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")
		self.locationHoursTitle = CTkLabel(self.locationHoursFrame, text="Location Hours", fg_color="gray30", corner_radius=6)
		self.locationHoursTitle.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

		self.locationHoursSundayLabel = CTkLabel(self.locationHoursFrame, text="Sunday:")
		self.locationHoursSundayLabel.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursSundayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursSundayEntry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursMondayLabel = CTkLabel(self.locationHoursFrame, text="Monday:")
		self.locationHoursMondayLabel.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursMondayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursMondayEntry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursTuesdayLabel = CTkLabel(self.locationHoursFrame, text="Tuesday:")
		self.locationHoursTuesdayLabel.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursTuesdayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursTuesdayEntry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursWednesdayLabel = CTkLabel(self.locationHoursFrame, text="Wednesday:")
		self.locationHoursWednesdayLabel.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursWednesdayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursWednesdayEntry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursThursdayLabel = CTkLabel(self.locationHoursFrame, text="Thursday:")
		self.locationHoursThursdayLabel.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursThursdayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursThursdayEntry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursFridayLabel = CTkLabel(self.locationHoursFrame, text="Friday:")
		self.locationHoursFridayLabel.grid(row=6, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursFridayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursFridayEntry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
		self.locationHoursSaturdayLabel = CTkLabel(self.locationHoursFrame, text="Saturday:")
		self.locationHoursSaturdayLabel.grid(row=7, column=0, padx=(10, 0), pady=10, sticky="ew")
		self.locationHoursSaturdayEntry = CTkEntry(self.locationHoursFrame, placeholder_text="9am-6pm")
		self.locationHoursSaturdayEntry.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

		self.exportButton = CTkButton(self, text="Save", command=self.export)
		self.exportButton.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

	def export(self):
		currentDirectory = join(dirname(realpath(__file__)), "libs")
		with open(join(currentDirectory, "locationInformation.csv"), "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerow(["locationName", "sundayHours", "mondayHours", "tuesdayHours", "wednesdayHours", "thursdayHours", "fridayHours", "saturdayHours"])
			writer.writerow([self.locationNameEntry.get(), self.locationHoursSundayEntry.get(), self.locationHoursMondayEntry.get(), self.locationHoursTuesdayEntry.get(), self.locationHoursWednesdayEntry.get(), self.locationHoursThursdayEntry.get(), self.locationHoursFridayEntry.get(), self.locationHoursSaturdayEntry.get()])


# app = App()
# app.mainloop()

with open(join(dirname(realpath(__file__)),"libs", "employeeInformation.csv"), "r") as file:
	reader = csv.DictReader(file)
	data = [row for row in reader]
for row in data:
	print(row)
