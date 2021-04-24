import alpaca_trade_api as tradeapi
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from statistics import mean, median
import os
from alpaca_trade_api.stream2 import StreamConn
import threading

API_KEY = "your api key here"
API_SECRET = "your api secret here"
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

account = tradeapi.REST(API_KEY, API_SECRET, BASE_URL,
                    api_version="v2").get_account()
days = 1000

"choosing stocks"
stock1 = "ADBE"
stock2 = "AAPL"

def fdma_test(stock1, stock2):

    "get barsets for named stocks"
    adobe_barset = api.get_barset(stock1, "day", limit=days)
    apple_barset = api.get_barset(stock2, "day", limit=days)
    adobe_bars = adobe_barset[stock1]
    apple_bars =apple_barset[stock2]

    def process_history(stock_bars):
        data = []
        time= []
        for i in range(days):
            c = stock_bars[i].c
            t = stock_bars[i].t
            data.append(c)
            time.append(t)
        return data, time 
    stock1_data, stock1_time = process_history(adobe_bars)
    stock2_data, stock2_time = process_history(apple_bars)

    "process historical data"
    history_close = pd.DataFrame(stock1_data, columns=[stock1])
    history_close[stock2] = stock2_data

    "get current spreads"
    stock1_current = stock1_data[days-1]
    stock2_current = stock2_data[days-1]
    current_spread = (stock1_current-stock2_current)

    "start five day moving average strategy"
    moving_avg_day_count = 5
    stock1_last = []
    for i in range(moving_avg_day_count):
        stock1_last.append(stock1_data[days-1]-i)

    stock2_last = []
    for i in range(moving_avg_day_count):
        stock2_last.append(stock2_data[days-1]-1)

    "moving average for adobe"
    stock1_history = pd.DataFrame(stock1_last)
    stock1_fdma = stock1_history.mean()
    "movinf average for apple"
    stock2_history = pd.DataFrame(stock2_last)
    stock2_fdma = stock2_history.mean()

fdma_test(stock1, stock2)
