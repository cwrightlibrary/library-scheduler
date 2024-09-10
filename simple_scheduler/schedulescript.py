from prettytable import PrettyTable

def list_to_string(eList):
    hrsDict = {}
    hrsString = ""
    for e in eList:
        name, start, end = e.firstName, e.printHours[0], e.printHours[1]
        hrs = f"{start}-{end}"
        if hrs not in hrsDict:
            hrsDict[hrs] = []
        hrsDict[hrs].append(name)
    for hrs, names in hrsDict.items():
        hrsString += f"{hrs}:\n{",\n".join(names)}\n\n".replace(":00", "")
    return hrsString

class Tuesday:
    def __init__(self):
        self.data = PrettyTable(
            ["full time", "part time", "security", "lunch breaks", "schedule changes"]
        )
        self.schedule = PrettyTable(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"])
        self.puw = ["pick-up window", "", "", "", "", "", ""]
        self.floorLead = ["floor lead", "", "", "", "", "", ""]
        self.sp1a = ["service point 1", "", "", "", "", "", ""]
        self.sp1b = ["service point 1", "", "", "", "", "", ""]
        self.sp2a = ["service point 2", "", "", "", "", "", ""]
        self.sp2b = ["service point 1", "", "", "", "", "", ""]
        self.programsMeetings = ["programs/meetings", "", "", "", "", "", ""]
        self.projectTime = ["project time", "", "", "", "", "", ""]
    
    def insert_employee_data(self, eLists):        
        fullTimeString = list_to_string(eLists[0])
        partTimeString = list_to_string(eLists[1])
        securityTimeString = list_to_string(eLists[2])
        
        self.data.add_row([fullTimeString, partTimeString, securityTimeString, "", ""])

    def insert_rows(self):
        self.schedule.add_row(["workroom", "", "", "", "", "", ""], divider=True)
        self.schedule.add_row(self.puw)
        self.schedule.add_row(self.floorLead, divider=True)
        self.schedule.add_row(["front desk", "", "", "", "", "", ""], divider=True)
        self.schedule.add_row(self.sp1a)
        self.schedule.add_row(self.sp1b, divider=True)
        self.schedule.add_row(["computer desk", "", "", "", "", "", ""], divider=True)
        self.schedule.add_row(self.sp2a)
        self.schedule.add_row(self.sp2b, divider=True)
        self.schedule.add_row(
            ["staff/time permitting", "", "", "", "", "", ""], divider=True
        )
        self.schedule.add_row(self.programsMeetings)
        self.schedule.add_row(self.projectTime)

    def print_all(self):
        print(self.data)
        print(self.schedule)
