from customtkinter import *

class LocationName(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.entry = CTkEntry(self, placeholder_text="Location Name")
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="new")

class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("scheduler")
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.location_name_frame = LocationName(self)
        self.location_name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.button = CTkButton(self, text="Enter", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
    def button_callback(self):
        string = self.location_name_frame.entry.get()
        print(string)

app = App()
app.mainloop()
