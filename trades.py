from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST,TimeFrame
import pandas as pd
import time

load_dotenv()
api = REST()

def openingRise(name: str, bufferTime: str, x: float):
	last = api.get_barset(name, 'day', limit=1)
	last
	lastClose = last[name][0]

	time.sleep(bufferTime)

	curr = api.get_last_trade(name)
	currentPrice = curr["price"]
	if (currentPrice - lastClose)*100 / lastClose >= x/100:
		# print("yes") '''BUY'''