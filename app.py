import traceback

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
    send_from_directory,
    send_file
)

import pandas as pd
import openpyxl
import numpy as np

import csv
import os

from src.utils.employee_factory import create_manager, create_cook, create_waiter
from src.Restaurant import Restaurant

USER_CSV_PATH = "data/employee.csv"

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

def write_order_to_csv(table_id, order_items, path="data/orders.csv"):
    fieldnames = ["table_id", "food_item", "price", "total_quantity", "total_price"]
    with open(path, mode="a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in order_items:
            writer.writerow({
                "table_id": table_id,
                "food_item": item["food_item"],
                "price": item["price"],
                "total_quantity": item["total_quantity"],
                "total_price": item["total_price"]
            })

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
            # Store username in session
            session['username'] = username
            
            role = check_role(username, password)
            
            if role.lower() == "manager":
                return redirect(url_for("manager"))
            
            elif role.lower() == "waiter":    
                return redirect(url_for("waiter"))
            
            elif role.lower() == "cook":
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

        emp_id = restaurant.curr_emp_id + 1
        restaurant.curr_emp_id += 1
        
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
                    'name': row['name'],
                    'role': row['role']
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
    
    
    tables_file_path = os.path.join('data', 'tables.csv')
    waiters_file_path = os.path.join('data', 'waiters.csv')
    employee_file_path = os.path.join('data', 'employee.csv')

    employee_df = pd.read_csv(employee_file_path, index_col=0)
    
    current_employees = employee_df[employee_df.index != employee_id]
    current_employees.to_csv(employee_file_path)
    
    removed_employee_role = employee_df[employee_df.index == employee_id].role.item()
    
    if removed_employee_role.lower() == "waiter":
        waiter_df = pd.read_csv(waiters_file_path, index_col=0)
        tables_df = pd.read_csv(tables_file_path, index_col=0)
        
        current_waiters = waiter_df[waiter_df.index != employee_id]
        current_waiters.to_csv(waiters_file_path)
        
        tables_df.loc[tables_df.waiter_id == employee_id, "waiter_id"] = np.nan
        tables_df.to_csv(tables_file_path)
        
    elif removed_employee_role.lower() == "manager":
        pass
            
    
    # elif current_employee_role.lower() == "cook":
    #     pass
        

    flash('Employee deleted successfully!', 'success')
    return redirect('/view_employees')

@app.route('/api/update_table_config', methods=['POST'])
def update_table_config():
    data = request.json
    table_id = data.get('table_id')
    size = data.get('size', 'small')
    seats = data.get('seats', 4)
    joined_with = data.get('joined_with', [])
    
    if not table_id:
        return jsonify({'success': False, 'message': 'Missing table ID'}), 400
    
    # Read the current tables configuration
    tables_config = []
    try:
        with open('data/table_config.csv', 'r') as file:
            reader = csv.DictReader(file)
            tables_config = list(reader)
    except FileNotFoundError:
        # If file doesn't exist, create an empty list
        tables_config = []
    
    # Find if this table already has a configuration
    table_found = False
    for table in tables_config:
        if table['table_id'] == str(table_id):
            table['size'] = size
            table['seats'] = str(seats)
            table['joined_with'] = ','.join(joined_with) if joined_with else ''
            table_found = True
            break
    
    # If table not found, add a new configuration
    if not table_found:
        tables_config.append({
            'table_id': str(table_id),
            'size': size,
            'seats': str(seats),
            'joined_with': ','.join(joined_with) if joined_with else ''
        })
    
    # Write the updated configuration back to the CSV
    try:
        with open('data/table_config.csv', 'w', newline='') as file:
            fieldnames = ['table_id', 'size', 'seats', 'joined_with']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tables_config)
    except Exception as e:
        print(f"Error writing to table_config.csv: {e}")
        return jsonify({'success': False, 'message': 'Error updating table configuration'}), 500
    
    return jsonify({'success': True})

