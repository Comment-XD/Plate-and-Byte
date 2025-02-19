from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)

import pandas as pd
import csv
import os

# from src.Restaurant import Restaurant
# from src.Manager import Manager
# from src.Employee import Employee
USER_CSV_PATH = "data/users.csv"

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
    
# --------Root Path----------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if check_credential(username, password):
            return redirect(url_for("home"))
        
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

# ----------- Home Page ----------------- #
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")
    
# Route for adding tables to grid
@app.route("/restaraunt", methods=["POST"])
def set_restaurant_dim():
    return

# Route for adding tables to grid
@app.route("/add_tables", methods=["POST"])
def add_tables():
    return

# Route for the changing the pov of employee and manager
@app.route("/pov", methods=["POST"])
def change_pov():
    return


if __name__ == "__main__":
    app.run(debug=True, port=8000)