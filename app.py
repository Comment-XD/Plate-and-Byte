from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import pandas as pd

app = Flask(__name__)

# root path
@app.route("/")
def root():
    return render_template("index.html")

# Route for adding tables to grid
@app.route("/add_tables", methods=["POST"])
def add_tables():
    return

# Route changing the sidebar for access of employee and manager
@app.route("/sidebar", methods=["POST"])
def activate_sidebar():
    return

# Route for the changing the pov of employee and manager
@app.route("/pov", methods=["POST"])
def change_pov():
    return


if __name__ == "__main__":
    app.run(debug=True)