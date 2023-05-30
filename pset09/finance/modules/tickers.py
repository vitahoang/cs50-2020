import urllib.parse

import requests
import yfinance as yf


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


def get_quote(q: str):
    """Look up for quote"""
    try:
        ticker = yf.Ticker(q).info
    except requests.RequestException:
        return None

    # Parse response
    try:
        key = ('symbol',
               'previousClose',
               'open',
               'dayLow', 'dayHigh',
               'currentPrice', 'volume')
        _quote = {k: v for k, v in ticker.items() if k in key}
        _quote['change'] = round(_quote['currentPrice'] - _quote[
            'previousClose'], 2)
        _quote['changePercent'] = "{:.2%}".format(_quote['change'] / _quote[
            'previousClose'])
        print(_quote)
        return _quote
    except (KeyError, TypeError, ValueError):
        return None
