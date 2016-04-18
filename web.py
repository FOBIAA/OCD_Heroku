#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template, session, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from interface import Interface
from functools import wraps
from models import *

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
    if request.method == "POST":
        interface.refresh()
        session["username"] = request.form["username"]
        flash("Welcome to your bank " + session["username"])
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db.session.add(Client(session["username"], request.form["password"],
                              request.form["email"], request.form["balance"]))
        db.session.commit()
        # Send code 307 to preserve the post request
        return redirect(url_for("login"), code=307)
    return render_template("register.html")

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
