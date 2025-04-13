from src.Employee import Employee  # Assuming Cook inherits from CrewMember
from src.CrewMember import CrewMember


class Cook(CrewMember):
    def __init__(self, name, id, username, password):
        super().__init__(name, id, username, password, "Cook")