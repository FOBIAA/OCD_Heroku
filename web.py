#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from interface import Interface
from functools import wraps

# initialize with template folder in /static
app = Flask(__name__, template_folder="static")
# configure app from object of current environment
app.config.from_object(os.environ['APP_SETTINGS'])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)
# Instantiate an info object
interface = Interface()


def defaults(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" not in session:
            session["username"] = "FOBIAA"
        return f(*args, **kwargs)
    return wrap


# handle url requests
@app.route("/")
@app.route("/dashboard/")
@defaults
def dashboard():
    return render_template("dashboard.html", interface=interface)


@app.route("/transfer/")
@defaults
def transfer():
    return render_template("transfer.html", interface=interface)


@app.route("/donation/")
@app.route("/ocd/")
def ocd():
    return render_template("ocd.html", interface=interface)


@app.route("/login/", methods=["GET", "POST"])
def login():
    session.pop("username")
    interface.refresh()
    return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
