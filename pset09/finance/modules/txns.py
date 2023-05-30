from flask import session

from modules.tickers import get_quote
from modules.users import get_balance, set_balance


def add_txn(db, portfolio, bid):
    traded_price = float(get_quote(portfolio["ticker"])["currentPrice"])
    total_value = round(traded_price * float(bid["size"]), 2)
    get_balance(db, portfolio["user_id"])
    if bid["txn_type"] == "sell":
        if portfolio["size"] < bid["size"]:
            return
    else:
        if session["user_balance"] < total_value:
            return

    if session["user_balance"] < total_value:
        return
    try:
        txn_id = db.execute(
            "INSERT INTO txns (txn_type, portfolio_id, size, "
            "traded_price, total_value, pre_balance, post_balance) "
            "VALUES (?, ?, ?, ?, ? ,? ,?)",
            bid["txn_type"],
            portfolio["id"],
            bid["size"],
            traded_price,
            total_value,
            session["user_balance"],
            round(float(session["user_balance"]) - total_value, 2),
        )
        txn = get_txn_by_id(db, txn_id)
        set_balance(db, txn["id"], txn["post_balance"])

        return txn
    except Exception as e:
        raise e


def get_txn_by_id(db, txn_id):
    try:
        txn = db.execute(
            "SELECT * FROM txns WHERE id = ?", txn_id
        )[0]
        return txn
    except Exception as e:
        raise e
