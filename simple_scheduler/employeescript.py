from datetime import datetime
from math import modf

def convert_time(t):
    h = int(modf(t)[1])
    m = ((modf(t)[0] * 100) * 0.6) / 100
    tString = str(h + m).replace(".", ":")
    if tString[-2] == ":":
        tString += "0"
    if tString[1] == ":":
        tString = "0" + tString
    tString = datetime.strptime(tString, "%H:%M")
    tString = tString.strftime("%I:%M").lstrip("0")
    return tString

class Employee:
    def __init__(self, name, hours, lunch, leave, programs, rank, frames):
        self.name = name
        self.hours = hours
        self.lunch = lunch
        
        self.firstName = self.name.split(" ")[0]
        self.initials = "".join(n[0] for n in self.name.replace("-", " ").split(" "))
        self.rank = rank
        
        self.leave = leave
        self.programs = programs
        self.frames = frames
        
        self.printHours = [convert_time(self.hours[0]), convert_time(self.hours[1])]
        if self.lunch != None: self.printLunch = convert_time(self.lunch)