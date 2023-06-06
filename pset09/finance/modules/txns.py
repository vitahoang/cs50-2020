from flask import session

from error import *

from helpers import decimal2, moneyfmt
from modules.portfolios import update_portfolio
from modules.tickers import get_quote
from modules.users import get_balance, set_balance


def sell_txn(db, portfolio, size):
    traded_price = decimal2(get_quote(portfolio["ticker"])["currentPrice"])
    total_value = traded_price * decimal2(size)
    if portfolio["size"] < size:
        return LowPortfolio
    pre_balance = get_balance(db, portfolio["user_id"])
    try:
        post_balance = pre_balance + total_value
        txn_id = db.execute(
            "INSERT INTO txns (txn_type, user_id, portfolio_id, size, "
            "traded_price, total_value, pre_balance, post_balance) "
            "VALUES (?, ?, ?, ?, ?, ? ,? ,?)",
            "sell",
            portfolio["user_id"],
            portfolio["id"],
            size,
            moneyfmt(traded_price),
            moneyfmt(total_value),
            moneyfmt(pre_balance),
            moneyfmt(post_balance),
        )
        txn = get_txn_by_id(db, txn_id)
        update_portfolio(db, portfolio, txn)
        set_balance(db, portfolio["user_id"], moneyfmt(post_balance))

        return txn
    except Exception as e:
        set_balance(db, portfolio["user_id"], moneyfmt(pre_balance))
        raise e


def buy_txn(db, portfolio, size):
    traded_price = decimal2(get_quote(portfolio["ticker"])["currentPrice"])
    total_value = traded_price * decimal2(size)
    pre_balance = get_balance(db, portfolio["user_id"])

    # end if bid size > balance
    if total_value > decimal2(session["user_balance"]):
        raise LowBalance

    try:

        # add transaction
        post_balance = decimal2(session["user_balance"]) - total_value
        txn_id = db.execute(
            "INSERT INTO txns (txn_type, user_id, portfolio_id, size, "
            "traded_price, total_value, pre_balance, post_balance) "
            "VALUES (?, ?, ?, ?, ?, ? ,? ,?)",
            "buy",
            portfolio["user_id"],
            portfolio["id"],
            size,
            moneyfmt(traded_price),
            moneyfmt(total_value),
            moneyfmt(pre_balance),
            moneyfmt(post_balance),
        )
        txn = get_txn_by_id(db, txn_id)
        # set new balance
        set_balance(db, portfolio["user_id"], moneyfmt(post_balance))
        update_portfolio(db, portfolio, txn)
        return txn
    except Exception as e:
        set_balance(db, portfolio["user_id"], moneyfmt(pre_balance))
        raise e


def get_txn_by_id(db, txn_id):
    try:
        txn = db.execute(
            "SELECT * FROM txns WHERE id = ?", txn_id
        )[0]
        return txn
    except Exception as e:
        raise e


def get_txns_by_userid(db, user_id: str) -> list:
    try:
        txns = db.execute(
            "SELECT txns.id,txns.created_date,txns.txn_type,"
            "portfolios.ticker,txns.size,txns.traded_price,txns.total_value,txns.pre_balance,txns.post_balance FROM txns JOIN portfolios ON txns.portfolio_id=portfolios.id WHERE portfolios.user_id=?",
            user_id
        )
        return txns
    except Exception as e:
        raise e