@app.route('/api/save_layout', methods=['POST'])
def save_layout():
    data = request.json
    tables = data.get('tables', [])
    joined_tables = data.get('joinedTables', {})
    
    if not tables:
        return jsonify({'success': False, 'message': 'No table data provided'}), 400
    
    # Save table layout configuration
    try:
        # Save table positions and sizes
        with open('data/table_layout.csv', 'w', newline='') as file:
            fieldnames = ['table_id', 'position_left', 'position_top', 'size', 'seats']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for table in tables:
                position = table.get('position', {})
                writer.writerow({
                    'table_id': table['id'],
                    'position_left': position.get('left', 0),
                    'position_top': position.get('top', 0),
                    'size': table.get('size', 'small'),
                    'seats': table.get('seats', 4)
                })
        
        # Save joined tables information
        with open('data/joined_tables.csv', 'w', newline='') as file:
            fieldnames = ['primary_table_id', 'joined_table_ids']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for primary_id, joined_ids in joined_tables.items():
                writer.writerow({
                    'primary_table_id': primary_id,
                    'joined_table_ids': ','.join(joined_ids) if joined_ids else ''
                })
                
        return jsonify({'success': True, 'message': 'Layout saved successfully'})
    
    except Exception as e:
        print(f"Error saving layout: {e}")
        return jsonify({'success': False, 'message': f'Error saving layout: {str(e)}'}), 500

