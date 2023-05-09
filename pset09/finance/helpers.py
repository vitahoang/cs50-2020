import os
import requests
import urllib.parse
import yfinance as yf

from flask import redirect, render_template, request, session, make_response
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("pages/apology.html", top=code,
                           bottom=escape(message)), code


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


def search_ticker(keywords: str):
    """Look up for tickers"""
    # Contact API
    try:
        # api_key = os.environ.get("API_KEY")
        # url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH" \
        #       f"&keywords={urllib.parse.quote_plus(keywords)}&apikey={api_key}"
        yh_headers = {"scheme": "https",
                      "accept": "text/html,application/xhtml+xml,"
                                "application/xml;q=0.9,image/avif,"
                                "image/webp,image/apng,*/*;q=0.8,"
                                "application/signed-exchange;v=b3;q=0.7",
                      "accept-encoding": "gzip, deflate, br",
                      "accept-language": "vi-VN,vi;q=0.9",
                      "cache-control": "max-age=0",
                      "upgrade-insecure-requests": "1",
                      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                                    "10_15_7) AppleWebKit/537.36 (KHTML, "
                                    "like Gecko) Chrome/112.0.0.0 "
                                    "Safari/537.36",
                      }
        yh_url = f"https://query1.finance.yahoo.com/v1/finance/search?q" \
                 f"={urllib.parse.quote_plus(keywords)}" \
                 f"&lang=en-US&region=US&quotesCount=10&newsCount=0" \
                 f"&enableFuzzyQuery=false&quotesQueryId" \
                 f"=tss_match_phrase_query&multiQuoteQueryId" \
                 f"=multi_quote_single_token_query&enableCb=true" \
                 f"&enableNavLinks=true&enableEnhancedTrivialQuery=true" \
                 f"&enableCulturalAssets=true&enableLogoUrl=true" \
                 f"&researchReportsCount=2"
        response = requests.get(yh_url, headers=yh_headers)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        matched = response.json()["quotes"]
        return matched
    except (KeyError, TypeError, ValueError):
        return None


def get_quote(q: str):
    """Look up for quote"""
    try:
        # api_key = os.environ.get("API_KEY")
        # url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE" \
        #       f"&symbol={urllib.parse.quote_plus(ticker)}&apikey={api_key}"
        # response = requests.get(url)
        # response.raise_for_status()
        ticker = yf.Ticker(q).info
    except requests.RequestException:
        return None
    # Parse response
    try:
        # quote = response.json()["Global Quote"]
        key = ('symbol',
               'previousClose',
               'open',
               'dayLow', 'dayHigh',
               'currentPrice', 'volume')
        _quote = {k: v for k, v in ticker.items() if k in key}
        _quote['change'] = round(_quote['currentPrice'] - _quote[
            'previousClose'], 2)
        _quote['changePercent'] = str(round(_quote['change'] / _quote[
            'previousClose'] * 100, 2)) + '%'
        print(_quote)
        return _quote
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
