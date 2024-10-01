import yfinance as yf
import pandas as pd
import time
import os

# Define the ticker symbol and the period for the data
# ticker_symbol = 'AAPL'  # Change to your desired ticker
start_date = '2014-09-30'  # 10 years ago from today
end_date = '2024-09-30'  # Today's date

folder_path = 'C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\YFinanceHistorical\\'

tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\50Tickers.csv')
tickers = tickers_df['Tickers'].tolist()

for ticker in tickers:
    # Fetch historical daily data
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

    # Display the first few rows of the data
    print(data.head())

    # Optionally, save to a CSV file
    data.to_csv(f'{ticker}_daily_data.csv')
    data.to_csv(os.path.join(folder_path, f'{ticker}_daily_data.csv'))

    time.sleep(10)
