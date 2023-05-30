def get_portfolio(db, user_id, ticker) -> dict:
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
            user_id, ticker)[0]
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
    port_id = db.execute(
        "INSERT INTO portfolios (user_id, ticker) VALUES (?, ?)",
        user_id, ticker)
    return port_id


def update_portfolio(db, portfolio, txn):
    # calculate a new size
    size = portfolio["size"]
    entry_price = portfolio["entry_price"]

    # if bought, need to add more size and calculate new entry_price
    if txn["txn_type"] == "buy":
        size += txn["size"]
        entry_price = round(
            (
                    float(portfolio["size"] * portfolio[
                        "entry_price"])
                    + txn["total_value"]
            )
            / float(size), 2)

    # if sold, just need to subtract the size
    size -= txn["size"]
    if size < 0:
        return False

    try:
        db.execute("UPDATE portfolios SET size = ?, entry_price = ?, "
                   "updated_date = CURRENT_TIMESTAMP WHERE id = ?",
                   size,
                   entry_price,
                   portfolio["id"],
                   )
        return True
    except Exception as e:
        raise e
