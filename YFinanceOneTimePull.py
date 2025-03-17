import yfinance as yf
import pandas as pd
import time
import os

folder_path = 'C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\YFinance\\'
tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\50Tickers.csv')
tickers = tickers_df['Tickers'].tolist()

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

for ticker in tickers:

    print(f"Fetching data for {ticker}")

    historical_data = yf.download(ticker, period="3y")

    if not historical_data.empty:
        file_path = os.path.join(folder_path, f"{ticker}.csv")
        historical_data.to_csv(file_path)
        print(f"Saved {ticker} data to {file_path}")
    else:
        print(f"No data found for {ticker}")

    

    # time.sleep(1)

