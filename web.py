#!/usr/bin/env python

# import needed libraries
from __future__ import division
import os, sqlalchemy
from flask import Flask, render_template, session, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from interface import Interface
from functools import wraps
from datetime import datetime

# initialize with template folder in /static
app = Flask(__name__, template_folder="static")
# configure app from object of current environment
app.config.from_object(os.environ['APP_SETTINGS'])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)
# Instantiate an info object
interface = Interface()
from models import *


def default_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" not in session:
            session["username"] = "FOBIAA"
        return f(*args, **kwargs)
    return wrap


# handle url requests
@app.route("/")
@app.route("/dashboard/")
@default_login
def dashboard():
    return render_template("dashboard.html", interface=interface)


@app.route("/transfer/", methods=["GET", "POST"])
@default_login
def transfer():
    if request.method == "POST":
        client = Client.query.get(session["username"])
        try:
            money = float(request.form["money"])
        except ValueError:
            money = None
        donation = 0
        if request.form["ocd"] == "true":
            try:
                donation = float(request.form["amount"])
            except ValueError:
                donation = None
            if request.form["type"] == "percent":
                donation *= money / 100
            db.session.add(Donation(session["username"], datetime.now(), donation))
            client.score += donation
            interface.donations = None
            flash("You donated " + str(donation) + "AED, Thanks")
        if client.frequency == "odd":
            client.frequency = "even"
        elif client.frequency == "even":
            client.frequency = "odd"
        if request.form["hide"] == "true":
            client.checkbox = "hide"
            client.app = "disable"
        elif request.form["enabled"] == "true":
            client.app = "enable"
        client.balance -= money + donation
        db.session.commit()
        flash("Your Transaction Has Been Sent")
        interface.check_awards()
        interface.refresh()
        return redirect(url_for("dashboard"))
    return render_template("transfer.html", interface=interface)


@app.route("/ocd/", methods=["GET", "POST"])
@default_login
def ocd():
    if request.method == "POST":
        client = Client.query.get(session["username"])
        client.type = request.form["type"]
        try:
            client.amount = float(request.form["amount"])
        except ValueError:
            client.amount = None
        client.frequency = request.form["frequency"]
        client.reveal = request.form["reveal"]
        DonatesTo.query.filter_by(client=session["username"]).delete()
        for image in request.form["charity"].split():
            db.session.add(DonatesTo(session["username"], image))
        client.checkbox = request.form["checkbox"]
        client.app = request.form["app"]
        db.session.commit()
        interface.refresh()
        flash("Your Settings Were Saved")
        return redirect(url_for("ocd"))
    return render_template("ocd.html", interface=interface)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        client = Client.query.get(request.form["username"])
        if client is not None:
            if client.password == request.form["password"]:
                interface.refresh()
                session["username"] = request.form["username"]
                interface.check_awards()
                flash("Welcome to Your Bank " + session["username"])
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong Password, Try Again")
                return redirect(url_for("login"))
        else:
            flash("The User Doesn't Exist")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            db.session.add(Client(request.form["username"], request.form["password"],
                                  request.form["email"], request.form["balance"]))
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            flash(request.form["username"] + " is Already Taken")
            return redirect(url_for("register"))
        # Send code 307 to preserve the post request
        return redirect(url_for("login"), code=307)
    return render_template("register.html")


@app.route("/logout/")
def logout():
    interface.refresh()
    session.clear()
    return redirect(url_for("login"))


# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
