import pandas as pd
import yfinance as yf
import os
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from datetime import date, timedelta
today = date.today()


def GetStockData(stock):
    #gets stock data from today back 14yrs. stock and date inputs should be strings and progress should be booleen
    end_date = today.strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=5000)).strftime("%Y-%m-%d")
    progress = False
    stock_data = yf.download(stock, start_date, end_date, progress)
    stock_data["Date"] = stock_data.index
    stock_data = stock_data [["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    stock_data.reset_index(drop=True, inplace=True)
    return stock_data


stocks_of_intrest = ['AAPL', 'MSTF', 'TSLA', 'DB']


AAPL_data = GetStockData('AAPL')
MSFT_data = GetStockData('MSFT')


#write to sql 
DRIVER_NAME = '{SQL Server}'
SERVER_NAME = 'PROMETHEUS\SQLEXPRESS'
DATABASE_NAME ='StockData'
PASS = os.environ.get('PASSOS')
USER = os.environ.get('USEROS')

#connection_string_admin = f"""DRIVER={DRIVER_NAME}; SERVER={SERVER_NAME}; DATABASE={DATABASE_NAME}; Trust_Connection=yes"""
connection_string_etl = f"""DRIVER={DRIVER_NAME}; SERVER={SERVER_NAME}; DATABASE={DATABASE_NAME}; UID={USER}; PWD={PASS}"""

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string_etl})
engine = create_engine(connection_url) 

MSFT_data.to_sql(name='MSFT', con=engine, schema='dbo', if_exists='replace', index=False)