from src.CrewMember import CrewMember

"""Waiter Class - Used for employees with "Waiter" role"""
class Waiter(CrewMember):
    def __init__(self, name, id, username, password):
        super().__init__(name, id, username, password, "Waiter")