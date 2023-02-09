import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, \
    make_response, jsonify
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.secret_key = "super secret key"

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Set API_KEY
os.environ.setdefault("API_KEY", "12434")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            flash("invalid username and/or password", "error")
            return render_template("pages/login.html")

        # Remember which user has logged in
        if check_password_hash(rows[0]["hash"],
                               request.form.get("password")):
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            flash("Let's print some money!💸💸💸", "success")
            return redirect("/")

        flash("invalid username and/or password", "error")
        return render_template("pages/login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("pages/login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        if len(db.execute("SELECT username FROM users WHERE username LIKE ?",
                          username)) != 0:
            return flash("username has been taken", "error")
        password_hash = generate_password_hash(password)
        if db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                      username, password_hash):
            flash("Your account has been created successfully!",
                  "success")
            return render_template("pages/login.html")
    else:
        return render_template("pages/register.html")
