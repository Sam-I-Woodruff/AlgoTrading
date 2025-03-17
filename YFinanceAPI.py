import yfinance as yf
import pandas as pd
import time
import os

# Define the date range
# start_date = '2014-09-30'
# end_date = '2024-09-30'

folder_path = 'C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\YFinanceTenYears\\'
tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\50Tickers.csv')
tickers = tickers_df['Tickers'].tolist()

for ticker in tickers:

    print(f"Fetching data for {ticker}")

    historical_data = yf.download(ticker, period="10y")

    print(historical_data[['Open', 'High', 'Low', 'Close', 'Volume']])

    time.sleep(5)

