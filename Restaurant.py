from Layout import Layout
from Manager import Manager
from CrewMember import CrewMember
from Busboy import Busboy
from Waiter import Waiter
from Cook import Cook
from Employee import Employee


class Restaurant:
    def __init__(self, name, ID):
        self.name = name
        self.restaurantID = ID
        self.employees = [] #list of employees
        self.layout = Layout(self)
        self.staticID = 0
        self.IDs = []

    ######Number Generating Method(s)
    def generteID(self):
        temp = self.restaurantID * 10000 + self.staticID
        self.IDs.append(temp)
        self.staticID += 1
        return temp
    #####End Group

    ######Adding Employee Methods
    def addCrewMember(self, name, role, username, password):
        self.employees.append(CrewMember(name, role, self.generteID(), username, password))

    def addManager(self, name, role, username, password):
        self.employees.append(Manager(name, self.generteID(), username, password))

    def addBusboy(self, name, role, username, password):
        self.employees.append(Busboy(name, self.generteID(), username, password))

    def addWaiter(self, name, role, username, password):
        self.employees.append(Waiter(name, self.generteID(), username, password))

    def addCook(self, name, role, username, password):
        self.employees.append(Cook(name, self.generteID(), username, password))
    #####End Group

    ######Searching Specific Employee Methods
    def getEmployeeByName(self, name):
        name = str(name)
        for employee in self.employees:
            if employee.name.lower() == name.lower():
                return employee

        return None

    def getEmployeeByID(self, ID):
        ID = str(ID)
        for employee in self.employees:
            if employee.ID == ID:
                return employee

        return None

    def getEmployeeByLogin(self, username, password):
        username = str(username)
        password = str(password)
        for employee in self.employees:
            if employee.username == username:
                if employee.password == password:
                    employee.failedLoginAttempts = 0
                    return employee
                employee.failedLoginAttempts += 1
        else:

            return "Employee Username or Password is incorrect"

        return None
    #####End Group

    ######Searching Employees Methods
    def getEmployeesByNamePart(self, NamePart):
        NamePart = str(NamePart)
        temp = []
        for i in self.employees:
            for employee in self.employees:
                if len(employee.name) >= len(NamePart):
                    for j in range(len(employee.name) - len(NamePart) + 1):
                        print(str((employee.name[j: j + len(NamePart)])) + " == " + str(NamePart))
                        if ((str(employee.name[j: j + len(NamePart)].lower())) == NamePart.lower()):
                            temp.append(employee)

        return temp

    def getEmployeesByIDPart(self, IDPart):
        IDPart = str(IDPart)
        temp = []
        for i in self.employees:
            for employee in self.employees:
                if len(employee.ID) >= len(IDPart):
                    for j in range(len(employee.ID) - len(IDPart) + 1):
                        print(str((employee.ID[j: j + len(IDPart)])) + " == " + str(IDPart))
                        if ((str(employee.ID[j: j + len(IDPart)])) == IDPart):
                            temp.append(employee)

        return temp
    #####End Group


