import urllib.parse
import csv
import datetime
import urllib
import uuid

import pytz as pytz
import requests

from helpers import apology


def search_ticker(keywords: str):
    """Look up for tickers"""
    # Contact API
    try:
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
                                    "10_15_7) AppleWebKit/537.36 (HTML, "
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


def get_quote(symbol: str):
    """Look up for quote"""
    """Look up quote for symbol."""
    if symbol == "":
        return apology("Blank ticker", 400)

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())},
                                headers={"User-Agent": "python-requests",
                                         "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(
            csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        cur_quote = quotes[0]
        if float(cur_quote["Volume"]) == 0:
            return None
        print(cur_quote)
        price = round(float(cur_quote["Adj Close"]), 2)
        change = round(float(cur_quote["Open"]) - price, 2)
        change_percent = "{:.2%}".format(change / float(cur_quote["Open"]))
        return dict({
            "ticker": symbol,
            "currentPrice": price,
            "change": change,
            "changePercent": change_percent,
            "volume": cur_quote["Volume"]
        })
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
