from decimal import Decimal
from functools import wraps

from flask import session, redirect

from helpers import decimal2


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_balance(db, user_id: int) -> Decimal:
    try:
        balance = decimal2(db.execute("SELECT account_balance FROM users "
                                      "WHERE id = ?", user_id)[0]
                           ["account_balance"])
        session["user_balance"] = balance
    except Exception as e:
        raise e
    return balance


def set_balance(db, user_id: int, new_balance: str) -> Decimal:
    try:
        db.execute("UPDATE users SET account_balance = ? WHERE id = ?",
                   new_balance,
                   user_id,
                   )
        session["user_balance"] = new_balance
        return decimal2(new_balance)
    except Exception as e:
        raise e
