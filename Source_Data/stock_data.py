import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta
today = date.today()


def GetStockData(stock, start_date, end_date, progress):
    #gets stock data from today back 14yrs. stock and date inputs should be strings and progress should be booleen
    stock_data = yf.download(stock, start_date, end_date, progress)
    stock_data["Date"] = stock_data.index
    stock_data = stock_data [["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    stock_data.reset_index(drop=True, inplace=True)
    return stock_data

end_date = today.strftime("%Y-%m-%d")
start_date = (date.today() - timedelta(days=5000)).strftime("%Y-%m-%d")
print(type(start_date))
AAPL_data = GetStockData('AAPL', start_date, end_date, False)

print(AAPL_data)


