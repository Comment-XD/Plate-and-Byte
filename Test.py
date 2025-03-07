employee = "something"
NamePart = "Thing"
temp = []


for j in range(len(employee) - len(NamePart) + 1):
    print(str((employee[j: j + len(NamePart)])) + " == " + str(NamePart))
    if ((str(employee[j: j + len(NamePart)].lower())) == NamePart.lower()):
        print("found")
        break

