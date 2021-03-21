from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST,TimeFrame
import pandas as pd
from alpaca_trade_api.stream2 import StreamConn
import threading
#load_dotenv()

API_KEY = "api key here"
API_SECRET = "api secret here"
BASE_URL = "https://paper-api.alpaca.markets"

api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

account = REST(API_KEY, API_SECRET, BASE_URL,
                    api_version="v2").get_account()

def runTest():
    blocked = False
    if account.trading_blocked:
        blocked = True

    if blocked == False:
        print("running")
                
        connection = StreamConn(API_KEY, API_SECRET, base_url=BASE_URL,
                    data_url="wss://data.alpaca.markets",
                    data_stream="alpacadatav1")
        
        @connection.on(r'^AM.AAPL$')
        async def tradeInfo(connection, channels, data):
            symbol = data.symbol
            print("close: ", data.close)
            print("open: ", data.open)
            print("low: ", data.low)
            print("high: ", data.high)

            if data.close > data.open and data.open - data.low > 0.01:
                print("buying 1")
                api.submit_order(symbol, 1, "buy", 
                    "market", "day")
                print("bought")
                print("remaining: ", account.buy_power)
            #2do : sell and take profit later
        
        def startTest():
            connection.run(["AM.AAPL"])
            print("...requesting")

        websocketThread = threading.Thread(target=startTest, daemon=True)
        websocketThread.start()

runTest()
