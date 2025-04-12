from src.Employee import Employee

class CrewMember(Employee):  # Assuming CrewMember inherits from Employee
    def __init__(self, name, position, ID, username, password):
        super().__init__(name, position, ID, username, password)
