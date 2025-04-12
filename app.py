from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    get_flashed_messages, flash
)

import pandas as pd

import csv
import os
from src.utils.employee_factory import create_manager, create_cook, create_waiter
from src.Restaurant import Restaurant

USER_CSV_PATH = "data/users.csv"

def check_role(username, password):
    user_df = pd.read_csv(USER_CSV_PATH, index_col=0)
    if ((user_df.username == username) & (user_df.password == int(password))).any(): 
        return user_df.role
    
    return None

def check_credential(username, password):
    user_df = pd.read_csv(USER_CSV_PATH, index_col=0)
    if ((user_df.username == username) & (user_df.password == int(password))).any(): 
        return True
    
    return False

def add_user(username, password, role="user"):
    if not os.path.exists(USER_CSV_PATH):
        with open(USER_CSV_PATH, mode="w") as file:
            file.write("username,password,role\n")

    with open(USER_CSV_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role])


def user_exists(username):
    user_df = pd.read_csv(USER_CSV_PATH)
    if (user_df["username"] == username).any():
        return True
    
    return False



app = Flask(__name__)
restaurant = Restaurant()
restaurant.load_employees_from_csv()
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# --------- Home Page --------- #
@app.route("/")
def home():
    return render_template("home.html")

# --------Root Path----------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if check_credential(username, password):
            return redirect(url_for("index"))
        
        else:
            return render_template("login.html", 
                                   error="That Plate and Byte account doesn't exist. Enter a different account.")
    
    return render_template("login.html")

# --------- Signup Page --------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if user_exists(username, password):
            return render_template("signup.html",
                                   error="User already exists")
        
        else:
            add_user(username, password)
            return render_template("login.html")
    
    return render_template("signup.html")

# --------- Employee Creation Page --------- #
@app.route('/add_employee_web', methods=['GET', 'POST'])
def add_employee_web():
    if request.method == 'GET':
        return render_template('add_employee.html')

    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if not all([name, username, password, role]):
            return "Missing fields", 400

        employee_file_path = os.path.join('data', 'employee.csv')
        if os.path.exists(employee_file_path):
            with open(employee_file_path, mode='r', newline='') as emp_csv:
                employee_reader = csv.DictReader(emp_csv)
                for row in employee_reader:
                    if row['username'] == username:
                        return "Username already exists.", 400

        emp_id = len(restaurant.employees) + 1

        if role == "Manager":
            new_employee = create_manager(name, username, password, emp_id)
        elif role == "Cook":
            new_employee = create_cook(name, username, password, emp_id)
        elif role == "Waiter":
            new_employee = create_waiter(name, username, password, emp_id)
        else:
            return "Invalid role", 400

        restaurant.employees.append(new_employee)
        restaurant.write_employee_to_csvs(new_employee)

        return redirect('/add_employee_web')  # Redirect back after adding

# Route to view all employees
@app.route('/view_employees')
def view_employees():
    employee_file_path = os.path.join('data', 'employee.csv')

    employees = []

    if os.path.isfile(employee_file_path):
        with open(employee_file_path, mode='r', newline='') as emp_csv:
            employee_reader = csv.DictReader(emp_csv)
            for row in employee_reader:
                employees.append({
                    'id': int(row['id']),
                    'name': row['name']
                })

    # Sort employees by ID
    employees = sorted(employees, key=lambda x: x['id'])

    return render_template('view_employees.html', employees=employees)

# Route to view one employee
@app.route('/employee/<int:employee_id>')
def view_employee(employee_id):
    employee_file_path = os.path.join('data', 'employee.csv')

    selected_employee = None

    if os.path.isfile(employee_file_path):
        with open(employee_file_path, mode='r', newline='') as emp_csv:
            employee_reader = csv.DictReader(emp_csv)
            for row in employee_reader:
                if int(row['id']) == employee_id:
                    selected_employee = row
                    break

    if not selected_employee:
        flash('Employee not found.', 'error')
        return redirect('/view_employees')

    return render_template('employee_detail.html', employee=selected_employee)

# Route to edit employee
@app.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee_file_path = os.path.join('data', 'employee.csv')

    employees = []

    if os.path.isfile(employee_file_path):
        with open(employee_file_path, mode='r', newline='') as emp_csv:
            employee_reader = csv.DictReader(emp_csv)
            employees = list(employee_reader)

    employee_to_edit = None
    for emp in employees:
        if int(emp['id']) == employee_id:
            employee_to_edit = emp
            break

    if not employee_to_edit:
        flash('Employee not found.', 'error')
        return redirect('/view_employees')

    if request.method == 'POST':
        employee_to_edit['name'] = request.form.get('name')
        employee_to_edit['username'] = request.form.get('username')
        employee_to_edit['password'] = request.form.get('password')
        employee_to_edit['role'] = request.form.get('role')

        # Save updated list
        with open(employee_file_path, mode='w', newline='') as emp_csv:
            fieldnames = ['id', 'username', 'name', 'password', 'role']
            writer = csv.DictWriter(emp_csv, fieldnames=fieldnames)
            writer.writeheader()
            for emp in employees:
                writer.writerow(emp)

        flash('Employee updated successfully!', 'success')
        return redirect(f'/employee/{employee_id}')

    return render_template('edit_employee.html', employee=employee_to_edit)

# Route to delete employee
@app.route('/employee/<int:employee_id>/delete', methods=['POST'])
def delete_employee(employee_id):
    employee_file_path = os.path.join('data', 'employee.csv')

    employees = []

    if os.path.isfile(employee_file_path):
        with open(employee_file_path, mode='r', newline='') as emp_csv:
            employee_reader = csv.DictReader(emp_csv)
            employees = list(employee_reader)

    employees = [emp for emp in employees if int(emp['id']) != employee_id]

    # Save updated list
    with open(employee_file_path, mode='w', newline='') as emp_csv:
        fieldnames = ['id', 'username', 'name', 'password', 'role']
        writer = csv.DictWriter(emp_csv, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)

    flash('Employee deleted successfully!', 'success')
    return redirect('/view_employees')
@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)