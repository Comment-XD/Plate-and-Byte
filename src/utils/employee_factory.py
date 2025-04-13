from src.Manager import Manager
from src.Cook import Cook
from src.Waiter import Waiter

def create_manager(name, username, password, emp_id):
    return Manager(name, emp_id, username, password)

def create_cook(name, username, password, emp_id):
    return Cook(name, emp_id, username, password)

def create_waiter(name, username, password, emp_id):
    return Waiter(name, emp_id, username, password)