from tuesdayemployees import *
from schedulescript import Tuesday

fullTime = []
partTime = []
securityTime = []

for e in employees:
    if e.hours[1] - e.hours[0] >= 6 and e.rank < 13:
        fullTime.append(e)
    elif e.rank > 13 and e.rank < 20:
        partTime.append(e)
    elif e.rank > 19 or e.rank == 13:
        securityTime.append(e)

fullTime = sorted(fullTime, key=lambda x: x.hours[0])
partTime = sorted(partTime, key=lambda x: x.hours[0])
securityTime = sorted(securityTime, key=lambda x: x.hours[0])

tuesday = Tuesday()
tuesday.insert_employee_data([fullTime, partTime, securityTime])

compHours = [[9, 11], [11, 1], [1, 2], [2, 4], [4, 6], [6, 8]]

for e in employees:
    for i in range(len(e.frames)):
        if e.frames[i] == "puw":
            if tuesday.puw[i + 1] != "":
                tuesday.puw[i + 1] += " 'til " + e.printHours[0].replace(":00", "") + "\n" + e.firstName + " at " + e.printHours[0].replace(":00", "")
            else:
                if e.hours[0] > compHours[i][0] and e.hours[0] < compHours[i][1]:
                    tuesday.puw[i + 1] = e.firstName = " at " + e.printHours[0].replace(":00", "")
                else:
                    tuesday.puw[i + 1] = e.firstName
        elif e.frames[i] == "floor lead":
            tuesday.floorLead[i + 1] = e.firstName
        elif e.frames[i] == "sp1a":
            tuesday.sp1a[i + 1] = e.firstName
        elif e.frames[i] == "sp1b":
            tuesday.sp1b[i + 1] = e.firstName
        elif e.frames[i] == "sp2a":
            tuesday.sp2a[i + 1] = e.firstName
        elif e.frames[i] == "sp2b":
            tuesday.sp2b[i + 1] = e.firstName

tuesday.insert_rows()
tuesday.print_all()

print(chris.frames)
