from Layout import Layout
from Manager import Manager
from CrewMember import CrewMember
from Busboy import Busboy
from Waiter import Waiter
from Cook import Cook
from Employee import Employee
from Data import Data

import csv
import os


class Restaurant:
    def __init__(self):
        self.employees = []
        self.activeEmployee = None  # Assume login system will set this
        self.level2Access = ["Manager", "Admin"]
        self.level3Access = ["Admin"]

    def generateID(self):
        return len(self.employees) + 1


# WRITE EMPLOYEE TO BOTH EMPLOYEE.CSV and USER.CSV
    def write_employee_to_csvs(self, employee):
        if not os.path.exists('data'):
            os.makedirs('data')

        employee_file_path = os.path.join('data', 'employee.csv')
        users_file_path = os.path.join('data', 'users.csv')

        employee_fieldnames = ['id', 'username', 'password', 'first name', 'last name', 'role']
        user_fieldnames = ['id', 'username', 'password', 'role']

        employee_file_exists = os.path.isfile(employee_file_path)
        users_file_exists = os.path.isfile(users_file_path)

        with open(employee_file_path, mode='a', newline='') as emp_csv:
            employee_writer = csv.DictWriter(emp_csv, fieldnames=employee_fieldnames)
            if not employee_file_exists:
                employee_writer.writeheader()

            first_name = getattr(employee, 'first_name', 'Not Provided')
            last_name = getattr(employee, 'last_name', 'Not Provided')

            employee_writer.writerow({
                'id': employee.id,
                'username': employee.username,
                'password': employee.password,
                'first name': first_name,
                'last name': last_name,
                'role': employee.role
            })

        with open(users_file_path, mode='a', newline='') as user_csv:
            user_writer = csv.DictWriter(user_csv, fieldnames=user_fieldnames)
            if not users_file_exists:
                user_writer.writeheader()

            user_writer.writerow({
                'id': employee.id,
                'username': employee.username,
                'password': employee.password,
                'role': employee.role
            })


#Simplified privilege check to one method.
    def _add_employee_with_privilege_check(self, employee_class, required_access, name, username, password, role=None):
        if self.activeEmployee and self.activeEmployee.role in required_access:
            emp_id = self.generateID()
            if role:
                new_employee = employee_class(name, role, emp_id, username, password)
            else:
                new_employee = employee_class(name, emp_id, username, password)
            self.employees.append(new_employee)
            self.write_employee_to_csvs(new_employee)
        else:
            required_level = 2 if required_access == self.level2Access else 3
            print(f"Action canceled --- Privilege Level Error, must be level {required_level}")

    # Public Add Methods Simplified with methods
    def addCrewMember(self, name, role, username, password):
        self._add_employee_with_privilege_check(CrewMember, self.level2Access, name, username, password, role)

    def addManager(self, name, username, password):
        self._add_employee_with_privilege_check(Manager, self.level3Access, name, username, password)

    def addBusboy(self, name, username, password):
        self._add_employee_with_privilege_check(Busboy, self.level2Access, name, username, password)

    def addWaiter(self, name, username, password):
        self._add_employee_with_privilege_check(Waiter, self.level2Access, name, username, password)

    def addCook(self, name, username, password):
        self._add_employee_with_privilege_check(Cook, self.level2Access, name, username, password)


### Loads our employees into classes.
    def load_employees_from_csv(self):
        employee_file_path = os.path.join('data', 'employee.csv')

        if not os.path.isfile(employee_file_path):
            print("No employee.csv file found.")
            return

        with open(employee_file_path, mode='r', newline='') as emp_csv:
            employee_reader = csv.DictReader(emp_csv)
            for row in employee_reader:
                role = row['role']
                emp_id = int(row['id'])
                username = row['username']
                password = row['password']
                first_name = row['first name']
                last_name = row['last name']
                full_name = f"{first_name} {last_name}".strip()

                if role == 'Manager':
                    employee = Manager(full_name, emp_id, username, password)
                elif role == 'Cook':
                    employee = Cook(full_name, emp_id, username, password)
                elif role == 'Waiter':
                    employee = Waiter(full_name, emp_id, username, password)
                elif role == 'Busboy':
                    employee = Busboy(full_name, emp_id, username, password)

                self.employees.append(employee)

        print(f"Loaded {len(self.employees)} employees from employee.csv.")

    #  The "Get" Methods from your original class:

    def getEmployeeList(self):
        """Return list of all employee names."""
        return [emp.username for emp in self.employees]

    def getEmployeeByID(self, employee_id):
        """Return an employee object based on ID."""
        for emp in self.employees:
            if emp.id == employee_id:
                return emp
        print(f"No employee found with ID {employee_id}.")
        return None

    def getEmployeeByUsername(self, username):
        """Return an employee object based on username."""
        for emp in self.employees:
            if emp.username == username:
                return emp
        print(f"No employee found with username '{username}'.")
        return None

    def getEmployeeRole(self, username):
        """Return role of an employee based on username."""
        employee = self.getEmployeeByUsername(username)
        if employee:
            return employee.role
        return None
