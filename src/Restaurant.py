from src.Manager import Manager
from src.CrewMember import CrewMember
from src.Busboy import Busboy
from src.Waiter import Waiter
from src.Cook import Cook

import csv
import os


class Restaurant:
    def __init__(self):
        self.employees = []
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
        manager_file_path = os.path.join('data', 'managers.csv')
        waiter_file_path = os.path.join('data', 'waiters.csv')

        employee_fieldnames = ['id', 'username', 'name', 'password', 'role']
        user_fieldnames = ['id', 'username', 'password', 'role']
        manager_fieldnames = ['id', 'username', 'name', 'password']
        waiter_fieldnames = ['id', 'username', 'name', 'password']

        employee_file_exists = os.path.isfile(employee_file_path)
        users_file_exists = os.path.isfile(users_file_path)

        # ✅ Correct way to get full name now
        full_name = employee.name

        # Write to employee.csv
        with open(employee_file_path, mode='a', newline='') as emp_csv:
            employee_writer = csv.DictWriter(emp_csv, fieldnames=employee_fieldnames)
            if not employee_file_exists:
                employee_writer.writeheader()

            employee_writer.writerow({
                'id': employee.id,
                'username': employee.username,
                'name': full_name,
                'password': employee.password,
                'role': employee.role
            })
            
        
        # Write to users.csv
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
        
        # Write to managers.csv 
        if isinstance(employee, Manager):
            with open(manager_file_path, mode='a', newline='') as manager_csv:
                manager_writer = csv.DictWriter(manager_csv, fieldnames=manager_fieldnames)
                if not users_file_exists:
                    manager_writer.writeheader()

                manager_writer.writerow({
                    'id': employee.id,
                    'username': employee.username,
                    'password': employee.password,
                    'name': employee.name
                })
        
        # Write to waiter.csv
        elif isinstance(employee, Waiter):
            with open(waiter_file_path, mode='a', newline='') as waiter_csv:
                waiter_writer = csv.DictWriter(waiter_csv, fieldnames=waiter_fieldnames)
                if not users_file_exists:
                    waiter_writer.writeheader()

                waiter_writer.writerow({
                    'id': employee.id,
                    'username': employee.username,
                    'password': employee.password,
                    'name': employee.name
                })
                
        elif isinstance(employee, Cook):
            with open(users_file_path, mode='a', newline='') as cook_csv:
                cook_writer = csv.DictWriter(cook_csv, fieldnames=user_fieldnames)
                if not users_file_exists:
                    cook_writer.writeheader()

                cook_writer.writerow({
                    'id': employee.id,
                    'username': employee.username,
                    'password': employee.password,
                    'name': employee.name
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
                emp_id = int(row['id'])
                username = row['username']
                password = row['password']
                name = row['name']
                role = row['role']

                # Recreate correct object based on role
                if role == 'Manager':
                    employee = Manager(name, emp_id, username, password)
                elif role == 'Cook':
                    employee = Cook(name, emp_id, username, password)
                elif role == 'Waiter':
                    employee = Waiter(name, emp_id, username, password)
                else:
                    # fallback if unknown role
                    employee = CrewMember(name, emp_id, username, password, role)

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

####Cook Order Method takes from Orders.CSv finds it and copies it to sales then deletes from the orders.csv.
    def cook_order(self, table_number: int, food_item: str):
        orders_path = os.path.join('data', 'orders.csv')
        sales_path = os.path.join('data', 'sales.csv')

        updated_orders = []
        cooked_order = None

        # Read orders.csv and find the order
        with open(orders_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['table_number']) == table_number and row[
                    'food_item'].strip().lower() == food_item.strip().lower():
                    cooked_order = row
                else:
                    updated_orders.append(row)

        # If order found, write to sales.csv
        if cooked_order:
            # Ensure sales.csv exists with headers
            file_exists = os.path.isfile(sales_path)
            with open(sales_path, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['table_number', 'food_item', 'price', 'total_quantity',
                                                          'total_price'])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    'table_number': cooked_order['table_number'],
                    'food_item': cooked_order['food_item'],
                    'price': cooked_order['price'],
                    'total_quantity': cooked_order['total_quantity'],
                    'total_price': cooked_order['total_price']
                })

            # Overwrite orders.csv without the cooked order
            with open(orders_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['table_number', 'food_item', 'price', 'total_quantity',
                                                          'total_price'])
                writer.writeheader()
                writer.writerows(updated_orders)

            print(f"✅ Cooked and completed: {food_item} for Table {table_number}")
        else:
            print(f"❌ No matching order found for {food_item} at Table {table_number}")