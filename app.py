from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from src.Cook import Cook
from src.Waiter import Waiter
from src.Manager import Manager

import pandas as pd
import csv

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


@app.route("/manager")
def manager():
    return render_template("manager_index.html")

# --------- Employee List Path --------- #
@app.route("/manager/employee_list")
def manager_employee_list():
    return render_template("employee_list.html")
    
@app.route("/waiter")
def waiter():
    return render_template("waiter_index.html")
    
@app.route("/cook")
def cook_index():
    return render_template("cook_index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)