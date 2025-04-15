from src.Employee import Employee

from src.CrewMember import CrewMember

"""Manager Class - Used for employees with "Manager" role"""
class Manager(CrewMember):
    def __init__(self, name, id, username, password):
        super().__init__(name, id, username, password, "Manager")