@app.route('/api/load_layout', methods=['GET'])
def load_layout():
    try:
        # Load table positions and configurations
        table_layout = []
        if os.path.exists('data/table_layout.csv'):
            with open('data/table_layout.csv', 'r') as file:
                reader = csv.DictReader(file)
                table_layout = list(reader)
        
        # Load joined tables information
        joined_tables = {}
        if os.path.exists('data/joined_tables.csv'):
            with open('data/joined_tables.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    primary_id = row['primary_table_id']
                    joined_ids = row['joined_table_ids'].split(',') if row['joined_table_ids'] else []
                    if joined_ids:  # Only add if there are actually joined tables
                        joined_tables[primary_id] = joined_ids
        
        return jsonify({
            'success': True,
            'tableLayout': table_layout,
            'joinedTables': joined_tables
        })
    
    except Exception as e:
        print(f"Error loading layout: {e}")
        return jsonify({'success': False, 'message': f'Error loading layout: {str(e)}'}), 500

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

# Route to get waiters
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

@app.route('/api/current_waiter', methods=['GET'])
def get_current_waiter():
    # Get username from session (you'll need to set this during login)
    username = session.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    # Look up the waiter in the waiters.csv file
    try:
        with open('data/waiters.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('username') == username:
                    return jsonify({
                        'success': True,
                        'waiter_id': row.get('id', ''),
                        'waiter_name': row.get('name', '')
                    })
    except Exception as e:
        print(f"Error reading waiters.csv: {e}")
    
    return jsonify({'success': False, 'message': 'Waiter not found'})

@app.route('/api/tables', methods=['GET'])
def get_tables():
    tables = []
    waiters = {}
    
    # First load all waiters into a dictionary for quick lookup
    try:
        with open('data/waiters.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                waiters[row.get('id', '')] = {
                    'name': row.get('name', ''),
                    'username': row.get('username', '')
                }
    except Exception as e:
        print(f"Error reading waiters.csv: {e}")
    
    # Then load tables with waiter names
    try:
        with open('data/tables.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                waiter_id = row.get('waiter_id', '')
                waiter_name = waiters.get(waiter_id, {}).get('name', '') if waiter_id else ''
                
                tables.append({
                    'table_id': row.get('table_id', ''),
                    'status': row.get('status', 'Available'),
                    'waiter_id': waiter_id,
                    'waiter_name': waiter_name
                })
    except Exception as e:
        print(f"Error reading tables.csv: {e}")
        # If file doesn't exist or is empty, return empty list
        pass
    
    return jsonify(tables)

@app.route('/api/write_order', methods=['POST'])
def write_order():
    data = request.get_json()
    table_id = data.get('table_id')
    order_items = data.get('items')

    if not table_id or not order_items:
        return jsonify({'success': False, 'message': 'Missing table number or order items'}), 400

    try:
        write_order_to_csv(table_id, order_items)
        return jsonify({'success': True, 'message': 'Order saved successfully'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

@app.route('/api/menu')
def get_menu():
    try:
        menu_path = 'data/menu.csv'
        if not os.path.exists(menu_path):
            return jsonify({'success': False, 'message': 'Menu file not found'}), 404
            
        menu_items = []
        with open(menu_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert price to float
                if 'price' in row:
                    row['price'] = float(row['price'])
                menu_items.append(row)
                
        return jsonify({'success': True, 'menu': menu_items})
    except Exception as e:
        print(f"Error loading menu: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/save_menu', methods=['POST'])
def save_menu():
    try:
        data = request.json
        menu_items = data.get('menu_items')
        
        if not menu_items:
            return jsonify({'success': False, 'message': 'No menu items provided'})
        
        # Get the field names from the first item
        fieldnames = list(menu_items[0].keys())
        
        # Write to the menu.csv file
        with open('data/menu.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(menu_items)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/cook_order', methods=['POST'])
def cook_order_route():
    table_number = int(request.form['table_number'])
    food_item = request.form['food_item']
    restaurant.cook_order(table_number, food_item)
    flash(f"{food_item} for Table {table_number} has been cooked!", "success")
    return redirect('/cookqueue')

@app.route('/cookqueue')
def cook_queue():
    orders = []
    orders_path = os.path.join('data', 'orders.csv')
    if os.path.isfile(orders_path):
        with open(orders_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            orders = list(reader)
    return render_template('cookqueue.html', orders=orders)

from datetime import datetime
import os
import csv
from flask import request, render_template, redirect, flash, session


###Clock in clock out function.
@app.route('/clock', methods=['GET', 'POST'])
def clock_in_out():
    if 'username' not in session:
        flash("You must be logged in to access this page.", "error")
        return redirect('/login')

    username = session['username']
    employee_id = None

    # ✅ Use employee.csv to look up ID
    employee_path = os.path.join(os.path.dirname(__file__), 'data', 'employee.csv')
    try:
        with open(employee_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    employee_id = int(row['id'])
                    break
    except FileNotFoundError:
        flash("Error: employee.csv not found.", "error")
        return redirect('/')

    if not employee_id:
        flash("User not found in employee.csv.", "error")
        return redirect('/')

    if request.method == 'POST':
        action = request.form['action']  # 'in' or 'out'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Append to employee_time.csv at the end
        time_log_path = os.path.join(os.path.dirname(__file__), 'data', 'employee_time.csv')
        file_exists = os.path.isfile(time_log_path)

        with open(time_log_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['employee_id', 'username', 'action', 'timestamp'])
            writer.writerow([employee_id, username, action, timestamp])

        flash(f"You clocked {'in' if action == 'in' else 'out'} at {timestamp}", "success")
        return redirect('/clock')

    return render_template('clock.html', employee_id=employee_id)

#### Workload will allows managers to see the time clock and edit in an excel file

@app.route('/workload')
def workload():
    # Load employee names
    employees = {}
    emp_path = os.path.join(os.path.dirname(__file__), 'data', 'employee.csv')
    with open(emp_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employees[int(row['id'])] = row['username']

    # Load time punches
    punches = {}
    time_path = os.path.join(os.path.dirname(__file__), 'data', 'employee_time.csv')
    with open(time_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp_id = int(row['id'])  # ✅ Changed from 'employee_id' to 'id'
            action = row['action']
            timestamp = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")

            if emp_id not in punches:
                punches[emp_id] = []

            punches[emp_id].append((action, timestamp))

    # Calculate total time worked and prepare logs
    summary = {}
    detailed_logs = []

    for emp_id, logs in punches.items():
        logs.sort(key=lambda x: x[1])
        total_time = 0
        i = 0
        while i < len(logs) - 1:
            if logs[i][0] == 'in' and logs[i+1][0] == 'out':
                duration = (logs[i+1][1] - logs[i][1]).total_seconds() / 3600
                total_time += duration
                detailed_logs.append({
                    'username': employees.get(emp_id, f"ID {emp_id}"),
                    'clock_in': logs[i][1],
                    'clock_out': logs[i+1][1],
                    'hours': round(duration, 2)
                })
                i += 2
            else:
                i += 1  # skip mismatched or incomplete pairs

        summary[employees.get(emp_id, f"ID {emp_id}")] = round(total_time, 2)

    return render_template("workload.html", summary=summary, logs=detailed_logs)



@app.route('/export_workload')
def export_workload():


    # Paths
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'employee_time.csv')
    excel_path = os.path.join(os.path.dirname(__file__), 'data', 'workload_export.xlsx')

    # Convert CSV to Excel
    df = pd.read_csv(csv_path)
    df.to_excel(excel_path, index=False)

    # Serve file
    return send_file(excel_path, as_attachment=True)
@app.route("/manager")
def manager():
    return render_template("manager_index.html")

@app.route("/cook")
def cook():
    return render_template("cook_index.html")

@app.route("/waiter")
def waiter():
    return render_template("waiter_index.html")

@app.route('/menu/edit')
def menu_edit():
    return render_template('menu_edit.html')

@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)