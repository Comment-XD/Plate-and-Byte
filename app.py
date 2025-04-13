from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    get_flashed_messages, 
    flash,
    jsonify
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
        role = user_df.loc[(user_df.username == username) & (user_df.password == int(password))].role.values[0]
        return role
    
    return None


def check_credential(username, password):
    user_df = pd.read_csv(USER_CSV_PATH, index_col=0)
    if ((user_df.username == username) & (user_df.password == int(password))).any(): 
        return True
    
    return False

def add_user(username, password, role="waiter"):
    user_df = pd.read_csv(USER_CSV_PATH)
    user_id = user_df["id"].iloc[-1] + 1 if not user_df.empty else 1
    with open(USER_CSV_PATH, mode="a", newline="\n") as file:
        
        writer = csv.writer(file)
        writer.writerow([user_id, username, password, role])


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

# --------Login Path----------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if check_credential(username, password):

            role = check_role(username, password)
            
            if role == "manager":
                return redirect(url_for("manager"))
            
            elif role == "waiter":    
                return redirect(url_for("waiter"))
            
            elif role == "cook":
                return redirect(url_for("cook"))
        
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
        
        
        if user_exists(username):
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

@app.route('/api/update_table', methods=['POST'])
def update_table():
    # Get data from the request
    data = request.json
    table_id = data.get('table_id')
    status = data.get('status')
    waiter_id = data.get('waiter_id', '')
    
    # Validate required fields
    if not table_id or not status:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Map frontend status names to database status names
    status_mapping = {
        'available': 'Available',
        'occupied': 'Occupied',
        'dirty': 'Dirty'
    }
    
    # Convert status to the format used in CSV
    csv_status = status_mapping.get(status, 'Available')
    
    # Read the current tables data
    tables = []
    try:
        with open('data/tables.csv', 'r') as file:
            reader = csv.DictReader(file)
            tables = list(reader)
    except Exception as e:
        print(f"Error reading tables.csv: {e}")
        return jsonify({'success': False, 'message': 'Error reading tables data'}), 500
    
    # Find and update the specific table
    table_found = False
    for table in tables:
        if table['table_id'] == str(table_id):
            table['status'] = csv_status
            table['waiter_id'] = waiter_id
            table_found = True
            break
    
    if not table_found:
        return jsonify({'success': False, 'message': 'Table not found'}), 404
    
    # Write the updated data back to the CSV
    try:
        with open('data/tables.csv', 'w', newline='') as file:
            fieldnames = ['table_id', 'status', 'waiter_id']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tables)
    except Exception as e:
        print(f"Error writing to tables.csv: {e}")
        return jsonify({'success': False, 'message': 'Error updating tables data'}), 500
    
    return jsonify({'success': True})

# Add this route to your app.py file
@app.route('/api/waiters', methods=['GET'])
def get_waiters():
    waiters = []
    try:
        with open('data/waiters.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                waiters.append({
                    'id': row.get('id', ''),
                    'username': row.get('username', ''),
                    'name': row.get('name', '')
                })
    except Exception as e:
        print(f"Error reading waiters.csv: {e}")
        # If file doesn't exist or is empty, return empty list
        pass
    
    return jsonify(waiters)

@app.route('/api/tables', methods=['GET'])
def get_tables():
    tables = []
    try:
        with open('data/tables.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tables.append({
                    'table_id': row.get('table_id', ''),
                    'status': row.get('status', 'Available'),
                    'waiter_id': row.get('waiter_id', '')
                })
    except Exception as e:
        print(f"Error reading tables.csv: {e}")
        # If file doesn't exist or is empty, return empty list
        pass
    
    return jsonify(tables)

@app.route("/manager")
def manager():
    return render_template("manager_index.html")

@app.route("/cook")
def cook():
    return render_template("cook_index.html")

@app.route("/waiter")
def waiter():
    return render_template("waiter_index.html")


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)