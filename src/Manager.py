from src.Employee import Employee

from src.CrewMember import CrewMember

class Manager(CrewMember):
    def __init__(self, name, id, username, password):
        super().__init__(name, id, username, password, "Manager")