from _decimal import Decimal

from helpers import decimal2, moneyfmt
from error import *
from modules.tickers import get_quote
from modules.users import get_balance


def get_user_portfolio_by_ticker(db, user_id, ticker) -> dict:
    """
    Retrieves the portfolio with the specified user ID and ticker symbol
    from the database.

    Args:
        db: An instance of the database connection.
        user_id (int): The user ID for the portfolio to retrieve.
        ticker (str): The ticker symbol for the portfolio to retrieve.
        either 'long' or 'short'.

    Returns:
        dict: A dictionary containing the details of the retrieved portfolio.

    Raises:
        Exception: If an error occurs while retrieving the portfolio from
        the database.
    """
    try:
        portfolio = db.execute(
            "SELECT * FROM portfolios WHERE user_id = ? AND ticker = ?",
            user_id, ticker)
        return portfolio
    except Exception as e:
        raise e


def create_portfolio(db, user_id: int, ticker: str) -> int:
    """
    Creates a new portfolio in the database with the specified user ID & ticker

    Args:
        db: An instance of the database connection.
        user_id (int): The user ID for the portfolio.
        ticker (str): The ticker symbol for the portfolio.

    Returns:
        int: The ID of the newly created portfolio.

    Raises:
        None.
    """
    portfolio_id = db.execute(
        "INSERT INTO portfolios (user_id, ticker) VALUES (?, ?)",
        user_id, ticker)
    return portfolio_id


def update_portfolio(db, portfolio, txn):
    new_size, new_entry_price = Decimal(), Decimal()
    cur_size = decimal2(portfolio["size"])
    cur_entry_price = decimal2(portfolio["entry_price"])

    # if buy, need to add more size and calculate new entry_price
    if txn["txn_type"] == "buy":
        new_size = cur_size + decimal2(txn["size"])
        new_entry_price = (cur_size * cur_entry_price +
                           decimal2(txn["total_value"])) / new_size

    # if sell, just need to subtract the size
    if txn["txn_type"] == "sell":
        new_size = cur_size - decimal2(txn["size"])
        if new_size < 0:
            raise LowPortfolio
        new_entry_price = cur_entry_price

    try:
        db.execute("UPDATE portfolios SET size = ?, entry_price = ?, "
                   "total_value = ?,"
                   "updated_date = CURRENT_TIMESTAMP WHERE id = ?",
                   moneyfmt(new_size),
                   moneyfmt(new_entry_price),
                   moneyfmt(new_size * new_entry_price),
                   portfolio["id"],
                   )
        return True
    except Exception as e:
        raise e


def get_portfolio_by_userid(db, user_id: int):
    try:
        total_current_value = 0
        portfolios = db.execute("SELECT * FROM portfolios "
                                "WHERE user_id = ? AND size != '0'", user_id)
        if len(portfolios) == 0:
            raise PortfolioNotFound
        for ticker in portfolios:
            q = get_quote(ticker["ticker"])
            ticker["price_change"] = q['change']

            current_price = decimal2(q['currentPrice'])
            ticker["current_price"] = moneyfmt(current_price)

            current_value = decimal2(ticker['size']) * current_price
            ticker["current_value"] = moneyfmt(current_value, sep=',')

            total_current_value += current_value
            entry_value = decimal2(ticker["total_value"])
            ticker["pnl"] = moneyfmt(
                (current_value - entry_value) * 100 / entry_value)

        cash = get_balance(db, user_id)
        portfolios = {"cash": moneyfmt(cash, sep=","),
                      "tickers": portfolios,
                      "total_portfolio_value":
                          moneyfmt(cash + total_current_value, curr='$',
                                   sep=',')}
        return portfolios
    except Exception as e:
        raise e
