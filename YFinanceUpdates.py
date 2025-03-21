import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
import time
import os
from datetime import datetime, timedelta

# Function to get last valid market day
def get_last_market_day():
    nyse = mcal.get_calendar('NYSE')
    today = datetime.today().date()
    
    # Get market holidays and trading days
    valid_days = nyse.valid_days(start_date=(today - timedelta(days=10)).strftime('%Y-%m-%d'), 
                                 end_date=today.strftime('%Y-%m-%d'))
    
    # Convert to list of dates
    valid_days = pd.to_datetime(valid_days).date.tolist()

    # If today is a valid trading day, return the last one before today
    if today in valid_days:
        return valid_days[-2].strftime('%Y-%m-%d')  # Second to last day
    
    # Otherwise, return the last trading day
    return valid_days[-1].strftime('%Y-%m-%d')

# Get last valid market day
end_date = get_last_market_day()

# end_date = datetime.today().strftime('%Y-%m-%d')

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
            start_date = last_date_in_file.strftime('%Y-%m-%d')  # Start from next day
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
