from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST,TimeFrame
import pandas as pd

load_dotenv()
api = REST()

bars=api.get_bars("AAPL", TimeFrame.Minute, "2021-02-08", "2021-02-08", limit=10, adjustment='raw').df
print(bars["open"])

trade = api.get_last_trade("AAPL")
print(trade)

data = api.get_barset("AAPL", 'day', limit=2).df
data = data["AAPL"]
print(data["close"][0])
