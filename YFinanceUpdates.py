import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
import time
import os
from datetime import datetime, timedelta


def get_last_weekday():
    today = datetime.today()
    last_weekday = today - timedelta(days=1)  # Start with yesterday

    while last_weekday.weekday() > 4:  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
        last_weekday -= timedelta(days=1)  # Keep going back if it's Saturday/Sunday

    return last_weekday.strftime('%Y-%m-%d')

end_date = get_last_weekday()

folder_path = 'C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\YFinance\\'
tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\50Tickers.csv')
tickers = tickers_df['Tickers'].tolist()

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

for ticker in tickers:

    start_date = "2022-03-17"  # Default start date if no file exists. Defined here in case previous ticker ran with a different one.

    file_path = os.path.join(folder_path, f"{ticker}.csv")

    if os.path.exists(file_path):
        # Read existing file and get last date
        existing_data = pd.read_csv(file_path, index_col=0)
        if not existing_data.empty:
            last_date_in_file = pd.to_datetime(existing_data.index[-1])  # Explicitly convert to datetime
            start_date = (last_date_in_file + timedelta(days=1)).strftime('%Y-%m-%d')  # Start from next day
        else:
            print(f"{ticker} CSV exists but is empty, fetching full data.")

    if start_date >= end_date:
        print(f"{ticker} is up to date")
        continue #Immediately end this ticker and move on to next

    print(f"Fetching data for {ticker} from {start_date} to {end_date}")
    new_data = yf.download(ticker, start=start_date, end=end_date)

    if not new_data.empty:
        if os.path.exists(file_path):
            new_data.to_csv(file_path, mode='a', header=False)  # Append without writing headers
        else:
            new_data.to_csv(file_path)  # Create new file if it doesn't exist
        print(f"Updated {ticker} data in {file_path} from start date of {start_date}")
    else:
        print(f"No new data for {ticker}")
