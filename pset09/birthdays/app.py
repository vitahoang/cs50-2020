import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)
app.secret_key = "super secret key"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
PATH = "sqlite:///"
DIRNAME = "/Users/vitahoang/Code/cs50-2020/pset09/birthdays/"
DBNAME = "birthdays.db"
db = SQL(PATH+DIRNAME+DBNAME)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """The root route

    Returns:
        GET: render the default html with birthdays 
        POST: put a new birthday to db
    """

    if request.method == "POST":

        # TODO: Add the user's entry into the database
        form_data = request.form
        name = form_data.get("name")
        month = int(form_data.get("month"))
        day = int(form_data.get("day"))

        if day > 31 or day < 0 or month > 12 or month < 0:
            flash("Invalid day!", "danger")
            return render_template("index.html")

        if month in [4, 6, 8, 9, 11]:
            if day > 30:
                flash("Invalid day!", "danger")
                return render_template("index.html")

        if month == 2:
            if day > 29:
                flash("Invalid day!", "danger")
                return render_template("index.html")

        flash("A friend's brithday has been add to your list!", "success")
        db.execute("INSERT INTO `birthdays` (`name`,`month`,`day`) VALUES (?,?,?)", name, month, day)
        friends = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", friends=friends)

    if request.method == "GET":

        # TODO: Display the entries in the database on index.html
        friends = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", friends=friends)
