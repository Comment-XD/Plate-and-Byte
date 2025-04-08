from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)

from flask_login import (
    LoginManager, 
    login_required, 
    login_user, 
    logout_user, 
    UserMixin
)

import pandas as pd
import csv
import os

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

@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)