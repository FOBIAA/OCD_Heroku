#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template

# initialize with template folder in /
app = Flask(__name__, template_folder="static")

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

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
