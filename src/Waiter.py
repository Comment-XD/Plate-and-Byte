from src.CrewMember import CrewMember


class Waiter(CrewMember):
    def __init__(self, name, ID, username, password):
        super().__init__(name, "Waiter", ID, username, password)