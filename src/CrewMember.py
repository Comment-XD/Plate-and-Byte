from src.Employee import Employee

class CrewMember(Employee):
    def __init__(self, name, id, username, password, role):
        super().__init__(id, username, password, name, role)