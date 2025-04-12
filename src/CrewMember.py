from src.Employee import Employee

class CrewMember(Employee):
    def __init__(self, name, position, ID, username, password):
        self.super(name, position, ID, username, password)
