from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST,TimeFrame
import pandas as pd
from alpaca_trade_api.stream2 import StreamConn
import threading
import json
import time
from datetime import datetime
#load_dotenv()

API_KEY = "your api key here"
API_SECRET = "your api secret here"
BASE_URL = "https://paper-api.alpaca.markets"

api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
account = api.get_account()

def writeJSON(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def runTest():
    blocked = False
    if account.trading_blocked:
        blocked = True

    if blocked == False:
        print("running")
                
        connection = StreamConn(API_KEY, API_SECRET, base_url=BASE_URL,
                    data_url="wss://data.alpaca.markets",
                    data_stream="alpacadatav1")
        print("connecting...")
        
        @connection.on(r'^AM.AAPL$')
        async def tradeInfo(connection, channels, data):

            symbol = data.symbol
            print("close: ", data.close)
            print("open: ", data.open)
            print("low: ", data.low)
            print("high: ", data.high, "\n")
            now = datetime.now()
            now = now.strftime("%H:%M:%S")
            trades = {"ref": now, 
                        "symbol": symbol, 
                        "close": data.close, 
                        "open": data.open, 
                        "low": data.low, 
                        "high": data.high, 
                        "funds": account.buying_power}
                
            with open("store.json") as reserve:
                store = json.load(reserve)
            
                temp = store["tradeInfo"]
                temp.append(trades)
            writeJSON(store, file="store.json")
            # sell and take profit later
        connection.run(["AM.AAPL"])
        

runTest()
