#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initialize with template folder in /static
app = Flask(__name__, template_folder="static")
# configure app from object of current environment
app.config.from_object(os.environ['APP_SETTINGS'])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)


# handle url requests
@app.route("/")
@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/transfer/")
def transfer():
    return render_template("transfer.html")


@app.route("/donation/")
@app.route("/ocd/")
def ocd():
    return render_template("ocd.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
