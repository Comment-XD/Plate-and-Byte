from src.CrewMember import CrewMember

class Waiter(CrewMember):
    def __init__(self, name, id, username, password):
        super().__init__(name, id, username, password, "Waiter")