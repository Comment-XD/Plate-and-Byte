from Layout import Layout
from Manager import Manager
from CrewMember import CrewMember
from Busboy import Busboy
from Waiter import Waiter
from Cook import Cook
from Employee import Employee
from Data import Data

class Restaurant:
    def __init__(self, name, ID, ActiveEmployee):
        self.name = name
        self.restaurantID = ID
        self.employees = [] #list of employees
        self.layout = Layout(self)
        self.staticID = 0
        self.IDs = []
        self.activeEmployee = ActiveEmployee # this is the employee signed in
        self.data = Data()
        self.level3Access = ["Admin"]
        self.level2Access = ["Admin", "Manager"]

    ######Sets active employee
    def setActiveEmployee(self, newActiveEmployee):
        self.activeEmployee = newActiveEmployee
    #####End Group


    ######Number Generating Method(s)
    def generteID(self):
        temp = self.restaurantID * 10000 + self.staticID
        self.IDs.append(temp)
        self.staticID += 1
        return temp
    #####End Group

    ######Adding Employee Methods
    def addCrewMember(self, name, role, username, password):
        if self.activeEmployee.role in self.level2Access:
            self.employees.append(CrewMember(name, role, self.generteID(), username, password))
        else:
            print("Action canceled --- Privilege Level Error, must be level 2")

    def addManager(self, name, username, password):
        if self.activeEmployee.role in self.level2Access:
            self.employees.append(Manager(name, self.generteID(), username, password))
        else:
            print("Action canceled --- Privilege Level Error, must be level 3")

    def addBusboy(self, name, username, password):
        if self.activeEmployee.role in self.level2Access:
            self.employees.append(Busboy(name, self.generteID(), username, password))
        else:
            print("Action canceled --- Privilege Level Error, must be level 2")

    def addWaiter(self, name, username, password):
        if self.activeEmployee.role in self.level2Access:
            self.employees.append(Waiter(name, self.generteID(), username, password))
        else:
            print("Action canceled --- Privilege Level Error, must be level 2")

    def addCook(self, name, username, password):
        if self.activeEmployee.role in self.level2Access:
            self.employees.append(Cook(name, self.generteID(), username, password))
        else:
            print("Action canceled --- Privilege Level Error, must be level 2")

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

    ######General Getters
    def getData(self):
        return self.data

    def getLayout(self):
        return self.layout

    def getName(self):
        return self.name

    def getRestaurantID(self):
        return self.restaurantID

    def getEmployees(self):
        return self.employees

    def getActiveEmployee(self):
        return self.activeEmployee

    def getIDs(self):
        temp = []
        for person in self.employees:
            temp.append(person.ID)
    #####End Group


