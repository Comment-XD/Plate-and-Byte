class Employee:
    def __init__(self, name, position, ID, username, password):
        self.name = name
        self.position = position
        self.ID = str(ID)
        self.username = username
        self.password = password
        self.failedLoginAttempts = 0
