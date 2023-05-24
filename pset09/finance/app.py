import json
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, \
    make_response, jsonify, url_for
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, search_ticker, get_quote

# Configure application
app = Flask(__name__)
app.secret_key = "super secret key"

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Set API_KEY
os.environ.setdefault("IEX_API_KEY", "sk_e1dbd11abe3344b0a0233a9ea8a4ab9b")
os.environ.setdefault("API_KEY", "GF3Y0QEZSMFYRA0N")

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
    return render_template("pages/portfolio.html")


@app.route("/quote", methods=["GET"])
@login_required
def quote():
    """search stock quote."""
    q = request.args.get("q")
    scope = request.args.get("scope")
    if q and scope == "ticker":
        ticker_list = search_ticker(q)
        if ticker_list:
            return make_response(ticker_list, 200)
        else:
            return make_response(json.dumps({"message": "No Match"}), 404)

    if q and scope == "quote":
        _quote = get_quote(q)
        if _quote:
            return make_response(_quote, 200)
        else:
            return make_response("No Match", 404)

    return render_template("pages/quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("pages/buy.html")
    bid = request.json
    print(bid)


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


@login_required
@app.route("/profile", methods=["GET"])
def profile():
    """Query user profile"""
    print(session["user_id"])
    user = db.execute("SELECT id, username, account_balance FROM users WHERE "
                      "id = ?", session["user_id"])[0]
    if user:
        return make_response(
            jsonify(
                user_id=user["id"],
                username=user["username"],
                account_balance=user["account_balance"]
            ), 200)
    else:
        return make_response("No Match", 404)
