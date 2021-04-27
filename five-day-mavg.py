import json
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

account = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2").get_account()

blocked =  account.trading_blocked()
if not blocked:
    print("trading unrestricted")

days = 1000

"choosing stocks"
stock1 = "ADBE"
stock2 = "AAPL"

def fdma_test(stock1, stock2):

    #get barsets for named stocks
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

    #process historical data
    history_close = pd.DataFrame(stock1_data, columns=[stock1])
    history_close[stock2] = stock2_data

    #get current spreads
    stock1_current = stock1_data[days-1]
    stock2_current = stock2_data[days-1]
    current_spread = (stock1_current-stock2_current)

    #start five day moving average strategy
    moving_avg_day_count = 5
    stock1_last = []
    for i in range(moving_avg_day_count):
        stock1_last.append(stock1_data[days-1]-i)

    stock2_last = []
    for i in range(moving_avg_day_count):
        stock2_last.append(stock2_data[days-1]-1)
    #moving average for adobe
    stock1_history = pd.DataFrame(stock1_last)
    stock1_fdma = stock1_history.mean()
    #moving average for apple"
    stock2_history = pd.DataFrame(stock2_last)
    stock2_fdma = stock2_history.mean()
    
    #spread average
    spread_avg = min(stock1_fdma - stock2_data)
    spread_factor = 0.01
    wide_spread = spread_avg*(1+spread_factor)
    thin_spread = spread_avg*(1-spread_factor)

    # caclulation of shares to trade
    total_cash = float(account.buying_power)
    limit_stock1 = total_cash//stock1_current
    limit_stock2 = total_cash//stock2_current
    number_of_shares = int(min(limit_stock1, limit_stock2)/2)   

fdma_test(stock1, stock2)

portfolio = api.list_positiosn()
clock = api.get_clock()

if clock.is_open == True:
    if bool(portfolio) == False:
        if current_spread > wide_spread:
            #short top stock
            api.submit_order(symbol=stock1, qty=number_of_shares, side='sell',
                type="market", time_in_force="day")

            #long bottom stock
            api.submit_order(symbol=stock2, qty=number_of_shares, side="buy", 
                type ="market", time_in_force="day")
            print("short top-long bottom : sold-bought")

        elif current_spread < thin_spread:
            #long top stock
            api.submit_oder(symbol=stock1, qty=number_of_shares, side="buy", 
                type ="market", time_in_force="day")
            #short bottom stock
            api.submit_oder(symbol=stock2, qty-number_of_shares, side="sell", 
                type="market", time_in_force="day")
            print("long top-short botton : bought-sold")
    else:
        wide_trade_spread = spread_avg*(1+spread_factor+.03)
        thin_trade_spread = spread_avg*(1+spread_factor-.03)
        if current_spread<=wide_trade_spread and current_spread>=thin_trade_spread:
            api.close_position(stock1)
            api.close_position(stock2)
            print("position closed")
        else:
            print("no trades made, position open")
            pass
