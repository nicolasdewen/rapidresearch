import os
import requests
from flask import redirect, render_template, request, session
from functools import wraps
import json
from urllib.request import urlopen

def profile(ticker):
    """Look up profile for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
    response = urlopen(url)
    profile = response.read().decode("utf-8")
    return json.loads(profile)

def ratios(ticker):
    """Look up profile for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}"
    response = urlopen(url)
    ratios = response.read().decode("utf-8")
    return json.loads(ratios)

def metrics(ticker):
    """Look up metrics for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?limit=40&apikey={api_key}"
    response = urlopen(url)
    metrics = response.read().decode("utf-8")
    return json.loads(metrics)

def isgrowth(ticker):
    """Look up P&L growth stats for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/income-statement-growth/{ticker}?apikey={api_key}&limit=40"
    response = urlopen(url)
    isgrowth = response.read().decode("utf-8")
    return json.loads(isgrowth)

def ratings(ticker):
    """Look up ratings for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/rating/{ticker}?apikey={api_key}"
    response = urlopen(url)
    ratings = response.read().decode("utf-8")
    return json.loads(ratings)

def news(ticker):
    """Look up news for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=50&apikey={api_key}"
    response = urlopen(url)
    news = response.read().decode("utf-8")
    return json.loads(news)

def prices(ticker):
    """Look up prices for ticker."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line&apikey={api_key}"
    response = urlopen(url)
    prices = response.read().decode("utf-8")
    return json.loads(prices)

def gainers():
    """Look up gainers."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/gainers?apikey={api_key}"
    response = urlopen(url)
    gainers = response.read().decode("utf-8")
    return json.loads(gainers)

def losers():
    """Look up losers."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/losers?apikey={api_key}"
    response = urlopen(url)
    losers = response.read().decode("utf-8")
    return json.loads(losers)

def actives():
    """Look up actives."""

    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/actives?apikey={api_key}"
    response = urlopen(url)
    actives = response.read().decode("utf-8")
    return json.loads(actives)

def sectors():
    """Look up sector performance"""
    # Contact API
    api_key = os.environ.get("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/historical-sectors-performance?limit=50&apikey={api_key}"
    response = urlopen(url)
    sectors = response.read().decode("utf-8")
    return json.loads(sectors)
